# -*- coding: utf-8 -*-
##########################################
#           peakutils                    #
#          2023.02.23                    #
##########################################
__author__ = "Keren Zhou"
__version__ = "v1.5"

import sys
import tempfile
from copy import copy
from collections import defaultdict
from scipy import stats
import numpy as np
import pandas as pd
import math
from multiprocessing import get_context
from contextlib import closing

from PEALS.collection import bedutils
from PEALS.collection import functools
from PEALS.collection import bamtool
from PEALS.stats import correction
from PEALS.io import signals
from PEALS.io import streamtools

def getTxidFromPeakid(options, peakid):
    txid = peakid.split(options.idsepdict['peakid'])[0].split(options.idsepdict['genetx'])[1]
    return txid

def posToCoor(pos, exonList):
    ## covert indexed postion in the exons of tx into genomic coordinate
    iend = 0
    for i in range(len(exonList)):
        exon = exonList[i]
        exonLen = exon[1] - exon[0]
        istart = iend
        iend += exonLen
        if istart <= pos and pos < iend:
            relaPos = pos - istart
            coor = exon[0] + relaPos
            block = i
            break
    return [coor, block]

def peakCoorToBed(options, peakBlockList, peakIpCovList, peakFlagList, txBed, rgb=0):
    ## convert peakBlockList to bed
    ## peakBlockList, intermidiate ouput of peakToCorpeak.
    ## peakBlockList format: [[peakBlock, peak], ...], eg. [[[29337324, 29337411], [29338281, 29338501], [29338281, 29338426]], 29338344]
    chrom = txBed.chr
    strand = txBed.strand
    geneid = txBed.name.split(options.idsepdict['txinfo'])[0]
    txid = txBed.name.split(options.idsepdict['txinfo'])[3]
    peakid = options.idsepdict['genetx'].join([geneid, txid])
    peakRowList = []
    for i in range(len(peakBlockList)):
        peak = peakBlockList[i]
        peakIpCov = peakIpCovList[i]
        peakFlag = peakFlagList[i]
        ## peak, [peakBlock, peak]
        peakBlock = peak[0]
        pstart = peakBlock[0][0]
        pend = peakBlock[-1][-1]
        bcount = len(peakBlock)
        bsizeList = []
        bstartList = []
        for j in range(bcount):
            start = peakBlock[j][0]
            end = peakBlock[j][1]
            bsize =  end - start
            bstart = start - pstart
            bsizeList.append(bsize)
            bstartList.append(bstart)
        score = sum(bsizeList)
        bsize = ','.join(map(str, bsizeList))
        bstart = ','.join(map(str, bstartList))
        bed12Row = [chrom, pstart, pend, peakid, score, strand]
        bed12Row += [pstart, pend, rgb, bcount, bsize, bstart]
        ## extra information
        infoList = [peakFlag, peakIpCov]
        peakRowList.append(bed12Row + infoList)
    return peakRowList

def peakToCorpeak(options, peakSiteList, peakIpCovList, peakFlagList, txBed):
    ## covert peaks with index of tx into genomic coordinates
    ## peakSiteList: the peak locus on transcripts, outputs from peakcall.decodeFinpeaks, eg [ [0, 20, 100], ...]
    ## txBed, reslults from buildTxBed(txBed12), bedutils.buildbed(row).decode()
    exonList = txBed.exon
    peakBlockList = []
    for peakSite in peakSiteList:
        ## eg [0, 20, 100]
        start, peak, end = peakSite
        scoor, sblock = posToCoor(start, exonList)
        pcoor, pblock = posToCoor(peak, exonList)
        ecoor, eblock = posToCoor(end, exonList)
        ## determin blocks for exons
        blockList = []
        if sblock == eblock:
            blockCoor = [scoor, ecoor]
            blockList.append(blockCoor)
        else:
            sblockCoor = [scoor, exonList[sblock][1]]
            eblockCoor = [exonList[eblock][0], ecoor + 1]
            blockList.append(sblockCoor)
            for i in range(sblock + 1, eblock):
                blockList.append(exonList[i])
            blockList.append(eblockCoor)
        peakBlockList.append([blockList, pcoor])
    ## convert peaks into bed12 format
    ## [ bed12Row + [peakFlag, peakIpCov], ...]
    peakRowList = peakCoorToBed(options, peakBlockList, peakIpCovList, peakFlagList, txBed)
    return peakRowList

