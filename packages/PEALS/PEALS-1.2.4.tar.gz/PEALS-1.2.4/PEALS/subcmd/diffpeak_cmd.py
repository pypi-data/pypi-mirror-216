# ------------------------------------
# python modules
# ------------------------------------

import os
import sys
import time
from datetime import timedelta
import pickle

# own module
from PEALS.io.constant import *
from PEALS.collection import bamtool
from PEALS.collection import gfftools
from PEALS.collection import functools
from PEALS.stats import peaktest
from PEALS.stats import correction
from PEALS.peak import peakutils
from PEALS.peak import peakcall
from PEALS.io import report
from PEALS.io import signals
from PEALS.io import streamtools

# ------------------------------------
# PEALS python modules
# ------------------------------------
from PEALS.collection import optioncheck
# ------------------------------------
# Main function
# ------------------------------------

def run( args ):
    """The Main function/pipeline for PEALS.
    """
    # Parse options...
    startTime = time.monotonic()
    options = optioncheck.validateDiffpeakArgs( args )
    # end of parsing commandline options
    options.poolmode = 'pool'
    options.bedflag = True
    options.bamsoftware = 'bedtools'
    ## seting NUMEXPR_MAX_THREADS to avoid warnings:
    ## Note: NumExpr detected 28 cores but "NUMEXPR_MAX_THREADS" not set, so enforcing safe limit of 8. 
    os.environ['NUMEXPR_MAX_THREADS'] = str(options.thread)
    ## alias for logging
    info = options.info
    warn = options.warn
    debug = options.debug
    error = options.error
    ## prefix for tempory file, including path
    tempPrefix = os.path.join(options.tempdir, "_".join([options.tempre, options.prefix]))
    ## prepare genome information
    ## info
    info("Reading information from chromosome size file.")
    options.chrsizedict = signals.readGenomeSize(options)
    ## info
    info("Reading information from input sample matrix file ({}).".format(os.path.basename(options.matrix)))
    options = functools.buildFullMatrix(options)
    debug("The final information of input sample matrix file is as follow:{}".format(options.matrixdf.to_markdown()))
    ## output buildFullMatrix to tempory file
    fullMatrixFile = tempPrefix + '.fullmatrix.tmp'
    options.matrixdf.to_csv(fullMatrixFile, sep='\t', header=True, index=True)
    ## info
    info("Creating soft symbolic links to input bam and bai files.")
    functools.bamToSymlink(options)
    ## assign arguments to variables
    cipBamList = options.ipcontrol
    cinputBamList = options.inputcontrol
    clabelList = options.labelcontrol
    tipBamList = options.iptreat
    tinputBamList = options.inputtreat
    tlabelList = options.labeltreat
    ## get all input bam
    allBamList = cipBamList + cinputBamList + tipBamList + tinputBamList
    ## convert bam to bedGraph
    if options.reuse is False:
        info( BAM_TO_COVERAGE_LOG )
        bamtool.runConvertBamToBgParallel(options, allBamList)
    else:
        info("Skip the preparation of genome-wide reads coverage!")
    ## info
    ## getting reads on transcripts
    info( GET_TX_EXP_LOG )
    ipBamList = cipBamList + cinputBamList
    inputBamList = tipBamList + tinputBamList
    if options.expmethod == 'count':
        txReadCountDf = signals.getReadCountsDf(options, options.gff, 'transcript', allBamList, normalize=False, keeplen=True)
        info('Use raw reads count to estimate the transcript expression for filtering.')
        ## filter out transcripts with low expression in input and low ip signals in ip sample
        txExpDf = txReadCountDf.iloc[:, range(1, txReadCountDf.shape[1])]
    else:
        txExpDf = signals.getReadCountsDf(options, options.gff, 'transcript', allBamList, normalize=True, keeplen=False)
    ## filter out transcripts with low expression in input and low ip signals in ip sample
    subTxExpDf = signals.getFilterExpDf(options, txExpDf, options.expcutoff, ipBamList, inputBamList)
    ## re-estimate the expression when using raw count to filter
    if options.expmethod == 'count':
        txExpDf = signals.normalizeReadCountDf(options, 'TPM', txReadCountDf)
        txExpDf = signals.getFilterExpDf(options, txExpDf, 0, ipBamList, inputBamList, log=False)
        subTxExpDf = txExpDf.loc[subTxExpDf.index.to_list()]
    ## info estimate gene expression
    info( "Obtaining read counts of genes from input samples..." )
    geneExpDf = signals.getReadCountsDf(options, options.gff, 'gene', allBamList, normalize=False, keeplen=False)
    ## prepare annotation information by constructing txid annotation and bed12
    ## info decoding transcript information from annotation
    info( DECODE_ANNO_LOG.format(options.gff) )
    txidList = subTxExpDf.index.to_list()
    txBedDict = gfftools.gffToTxBedDict(options, txidList)
    info( '{} transcripts were used in gene annotation file'.format(len(txBedDict.keys())) )
    ## calling peaks from control and treat condition
    if options.reuse is False:
        ## info
        info( "Trying to call peak candidates from control samples..." )
        controlPeakRowList = findPeakFromSample(options, txBedDict, cipBamList, cinputBamList, clabelList, geneExpDf, subTxExpDf, 'control')
        ## info
        info( "Trying to call peak candidates from treated samples..." )
        treatPeakRowList = findPeakFromSample(options, txBedDict, tipBamList, tinputBamList, tlabelList, geneExpDf, subTxExpDf, 'treated')
        info( "Merging peak candidates from control and treated conditions..." )
        peakRowList = controlPeakRowList + treatPeakRowList
        ''' just used for development
        ### for reuse
        streamtools.dumpPeakToMbb(peakRowList, 'combine.peak.mbb', folder=options.outputdir)
        '''
    else:
        ## info
        info("Reading \"combine.peak.mbb\" instead of calling peaks!")
        peakRowList = streamtools.readPeakFromMbb(['combine.peak.mbb'], bufferSize=options.buffer, folder=options.outputdir)
        tempCombinePeak = tempPrefix + '.combine.peak.bed'
        streamtools.peakToFile(peakRowList, tempCombinePeak, bed12=False, folder=None)
        info( "Merging peak candidates from control and treated conditions..." )
    ## pool peaks from conditions
    poolPeakRowList = peakutils.poolPeak(options, peakRowList, 2, options.prefix, peakMode='merge', txBedDict=txBedDict)
    tempPoolPeak = tempPrefix + '.pool.peak.bed'
    streamtools.peakToFile(poolPeakRowList, tempPoolPeak, bed12=False, folder=None)
    ## finding differential peaks
    options.poolmode = 'diff'
    sampleCount = max(len(options.ipcontrol), len(options.iptreat))
    #AlltestBamList = functools.removeDupBam(options, cipBamList + cinputBamList + tipBamList + tinputBamList)
    AlltestBamList = cipBamList + cinputBamList + tipBamList + tinputBamList
    ## info
    info( "Performing statistical testing on peak candidates..." )
    if sampleCount == 1:
        ### running code
        peakReadCountDf = peakutils.getPeakReadCountsDf(options, poolPeakRowList, AlltestBamList, normalize=False)
        #pickle.dump( peakReadCountDf, open(options.outputdir + '/PEALS_tmp_peakReadCountDf.tmp', "wb") )
        #pickle.dump( options, open(options.outputdir + '/PEALS_tmp_options.tmp', "wb") )
        testResDf = peaktest.runFisherTest(options, peakReadCountDf)
    else:
        ## inputand ip reads for peak
        ##inputTestBamList = functools.removeDupBam(options, cinputBamList + tinputBamList)
        inputTestBamList = cinputBamList + tinputBamList
        ## get the gene counts from input read count df
        geneInputReadCountDf = geneExpDf.loc[:, functools.getBamidList(options, inputTestBamList)]
        ## output raw read counts
        tempReadCountFile = tempPrefix + '.gene.raw.counts.tmp'
        geneInputReadCountDf.to_csv(tempReadCountFile, sep='\t', header=True, index=True)
        info( "Obtaining read counts of peak candidates from IP and input libraries..." )
        peakReadCountDf = peakutils.getPeakReadCountsDf(options, poolPeakRowList, AlltestBamList, normalize=False)
        ## output raw read counts
        tempReadCountFile = tempPrefix + '.raw.counts.tmp'
        peakReadCountDf.to_csv(tempReadCountFile, sep='\t', header=True, index=True)
        ## normalization step 1
        info( "Normalizing IP read counts of peak candidates by calculating sample-wise factors..." )
        peakIpReadCountNorDf, peakInputReadCountNorDf = correction.normalizeByEnrichment(options, peakReadCountDf, geneInputReadCountDf)
        ## normalization step 2
        info( "Adjusting normalizeed IP read counts of peak candidates with pre-IP RNA levels..." )
        adjustPeakIpReadCountDf = correction.adjustByPreipGeneShrinkFc(options, peakIpReadCountNorDf, geneInputReadCountDf)
        ## output normalized read counts
        tempReadCountFile = tempPrefix + '.normalized.counts.tmp'
        normalizedPeakReadCountDf = peakInputReadCountNorDf.join(adjustPeakIpReadCountDf)
        normalizedPeakReadCountDf.to_csv(tempReadCountFile, sep='\t', header=True, index=True)
        ## only perform significance test on peak candidates
        info( "Filtering non-peak candidates..." )
        adjustPeakIpReadCountDf = adjustPeakIpReadCountDf[ adjustPeakIpReadCountDf.index.str.contains(options.peakregex, regex = True) ]
        ## info
        info( "testing the significance of peak candidates upon conditions..." )
        testResDf = peaktest.runGlmNbinomTest(options, adjustPeakIpReadCountDf, plot=True, skipSubplot=True)
    ## outputs
    info( "Reporting final peaks..." )
    ### running code
    report.peakReport(options, txBedDict, testResDf, poolPeakRowList)
    ## generate bigwig signal track
    if functools.checkBgFiles(options) is True:
        ## Generating bigWig signal track
        if options.nobwtrack is False:
            ## info
            info("Generating bigWig signal track...")
            signals.runConvertBgToBwParallel(options, allBamList)
            ## info
            info("Generating bigWig signal track done.")
    if options.keeptemp is False:
        ## delete all temporary files
        info("Cleaning up all temporary files...")
        functools.delTempFile(options)
    ## end the program with message
    info( "Program ends." )
    ## output running time
    endTime = time.monotonic()
    runTime = timedelta(seconds=endTime - startTime)
    info(RUNNING_TIME.format(runTime))

