# -*- coding: utf-8 -*-
##########################################
#           peakcall                     #
#          2023.02.23                    #
##########################################
__author__ = "Keren Zhou"
__version__ = "v2.0"

import os
import sys
import numpy as np
from collections import defaultdict
from findpeaks import findpeaks
from multiprocessing import get_context, Semaphore
from contextlib import closing
import tqdm

# own module
from PEALS.collection import bamtool
from PEALS.collection import gfftools
from PEALS.collection import functools
from PEALS.io import signals
from PEALS.peak import peakutils

def findMcSubGroup(options, subCovArr):
    # to find the most consecutive step group where ip/input >= ratioCutoff
    indexArr = np.arange(len(subCovArr))
    subCovArr = functools.csaps(indexArr, subCovArr, indexArr)[0]
    ## find index
    subOverIndexArr = np.where(subCovArr >= 1)[0]
    if subOverIndexArr.size > 0:
        ## find the most consecutive index array
        groupList = functools.findConGroup(subOverIndexArr)
        groupCovSumMeanList = [subCovArr[arr].mean() for arr in groupList]
        #most consecutive group
        mcGroupIndex = groupCovSumMeanList.index(max(groupCovSumMeanList))
        mcGroup = groupList[mcGroupIndex]
        return mcGroup
    else:
        return False

def peakIpOverInput(options, peaks, ipCovArr, subCovArr, signalRatio, meanCutoff):
    start, peak, end = peaks
    peakFlag = False
    ratio = 0
    ## make the PCR duplicate region as non-peak
    complexityRate = functools.estimateRegionCompexity(ipCovArr)
    if complexityRate < options.comprate:
        complexFlag = False
    else:
        complexFlag = True
    # determin a peak and status and refine peak region
    if subCovArr.sum() >= 0:
        mcGroup = findMcSubGroup(options, subCovArr)
        if mcGroup is not False:
            ## the start and end index of most consecutive step group in subCovArr
            smcIndex = mcGroup[0]
            emcIndex = mcGroup[-1]
            ## determin the index of confident interval
            mcipCovArr = ipCovArr[smcIndex:emcIndex]
            if mcipCovArr.size >= options.peaksize:
                ratio = signalRatio
                lMargin, rMargin = peakutils.centerPeak(options, mcipCovArr, ratio, meanCutoff)
                ## final peak start and end
                newStart = start + smcIndex + lMargin
                newEnd = start + smcIndex + rMargin
                peakFlag = True
            else:
                lMargin, rMargin = peakutils.centerPeak(options, ipCovArr, ratio, meanCutoff)
                newStart = start + lMargin
                newEnd = start + rMargin
        else:
            lMargin, rMargin = peakutils.centerPeak(options, ipCovArr, ratio, meanCutoff)
            newStart = start + lMargin
            newEnd = start + rMargin
    else:
        lMargin, rMargin = peakutils.centerPeak(options, ipCovArr, ratio, meanCutoff)
        newStart = start + lMargin
        newEnd = start + rMargin
    ## change the peakFlag by the region complexity
    if complexFlag is False:
        peakFlag = False
    ## refind peak location
    if peak <= newStart or peak >= newEnd:
        peak = int((newStart + newEnd) / 2)
    ## peaks returned structure
    peaks = [newStart, peak, newEnd]
    return [peaks, peakFlag]

def decodeFindpeaks(options, fpFitRes, ipCovArr, inputCovArr, ipMeanCov, offset, onipFlag=True):
    txLength = ipCovArr.size
    results = fpFitRes['df']
    peakRegionidList = sorted(results.labx.unique())
    peakSiteList = []
    peakIpCovList = []
    peakFlagList = []
    ## substract input from ip
    subCovArr = np.subtract(ipCovArr, inputCovArr)
    ## deal with each region
    regionLen = len(peakRegionidList)
    for i in range(regionLen):
        regionid = peakRegionidList[i]
        if regionLen == 1:
            df = results
        else:
            df = results.loc[results['labx'] == regionid]
        ## df.x, eg. Series([1,2,3,4], Name: x, dtype: int64)
        ## skip region smaller than peaksize
        if df.x.size < options.peaksize:
            continue
        start = int(min(df.x))
        end = int(max(df.x))
        rpeakList = sorted(df.loc[df['peak'] == True].x.unique())
        if len(rpeakList) == 0:
            peak = df['y'].idxmax()
        else:
            peak = rpeakList[0]
        ## remove peak not between start and end
        if ipCovArr[peak] <= ipCovArr[start] or ipCovArr[peak] <= ipCovArr[end]:
            continue
        peaks = [start, peak, end]
        ## calculate ip/iput ratio of this region
        pipCovArr = ipCovArr[start:end]
        pinputCovArr = inputCovArr[start:end]
        psubCovArr = subCovArr[start:end]
        signalRatio = pipCovArr.sum() / (pinputCovArr.sum() + 1)
        ##peak with ip over input
        refinePeaks, peakFlag = peakIpOverInput(options, peaks, pipCovArr, psubCovArr, signalRatio, ipMeanCov)
        if onipFlag is False:
            peakFlag = False
        peakIpCovSum = ipCovArr[refinePeaks[0]:refinePeaks[2]].sum()
        ## filter small peaks
        if refinePeaks[2] - refinePeaks[0] >= options.peaksize:
            ## re-map peak start and and with start-index of input covArr
            refinePeaks[0] += offset
            refinePeaks[2] += offset
            peakSiteList.append(refinePeaks)
            peakIpCovList.append(peakIpCovSum)
            peakFlagList.append(peakFlag)
    return [peakSiteList, peakIpCovList, peakFlagList]