def slimOverlapPeak(bulkArgsList):
    ## remove redundant peakRow from same gene
    ##peakRow -> [bed12Row + [peakFlag, peakIpCoverage, peakTxExp]]
    options, peakRowList = bulkArgsList
    #peakRowList = [k + [rcount] for k,rcount in itertools.groupby(peakRowList)]
    ## remove any overlap peaks
    peakRowList = sorted(peakRowList, key=lambda x:(int(x[1]), int(x[2])))
    peakNum = len(peakRowList)
    finalPeakRowList = []
    skipIndexDict = {}
    for i in range(peakNum):
        ## skip the invalid index
        if i in skipIndexDict:
            continue
        cpeakRow = peakRowList[i][0:12]
        cpeakLocus = cpeakRow[0:3] + cpeakRow[3].split(options.idsepdict['txinfo'])[0:1] + cpeakRow[4:]
        cpeakFlag = peakRowList[i][12]
        cpeakIpCov = peakRowList[i][13]
        cpeakTxExp = peakRowList[i][14]
        cpeakBedops = bedutils.bed12ops(cpeakRow)
        keepFlag = True
        for j in range(i + 1, peakNum):
            tpeakRow = peakRowList[j][0:12]
            tpeakLocus = tpeakRow[0:3] + tpeakRow[3].split(options.idsepdict['txinfo'])[0:1] + tpeakRow[4:]
            tpeakFlag = peakRowList[j][12]
            tpeakIpCov = peakRowList[j][13]
            tpeakTxExp = peakRowList[j][14]
            tpeakBedops = bedutils.bed12ops(tpeakRow)
            ## break if latter peak j did not fall in peak i
            if cpeakRow[2] < tpeakRow[1]:
                keepFlag = True
                break
            ## skip if not the same strand
            if cpeakRow[5] != tpeakRow[5]:
                continue
            ## peaks on the same location
            if cpeakLocus == tpeakLocus:
                if cpeakFlag is True and tpeakFlag is False:
                    skipIndexDict[j] = 1
                    continue
                if cpeakFlag is False and tpeakFlag is True:
                    skipIndexDict[i] = 1
                    keepFlag = False
                    break
                ## peak with higher expression level of tx => peaks with higher coverage
                if math.isclose(cpeakIpCov, tpeakIpCov, rel_tol=options.reltol):
                    if cpeakTxExp >= tpeakTxExp:
                        skipIndexDict[j] = 1
                        continue
                    else:
                        cpeakRow, cpeakLocus, cpeakTxExp = [tpeakRow, tpeakLocus, tpeakTxExp]
                        cpeakFlag, cpeakIpCov, cpeakBedops = [tpeakFlag, tpeakIpCov, tpeakBedops]
                        skipIndexDict[j] = 1
                        continue
                elif cpeakIpCov >= tpeakIpCov:
                    skipIndexDict[j] = 1
                    continue
                else:
                    cpeakRow, cpeakLocus, cpeakTxExp = [tpeakRow, tpeakLocus, tpeakTxExp]
                    cpeakFlag, cpeakIpCov, cpeakBedops = [tpeakFlag, tpeakIpCov, tpeakBedops]
                    skipIndexDict[j] = 1
                    continue
            ## try to intersect peaks
            intersect = cpeakBedops.intersect(tpeakRow, score='sum', s=True, tx=False, part=True, cds=False, rescue=False, buildFlag=False)
            if bool(intersect) is True:
                if cpeakFlag is True and tpeakFlag is False:
                    skipIndexDict[j] = 1
                    continue
                if cpeakFlag is False and tpeakFlag is True:
                    skipIndexDict[i] = 1
                    keepFlag = False
                    break
                ## peak with higher expression level of tx => peaks with higher coverage => peak sizes => peak blocks
                if math.isclose(cpeakIpCov, tpeakIpCov, rel_tol=options.reltol):
                    tpeakBed = bedutils.buildbed(tpeakRow)
                    if math.isclose(cpeakTxExp, tpeakTxExp, rel_tol=options.reltol):
                        if sum(cpeakBedops.a.bsize) >= sum(cpeakBedops.b.bsize):
                            if cpeakBedops.a.bcount >= tpeakBed.bcount:
                                skipIndexDict[j] = 1
                            else:
                                cpeakRow, cpeakLocus, cpeakTxExp = [tpeakRow, tpeakLocus, tpeakTxExp]
                                cpeakFlag, cpeakIpCov, cpeakBedops = [tpeakFlag, tpeakIpCov, tpeakBedops]
                                skipIndexDict[j] = 1
                        else:
                            cpeakRow, cpeakLocus, cpeakTxExp = [tpeakRow, tpeakLocus, tpeakTxExp]
                            cpeakFlag, cpeakIpCov, cpeakBedops = [tpeakFlag, tpeakIpCov, tpeakBedops]
                            skipIndexDict[j] = 1
                    elif cpeakTxExp >= tpeakTxExp:
                        skipIndexDict[j] = 1
                    else:
                        cpeakRow, cpeakLocus, cpeakTxExp = [tpeakRow, tpeakLocus, tpeakTxExp]
                        cpeakFlag, cpeakIpCov, cpeakBedops = [tpeakFlag, tpeakIpCov, tpeakBedops]
                        skipIndexDict[j] = 1
                elif cpeakIpCov > tpeakIpCov:
                    skipIndexDict[j] = 1
                    continue
                else:
                    cpeakRow, cpeakLocus, cpeakTxExp = [tpeakRow, tpeakLocus, tpeakTxExp]
                    cpeakFlag, cpeakIpCov, cpeakBedops = [tpeakFlag, tpeakIpCov, tpeakBedops]
                    skipIndexDict[j] = 1
        ## construct peakRow -> [bed12Row + [peakFlag, peakIpCoverage, peakTxExp]]
        peakRow = cpeakRow + [cpeakFlag, cpeakIpCov, cpeakTxExp]
        ## discard peaks if keepFlag is False
        if keepFlag is False:
            continue
        ## append peakRow to finalPeaks
        finalPeakRowList.append(peakRow)
    return finalPeakRowList

