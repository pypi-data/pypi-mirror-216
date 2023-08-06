# -*- coding: utf-8 -*-
##########################################
#           correction                   #
#          2022.3.16                     #
##########################################
__author__ = "Keren Zhou"
__version__ = "v1.0"

import re
import pandas as pd
import numpy as np
from scipy import stats
from collections import defaultdict

from PEALS.stats import peaktest
from PEALS.collection import functools

def calMedianRatio(df):
    ## calculate the size factor for each library by median of ratio
    ## ref https://hbctraining.github.io/DGE_workshop/lessons/02_DGE_count_normalization.html
    ## df, row:gene, column:sample
    ## remove row with low counts, avoid the o of geometric mean
    df = df[ (df >0).all(axis=1)] 
    ## creates a pseudo-reference sample (row-wise geometric mean), stats.gmean(df, axis=1)
    ## calculates ratio of each sample to the reference, df.divide(stats.gmean(df, axis=1), axis=0)
    ## calculate the normalization factor for each sample (size factor)
    ## data structure of sizeFactorArr
    '''sizeFactorArr
    input_0_0    0.870778
    input_0_1    0.951707
    ip_1_0       1.075325
    ip_1_1       1.144250
    dtype: float64
    '''
    medianRatioSeries = df.divide(stats.gmean(df, axis=1), axis=0).median(axis=0)
    return medianRatioSeries

def normalizeCountDf(readDf, sizeFactorSeries):
    norReadDf = readDf.divide(sizeFactorSeries, axis=1)
    return norReadDf

def normalizeDfByMedian(options, readDf):
    ## the the median-of-ratio
    sizeFactorSeries = calMedianRatio(readDf)
    ## debug
    options.debug("Normalize read counts by estimated size factor:\n" + sizeFactorSeries.to_markdown())
    ## the normalized input reads for each gene
    norReadDf = normalizeCountDf(readDf, sizeFactorSeries)
    return norReadDf

