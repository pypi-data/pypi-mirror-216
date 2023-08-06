# -*- coding: utf-8 -*-
##########################################
#           peaktest                     #
#          2021.8.5                      #
##########################################
__author__ = "Keren Zhou"
__version__ = "v1.0"

import sys
import os
import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger
import math
import mpmath
import logging
import pickle

from PEALS.peak import peakutils
from PEALS.collection import bamtool
from PEALS.collection import functools
from PEALS.stats import statstools

## suppress warnings from rpy2
rpy2_logger.setLevel(logging.ERROR)

def runNbinomTest(options, peakReadCountDf):
    ## normalize by the library size first
    bamidList = peakReadCountDf.columns
    subMatrixDf = options.matrixdf.loc[bamidList, ]
    libSizeDf = subMatrixDf['lib_size']
    libSizeFactor = libSizeDf.div(libSizeDf.min())
    options.debug("Normalize reads count by sequencing depth with library size factors:\n" + libSizeFactor.to_markdown())
    peakReadCountNorDf = peakReadCountDf.div(libSizeFactor)
    ## get ip and input sample id
    inputBamidList = functools.getBamidFromDf(subMatrixDf, [['library', 'input']], ['replicate'], ascending=True)
    ipBamidList = functools.getBamidFromDf(subMatrixDf, [['library', 'ip']], ['replicate'], ascending=True)
    ## peakReadCountNorDf, peak read counts dataframe
    ## ipCol, inputCol, the index of ip and input column
    ## The probability mass function of the number of failures for nbinom is:
    ## f(k) = C(k+n-1, n-1) * p**n * (1-p)**k
    ## get reads of ip and input, and replace peak 0 read with 1
    ipReads = peakReadCountNorDf[ipBamidList].replace(0, 1).squeeze()
    inputReads = peakReadCountNorDf[inputBamidList].replace(0, 1).squeeze()
    ## get the successful probability p0
    prob = ipReads.sum() / (ipReads.sum() + inputReads.sum())
    p0 = robjects.FloatVector([prob])[0]
    ## only keep peaks for downstream analysis
    ##filterDf = peakReadCountNorDf.filter(regex=r'\|\d+\|T$', axis=0)
    ##ipReads = filterDf[ipBamidList].replace(0, 1).squeeze()
    ##inputReads = filterDf[inputBamidList].replace(0, 1).squeeze()
    ## get the p-value to H0: p < p0, using pnbinom in R, get high precision of p-value
    k = robjects.FloatVector(inputReads.to_numpy())
    size = robjects.FloatVector(ipReads.to_numpy())
    log10PvalArr = np.array(robjects.r['pnbinom'](k, size, p0, log='TRUE')) / np.log(10)
    ## perform fdr corrections
    alpha = 0.05
    ## transfer 'BH' to 'padjmethod'
    #if options.padjmethod == 'BH':
    #    padjmethod = 'BH'
    #else:
    #    padjmethod = 'none'
    #fdrArr = statstools.fdr_correction(mpmath.mpf(10) ** log10PvalArr, alpha=alpha, method=padjmethod)[1]
    # use R to calculate the adjusted P-value
    pvalArr = mpmath.mpf(10) ** log10PvalArr
    fdrArr = np.array(robjects.r['p.adjust'](robjects.FloatVector(pvalArr), method = options.padjmethod))
    log10FdrArr = np.array([mpmath.log10(fdr) for fdr in fdrArr])
    ## example results
    ## array([-7.69204611e-02, -4.06128956e-02, -7.69204611e-02, ...,  -7.69204611e-02, -1.55633270e-01, -3.35241642e-06])
    log2FcArr = np.log2(ipReads.divide(inputReads)).to_numpy()
    dataArr = np.vstack((log2FcArr, log10PvalArr, log10FdrArr)).T
    nbinomResDf =  pd.DataFrame(data = dataArr, columns = ['log2fc', 'log10pval', 'log10padj'], index =peakReadCountNorDf.index)
    ## add reads to dataframe
    nbinomResDf['ipMean'] = peakReadCountNorDf[ipBamidList]
    nbinomResDf['inputMean'] = peakReadCountNorDf[inputBamidList]
    ##filter out non-peak
    nbinomResDf = nbinomResDf.filter(regex=options.peakregex, axis=0)
    ## example results:
    '''the structure of nbinomResDf
                                                          log2fc log10pval             log10fdr      ipMean   inputMean
    peakid
    ENSG00000279124.1:ENST00000625078.1|shNS:rep1|2|T    0.77444 -0.624764   -0.124156355588276   29.068884   16.994117
    ENSG00000279124.1:ENST00000625078.1|shNS:rep1|3|T    1.69116  -2.28794    -1.55436159657553   34.659054   10.733126
    ENSG00000279124.1:ENST00000625078.1|shNS:rep1|5|T    1.66588  -2.30837    -1.57406449106716   36.895122   11.627553
    ENSG00000279124.1:ENST00000625078.1|shNS:rep1|6|T   0.514573 -0.255656                  0.0    8.944272    6.260990
    ENSG00000279730.2:ENST00000623146.2|shNS:rep1|1|T    1.56986  -14.8171    -13.6633373897861  382.367624  128.797516
    ...                                                      ...       ...                  ...         ...         ...
    ENSG00000185220.12:ENST00000329291.6|shNS:rep1|6|T   3.47843  -33.6471    -32.2319074831034  239.259274   21.466253
    ENSG00000185220.12:ENST00000329291.6|shNS:rep1|7|T   1.32193 -0.527333  -0.0656621012841558    2.236068    0.894427
    ENSG00000185220.12:ENST00000355360.8|shNS:rep1|1|T  0.321928 -0.263666                  0.0    1.118034    0.894427
    ENSG00000233084.2:ENST00000430973.1|shNS:rep1|2|T    1.21552  -9.57693    -8.53759928616526  452.803765  194.985128
    '''
    ## return glmNbinom results and normalized counts
    return nbinomResDf