def mergePeakPerTxCall(options, label, txidExpDict, txPeakCallResultList):
    ## the peakid must be unique, peakid = geneid:labelTxid|condition|number
    ##labelTxid is like txid|mature or txid|primary
    ## merge peaks from same gene
    genePeakRowDict = defaultdict(dict)
    for peakRowList in txPeakCallResultList:
        if bool(peakRowList) is False:
            continue
        for peakRow in peakRowList:
            ##peakRow -> [bed12Row + [peakFlag, peakIpCoverage]]
            chrom = peakRow[0]
            geneid, txid = peakRow[3].split(options.idsepdict['genetx'])
            realTxid = txid.split(options.idsepdict['labeltxid'])[0]
            ## add tx exp to peakRow and record peakRow by geneid-chrom
            ## in case a gene has duplicates located on to different chromosomes
            if geneid not in genePeakRowDict:
                genePeakRowDict[geneid] = defaultdict(list)
            genePeakRowDict[geneid][chrom].append(peakRow + [ txidExpDict[realTxid] ])
    ## Clean up
    del txPeakCallResultList
    ##get peakRowList for each gene
    bulkArgsList = []
    for geneid in sorted(genePeakRowDict.keys()):
        chromList = sorted(genePeakRowDict[geneid].keys())
        for chrom in chromList:
            peakRowList = genePeakRowDict[geneid][chrom]
            bulkArgsList.append([options, peakRowList])
    ##remove redundant peaks of each gene in parallel
    chunksize = max(1, int(len(bulkArgsList) / options.thread))
    genePeakRowList = []
    with closing(get_context(options.threadstart).Pool(options.thread)) as pool:
        imapUnordered = pool.imap_unordered(slimOverlapPeak, bulkArgsList, chunksize=chunksize)
        for result in imapUnordered:
            genePeakRowList.append(result)
    ## clean up
    del genePeakRowDict
    del bulkArgsList
    ## merge peaks from same chromosome
    chrPeakRowDict = defaultdict(list)
    chrTxidExpDict = defaultdict(dict)
    for peakRowList in genePeakRowList:
        for peakRow in peakRowList:
            ##peakRow -> [bed12Row + [peakFlag, peakIpCoverage, peakTxExp]]
            bedRow = peakRow[0:12]
            chrom = bedRow[0]
            ## record peakRow by chrom
            chrPeakRowDict[chrom].append(peakRow)
    ##get peakRowList for each chrom
    bulkArgsList = []
    for chrom in sorted(chrPeakRowDict.keys()):
        bulkArgsList.append([options, chrPeakRowDict[chrom]])
    ##remove redundant peaks of each chrom in parallel
    chunksize = max(1, int(len(bulkArgsList) / options.thread))
    chrPeakRowList = []
    with closing(get_context(options.threadstart).Pool(options.thread)) as pool:
        imapUnordered = pool.imap_unordered(slimOverlapPeak, bulkArgsList, chunksize=chunksize)
        for result in imapUnordered:
            chrPeakRowList.append(result)
    ## clean up
    del chrPeakRowDict
    del chrTxidExpDict
    del bulkArgsList
    ## decode into a list and make peakid unique
    ## peakRow -> [bed12Row + [peakFlag, peakIpCoverage, txExp]]
    peakidDict = defaultdict(int)
    finalPeakRowList = []
    for peakRowList in chrPeakRowList:
        for peakRow in peakRowList:
            bedRow = peakRow[0:12]
            peakid = bedRow[3]
            peakidDict[peakid] += 1
            peakFlag = peakRow[12]
            if peakFlag is True:
                peakFlag = 'T'
            else:
                peakFlag = 'F'
            ## peakid = geneid:txid|condition|number|T or geneid:txid|condition|number|F
            peakRow[3] = options.idsepdict['peakid'].join([peakRow[3], label, str(peakidDict[peakid]), peakFlag])
            finalPeakRowList.append(peakRow)
    ## return sorted peak
    finalPeakRowList = sorted(finalPeakRowList, key=lambda x:(x[0], x[1], x[2]))
    return finalPeakRowList