def findPeakFromSample(options, txBedDict, ipBamList, inputBamList, labelList, geneExpDf, txExpDf, condition):
    info = options.info
    warn = options.warn
    debug = options.debug
    error = options.error
    ## creating ip-input bam pairs, 3D list
    if len(ipBamList) != len(inputBamList):
        pairBamList3d = [ [ ipBamList, inputBamList ] ]
        labelList = [ options.labelref ]
    else:
        sampleCount = len(ipBamList)
        ## if --call-with-binary is specified, just call peaks on pool samples
        if options.binary is True:
            pairBamList3d = [ [ ipBamList, inputBamList ] ]
            labelList = [ options.labelref ]
        else:
            pairBamList3d = [ [ [ ipBamList[i] ], [ inputBamList[i] ] ] for i in range(sampleCount) ]
            ## add pool sample
            if sampleCount > 1:
                pairBamList3d += [ [ ipBamList, inputBamList ] ]
                labelList += [ options.labelref ]
    ## generating peak candidates from ip and input bam
    peakRowList = []
    if options.binary is True:
        ## read binary files into peakRowList
        bamidList = sorted(set(map(lambda x: options.bamdict[x], ipBamList)))
        binaryFileList = sorted(options.matrixdf.loc[bamidList, ]['binary'].unique())
        binaryFileForLog = ','.join(map(lambda x: os.path.basename(x), binaryFileList))
        info( READ_BINARY_LOG.format(binaryFileForLog) )
        peakRowList = streamtools.readPeakFromMbb(binaryFileList, bufferSize=options.buffer, folder=options.binarydir)
    ## info
    info("Starting to call peaks on IP and input libraries...")
    for i in range(len(pairBamList3d)):
        bamList = pairBamList3d[i]
        label = labelList[i]
        subIpBamList, subInputBamList = bamList
        ipBamName = ','.join(map(lambda x:os.path.basename(x), subIpBamList))
        inputBamName = ','.join(map(lambda x:os.path.basename(x), subInputBamList))
        ## info
        info( CALL_PEAK_LOG.format(ipBamName, inputBamName) )
        ### running code
        perPeakRowList = peakcall.callPeak(options, txBedDict, txExpDf, bamList, label)
        ''' just used for development
        ## write peakRowList to binary file *.mbb
        if label != options.labelref:
            binaryFile = functools.getCellByBam(options, subIpBamList[0], 'binary')
            pickle.dump( perPeakRowList, open(binaryFile, "wb") )
        '''
        ## append peakRowList
        peakRowList.extend(perPeakRowList)
        ## info
        info( CALL_PEAK_DONE_LOG.format(ipBamName, inputBamName) )
    ## testing the significance
    sampleCount = max([len(ipBamList), len(inputBamList)])
    ##testBamList = functools.removeDupBam(options, ipBamList + inputBamList)
    testBamList = ipBamList + inputBamList
    if sampleCount == 1:
        ## info
        info("Performing statistical testing on peak candidates...")
        ### running code
        peakReadCountDf = peakutils.getPeakReadCountsDf(options, peakRowList, testBamList, normalize=False)
        testResDf = peaktest.runNbinomTest(options, peakReadCountDf)
        info("Statistical testing on peak candidates done.")
    else:
        ## info
        info("Finding consensus peak candidates from replicates...")
        ## running peak pooling
        peakRowList = peakutils.poolPeak(options, peakRowList, sampleCount, condition, peakMode='intersect', txBedDict=None)
        ## info
        info("Performing statistical testing on peak candidates...")
        ## get reads of peakid
        debug("Obtaining reads for peak candidates...")
        peakReadCountDf = peakutils.getPeakReadCountsDf(options, peakRowList, testBamList, normalize=False)
        if options.peaksizefactor == 'gene':
            ## obtain gene read counts
            subGeneExpDf = geneExpDf.loc[:, peakReadCountDf.columns]
            sizeFactorSeries = correction.calMedianRatio(subGeneExpDf)
            ## normalize peak read counts
            info( "Normalize the read count of peak candidates by estimated size factors: \n" + sizeFactorSeries.to_markdown() )
            peakReadCountDf = correction.normalizeCountDf(peakReadCountDf, sizeFactorSeries)
        debug("Testing the significance of peak candidates...")
        testResDf = peaktest.runGlmNbinomTest(options, peakReadCountDf, plot=False, skipSubplot=False)
        ## info
        info("Statistical testing on peak candidates done.")
    ## reflag the peak by testing results
    info( "Reconstuct the peak candidates..." )
    peakRowList = report.peakReflag(options, testResDf, peakRowList)
    info( "Peak calling for condition ({}) done.".format(condition) )
    ## return testing results
    return peakRowList
