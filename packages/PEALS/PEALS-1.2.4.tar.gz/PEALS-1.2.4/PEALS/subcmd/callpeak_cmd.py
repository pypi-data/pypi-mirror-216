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
    options = optioncheck.validateCallpeakArgs( args )
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
    ## get inputs
    ipBamList = options.ip
    inputBamList = options.input
    labelList = options.label
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
    ## get all input bam
    allBamList = ipBamList + inputBamList
    ## info
    info( BAM_TO_COVERAGE_LOG )
    ## convert bam to bedGraph
    bamtool.runConvertBamToBgParallel(options, allBamList)
    ## getting reads on transcripts
    ## info
    info( GET_TX_EXP_LOG )
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
    ## info decoding transcript information from annotation
    info( DECODE_ANNO_LOG.format(options.gff) )
    txidList = subTxExpDf.index.to_list()
    ## prepare annotation information by constructing txid annotation and bed12
    txBedDict = gfftools.gffToTxBedDict(options, txidList)
    info( '{} transcripts were used from the gene annotation file'.format(len(txBedDict.keys())) )
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
        perPeakRowList = peakcall.callPeak(options, txBedDict, subTxExpDf, bamList, label)
        ''' just used for development
        ## write peakRowList to binary file *.pb
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
    ## removing any duplicate bams
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
        peakRowList = peakutils.poolPeak(options, peakRowList, sampleCount, options.prefix, peakMode='intersect', txBedDict=None)
        ## info
        info("Performing statistical testing on peak candidates...")
        ## get reads of peakid
        debug("Obtaining reads for peak candidates...")
        peakReadCountDf = peakutils.getPeakReadCountsDf(options, peakRowList, testBamList, normalize=False)
        if options.peaksizefactor == 'gene':
            ## obtain gene read counts
            geneReadCountDf = signals.getReadCountsDf(options, options.gff, 'gene', testBamList, normalize=False, keeplen=False)
            sizeFactorSeries = correction.calMedianRatio(geneReadCountDf)
            ## normalize peak read counts
            info( "Normalize the read count of peak candidates by estimated size factors: \n" + sizeFactorSeries.to_markdown() )
            peakReadCountDf = correction.normalizeCountDf(peakReadCountDf, sizeFactorSeries)
        debug("Testing the significance of peak candidates...")
        testResDf = peaktest.runGlmNbinomTest(options, peakReadCountDf, plot=True, skipSubplot=False)
        ## info
        info("Statistical testing on peak candidates done.")
    ## outputs
    info("Reporting final peaks...")
    ### running code
    report.peakReport(options, txBedDict, testResDf, peakRowList)
    ## Generating bigWig signal track
    if options.nobwtrack is False:
        ## info
        info("Generating bigWig signal track...")
        signals.runConvertBgToBwParallel(options, allBamList)
        ## info
        info("Generating bigWig signal track done.")
    ## delete all temporary files
    if options.keeptemp is False:
        info("Cleaning up all temporary files...")
        functools.delTempFile(options)
    ## end the program with message
    info("Program ends.")
    ## output running time
    endTime = time.monotonic()
    runTime = timedelta(seconds=endTime - startTime)
    info(RUNNING_TIME.format(runTime))