def getIntersectPeakidPairFromPeak(options, peakRowList):
    ## running bedtools by command
    command = ' -s -split -wa -wb -nonamecheck '
    runResRowList = functools.runBedtools(options, command, peakRowList, peakRowList)
    ## only keep paired-peakid
    pariedidList = [ [ row[3], row[15] ] for row in runResRowList ]
    ## remove self intersection, likle [peakid1, peakid1]
    pariedidList = list(filter(lambda x:x[0] != x[1], pariedidList))
    return pariedidList

def getNonIntersectPeak(options, peakRowList, excPeakRowList):
    ## running bedtools by command
    command = ' -s -split -v -nonamecheck '
    runResRowList = functools.runBedtools(options, command, peakRowList, excPeakRowList)
    ## construct peakdict
    remainPeakidDict = {}
    for row in runResRowList:
        peakid = row[3]
        remainPeakidDict[peakid] = 1
    ## get filtered peakRowList without excPeakRowlist
    nonIntersectPeakRowList = []
    for peakRow in peakRowList:
        peakid = peakRow[3]
        if peakid in remainPeakidDict:
            nonIntersectPeakRowList.append(peakRow[0:12])
    return nonIntersectPeakRowList

def getNetworkEdgeFromPeak(options, peakRowList, peakidDict):
    ## peakRowList consisted of peaks from rep1, rep2, ..., and merge
    ## sort bed by chomoosome and then start
    ## get intersected peaks
    intersectResList = getIntersectPeakidPairFromPeak(options, peakRowList)
    ## construct overlap paired id list, [(peak1, peak2), (peak2, peak4), ...]
    intersectTupleList = []
    recordDict = {}
    for row in intersectResList:
        peakid1 = row[0]
        peakid2 = row[1]
        key = '_'.join([peakid1, peakid2])
        keyRev = '_'.join([peakid2, peakid1])
        ## skip b-a overlaps from a-b
        if key not in recordDict and keyRev not in recordDict:
            recordDict[key] = 1
            recordDict[keyRev] = 1
        else:
            continue
        intersectTupleList.append((peakid1, peakid2))
    ## find edge groups of network, [[('A', 'B'), ('B', 'C'), ('C', 'D')], ..]
    rawNetworkEdgeGroupList = functools.findNetworkEdgeGroup(intersectTupleList)
    return rawNetworkEdgeGroupList

def runMergePeakOnTx(options, poolBed, peakRow, txBedDict):
    mergeBed = poolBed.merge(peakRow, score='min', s=True, tx=True, overlap=True, cds=False, buildFlag=False, sep=options.idsepdict['bedutils'])
    mergeFlag = False
    if bool(mergeBed) is True:
        ##poolBed.a.name:peakid1=peakid2...
        poolTxidList = sorted(set(map(lambda x: getTxidFromPeakid(options, x), poolBed.a.name.split(options.idsepdict['bedutils']))))
        poolTxBedList = list(map(lambda x:txBedDict[x], poolTxidList))
        txid2 = getTxidFromPeakid(options, peakRow[3])
        txBed2 = txBedDict[txid2]
        for txBed1 in poolTxBedList:
            if txBed1.name != txBed2.name:
                intersectTxBed1 = mergeBed.intersect(txBed1, score='min', s=True, tx=True, part=False, cds=False, rescue=False, buildFlag=True, sep=options.idsepdict['bedutils'])
                intersectTxBed2 = mergeBed.intersect(txBed2, score='min', s=True, tx=True, part=False, cds=False, rescue=False, buildFlag=True, sep=options.idsepdict['bedutils'])
                ## if mergeBed on one of the tx, then break
                if bool(intersectTxBed1) is True or bool(intersectTxBed2) is True:
                    mergeFlag = True
                    break
            else:
                mergeFlag = True
                break
    if mergeFlag is False:
        mergeBed = False
    return mergeBed

