# -*- coding: utf-8 -*-
##########################################
#           streamtool                   #
#          2022.3.24                     #
##########################################
__author__ = "Keren Zhou"
__version__ = "v1.1"

import os
import sys
import pandas as pd
import numpy as np
from multiprocessing import get_context
from contextlib import closing
import tempfile
import pyBigWig

from PEALS.collection import functools
from PEALS.collection import bamtool

def readGenomeSize(options):
    gsize = options.gsize
    chromSizeDict = {}
    with open(gsize, 'r') as f:
        for line in f:
            row = line.strip().split('\t')
            chrom = row[0]
            chromSize = int(row[1])
            chromSizeDict[chrom] = chromSize
    return chromSizeDict

def convertBgToDataFrame(bedGraphFile, strand):
    ## load bedGraph into pandas dataframe
    baseReadCovDf = pd.read_csv(bedGraphFile, header=None, sep="\t", index_col=0, skiprows=0)
    ## add strand information to column 4
    if strand == '+':
        baseReadCovDf[4] = 0
    else:
        baseReadCovDf[4] = 1
    '''
    baseReadCovDf
                               1       2  3  4
    0
    chr1                   11958   12058  1  0
    chr1                   13836   13936  1  0
    chr1                   13987   14087  1  0
    chr1                   14218   14318  1  0
    chr1                   14360   14361  1  0
    [10139535 rows x 4 columns]
    '''
    return baseReadCovDf

def readBgToCovDf(bulkArgs):
    ## strand will be '+' or '-'
    options, bam, strand, ipType = bulkArgs
    library = options.library
    bamName = os.path.basename(bam)
    ## debug
    if options.library == 0:
        options.debug('Reading genome-wide coverage for bam ({})...'.format(bamName))
    else:
        options.debug('Reading genome-wide coverage for bam ("{}" strand, {})...'.format(strand, bamName))
    ## determin coverage file name
    forwardBgFile, reverseBgFile = bamtool.tempfileFromBam(options, bam, 'bg')
    ## store the bedgraph coverage data
    if strand == '+':
        baseReadCovDf = convertBgToDataFrame(forwardBgFile, '+')
    else:
        baseReadCovDf = convertBgToDataFrame(reverseBgFile, '-')
    ## debug
    if options.library == 0:
        options.debug('Reading genome-wide coverage for bam ({}) done.'.format(bamName))
    else:
        options.debug('Reading genome-wide coverage for bam ("{}" strand, {}) done.'.format(strand, bamName))
    ## return results
    return [baseReadCovDf, ipType]

def readBgToCovDfParallel(options, ipBamList, inputBamList):
    if options.library == 0:
        loopCount = len(ipBamList + inputBamList)
    else:
        loopCount = len(ipBamList + inputBamList) * 2
    if loopCount > options.thread:
        thread = options.thread
    else:
        thread = loopCount
    ## get bulkArgsList
    bulkArgsList = []
    bamList = [ipBamList, inputBamList]
    ipTypeList = ['ip', 'input']
    for i in range(2):
        typeBamList = bamList[i]
        ipType = ipTypeList[i]
        for bam in typeBamList:
            if options.library == 0:
                strandList = ['+']
            else:
                strandList = ['+', '-']
            for strand in strandList:
                bulkArgsList.append([options, bam, strand, ipType])
    ## get base coverage per bam
    baseReadCovDfList2d = [ [], [] ]
    with closing(get_context(options.threadstart).Pool(thread)) as pool:
        imap = pool.imap(readBgToCovDf, bulkArgsList)
        for result in imap:
            baseReadCovDf, ipType = result
            if ipType == 'ip':
                baseReadCovDfList2d[0].append(baseReadCovDf)
            else:
                baseReadCovDfList2d[1].append(baseReadCovDf)
    finalBaseReadCovDfList = [ [], [] ]
    for i in range(2):
        baseReadCovDfList = baseReadCovDfList2d[i]
        if len(baseReadCovDfList) > 1:
            baseReadCovDf = pd.concat(baseReadCovDfList)
        else:
            baseReadCovDf = baseReadCovDfList[0]
        finalBaseReadCovDfList[i] = baseReadCovDf
    return finalBaseReadCovDfList