def normalizeByEnrichment(options, peakReadCountDf, geneInputReadCountDf):
    ## get bamidList
    bamidList = peakReadCountDf.columns
    subMatrixDf = options.matrixdf.loc[bamidList, ]
    inputBamidList = functools.getBamidFromDf(subMatrixDf, [['library', 'input']], ['condition', 'replicate'], ascending=True)
    ipBamidList = functools.getBamidFromDf(subMatrixDf, [['library', 'ip']], ['condition', 'replicate'], ascending=True)
    ## get bamid for ip libraries
    cipBamidList = functools.getBamidFromDf(subMatrixDf, [['library', 'ip'], ['condition', 'control']], ['replicate'], ascending=True)
    tipBamidList = functools.getBamidFromDf(subMatrixDf, [['library', 'ip'], ['condition', 'treated']], ['replicate'], ascending=True)
    ## normalize input reads by median-of-ratio of genes
    inputSizeFactorSeries = calMedianRatio(geneInputReadCountDf)
    options.debug("Normalize gene read counts by estimated size factor:\n" + inputSizeFactorSeries.to_markdown())
    geneNorInputReadCountDf = normalizeCountDf(geneInputReadCountDf, inputSizeFactorSeries)
    ## get normalized input
    peakInputDf = peakReadCountDf.loc[:, inputBamidList]
    peakNorInputDf = normalizeCountDf(peakInputDf, inputSizeFactorSeries)
    ## reorder the column
    geneNorInputReadCountDf = geneNorInputReadCountDf.reindex(columns=inputBamidList)
    ## construct gene counts to each peak
    peakGeneDict = defaultdict(list)
    for peakid in peakReadCountDf.index:
        geneid = peakid.split(options.idsepdict['peakid'])[0].split(options.idsepdict['genetx'])[0]
        peakGeneDict[geneid].append(peakid)
    ## get IP read count df of peak
    peakIpDf = peakReadCountDf.loc[:, ipBamidList]
    ## copy peakIpDf to a new df
    peakGeneInputDf = peakIpDf.copy()
    geneidList = sorted(peakGeneDict.keys())
    geneidReadCountList = [ geneNorInputReadCountDf.loc[i, :].to_list() for i in geneidList ]
    for i in range(len(geneidList)):
        peakidList = peakGeneDict[geneidList[i]]
        peakGeneInputDf.loc[ peakidList, :] = geneidReadCountList[i]
    ## remove any zero from inputs
    peakNonZeroGeneInputDf = peakGeneInputDf.loc[(peakGeneInputDf > 0).all(axis=1)]
    peakidList = peakNonZeroGeneInputDf.index.to_list()
    ## estimate the ip efficiency by ip/input in peak region
    ## using all corrected peak regions to calculate the IP enrichment factor
    peakIpFilterDf = peakIpDf.loc[peakidList, :]
    peakOnlyIpDf = peakIpFilterDf[peakIpFilterDf.index.str.contains(options.peakregex, regex = True)]
    if options.estipeff == 'within':
        ## normalize by the library size first
        libSizeDf = subMatrixDf.loc[ipBamidList, :]['lib_size']
        libSizeFactor = libSizeDf.div(libSizeDf.min())
        options.info("Normalize IP reads count by sequencing depth with library size factors:\n" + libSizeFactor.to_markdown())
        peakNorIpDf = peakIpDf.div(libSizeFactor)
        ## get gene reads count df
        peakOnlyNorInputDf = peakGeneInputDf.loc[peakidList, ]
        ## normalize IP read counts per condition
        conditionList = ['control', 'treated']
        bamidList2d = [cipBamidList, tipBamidList]
        for i in range(2):
            condition = conditionList[i]
            bamidList = bamidList2d[i]
            ## divide the IP reads count by gene counts
            ipEfficiencyDf = peakOnlyIpDf.loc[:, bamidList].div(peakOnlyNorInputDf.loc[:, bamidList])
            ## determining the the size factor with median-of-ratio
            ipSizeFactorSeries = calMedianRatio(ipEfficiencyDf)
            ## debug
            options.info("Normalize IP read counts ({}) by estimated IP efficiency factor:\n".format(condition) + ipSizeFactorSeries.to_markdown())
            ## normalize by calcualted IP efficiency factors
            peakNorIpDf.loc[:, bamidList] = normalizeCountDf(peakNorIpDf.loc[:, bamidList], ipSizeFactorSeries)
    elif options.estipeff == 'across':
        ## only use peaks that are higher than 25% in all samples
        options.info("only use top 50\% enriched peaks in all samples.")
        peakOnlyIpDf = peakOnlyIpDf[ peakOnlyIpDf > peakOnlyIpDf.quantile(0.5) ]
        ## filter out rows contain NaN in any columns
        peakOnlyIpDf = peakOnlyIpDf[peakOnlyIpDf.notnull().all(1)]
        peakidList = peakOnlyIpDf.index.to_list()
        options.info("{} of peak candidates used for calculating the IP efficiency factors.".format(len(peakidList)))
        ## retrive corresponding gene counts
        peakOnlyNorInputDf = peakGeneInputDf.loc[peakidList, ]
        ## divide the IP reads count by gene counts
        ipEfficiencyDf = peakOnlyIpDf.div(peakOnlyNorInputDf)
        ## determining the the size factor with median-of-ratio
        ipSizeFactorSeries = calMedianRatio(ipEfficiencyDf)
        ## debug
        options.info("Normalize IP read counts by estimated IP efficiency factor:\n" + ipSizeFactorSeries.to_markdown())
        ## normalize by calcualted IP efficiency factors
        peakNorIpDf = normalizeCountDf(peakIpDf, ipSizeFactorSeries)
    return [peakNorIpDf, peakNorInputDf]