def mergeNetworkEdge(bulkArgs):
    ##networkEdgeGroup: [('A', 'B'), ('B', 'C'), ('C', 'D')], the element must be unique
    options, edpeakRowList, txBedList, networkEdgeGroup, repCount = bulkArgs
    ## sort the input peakRowList by coordinates
    edpeakRowList = sorted(edpeakRowList, key=lambda x:(x[0], x[1], x[2]))
    ## construct sub-peakRowDict
    peakRowDict = defaultdict(dict)
    for i in range(len(edpeakRowList)):
        peakRow = edpeakRowList[i]
        peakid = peakRow[3]
        peakRowDict[peakid]['rank'] = i
        peakRowDict[peakid]['bed'] = peakRow[0:12]
        ## [peakFlag, peakIpCoverage, txExp]
        peakRowDict[peakid]['val'] = peakRow[12:]
    ## construct txid-bedDict
    txBedDict = {}
    for txBed in txBedList:
        txid = txBed.name.split(options.idsepdict['txinfo'])[3]
        txBedDict[txid] = txBed
    ## iterate the peak row and record information
    peakidList = []
    for peakid1, peakid2 in networkEdgeGroup:
        ## label, like shNS, shMETTL14,
        label1 = peakid1.split(options.idsepdict['peakid'])[1]
        label2 = peakid2.split(options.idsepdict['peakid'])[1]
        ## record the sample count
        peakidList.append(peakid1)
        peakidList.append(peakid2)
    ## unique and sort peaks by coordinates
    peakidList = list(set(peakidList))
    peakidList = sorted(peakidList, key=lambda x: peakRowDict[x]['rank'])
    ## try to merge peaks from samples and reference
    poolPeakRowList = []
    ambiguousFlag = False
    peakRow = peakRowDict[peakidList[0]]['bed']
    poolBed = bedutils.bed12ops(peakRow)
    for i in range(1, len(peakidList)):
        peakid = peakidList[i]
        peakRow = peakRowDict[peakid]['bed']
        poolBed = runMergePeakOnTx(options, poolBed, peakRow, txBedDict)
        ## if 2 peaks has different transcript structure, then set ambiguousFlag as True
        if bool(poolBed) is False:
            ambiguousFlag = True
            break
    if ambiguousFlag is False:
        peakRow = poolBed.a.list
        peakRow[4] = poolBed.a.exonlength
        peakRow[6] = poolBed.a.start
        peakRow[7] = poolBed.a.end
        poolPeakRowList.append(peakRow)
    else:
        bulkArgs = [options, edpeakRowList]
        peakRowList = slimOverlapPeak(bulkArgs)
        for peakRow in peakRowList:
            poolPeakRowList.append(peakRow[0:12])
    ## select unique txid for peak with higher expression of corresponding transcript
    for i in range(len(poolPeakRowList)):
        peakidList = poolPeakRowList[i][3].split(options.idsepdict['bedutils'])
        poolPeakRowList[i][3] = sorted(peakidList, key=lambda x:peakRowDict[x]['val'][2], reverse=True)[0]
    return poolPeakRowList