def callPeakPerTx(bulkArgs):
    ## the libSize is input bam relative to ip bam, reads(input)/reads(ip)
    ## only ip - input > 0 will be considered as a peak candidate
    ## return peak list: [ bed12Row, bed12Row, ...] or [[start, peak, end], ...]
    ## decode bulk arguments
    options, txBed, ipCovArr, inputCovArr, ipMeanCov, inputMeanCov, offset = bulkArgs
    peakSiteList = []
    ## call on ip sample
    ## smooth the coverage data of tx
    ipSmoothCovArr = functools.smoothCsaps(options, ipCovArr)
    ## find peaks on smoothed coverage of tx, local maxima-minima
    fp = findpeaks(method='peakdetect', lookahead=options.lookahead, verbose=0)
    fpFitRes = fp.fit(ipSmoothCovArr)
    ## peakSiteList, [ [start, peak, end], ...]
    ipPeakSiteList, peakIpCovList, peakIpFlagList = decodeFindpeaks(options, fpFitRes, ipCovArr, inputCovArr, ipMeanCov, offset, onipFlag=True)
    if len(ipPeakSiteList):
        ## whether to convert to bed
        if options.bedflag is True:
            ## convert tx coordinates to genomic coordiates, peakBedRowList
            ## [ bed12Row + [peakFlag, peakIpCov], ...]
            peakSiteList = peakutils.peakToCorpeak(options, ipPeakSiteList, peakIpCovList, peakIpFlagList, txBed)
    return peakSiteList

def callPeakPerTxBulkArgsCount(options, chromList, chromTxDict, txBedDict):
    count = 0
    for chrom in chromList:
        for txid in sorted(chromTxDict[chrom]):
            txBed = txBedDict[txid]
            count += functools.splitCovArrayCount(txBed, options.txsizemax, options.txoptsize)
    return count

def prepareCallPeakPerTxBulkArgs(options, semaphore, chromList, chromTxDict, txBedDict, ipBgCovDf, inputBgCovDf, scaleFactorList):
    ipScaleFactor, inputScaleFactor = scaleFactorList
    for chrom in chromList:
        chromSize = options.chrsizedict[chrom]
        ipBaseCovArr, ipMeanCov = signals.readChromReadBaseCov(options, ipBgCovDf.loc[chrom,], chromSize, ipScaleFactor, operator='divide')
        inputBaseCovArr, inputMeanCov = signals.readChromReadBaseCov(options, inputBgCovDf.loc[chrom,], chromSize, inputScaleFactor, operator='divide')
        for txid in sorted(chromTxDict[chrom]):
            txBed = txBedDict[txid]
            txIpBaseCovArr = signals.txBaseCov(options, ipBaseCovArr, txBedDict[txid])
            txInputBaseCovArr = signals.txBaseCov(options, inputBaseCovArr, txBedDict[txid])
            ## split Coverage array into sub arrays
            ipCovArrList, inputCovArrList, indexList = functools.splitCovArray(txIpBaseCovArr, txInputBaseCovArr, ipMeanCov, options.txsizemax, options.txoptsize)
            ## loop each split arrays
            for i in range(len(indexList)):
                ipCovSplitArr = ipCovArrList[i]
                inputCovSplitArr = inputCovArrList[i]
                offset = indexList[i][0]
                semaphore.acquire()
                yield [ options, txBed, ipCovSplitArr, inputCovSplitArr, ipMeanCov, inputMeanCov, offset ]