def normalizeByEnrichmentByGenesum(options, peakReadCountDf):
    ## get bamidList
    bamidList = peakReadCountDf.columns
    subMatrixDf = options.matrixdf.loc[bamidList, ]
    inputBamidList = functools.getBamidFromDf(subMatrixDf, [['library', 'input']], ['condition', 'replicate'], ascending=True)
    ipBamidList = functools.getBamidFromDf(subMatrixDf, [['library', 'ip']], ['condition', 'replicate'], ascending=True)
    ## normalize input reads by median-of-ratio
    options.debug("Normalize input read counts of peak candidates.")
    peakInputDf = peakReadCountDf.loc[:, inputBamidList]
    peakNorInputDf = normalizeDfByMedian(options, peakInputDf)
    ## remove any zero from inputs
    peakNorInputDf = peakNorInputDf.loc[(peakNorInputDf > 0).all(axis=1)]
    peakidList = peakNorInputDf.index.to_list()
    ## get the gene-level counts of INPUT library, by summing up peak-level read counts of each gene
    peakGeneDict = defaultdict(list)
    for peakid in peakNorInputDf.index:
        geneid = peakid.split(options.idsepdict['peakid'])[0].split(options.idsepdict['genetx'])[0]
        peakGeneDict[geneid].append(peakid)
    ## get geneid list
    geneidList = sorted(peakGeneDict.keys())
    geneSumList = [ peakNorInputDf.loc[ peakGeneDict[i], :].sum(axis=0).to_list() for i in geneidList ]
    ## get the gene-level counts of INPUT library, by summing up peak-level read counts of each gene
    inputGeneSumDf = peakNorInputDf.copy()
    colMapDict = dict(zip(inputBamidList, ipBamidList))
    inputGeneSumDf.rename(columns=colMapDict, inplace=True)
    for i in range(len(geneidList)):
        peakidList = peakGeneDict[geneidList[i]]
        inputGeneSumDf.loc[ peakidList, :] = geneSumList[i]
    ## normalize ip reads
    peakIpDf = peakReadCountDf.loc[:, ipBamidList]
    ## get peak region with high ip-affinity
    ## using all corrected peak regions to calculate the IP enrichment factor
    peakIpDf = peakReadCountDf.loc[peakidList, ipBamidList]
    peakOnlyIpDf = peakIpDf[peakIpDf.index.str.contains(options.peakregex, regex = True)]
    peakTopIpDf = peakOnlyIpDf[(peakOnlyIpDf > peakOnlyIpDf.quantile(0.75)).all(axis=1)]
    peakidList = peakTopIpDf.index.to_list()
    inputGeneSumHighDf = inputGeneSumDf.loc[peakidList, :]
    ## to avoid 0 in dataframe
    nonZeroMinVal = inputGeneSumHighDf[(inputGeneSumHighDf > 0).all(axis=1)].min().min()
    inputGeneSumHighDf.replace(0, nonZeroMinVal, inplace=True)
    ## get enrichment df
    ipEnrichDf = peakEnrichIpDf.div(inputGeneSumHighDf)
    ## determining the the size factor with median-of-ratio
    ipSizeFactorSeries = calMedianRatio(ipEnrichDf)
    ## combine ip and input size factors
    peakIpNorDf = normalizeCountDf(peakIpDf, ipSizeFactorSeries)
    return [peakIpNorDf, peakInputNorDf]