def intersectNetworkEdge(bulkArgs):
    ##networkEdgeGroup: [('A', 'B'), ('B', 'C'), ('C', 'D')], the element must be unique
    options, edpeakRowList, txBedList, networkEdgeGroup, repCount = bulkArgs
    ## sort the input peakRowList by coordinates
    edpeakRowList = sorted(edpeakRowList, key=lambda x:(x[0], x[1], x[2]))
    ## construct sub-peakRowDict
    peakRowDict = defaultdict(dict)
    for i in range(len(edpeakRowList)):
        peakRow = edpeakRowList[i]
        peakid = peakRow[3]
        peakRowDict[peakid]['rank'] = i
        peakRowDict[peakid]['bed'] = peakRow[0:12]
        ## [peakFlag, peakIpCoverage, txExp]
        peakRowDict[peakid]['val'] = peakRow[12:]
    ## construct txid-bedDict
    txBedDict = {}
    for txBed in txBedList:
        txid = txBed.name.split(options.idsepdict['txinfo'])[3]
        txBedDict[txid] = txBed
    ## iterate the peak row and record information
    labelCountDict = defaultdict(int)
    ambiguousFlag = False
    refPeakidList = []
    peakidList = []
    for peakid1, peakid2 in networkEdgeGroup:
        ## label, like shNS_rep1, POOL_REF
        label1 = peakid1.split(options.idsepdict['peakid'])[1]
        label2 = peakid2.split(options.idsepdict['peakid'])[1]
        ## skip the reference peak
        if label1 == options.labelref:
            refPeakidList.append(peakid1)
            continue
        if label2 == options.labelref:
            refPeakidList.append(peakid2)
            continue
        ## record the sample count
        peakidList.append(peakid1)
        peakidList.append(peakid2)
        labelCountDict[label1] += 1
        labelCountDict[label2] += 1
    ## judge whether the peaks uniquely overlap with each other
    labelList = sorted(labelCountDict.keys())
    if len(labelList) > 0:
        peakidCountList = list(map(lambda x:labelCountDict[x], labelList))
        equalCountFlag = all(i == peakidCountList[0] for i in peakidCountList)
        if (peakidCountList[0] < repCount and equalCountFlag) is False:
            ambiguousFlag = True
    else:
        ambiguousFlag = True
    ## unique and sort peaks by coordinates
    refPeakidList = list(set(refPeakidList))
    refPeakidList = sorted(refPeakidList, key=lambda x: peakRowDict[x]['rank'])
    peakidList = list(set(peakidList))
    peakidList = sorted(peakidList, key=lambda x: peakRowDict[x]['rank'])
    ## try to intersect peaks from samples and reference
    poolPeakRowList = []
    if ambiguousFlag is False:
        ## get overlap peaks from samples
        peakRow = peakRowDict[peakidList[0]]['bed']
        poolBed = bedutils.bed12ops(peakRow)
        for i in range(1, len(peakidList)):
            peakid = peakidList[i]
            peakRow = peakRowDict[peakid]['bed']
            poolBed = poolBed.intersect(peakRow, score='min', s=True, tx=True, part=False, cds=False, rescue=False, buildFlag=False, sep=options.idsepdict['bedutils'])
            ## if 2 peaks has different transcript structure, then set ambiguousFlag as True
            if bool(poolBed) is False:
                ambiguousFlag = True
                break
        ##if ambiguousFlag is False:
        ##    ## try to intersect with reference peak
        ##    refPeakidList = sorted(set(refPeakidList))
        ##    if len(refPeakidList) == 1 and ambiguousFlag is False:
        ##        refPeakid = refPeakidList[0]
        ##        mergePeakFlag = peakRowDict[refPeakid]['val'][0]
        ##        if mergePeakFlag is True:
        ##            peakRow = peakRowDict[refPeakid]['bed']
        ##            poolMergeBed = poolBed.intersect(peakRow, score='min', s=True, tx=True, part=False, cds=False, rescue=False, buildFlag=False, sep=options.idsepdict['bedutils'])
        ##            if bool(poolMergeBed) is True:
        ##                poolBed = poolMergeBed
        if ambiguousFlag is False:
            peakRow = poolBed.a.list
            peakRow[4] = poolBed.a.exonlength
            peakRow[6] = poolBed.a.start
            peakRow[7] = poolBed.a.end
            poolPeakRowList.append(peakRow)
    ## take peaks from reference for ambiguous peaks if nessesarry
    if ambiguousFlag is True:
        refPeakidList = sorted(set(refPeakidList))
        if len(refPeakidList) >= 1:
            for peakid in refPeakidList:
                poolPeakRowList.append(peakRowDict[peakid]['bed'])
        else:
            ## if no peak in reference, try to keep the refined one
            bulkArgs = [options, edpeakRowList]
            peakRowList = slimOverlapPeak(bulkArgs)
            for peakRow in peakRowList:
                poolPeakRowList.append(peakRow[0:12])
    ## select unique txid for peak with higher expression of corresponding transcript
    for i in range(len(poolPeakRowList)):
        peakidList = poolPeakRowList[i][3].split(options.idsepdict['bedutils'])
        poolPeakRowList[i][3] = sorted(peakidList, key=lambda x:peakRowDict[x]['val'][2], reverse=True)[0]
    return poolPeakRowList

