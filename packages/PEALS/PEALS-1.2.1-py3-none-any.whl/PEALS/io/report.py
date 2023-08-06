# -*- coding: utf-8 -*-
##########################################
#           utility                      #
#          2021.8.5                      #
##########################################
__author__ = "Keren Zhou"
__version__ = "v1.0"

import os
import sys
import numpy as np
import math
import re
from collections import defaultdict

from PEALS.collection import bedutils

def getSigTestResDf(options, testResDf):
    ## filter results by fdr, pvalue and fold enrichment
    if options.poolmode == 'pool':
        pvalcutoff = math.log10(options.pvalcutoff)
        padjcutoff = math.log10(options.padjcutoff)
        foldcutoff = math.log2(options.foldcutoff)
        testResDf = testResDf.loc[ (testResDf['log10padj'] <= padjcutoff) & (testResDf['log10pval'] <= pvalcutoff) & (testResDf['log2fc'] >= foldcutoff) ]
    elif options.poolmode == 'diff':
        pvalcutoff = math.log10(options.diffpvalcutoff)
        padjcutoff = math.log10(options.diffpadjcutoff)
        foldcutoff = math.log2(options.difffoldcutoff)
        testResDf = testResDf.loc[ (testResDf['log10padj'] <= padjcutoff) & (testResDf['log10pval'] <= pvalcutoff) ]
        if foldcutoff == 1:
            testResDf = testResDf.loc[ (testResDf['log2fc'] < - foldcutoff) | (testResDf['log2fc'] > foldcutoff) ]
        else:
            testResDf = testResDf.loc[ (testResDf['log2fc'] <= - foldcutoff) | (testResDf['log2fc'] >= foldcutoff) ]
    return testResDf

def peakReflag(options, testResDf, peakRowList):
    testSigResDf = getSigTestResDf(options, testResDf)
    peakCount = len(peakRowList)
    for i in range(peakCount):
        ## peakid = geneid:txid|condition|number|T(|F)
        peakid = peakRowList[i][3]
        peakidRow = peakid.split(options.idsepdict['peakid'])
        peakFlag = peakRowList[i][12]
        if peakFlag is True:
            if peakid in testSigResDf.index:
                peakidRow[3] = 'T'
                peakRowList[i][12] = True
            else:
                peakidRow[3] = 'F'
                peakRowList[i][12] = False
            peakRowList[i][3] = options.idsepdict['peakid'].join(peakidRow)
    return peakRowList

def peakReport(options, txBedDict, testResDf, peakRowList):
    ## peakRowList = [bed12Row, bed12Row, ...]
    peakBed = os.path.join(options.outputdir, options.prefix + '.bed')
    peakTxt = os.path.join(options.outputdir, options.prefix + '.txt')
    ## get significant peaks
    testResDf = getSigTestResDf(options, testResDf)
    ## sort testing results by log10padj
    testResDf = testResDf.sort_values(by=['log10padj'])
    ## output bed
    bedRow = ['chrom', 'chromStart', 'chromEnd', 'name', 'score', 'strand']
    bedRow += ['thickStart', 'thickEnd', 'itemRgb', 'blockCount', 'blockSizes', 'blockStarts']
    txtRow = bedRow + ['log2FC', 'log10Pval', 'log10Padj', 'peakLength']
    if options.poolmode == 'pool':
        txtRow += ['ipMean', 'inputMean']
    else:
        if 'cinputMean' in testResDf and 'tinputMean' in testResDf:
            txtRow += ['controlIpMean', 'controlInputMean', 'treatedIpMean', 'treatedInputMean']
        else:
            txtRow += ['controlIpMean', 'treatedIpMean']
    txtRow += ['geneid', 'geneName', 'geneType', 'txid', 'txName', 'txType']
    ## add '#' to first row
    bedRow[0] = '#chrom'
    ## convert peakRowList to dict
    peakBedDict = {}
    for peakRow in peakRowList:
        ## get peakid, geneid:txid|condition|number|T(|F)
        peakid = peakRow[3]
        peakBedDict[peakid] = peakRow[0:12]
    ## preparing for output
    uniqDict = defaultdict(int)
    with open(peakBed, 'w') as bedOut, open(peakTxt, 'w') as txtOut:
        bedOut.write('\t'.join(bedRow) + '\n')
        txtOut.write('\t'.join(txtRow) + '\n')
        for peakid in testResDf.index:
            bedRow = peakBedDict[peakid]
            ## get peak annotations
            geneid, labelTxid = peakid.split(options.idsepdict['peakid'])[0].split(options.idsepdict['genetx'])
            #geneid, geneName, geneType, labelTxid, txName, txType = txBedDict[labelTxid].name.split(':')
            txidInforList = txBedDict[labelTxid].name.split(options.idsepdict['txinfo'])
            ## reget the transcript id
            txidInforList[3] = txidInforList[3].split(options.idsepdict['labeltxid'])[0]
            ## rename peakid in format: geneid+number
            bedRow[3] = '{}{}{}'.format(geneid, options.idsepdict['peakid_out'], uniqDict[geneid] + 1)
            ## get testing results of this peak
            peakTestRes = testResDf.loc[peakid, :]
            log2fc = peakTestRes['log2fc']
            log10pval = peakTestRes['log10pval']
            log10padj = peakTestRes['log10padj']
            ## re-value bed score
            peakLength = bedutils.buildbed(bedRow).exonlength
            bedRow[4] = -peakTestRes['log10pval']
            ## construct txtRow
            txtRow = bedRow + [log2fc, log10pval, log10padj, peakLength]
            ## get additional information
            if options.poolmode == 'pool':
                ipMean = peakTestRes['ipMean']
                inputMean = peakTestRes['inputMean']
                txtRow += list(map(lambda x: round(x, 3), [ipMean, inputMean]))
            else:
                cipMean = peakTestRes['cipMean']
                tipMean = peakTestRes['tipMean']
                if 'cinputMean' in testResDf and 'tinputMean' in testResDf:
                    cinputMean = peakTestRes['cinputMean']
                    tinputMean = peakTestRes['tinputMean']
                    txtRow += list(map(lambda x: round(x, 3), [cipMean, cinputMean, tipMean, tinputMean]))
                else:
                    txtRow += list(map(lambda x: round(x, 3), [cipMean, tipMean]))
            ## add txid information
            txtRow += txidInforList
            ## output bed format
            bedOut.write('\t'.join(map(str, bedRow)) + '\n')
            txtOut.write('\t'.join(map(str, txtRow)) + '\n')
            ## output txt format
            uniqDict[geneid] += 1