def adjustByPreipGeneShrinkFc(options, peakNorIpDf, geneReadCountDf):
    ## peakNorIpDf, normalized ip read counts, geneReadCountDf, raw input read counts
    bamidList = peakNorIpDf.columns.to_list()
    subMatrixDf = options.matrixdf.loc[bamidList, ]
    cipBamidList = functools.getBamidFromDf(subMatrixDf, [['condition', 'control']], ['condition', 'replicate'], ascending=True)
    tipBamidList = functools.getBamidFromDf(subMatrixDf, [['condition', 'treated']], ['condition', 'replicate'], ascending=True)
    ## calculate the normalize factors by calculating the DE shrinkaged with "apeglm"
    ## to eliminate the overestimation of DE by lowly expressed genes
    options.debug("Estimating the gene expresion changes between conditions...")
    testResDf = peaktest.runGlmNbinomTest(options, geneReadCountDf, plot=False, skipSubplot=True)
    ## fill "NaN" by 1
    testResDf.fillna(1, inplace=True)
    ## create the geneShrinkFcDf
    colNameList = peakNorIpDf.columns.to_list()
    geneShrinkFcDf = pd.concat( [ np.exp2(testResDf['log2fc']) ] * len(colNameList), axis=1 )
    geneShrinkFcDf.columns = colNameList
    ## change normalize factor, allways normalize to lower one
    for column in cipBamidList:
        greaterIndexList = geneShrinkFcDf[column][ geneShrinkFcDf[column] < 1 ].index.to_list()
        lessIndexList = geneShrinkFcDf[column][ geneShrinkFcDf[column] > 1 ].index.to_list()
        geneShrinkFcDf[column].loc[greaterIndexList, ] = np.divide(1, geneShrinkFcDf[column].loc[greaterIndexList, ])
        geneShrinkFcDf[column].loc[lessIndexList, ] = 1.0
    for column in tipBamidList:
        lessIndexList = geneShrinkFcDf[column][ geneShrinkFcDf[column] < 1 ].index.to_list()
        geneShrinkFcDf[column].loc[lessIndexList, ] = 1.0
    ## extract input counts of corresponding gene
    peakGeneWiseFactorDict = {}
    for peakid in peakNorIpDf.index:
        geneid = peakid.split(options.idsepdict['peakid'])[0].split(options.idsepdict['genetx'])[0]
        peakGeneWiseFactorDict[peakid] = geneShrinkFcDf.loc[geneid,:].to_list()
    ## construct peakid->gene input counts df
    peakGeneWiseFactorDf = pd.DataFrame.from_dict(peakGeneWiseFactorDict, orient='index', columns = colNameList)
    ## normalize peak ip reads by factor
    options.debug("Normalize IP read counts by gene fold changes.")
    peakReadCountNorDf = peakNorIpDf.div(peakGeneWiseFactorDf)
    return peakReadCountNorDf

def adjustByPreipGeneLevel(options, peakNorIpDf, geneReadCountDf):
    ## peakNorIpDf, normalized ip read counts, geneReadCountDf, raw input read counts
    bamidList = peakNorIpDf.columns.to_list() + geneReadCountDf.columns.to_list()
    subMatrixDf = options.matrixdf.loc[bamidList, ]
    ipBamidList = subMatrixDf[ subMatrixDf['library'] == 'ip' ].sort_values(by=['condition', 'replicate'], ascending=True).index.to_list()
    inputBamidList = subMatrixDf[ subMatrixDf['library'] == 'input' ].sort_values(by=['condition', 'replicate'], ascending=True).index.to_list()
    colMapDict = dict(zip(inputBamidList, ipBamidList))
    ## the normalized input reads of gene by using median-of-ratio
    options.debug("Normalize gene read counts of input samples...")
    geneInputNorDf = normalizeDfByMedian(options, geneReadCountDf)
    ## replace zero with min expression
    minVal = geneInputNorDf[(geneInputNorDf > 0).all(1)].min().mean()
    geneInputNorDf.replace(0, minVal, inplace=True)
    ## debug
    options.debug("Adjust gene read counts across input samples by normalizing to 1.")
    geneWiseFactorDf = geneInputNorDf.div(geneInputNorDf.mean(axis=1), axis=0)
    ## extract input counts of corresponding gene
    peakGeneWiseFactorDict = {}
    columns = geneWiseFactorDf.iloc[0,:].index.to_list()
    mapToIpColumns = list(map(lambda x:colMapDict[x], columns))
    for peakid in peakNorIpDf.index:
        geneid = peakid.split(options.idsepdict['peakid'])[0].split(options.idsepdict['genetx'])[0]
        peakGeneWiseFactorDict[peakid] = geneWiseFactorDf.loc[geneid,:].to_list()
    ## construct peakid->gene input counts df
    peakGeneWiseFactorDf = pd.DataFrame.from_dict(peakGeneWiseFactorDict, orient='index', columns=mapToIpColumns)
    ## normalize peak ip reads by factor
    options.debug("Normalize IP read counts by normalzed gene read counts.")
    peakReadCountNorDf = peakNorIpDf.div(peakGeneWiseFactorDf)
    return peakReadCountNorDf