def poolPeakBySplitParallel(options, peakRowList, repCount, peakMode, txBedDict):
    ## build peakid -> peakRow dictionary
    peakRowDict = {}
    for peakRow in peakRowList:
        peakid = peakRow[3]
        peakRowDict[peakid] = peakRow
    ## record the intersect peakid
    intersectDict = {}
    bulkArgsList = []
    networkEdgeGroupList = getNetworkEdgeFromPeak(options, peakRowList, peakRowDict)
    for networkEdgeGroup in networkEdgeGroupList:
        edgePeakidList = []
        txidList = []
        for networkEdgeTuple in networkEdgeGroup:
            for peakid in networkEdgeTuple:
                edgePeakidList.append(peakid)
                txid = getTxidFromPeakid(options, peakid)
                txidList.append(txid)
                intersectDict[peakid] = 1
        edpeakRowList = list(map(lambda x:peakRowDict[x], sorted(set(edgePeakidList))))
        txBedList = []
        if txBedDict is not None:
            txBedList = list(map(lambda x:txBedDict[x], sorted(set(txidList))))
        bulkArgsList.append( [ options, edpeakRowList, txBedList, networkEdgeGroup, repCount ] )
    ## get intersected peaks in parallel
    chunksize = max(1, int(len(bulkArgsList) / options.thread))
    poolPeakRowList = []
    with closing(get_context(options.threadstart).Pool(options.thread)) as pool:
        if peakMode == 'intersect':
            imapUnordered = pool.imap_unordered(intersectNetworkEdge, bulkArgsList, chunksize=chunksize)
        elif peakMode == 'merge':
            imapUnordered = pool.imap_unordered(mergeNetworkEdge, bulkArgsList, chunksize=chunksize)
        for resultList in imapUnordered:
            for result in resultList:
                poolPeakRowList.append(result)
    ## reuse un-intersected peaks
    for peakid in sorted(peakRowDict.keys()):
        if peakid not in intersectDict:
            peakRow = peakRowDict[peakid]
            poolPeakRowList.append(peakRow[0:12])
    return poolPeakRowList

def dedupPeak(peakRowList):
    peakDict = defaultdict(list)
    for peakRow in peakRowList:
        row = copy(peakRow)
        row[3] = 'NA'
        peak = '\t'.join(map(str, row[0:12]))
        peakDict[peak].append(peakRow)
    ## keep uniq peak locations
    peakRowList = []
    for peak in sorted(peakDict.keys()):
        ## sort peak by peakFlag, IpCov and txExp
        peakFlagCount = len(set(map(lambda x:x[12], peakDict[peak])))
        if peakFlagCount > 1:
            peakRow = sorted(filter(lambda x:x[12] is True, peakDict[peak]), key=lambda y: (y[13], y[14]), reverse=True)[0]
        else:
            peakRow = sorted(peakDict[peak], key=lambda x: (x[13], x[14]), reverse=True)[0]
        peakRowList.append(peakRow)
    return peakRowList

def poolPeak(options, peakRowList, repCount, label, peakMode='intersect', txBedDict=None):
    ## pooling peaks from replicates
    ## peakRowList consisted of peaks from rep1, rep2, ..., and merge
    ## construct peakid-peakRow dict
    ## the peakid must be unique, peakid = geneid:txid|condition|number|T(|F)
    ## peakRow = bed12Row + [peakFlag, peakIpCoverage, txExp]
    ## mode: intersect, merge
    peakRowDict = {}
    for peakRow in peakRowList:
        peakid = peakRow[3]
        peakRowDict[peakid] = peakRow
    ## pool any intersect peaks on peakRow with peakFlag is True
    tpeakRowList = list(filter(lambda x: x[12] is True, peakRowList))
    tpoolPeakRowList = poolPeakBySplitParallel(options, tpeakRowList, repCount, peakMode, txBedDict)
    ## pool any intersect peaks on peakRow with peakFlag is False
    fpeakRowList = list(filter(lambda x: x[12] is False, peakRowList))
    fpoolPeakRowList = poolPeakBySplitParallel(options, fpeakRowList, repCount, peakMode, txBedDict)
    ## exclude any false peaks that overlap with true peaks
    excfpoolPeakRowList = getNonIntersectPeak(options, fpoolPeakRowList, tpoolPeakRowList)
    ## get final poolPeakRowList
    poolPeakRowList = tpoolPeakRowList + excfpoolPeakRowList
    ## sort and get final peakRowList
    poolPeakRowList = sorted(poolPeakRowList, key=lambda x:(x[0], x[1]))
    reconPeakRowList = []
    ## reconstruct peakid with new label and filter by peaksize
    for i in range(len(poolPeakRowList)):
        peakRow = poolPeakRowList[i][0:12]
        peakBed = bedutils.buildbed(peakRow)
        ## filter out small peaks
        if peakBed.exonlength < options.peaksize:
            continue
        peakid = peakRow[3]
        peakidRow = peakid.split(options.idsepdict['bedutils'])[0].split(options.idsepdict['peakid'])
        peakFlag = peakidRow[3]
        ## reconstruct new peakid = geneid:txid#mature|condition|number|T(|F)
        peakRow[3] = options.idsepdict['peakid'].join([peakidRow[0], label, str(i+1), peakFlag])
        ## add additional values, like peakFlag, ipCov, txExp
        peakRow += peakRowDict[peakid][12:]
        reconPeakRowList.append(peakRow)
    ## remove any duplicate location records
    finalPeakRowList = dedupPeak(reconPeakRowList)
    finalPeakRowList = sorted(finalPeakRowList, key=lambda x:(x[0], x[1]))
    return finalPeakRowList