def readChromReadBaseCov(options, baseReadCovDf, chromSize, libScaleFactor, operator='divide'):
    ## test ip+input, running time 00:05:55, memory cost:11.83G
    ## unstranded:0,  fr-secondstrand:1, fr-firstrand:2,
    ## read 0-base coverage from outputs of bamtocov
    ## return a dictionary
    ## options
    library = options.library
    ## initialize baseCovArr with sizes of chromosomes
    if library == 0:
        ## array[cov]
        baseCovArr = np.zeros((1, chromSize), dtype=np.float32, order='C')
    else:
        ## array[[forward cov], [reverse cov]]
        baseCovArr = np.zeros((2, chromSize), dtype=np.float32, order='C')
    ## iterate by row baseReadCovDf to numpy array to speed up looping
    coverageArr = baseReadCovDf.to_numpy()
    for row in coverageArr:
        start = int(row[0])
        end = int(row[1])
        cov = float(row[2])
        strand = int(row[3])
        baseCovArr[strand][start:end] += cov
    ## version2, covert baseReadCovDf to numpy array to speed up looping
    ##for i in range(coverageArr.shape[0]):
    ##    start = int(coverageArr[i][0])
    ##    end = int(coverageArr[i][1])
    ##    cov = float(coverageArr[i][2])
    ##    strand = int(coverageArr[i][3])
    ##    baseCovArr[strand][start:end] += cov
    ## version3, without looping, but slow
    ##locusArr = [ np.arange(i[0], i[1], dtype=int).tolist() for i in baseReadCovDf.iloc[:,0:2].to_numpy()]
    ##covArr = baseReadCovDf.iloc[:,2].to_numpy()
    ##strandArr = baseReadCovDf.iloc[:,3].to_numpy()
    ##covArr = np.concatenate( [ np.full(shape=len(locusArr[i]), fill_value=covArr[i]).tolist() for i in range(covArr.size)], dtype=np.float32 )
    ##strandArr = np.concatenate( [ np.full(shape=len(locusArr[i]), fill_value=strandArr[i]).tolist() for i in range(strandArr.size)], dtype=np.int32 )
    ##locusArr = np.concatenate( locusArr, dtype=np.int32 )
    ##baseCovArr[strandArr, locusArr] = covArr
    ## scaling by the libary scale factor
    if libScaleFactor != 1:
        if operator == 'divide':
            baseCovArr = np.divide(baseCovArr, libScaleFactor)
    ## calculate mean coverage for data points that larger than 0
    meanCov = baseCovArr[baseCovArr > 0].mean()
    return [baseCovArr, meanCov]

def txBaseCov(options, baseCovArr, bedObj, txType='exon'):
    ## bed -> bedutils object from decode
    library = options.library
    chrom = bedObj.chr
    strand = bedObj.strand
    if strand == '+':
        nrow = 0
    else:
        nrow = 1
    txBaseCovList = []
    if txType == 'exon':
        for exon in bedObj.exon:
            start, end = exon
            txBaseCovList.append(baseCovArr[nrow][start:end].tolist())
    ## decode 2-d list to 1-d list
    txBaseCovArr = np.concatenate(txBaseCovList)
    return txBaseCovArr

def convertBgToBw(bulkArgsList):
    options, bam, strand, ipType = bulkArgsList
    bamName = os.path.basename(bam)
    ## get the library scale
    if options.bwscale == 'raw':
        libScaleFactor = 1
    if options.bwscale == 'rpm':
        libScaleFactor = functools.getCellByBam(options, bam, 'lib_size') / 1e6
    elif options.bwscale == 'paired':
        libScaleFactor = functools.getCellByBam(options, bam, 'paired_lib_scale')
    elif options.bwscale == 'whole':
        libScaleFactor = functools.getCellByBam(options, bam, 'whole_lib_scale')
    ## determin bw file
    forwardBwFile, reverseBwFile = bamtool.fileFromBam(options, bam, 'bw')
    if options.library == 0:
        bwFile = forwardBwFile
    else:
        if strand == '+':
            bwFile = forwardBwFile
        else:
            bwFile = reverseBwFile
    bwFileName = os.path.basename(bwFile)
    ## debug
    options.debug('Generating bigwig file ({})...'.format(bwFileName))
    ## read bedgraph to dataframe
    baseReadCovDf, __ = readBgToCovDf(bulkArgsList)
    ## drop the strand information
    baseReadCovDf.drop([4], axis=1, inplace=True)
    ## sort the coverage by chrom and start
    baseReadCovDf.sort_values(by=[0, 1], ascending=True, inplace=True)
    ## remove unwanted chromosomes
    allChromList = sorted(set(baseReadCovDf.index).intersection(set(options.chrsizedict.keys())))
    baseReadCovDf = baseReadCovDf.loc[allChromList, ]
    ## create bw header
    bwHeaderList = list(map(lambda x: (x, options.chrsizedict[x]), allChromList))
    ## creat bw using pyBigWig
    bw = pyBigWig.open(bwFile, "w")
    bw.addHeader(bwHeaderList)
    ## obtain chroms, starts, ends and values
    chromList = baseReadCovDf.index.to_list()
    startList = baseReadCovDf[1].to_list()
    endList = baseReadCovDf[2].to_list()
    valueList = baseReadCovDf[3].divide(libScaleFactor).to_list()
    ## add add entries to bw
    bw.addEntries(chromList, startList, ends=endList, values=valueList)
    ## close bw
    bw.close()
    ## debug
    options.debug('Generating bigwig file ({}) done.'.format(bwFileName))
    return True