def runCallPeakPerTxParallel(options, bamList, chromTxDict, txBedDict):
    ipBamList, inputBamList = bamList
    ipBamCount = len(ipBamList)
    inputBamCount = len(inputBamList)
    ## get library size
    ipLibSizeList = list(map(lambda x:functools.getCellByBam(options, x, 'lib_size'), ipBamList))
    inputLibSizeList = list(map(lambda x:functools.getCellByBam(options, x, 'lib_size'), inputBamList))
    ipLibSize = ','.join(map(str, ipLibSizeList))
    inputLibSize = ','.join(map(str, inputLibSizeList))
    options.debug("Obtain library size: ip({}), input({}).".format(ipLibSize, inputLibSize))
    ## get the library scaled factor
    if ipBamCount == inputBamCount == 1:
        ipLibScaleFactor, inputLibScaleFactor = list(map(lambda x:functools.getCellByBam(options, x, 'paired_lib_scale'), ipBamList + inputBamList))
    else:
        ipLibScaleFactor, inputLibScaleFactor = bamtool.getPairLibScale(options, ipBamList, inputBamList)
    options.debug("Obtain library scale factor: ip({}), input({}).".format(ipLibScaleFactor, inputLibScaleFactor))
    ## correct input scale factor by the ip ratio and bam number
    ipScaleFactor = ipLibScaleFactor * ipBamCount
    inputScaleFactor = inputLibScaleFactor / options.ipratio * inputBamCount
    scaleFactorList = [ipScaleFactor, inputScaleFactor]
    ## get coverage from bedGraph files
    options.debug("Reading reads coverage in parallel...")
    ipBgCovDf, inputBgCovDf = signals.readBgToCovDfParallel(options, ipBamList, inputBamList)
    options.debug("Preparing data for parallel calling of peak candidates ...")
    maxLoop = 5
    ## get chrom set from ip and input base coverage data
    chromSet = set(ipBgCovDf.index).union(set(inputBgCovDf.index))
    loopChromList, loopChunksizeList = functools.getLoopByChrom(options, chromTxDict, chromSet, maxLoop)
    ## determin the task number
    chromList = sum(loopChromList, [])
    taskCount = callPeakPerTxBulkArgsCount(options, chromList, chromTxDict, txBedDict)
    ## find peaks on tx in parallel
    options.debug("Calling peak candidates in parallel with the estimation of {} tasks...".format(taskCount))
    #pbar = tqdm(total=taskCount)
    txPeakCallResultList = []
    # start to pool
    thread = options.thread
    with closing(get_context(options.threadstart).Pool(thread)) as pool:
        semaphore = Semaphore(thread*4)
        ## using generator with semaphore to lock and release thread to avoid any stucks
        bulkArgsGenerator = prepareCallPeakPerTxBulkArgs(options, semaphore, chromList, chromTxDict, txBedDict, ipBgCovDf, inputBgCovDf, scaleFactorList)
        imapUnordered = pool.imap_unordered(callPeakPerTx, bulkArgsGenerator)
        if options.verbose >= 2:
            miniters = int(taskCount / 50)
            barFormat = 'INFO  @ Peak-calling status: {percentage:3.0f}% [elapsed: {elapsed}|estiamted remaining:{remaining}]\n'
            for result in tqdm.tqdm(imapUnordered, total=taskCount, mininterval=60, maxinterval=120, miniters=miniters, position=0, leave=True, ascii=True, bar_format=barFormat):
                if bool(result):
                    txPeakCallResultList.append(result)
                semaphore.release()
        else:
            for result in imapUnordered:
                if bool(result):
                    txPeakCallResultList.append(result)
                semaphore.release()
    return txPeakCallResultList

def callPeak(options, txBedDict, txExpDf, bamList, label):
    ## bamList: [ipBam, inputBam]
    ## label, sample label, e.g. shNS:rep1
    ## set bedflat always be True
    options.bedflag = True
    ## construct chrom -> tx dictionary
    chromTxDict = defaultdict(list)
    for txid in txExpDf.index:
        if options.rnatype == 'mature' or options.rnatype == 'mixture':
            labelTxid = options.idsepdict['labeltxid'].join([txid, 'mature'])
            chrom = txBedDict[labelTxid].chr
            chromTxDict[chrom].append(labelTxid)
        if options.rnatype == 'primary' or options.rnatype == 'mixture':
            labelTxid = options.idsepdict['labeltxid'].join([txid, 'primary'])
            ## skip if not in primary (e.g., transcripts contain only 1 exon)
            if labelTxid not in txBedDict:
                continue
            chrom = txBedDict[labelTxid].chr
            chromTxDict[chrom].append(labelTxid)
    ## find peaks on tx in parallel
    txPeakCallResultList = runCallPeakPerTxParallel(options, bamList, chromTxDict, txBedDict)
    ## remove redundent peaks
    options.debug("Removing redundant peak candidates...")
    ## construct tx expression dictionary from dataFrame
    inputTxExpDf = txExpDf.loc[:, ['input']]
    txidExpDict = {}
    for txid in inputTxExpDf.index:
        txidExpDict[txid] = inputTxExpDf.loc[txid, ][0]
    finalPeakRowList = peakutils.mergePeakPerTxCall(options, label, txidExpDict, txPeakCallResultList)
    ## return results
    return finalPeakRowList

if __name__ == '__main__':
    ## for test
    print('not support for direct running!')