def getArrMargin(dataArr, cutoff):
    overIndexArr = np.where(dataArr >= cutoff)[0]
    if overIndexArr.size > 0:
        ## find margin group
        lMargin = overIndexArr.min()
        rMargin = overIndexArr.max()
    else:
        lMargin = 0
        rMargin = dataArr.size
    marginSize = rMargin - lMargin
    return [lMargin, rMargin, marginSize]

def getMaxMargin(dataArr, center):
    size = dataArr.size
    ## get the highest coverage point
    maxIndex = int(np.mean(np.where(dataArr >= np.quantile(dataArr, 0.90))))
    ## fine-tune max margin by max value
    if maxIndex == 0:
        leftPct = 0.1 * center
    elif maxIndex == size - 1:
        leftPct = 0.9 * center
    else:
        leftPct = maxIndex / size * center
    rightPct = center - leftPct
    mMarginSize = size * (1 - center)
    mlMargin = int(size * leftPct)
    mrMargin = int(size * (1 - rightPct))
    return [mlMargin, mrMargin, mMarginSize]

def centerPeak(options, dataArr, ratio, cutoff):
    ## Center the candidate peak region by shearing points of which are less than --center of highest coverage
    peaksize = options.peaksize
    if ratio > 0:
        if ratio < 1:
             center = options.center * ( 1 + ratio )
        else:
            center = options.center * ( 1 + 1 / ratio )
    else:
        center = options.center
    ## make sure center percentage no more than 0.6
    if center > 0.6:
        center = 0.6
    elif center < options.center:
        center = options.center
    ## define maximum shear margin
    dataSize = dataArr.size
    ## get the cutoff of data points
    dataVal = dataArr.mean()
    dataArrQuant = np.quantile(dataArr, center)
    dataMaxQuant = np.quantile(np.array([0, dataArr.max()]), center)
    dataCutoff = max(dataArrQuant, dataMaxQuant, cutoff)
    mlMargin, mrMargin, mMarginSize = getMaxMargin(dataArr, center)
    ## get margin index
    lMargin, rMargin, marginSize = getArrMargin(dataArr, dataCutoff)
    if marginSize > peaksize:
        if marginSize > mMarginSize:
            if lMargin < mlMargin:
                lMargin = mlMargin
            if rMargin > mrMargin:
                rMargin = mrMargin
        else:
            if marginSize < min(peaksize * 4, 100):
                lMargin = mlMargin
                rMargin = mrMargin
    else:
        lMargin = 0
        rMargin = dataSize
    return [lMargin, rMargin]

def peakToSaf(options, peakRowList, safMatrixFile):
    safRowList = [['GeneID', 'Chr', 'Start', 'End', 'Strand']]
    ##  convert peakRow into the SAF-format
    for peakRow in peakRowList:
        bed12Row = peakRow[0:12]
        peakBed = bedutils.buildbed(bed12Row).decode()
        peakid = peakBed.name
        chrom = peakBed.chr
        strand = peakBed.strand
        for exon in peakBed.exon:
            safRow = [peakid, chrom, exon[0] + 1, exon[1], strand]
            safRowList.append(safRow)
    ## construct final saf file library
    with open(safMatrixFile, 'w', buffering=options.buffer) as temp:
        for row in safRowList:
            temp.write('\t'.join(map(str, row)) + '\n')

def getPeakReadCountsDf(options, peakRowList, bamList, normalize=False):
    ## the peak id must unique
    ## convert peakRowList to SAF format
    safMatrixFileTmp = tempfile.NamedTemporaryFile(suffix='.saf.tmp', prefix=options.tempre, dir=options.tempdir, delete=True)
    peakToSaf(options, peakRowList, safMatrixFileTmp.name)
    ## get reads into dataframe
    peakReadCountDf = signals.getReadCountsDf(options, safMatrixFileTmp.name, 'peak', bamList, normalize=False, keeplen=False)
    if normalize is True:
        sizeFactorSeries = correction.calMedianRatio(peakReadCountDf)
        ## debug
        options.debug("Normalize read counts by calculated size factor:")
        options.debug("\n" + sizeFactorSeries.to_markdown())
        ## get corrected reads
        peakReadCountDf = correction.normalizeCountDf(peakReadCountDf, sizeFactorSeries)
    ## delete safMatrixFileTmp file
    safMatrixFileTmp.close()
    ## return final reads dataframe
    return peakReadCountDf