def runFisherTest(options, peakReadCountDf):
    ## normalize by the library size first
    bamidList = peakReadCountDf.columns
    subMatrixDf = options.matrixdf.loc[bamidList, ]
    libSizeDf = subMatrixDf['lib_size']
    libSizeFactor = libSizeDf.div(libSizeDf.min())
    options.debug("Normalize reads count by sequencing depth with library size factors:\n" + libSizeFactor.to_markdown())
    peakReadCountNorDf = peakReadCountDf.div(libSizeFactor)
    ## convert into int64
    for i in peakReadCountNorDf.columns:
        try:
            peakReadCountNorDf[[i]] = peakReadCountNorDf[[i]].astype('int64')
        except:
            pass
    ## get ip and input bam id
    cinputBamidList = functools.getBamidFromDf(subMatrixDf, [['condition', 'control'], ['library', 'input']], ['replicate'], ascending=True)
    cipBamidList = functools.getBamidFromDf(subMatrixDf, [['condition', 'control'], ['library', 'ip']], ['replicate'], ascending=True)
    tinputBamidList = functools.getBamidFromDf(subMatrixDf, [['condition', 'treated'], ['library', 'input']], ['replicate'], ascending=True)
    tipBamidList = functools.getBamidFromDf(subMatrixDf, [['condition', 'treated'], ['library', 'ip']], ['replicate'], ascending=True)
    ## obtain read count in order:control input, contol ip, treated input, treated ip
    bamidList = cinputBamidList + cipBamidList + tinputBamidList + tipBamidList
    peakReadCountNorDf = peakReadCountNorDf.loc[:, bamidList]
    ''' to do the fisher exact test
        2x2 contingency table:
              input  ip
             +-----+-----+
    control  |  a  |  b  |
             +-----+-----+
    treated  |  c  |  d  |
             +-----+-----+
    '''
    testDf = peakReadCountNorDf.copy()
    testDf.columns = ['a', 'b', 'c', 'd']
    pvalArr = statstools.vectorize_fisher(testDf, alternative='two-sided')
    ## replace 0 with minumn pvalue
    pvalArr[pvalArr == 0] = pvalArr.min()
    ## transform to log10
    log10PvalArr = np.log(pvalArr) / np.log(10)
    ## perform fdr corrections
    alpha = 0.05
    ## transfer 'BH' to 'padjmethod'
    if options.padjmethod == 'BH':
        padjmethod = 'BH'
    else:
        padjmethod = 'BY'
    fdrArr = statstools.fdr_correction(mpmath.mpf(10) ** log10PvalArr, alpha=alpha, method=padjmethod)[1]
    log10FdrArr = np.array([mpmath.log10(fdr) for fdr in fdrArr])
    ## peakReadCountNorDf, peak read counts dataframe
    ## ipCol, inputCol, the index of ip and input column
    ## The probability mass function of the number of failures for nbinom is:
    ## f(k) = C(k+n-1, n-1) * p**n * (1-p)**k
    ## get the ratio of ratio
    cinputReads = peakReadCountNorDf.loc[:, cinputBamidList].replace(0, 1).squeeze()
    cipReads = peakReadCountNorDf.loc[:, cipBamidList].replace(0, 1).squeeze()
    tinputReads = peakReadCountNorDf.loc[:, tinputBamidList].replace(0, 1).squeeze()
    tipReads = peakReadCountNorDf.loc[:, tipBamidList].replace(0, 1).squeeze()
    cratioArr = cipReads.divide(cinputReads)
    tratioArr = tipReads.divide(tinputReads)
    log2FcArr = np.log2(tratioArr.divide(cratioArr)).to_numpy()
    ## example results
    dataArr = np.vstack((log2FcArr, log10PvalArr, log10FdrArr)).T
    fisherResDf =  pd.DataFrame(data = dataArr, columns = ['log2fc', 'log10pval', 'log10padj'], index =peakReadCountNorDf.index)
    ## add reads to dataframe
    fisherResDf['cipMean'] = peakReadCountNorDf[cipBamidList]
    fisherResDf['cinputMean'] = peakReadCountNorDf[cinputBamidList]
    fisherResDf['tipMean'] = peakReadCountNorDf[tipBamidList]
    fisherResDf['tinputMean'] = peakReadCountNorDf[tinputBamidList]
    ##filter out non-peak
    fisherResDf = fisherResDf.filter(regex=options.peakregex, axis=0)
    ## example results:
    '''the structure of fisherResDf
                                                        log2fc log10pval   log10fdr  cipMean   cinputMean   tipMean   tinputMean
    peakid
    ENSG00000279124.1:ENST00000625078.1|shNS:rep1|2|T     2        -3         -2        10         20         80          40
    ENSG00000279124.1:ENST00000625078.1|shNS:rep1|3|T     2        -3         -2        10         20         80          40
    ENSG00000279124.1:ENST00000625078.1|shNS:rep1|5|T     2        -3         -2        10         20         80          40
    ENSG00000279124.1:ENST00000625078.1|shNS:rep1|6|T     2        -3         -2        10         20         80          40
    ENSG00000279730.2:ENST00000623146.2|shNS:rep1|1|T     2        -3         -2        10         20         80          40
    ...                                                   2        -3         -2        10         20         80          40
    ENSG00000185220.12:ENST00000329291.6|shNS:rep1|6|T    2        -3         -2        10         20         80          40
    ENSG00000185220.12:ENST00000329291.6|shNS:rep1|7|T    2        -3         -2        10         20         80          40
    ENSG00000185220.12:ENST00000355360.8|shNS:rep1|1|T    2        -3         -2        10         20         80          40
    ENSG00000233084.2:ENST00000430973.1|shNS:rep1|2|T     2        -3         -2        10         20         80          40
    '''
    ## return fisher results and normalized counts
    return fisherResDf