def runConvertBgToBwParallel(options, bamList):
    bamCount = len(bamList)
    if options.library == 0:
        loopCount = bamCount
    else:
        loopCount = bamCount * 2
    if loopCount > options.thread:
        thread = options.thread
    else:
        thread = loopCount
    ## get bulkArgsList
    bulkArgsList = []
    for bam in bamList:
        if options.library == 0:
            strandList = ['+']
        else:
            strandList = ['+', '-']
        for strand in strandList:
            bulkArgsList.append([options, bam, strand, 'none'])
    ## convert bedGraph to bigwig track
    resultList = []
    with closing(get_context(options.threadstart).Pool(thread)) as pool:
        imap = pool.imap(convertBgToBw, bulkArgsList)
        for result in imap:
            resultList.append(result)

def getFilterExpDf(options, expDf, expCutoff, ipBamList, inputBamList, log=True):
    if expCutoff > 0:
        options.info('Filter expression with cutoff ({}).'.format(expCutoff))
    ## obtain label by bam
    ipBamidList = list(map(lambda x: options.bamdict[x], ipBamList))
    inputBamidList = list(map(lambda x: options.bamdict[x], inputBamList))
    ##
    ipMeanExpDf = expDf.loc[:, ipBamidList].mean(axis=1).to_frame(name='ip')
    inputMeanExpDf = expDf.loc[:, inputBamidList].mean(axis=1).to_frame(name='input')
    catMeanExpDf = pd.concat([ipMeanExpDf, inputMeanExpDf], axis=1)
    ## filter reads with at least options.expCutoff reads in ip or input
    if expCutoff == 0:
        filteredDf = catMeanExpDf[(catMeanExpDf > expCutoff).any(axis=1)]
    else:
        filteredDf = catMeanExpDf[(catMeanExpDf >= expCutoff).any(axis=1)]
    if log is True:
        options.info('After filtering, {} transcripts were left for peak calling.'.format(filteredDf.shape[0]))
    return filteredDf

def normalizeReadCountDf(options, expMethod, readCountDf):
    if expMethod != 'count':
        options.info('Normalize expression by using {}.'.format(expMethod))
    else:
        options.info('Use raw reads count to estimate the gene expression.'.format(expMethod))
    lengthDf = readCountDf.iloc[:, 0]
    countDf = readCountDf.iloc[:, range(1, readCountDf.shape[1])]
    totalReadDf = countDf.sum(axis=0)
    if expMethod == 'count':
        norExpDf = countDf
    elif expMethod == 'FRPKM':
        norExpDf = countDf.div(lengthDf, axis=0).div(totalReadDf, axis=1).multiply(1e9)
    elif expMethod == 'TPM':
        countPerbpDf = countDf.div(lengthDf, axis=0)
        norExpDf = countPerbpDf.div(countPerbpDf.sum(axis=0), axis=1).multiply(1e6)
    return norExpDf