def runGlmNbinomTest(options, peakReadCountDf, plot=True, skipSubplot=False):
    ## run generalized negative binomial regession model by DESeq2
    ## report error log or not
    ## check the input countDf, peak or gene
    indexNameList = list(map(lambda x:len(x.split(options.idsepdict['peakid'])), peakReadCountDf.index[0:100]))
    if np.mean(indexNameList) == 4:
        inputType = 'peak'
    else:
        inputType = 'gene'
    ## set verbose
    if options.verbose == 3:
        errorFlag = True
    else:
        errorFlag = False
    countMean = 0
    tempPrefixName = "_".join([options.tempre, options.prefix])
    tempPrefix = os.path.join(options.tempdir, tempPrefixName)
    ## construct the sample matrix requried by runGlmNbinomTest.R
    sampleMtx = tempPrefix + '.sample.matrix.tmp'
    bamidList = peakReadCountDf.columns
    functools.generateSampleMtxFile(options, bamidList, sampleMtx)
    ## construct the peak-counts matrix
    peakCountsMtx = tempPrefix + '.counts.matrix.tmp'
    peakReadCountDf.to_csv(peakCountsMtx, sep='\t', header=True, index=True)
    ## run runGlmNbinomTest.R, tempPrefix.glm.txt, tempPrefix.normalized.counts.txt
    outputPrefix = options.prefix
    if plot is True:
        plot = '--plot'
    else:
        plot = ''
    if skipSubplot is True:
        skipSubplot = '--skipsubplot'
    else:
        skipSubplot = ''
    if options.poolmode == 'pool':
        ## for identify significant peaks from replicates mode
        formula = "library"
        name = "library_ip_vs_input"
        relevel = "library:input"
        reduced = '1'
        if options.peaksizefactor == 'gene':
            skipsize = '--skipsize'
        else:
            skipsize = ''
    elif options.poolmode == 'diff':
        ## for differentially significant peaks from 2 conditions
        ##formula = "library + condition + library:condition"
        ##name = "libraryip.conditiontreat"
        ##relevel = "condition:control,library:input"
        ##reduced = "library + condition"
        formula = "condition"
        name = "condition_treated_vs_control"
        relevel = "condition:control"
        reduced = '1'
        skipsize = '--skipsize'
    if options.formula is not None:
        formula = options.formula
    if inputType == 'gene':
        skipsize = ''
        if options.shrink == 'none':
            shrink = 'apeglm'
        else:
            shrink = options.shrink
    else:
        shrink = options.shrink
    sep = options.idsepdict['peakid']
    ## generate commands of runGlmNbinomTest.R
    script = os.path.realpath(__file__)
    runGlmNbinomTestR = os.path.join(os.path.dirname(script), 'runGlmNbinomTest.R')
    command = 'Rscript {runGlmNbinomTestR} \
        --sample "{sampleMtx}" \
        --counts "{peakCountsMtx}" \
        --mean {countMean} \
        --formula "{formula}" \
        --relevel "{relevel}" \
        --name "{name}" \
        --shrink "{shrink}" \
        --sep "{sep}" \
        --prefix "{outputPrefix}" \
        --reduce "{reduced}" \
        --padjust "{padjmethod}" \
        --test "{testmethod}" \
        --fittype "{fittype}" \
        --temp "{temp}" \
        --output "{outputdir}" \
        {plot} {skipsize} {skipsubplot}'
    ## construct args dict
    runGlmNbinomTestArgsDict = {
        'runGlmNbinomTestR': runGlmNbinomTestR,
        'thread': options.thread,
        'sampleMtx': sampleMtx,
        'peakCountsMtx': peakCountsMtx,
        'countMean': countMean,
        'formula': formula,
        'relevel': relevel,
        'name': name,
        'shrink': shrink,
        'sep': sep,
        'outputPrefix': outputPrefix,
        'reduced': reduced,
        'padjmethod': options.padjmethod,
        'testmethod': options.test,
        'fittype': options.fittype,
        "temp": tempPrefix,
        'outputdir': options.outputdir,
        'plot': plot,
        'skipsize': skipsize,
        'skipsubplot': skipSubplot,
    }
    command = command.format(**runGlmNbinomTestArgsDict)
    ## running DESeq2
    ## print running command if neccessary
    options.debug(command)
    __ = functools.subprocessToList(command, errorFlag)
    ## print the information of size factors
    if options.peaksizefactor != 'gene' and options.poolmode == 'pool':
        sizefactorFile = tempPrefix + '.sizefactor.txt'
        sizeFactorDf = pd.read_csv(sizefactorFile, header=0, sep="\t", index_col=0)
        sizeFactorDf.index.name = 'id'
        sizeFactorDf.columns = ['size_factor']
        ## info
        options.info( "The reads count of peak candidates have been normalized by estimated size factors:\n" + sizeFactorDf.to_markdown() )
    ## result file used for downstream analysis
    glmNbinomResFile = tempPrefix + '.glm.txt'
    normalizeCountsFile = tempPrefix + '.normalized.counts.txt'
    ## read file to pandas dataframe
    glmNbinomResDf = pd.read_csv(glmNbinomResFile, header=0, sep="\t", index_col=0)
    ## avoid 0 in 'pvalue' and 'padj' column
    floatPoinInR = 2.225074e-308
    glmNbinomResDf['pvalue'].replace(0, floatPoinInR, inplace=True)
    glmNbinomResDf['padj'].replace(0, floatPoinInR, inplace=True)
    ## covert p-value and padj to log10
    glmNbinomResDf['log10pval'] = np.log10(glmNbinomResDf['pvalue'])
    glmNbinomResDf['log10padj'] = np.log10(glmNbinomResDf['padj'])
    ## drop column baseMean and lfcSE
    glmNbinomResDf = glmNbinomResDf.drop(['baseMean', 'lfcSE', 'pvalue', 'padj'], axis=1)
    ## rename column name
    glmNbinomResDf = glmNbinomResDf.rename(columns={"log2FoldChange": "log2fc"})
    '''
    structure of glmNbinomResDf
                                                  log2FoldChange          pvalue          padj
    peakid
    ENSG00000227232.5:ENST00000488147.1|shNS|1|T        2.410481    2.035719e-16  3.804146e-15
    ENSG00000227232.5:ENST00000488147.1|shNS|2|F       -0.034800    9.341240e-01  9.650615e-01
    '''
    ## column is bamid, row is peakid
    normalizeCountsDf = pd.read_csv(normalizeCountsFile, header=0, sep="\t", index_col=0)
    ## calculate average counts of each condiction, like control:ip
    ## add reads to glmNbinomResDf
    subMatrixDf = options.matrixdf.loc[bamidList, ]
    if options.poolmode == 'pool':
        ipBamidList = subMatrixDf[ subMatrixDf['library'] == 'ip' ].index.to_list()
        inputBamidList = subMatrixDf[ subMatrixDf['library'] == 'input' ].index.to_list()
        glmNbinomResDf['ipMean'] = normalizeCountsDf[ipBamidList].mean(axis=1)
        glmNbinomResDf['inputMean'] = normalizeCountsDf[inputBamidList].mean(axis=1)
    elif options.poolmode == 'diff':
        cipBamidList = subMatrixDf[ subMatrixDf['condition'] == 'control' ].index.to_list()
        tipBamidList = subMatrixDf[ subMatrixDf['condition'] == 'treated' ].index.to_list()
        glmNbinomResDf['cipMean'] = normalizeCountsDf[cipBamidList].mean(axis=1)
        glmNbinomResDf['tipMean'] = normalizeCountsDf[tipBamidList].mean(axis=1)
    ##filter out non-peak
    if inputType == 'peak':
        glmNbinomResDf = glmNbinomResDf.filter(regex=options.peakregex, axis=0)
    ## return glmNbinom results and normalized counts
    return glmNbinomResDf