def getReadCountsDf(options, annoFile, annoType, bamFileList, normalize=False, keeplen=False):
    ## annoType:peak, gene, transcript
    if annoType == "peak":
        readLength = functools.getReadLength(bamFileList[0])
        if options.extsize == 0:
            extsize = 0
        else:
            extsize = options.extsize - readLength
            if extsize < 0:
                options.error("The --extsize {} is smaller than the read length!".format(options.extsize))
                sys.exit(1)
    ## create temporary count file
    countTmp = tempfile.NamedTemporaryFile(suffix='.count.tmp', prefix=options.tempre, dir=options.tempdir, delete=True)
    bamFileParam = ' '.join(bamFileList)
    ## determin ienditifer and uniq prameter
    if annoType == 'peak':
        annoFormat = "SAF"
        identifier = ''
        if extsize != 0:
            extsizeParam = '--readExtension3 {}'.format(extsize)
        else:
            extsizeParam = ''
    elif annoType == 'gene':
        annoFormat = options.gfftype
        ## eg. -g gene_id
        identifier = '-g {}'.format(options.identifier.split(':')[0])
        extsizeParam = ''
    elif annoType == 'transcript':
        annoFormat = options.gfftype
        ## eg. -g transcript_id
        identifier = '-g {}'.format(options.identifier.split(':')[3])
        extsizeParam = ''
    ## count with fraction
    if options.nofraction is False:
        fractionParam = "--fraction"
    else:
        fractionParam = ''
    uniqueParam = "-C -M -O {}".format(fractionParam)
    fracOverlapParam = '--fracOverlap {}'.format(options.fracoverlap)
    ## whether to sort
    if options.sortbam is True:
        sortParam = ""
    else:
        sortParam = "--donotsort"
    ## deal with PCR duplicates
    if options.ignoredup is True:
        dupParam = "--ignoreDup"
    else:
        dupParam = ""
    ## count pair or extend
    if options.pairend is True:
        ##command = 'featureCounts -a {} -F {} {} -o {} -s {} -T {} -p {} --countReadPairs {} {} {}'
        ## remove the countReadParis will greatly speed-up the program
        command = 'featureCounts -a {} -F {} {} -o {} -s {} -T {} -p {} {} {} {} {}'
        command = command.format(annoFile, annoFormat, identifier, countTmp.name, options.library, options.thread, fracOverlapParam, uniqueParam, sortParam, dupParam, bamFileParam)
    else:
        command = 'featureCounts -a {} -F {} {} -o {} -s {} -T {} {} {} {} {} {} {}'
        command = command.format(annoFile, annoFormat, identifier, countTmp.name, options.library, options.thread, fracOverlapParam, extsizeParam, uniqueParam, sortParam, dupParam, bamFileParam)
    ## debug
    options.debug('Running featureCounts with command ({})...'.format(command))
    __ = functools.subprocessRun(command)
    ## debug
    options.debug('Running featureCounts done.')
    ## get reads into dataframe without header
    readCountDf = pd.read_csv(countTmp.name, header=None, sep="\t", index_col=0, skiprows=2)
    ## drop redundant columns
    if annoType == 'peak':
        ## drop redundant columns: Chr, Start, End, Strand, Length
        readCountDf = readCountDf.drop([1,2,3,4,5], axis=1)
    else:
        ## drop redundant columns: Chr, Start, End, Strand
        readCountDf = readCountDf.drop([1,2,3,4], axis=1)
    ## map bam files to index list
    ## bamidList = ['shNS_input_rep1', 'shNS_input_rep2', 'shNS_IP_rep1', 'shNS_IP_rep2']
    bamidList = list(map(lambda x: options.bamdict[x], bamFileList))
    ## rename the index and column
    if annoType == 'peak':
        readCountDf.index.name = 'peakid'
    elif annoType == 'gene':
        readCountDf.index.name = 'geneid'
    else:
        readCountDf.index.name = 'txid'
    ## rename column name
    lenColName = 'length'
    if annoType == 'peak':
        columNameList = bamidList
    else:
        columNameList = [ lenColName ] + bamidList
    readCountDf.set_axis(columNameList, axis=1, inplace=True)
    ## data structure of readCountDf, gene
    '''readCountDf
                       length shNS_input_rep1  shNS_input_rep2  shNS_IP_rep1  shNS_IP_rep2
    ENSG00000223972.5   200         0             0               0                 0
    ENSG00000227232.5   201         3             0               2                 1
    ENSG00000278267.1   204         0             0               0                 0
    ENSG00000243485.5   202         0             0               0                 0
    ENSG00000284332.1   203         0             0               0                 0
    dtype: float64'''
    ## delete temp file
    countTmpSummary = countTmp.name + '.summary'
    functools.deleteFile(countTmpSummary)
    countTmp.close()
    ##normalize if neccessary
    if normalize is True and annoType != 'peak':
        readCountDf = normalizeReadCountDf(options, options.expmethod, readCountDf)
    ## drop length column
    if keeplen is False:
        if lenColName in readCountDf:
            readCountDf.drop(lenColName, axis=1, inplace=True)
    return readCountDf
