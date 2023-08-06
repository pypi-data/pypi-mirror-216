# -*- coding: utf-8 -*-
##########################################
#           utility                      #
#          2023.3.24                     #
##########################################
__author__ = "Keren Zhou"
__version__ = "v1.2"

import os
import errno
import sys
import subprocess
import statistics
import networkx as nx
import itertools
import operator
import pathlib
import pandas as pd
import tempfile
import numpy as np
import math
from copy import copy
import bottleneck as bn
from csaps import csaps
from sklearn import preprocessing
from collections import defaultdict
import rpy2.robjects.packages as rpackages
from shutil import which

from PEALS.collection import bamtool
from PEALS.io import streamtools

def deleteFile(*files):
    for file in files:
        try:
            os.remove(file)
        except:
            pass

def checkSoftware(software, env):
    lang, version = env
    if lang == 'bash':
        install = which(software) is not None
    elif lang == 'R':
        install = rpackages.isinstalled(software)
    return install

def delTempFile(options):
    tempFileList = list(pathlib.Path(options.tempdir).glob(options.tempre + "*"))
    tempFileList = list(map(str, tempFileList))
    deleteFile(*tempFileList)

def checkBgFiles(options):
    bgFileList = list(pathlib.Path(options.tempdir).glob("*.bedGraph"))
    if len(bgFileList) >= 1:
        return True
    else:
        return False

class options(object):
    pass

# map list to dict structure
def list2Dict(listA, step=2):
    return dict(zip(listA[::step], listA[step - 1::step]))

# map list to str list
def list2Str(listA):
    return list(map(str, listA))

def compareNum(number, relate, cutoff):
    opsDict = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '==': operator.eq}
    return opsDict[relate](number, cutoff)

def getSortPeak(peakRowList):
    peakIndexDict = {}
    for i in range(len(peakRowList)):
        peakRowList[i][3] = '=='.join([peakRowList[i][3], str(i)])
        peakIndexDict[peakRowList[i][3]] = i
    sortedPeakRowList = sorted(peakRowList, key=lambda x:(x[0], int(x[1]), int(x[2])))
    ## get sorted index map to original index
    indexMapDict = {}
    for i in range(len(sortedPeakRowList)):
        originalIndex = peakIndexDict[sortedPeakRowList[i][3]]
        indexMapDict[i] = originalIndex
        sortedPeakRowList[i][3] = sortedPeakRowList[i][3].split('==')[0]
    return [sortedPeakRowList, indexMapDict]

def subprocessRun(command):
    run = subprocess.check_output(command, shell=True, stderr=subprocess.PIPE)
    return True

def subprocessToList(command, errorFlag=False):
    if errorFlag is True:
        runResList = bytes.decode(subprocess.check_output(command, shell=True, stderr=None)).split('\n')
    else:
        runResList = bytes.decode(subprocess.check_output(command, shell=True, stderr=subprocess.PIPE)).split('\n')
    runResRowList = list(map(lambda x:x.split('\t'), list(filter(lambda x: bool(x), runResList))))
    return runResRowList

def decodeSample(options):
    ##column_name:value or column_name:control=value1,treated=value2
    inforDict = {}
    ## must have keys, ['column', 'control'] or ['column', 'control', 'treated']
    column, infor = options.sample.split(':')
    ## record column name
    inforDict['column'] = column
    ## record value
    inforList = infor.split(',')
    if options.subprogram == 'callpeak':
        inforDict['value'] = inforList
    elif options.subprogram == 'diffpeak':
        valueList = []
        ## decode value for each condition
        for eachInfo in inforList:
            condition, value = eachInfo.split('=')
            inforDict[condition] = value
            valueList.append(value)
        valueList = list(set(valueList))
        ## record all values
        inforDict['value'] = valueList
    return inforDict

def getReadLength(bamFile):
    command = 'samtools view {} | head -n 100 | awk \'{{print $10}}\''.format(bamFile)
    readRowList = subprocessToList(command)
    readLenList = []
    for readRow in readRowList:
        read = readRow[0]
        readLenList.append(len(read))
    readLength = int(statistics.mean(readLenList))
    return readLength

def findNetworkEdgeGroup(pairedEdgeList):
    ## eg. pairedEdgeList = [("A","B"), ("B","C"), ("C","D"), ("E","F"), ("G","H"), ("H","I"), ("G","I"), ("G","J")]
    ## return: [ [('A', 'B'), ('B', 'C'), ('C', 'D')], [('E', 'F')], [('G', 'H'), ('H', 'I'), ('G', 'I'), ('G', 'J')] ]
    ## cunstruct a networkx object with edges and get the connected edges
    ## connEdgeList : [{'D', 'C', 'A', 'B'}, {'E', 'F'}, {'H', 'J', 'G', 'I'}]
    G = nx.Graph(pairedEdgeList)
    connEdgeList = list(nx.connected_components(G))
    ## create the map dict , for get the unique edge id for each nodes
    ## mapdict: {'D': 0, 'C': 0, 'A': 0, 'B': 0, 'E': 1, 'F': 1, 'H': 2, 'J': 2, 'G': 2, 'I': 2}
    mapdict = {z:x for x, y in enumerate(connEdgeList) for z in y }
    ## then append the id back to original data for groupby
    ## newList: [('A', 'B', 0), ('B', 'C', 0), ('C', 'D', 0), ('E', 'F', 1), ('G', 'H', 2), ('H', 'I', 2), ('G', 'I', 2), ('G', 'J', 2)]
    newList = [ x + (mapdict[x[0]],) for  x in pairedEdgeList]
    ## using groupby make the same edge id into one sublist
    ## [[('A', 'B'), ('B', 'C'), ('C', 'D')], [('E', 'F')], [('G', 'H'), ('H', 'I'), ('G', 'I'), ('G', 'J')]]
    newList = sorted(newList, key=lambda x: x[2])
    groupEdgeList = [list(group) for key , group in itertools.groupby(newList, key=lambda x : x[2])]
    groupEdgeList = list(map(lambda x:list(map(lambda y:y[0:2], x)), groupEdgeList))
    ## return the final group list
    return groupEdgeList

def runBedtools(options, command, peakRowListA, peakRowListB):
    peakRowListA = sorted(peakRowListA, key=lambda x:(x[0], x[1]))
    peakRowListB = sorted(peakRowListB, key=lambda x:(x[0], x[1]))
    ## get sorted chromosome
    sortedChromList = sorted(set(map(lambda x:x[0], peakRowListA + peakRowListB)))
    ## write sorted chromosome to temp file, will speed up bedtools
    gsizeTemp = tempfile.NamedTemporaryFile(suffix='.gsize.tmp', prefix=options.tempre, dir=options.tempdir, delete=True)
    with open(gsizeTemp.name, 'w', buffering=options.buffer) as out:
        for chrom in sortedChromList:
            row = '\t'.join([chrom, '1\n'])
            out.write(row)
    ## write peakRowList to temp bed file
    peakBedTempA = tempfile.NamedTemporaryFile(suffix='.bed.tmp', prefix=options.tempre, dir=options.tempdir, delete=True)
    streamtools.peakToFile(peakRowListA, peakBedTempA.name, bed12=True, folder=None)
    peakBedTempB = tempfile.NamedTemporaryFile(suffix='.bed.tmp', prefix=options.tempre, dir=options.tempdir, delete=True)
    streamtools.peakToFile(peakRowListB, peakBedTempB.name, bed12=True, folder=None)
    ## intersect peaks with bedtools -sorted -g
    command = 'bedtools intersect -a {} -b {} -g {} -sorted' + command
    command = command.format(peakBedTempA.name, peakBedTempB.name, gsizeTemp.name)
    ## run the command
    runResRowList = subprocessToList(command)
    ## delete temp file
    gsizeTemp.close()
    peakBedTempA.close()
    peakBedTempB.close()
    ## return final result
    return runResRowList

def buildBamLinkDict(options):
    ## get all input bams from matrix
    matrixDf = pd.read_csv(options.matrix, header=0, sep="\t", index_col=0, skiprows=0)
    allBamFileList = matrixDf['bam'].to_list()
    bamDict = {}
    for bam in allBamFileList:
        baseName = os.path.basename(bam)
        bamDict[baseName] = 1
    ## find bam  in specified directory
    if options.recursive is True:
        bamFileList = list(pathlib.Path(options.inputdir).glob("**/*.bam"))
        baiFileList = list(pathlib.Path(options.inputdir).glob("**/*.bai"))
    else:
        bamFileList = list(pathlib.Path(options.inputdir).glob("*.bam"))
        baiFileList = list(pathlib.Path(options.inputdir).glob("*.bai"))
    baiFileDict = {}
    for baiFile in baiFileList:
        fileFullPath = baiFile.absolute()
        ## skip the symbol link
        if os.path.islink(fileFullPath) is True:
            continue
        ## test.bam.bai
        bamFileName = os.path.splitext(fileFullPath.name)[0]
        if bamFileName not in bamDict:
            continue
        baiFileDict[bamFileName] = fileFullPath
    bamLinkDict = defaultdict(dict)
    for bamFile in bamFileList:
        fileFullPath = bamFile.absolute()
        ## skip the symbol link
        if os.path.islink(fileFullPath) is True:
            continue
        bamFileName = bamFile.name
        if bamFileName not in bamDict:
            continue
        ## check whehter bai exists
        try:
            baiFile = baiFileDict[bamFileName]
        except KeyError as e:
            options.error('The bai file of bam ({}) is not found!'.format(bamFileName))
            sys.exit(1)
        bamLinkDict[bamFileName]['bam'] = fileFullPath
        bamLinkDict[bamFileName]['bai'] = baiFile
    return bamLinkDict

def buildBinaryLinkDict(options):
    if options.recursive is True:
        binaryFileList = list(pathlib.Path(options.binarydir).glob("**/*" + options.binaryapp))
    else:
        binaryFileList = list(pathlib.Path(options.binarydir).glob("*" + options.binaryapp))
    binaryFileDict = {}
    for binaryFile in binaryFileList:
        fileFullPath = binaryFile.absolute()
        ## skip the symbol link
        if os.path.islink(fileFullPath) is True:
            continue
        ## test.bam.bai
        baseName = fileFullPath.name
        binaryFileDict[baseName] = fileFullPath
    return binaryFileDict

def subsetMatrix(options, matrixDf):
    if options.sample is not None:
        inforDict = decodeSample(options)
        subsetCol = inforDict['column']
        subsetValList = inforDict['value']
        ## subset the matrix
        matrixDf = matrixDf.loc[matrixDf[subsetCol].isin(subsetValList)]
        ## check and change the condition for diffpeak
        if options.subprogram == 'callpeak':
            value = subsetValList[0]
            matrixDf.loc[matrixDf[subsetCol] == value, 'condition'] = 'control'
        elif options.subprogram == 'diffpeak':
            ##rename the condition in sample matrix
            conditionList = ['control', 'treated']
            for condition in conditionList:
                value = inforDict[condition]
                matrixDf.loc[matrixDf[subsetCol] == value, 'condition'] = condition
    return matrixDf

def decodeMatrix(options):
    ## get sample matrix
    bamLinkDict = buildBamLinkDict(options)
    matrixDf = pd.read_csv(options.matrix, header=0, sep="\t", index_col=0, skiprows=0)
    ## subset matrix if neeeded
    matrixDf = subsetMatrix(options, matrixDf)
    ## load with binary files if necessary
    if options.binary is True:
        binaryFileDict = buildBinaryLinkDict(options)
        try:
            matrixDf['binary'] = list(map(lambda x: binaryFileDict[x], matrixDf['binary'].to_list()))
        except KeyError as e:
            options.error('No matched binary file found in --binary-dir!')
            sys.exit(1)
    ## get bam information
    bamFullPathList = []
    baiFullPathList = []
    bamLibSizeList = []
    bamSymlinkList = []
    baiSymlinkList = []
    bamUniqueList = []
    ## record the unique property of input bam
    bamUniqueDict = {}
    for index, row in matrixDf.iterrows():
        ## get corresponding bam and bai
        bamFileName =  row['bam']
        ## check whether bam is existed
        try:
            bamFullPath = str(bamLinkDict[bamFileName]['bam'])
            baiFullPath = str(bamLinkDict[bamFileName]['bai'])
        except KeyError as e:
            options.error('bam ({}) is not found in --input!'.format(bamFileName))
            sys.exit(1)
        bamFullPathList.append(bamFullPath)
        baiFullPathList.append(baiFullPath)
        ## get corresponding symbol link of bam and bai (under tempdir)
        bamSymlink = os.path.join(options.tempdir, index + '.bam')
        baiSymlink = os.path.join(options.tempdir, index + '.bam.bai')
        bamSymlinkList.append(bamSymlink)
        baiSymlinkList.append(baiSymlink)
        if bamFileName not in bamUniqueDict:
            bamUniqueDict[bamFileName] = 1
            bamUniqueList.append(1)
        else:
            bamUniqueList.append(0)
    matrixDf['bam'] = bamFullPathList
    matrixDf['bai'] = baiFullPathList
    matrixDf['lib_size'] = bamtool.getLibSizeParallel(options, bamFullPathList)
    matrixDf['symlink_bam'] = bamSymlinkList
    matrixDf['symlink_bai'] = baiSymlinkList
    matrixDf['bam_unique'] = bamUniqueList
    ## calculate lib scale
    if options.scalesample == 'to_small':
        ref = matrixDf['lib_size'].min()
        matrixDf['whole_lib_scale'] = matrixDf['lib_size'].div(ref)
    elif options.scalesample == 'to_large':
        matrixDf['whole_lib_scale'] = matrixDf['lib_size'].div(ref)
    elif options.scalesample == 'raw':
        matrixDf['whole_lib_scale'] = 1
    ## the libsize between correpsonding ip and input
    matrixDf['paired_lib_scale'] = 1
    return matrixDf

def buildFullMatrix(options):
    ## get sample matrix
    options.matrixdf = decodeMatrix(options)
    ## check any duplicate bam
    dupMatrixDf = options.matrixdf[ options.matrixdf['bam_unique'] == 0 ]
    if dupMatrixDf.empty is False:
        options.warn("Duplicated input bam files are detected!")
    ## build bamdict information
    ipTypeList  = ['ip', 'input', 'ip', 'input']
    conditionList = ['control', 'control', 'treated', 'treated']
    ##bamList = [cipBamList, cinputBamList, tipBamList, tinputBamList]
    bamList = [[], [], [], []]
    ## bamDict to record bam->bamid
    bamDict = {}
    for i in range(4):
        ipType = ipTypeList[i]
        condition = conditionList[i]
        query = 'library == "{}" & condition == "{}"'.format(ipType, condition)
        ## select dataframe by library and condition, then sort by replicate, finally convert to a list
        idList = options.matrixdf.query(query).sort_values(by=['replicate'], ascending=True).index.to_list()
        if len(idList) == 0:
            continue
        bamList[i] = options.matrixdf.loc[idList]['symlink_bam'].to_list()
        for j in range(len(bamList[i])):
            bam = bamList[i][j]
            bamid = idList[j]
            bamDict[bam] = bamid
    ## add bamdict to options
    options.bamdict = bamDict
    ## add bam and label to options
    matrixConditionList = sorted(options.matrixdf['condition'].unique())
    if len(matrixConditionList) == 1:
        ## add bam
        if matrixConditionList[0] == 'control':
            options.ip, options.input, __, __ = copy(bamList)
        else:
            __, __, options.ip, options.input = copy(bamList)
        ipBamList = options.ip
        inputBamList = options.input
        ## add label
        bamidList = list(map(lambda x:options.bamdict[x], options.ip))
        options.label = options.matrixdf.loc[bamidList]['label'].to_list()
    else:
        ## add bam
        options.ipcontrol, options.inputcontrol, options.iptreat, options.inputtreat = copy(bamList)
        ipBamList = options.ipcontrol + options.iptreat
        inputBamList = options.inputcontrol + options.inputtreat
        ## add label
        contolBamidList = list(map(lambda x:options.bamdict[x], options.ipcontrol))
        options.labelcontrol = options.matrixdf.loc[contolBamidList]['label'].to_list()
        treatBamidList = list(map(lambda x:options.bamdict[x], options.iptreat))
        options.labeltreat = options.matrixdf.loc[treatBamidList]['label'].to_list()
    ## calculate the libsize between correpsonding ip and input
    pairLibScaleDict = {}
    for i in range(len(ipBamList)):
        bamList = [ipBamList[i], inputBamList[i]]
        labelList = list(map(lambda x: options.bamdict[x], bamList))
        ## calculate lib scale
        if options.scalesample == 'to_small':
            ref = options.matrixdf.loc[labelList]['lib_size'].min()
            libScaleList = options.matrixdf.loc[labelList]['lib_size'].div(ref).to_list()
        elif options.scalesample == 'to_large':
            ref = options.matrixdf.loc[labelList]['lib_size'].max()
            libScaleList = options.matrixdf.loc[labelList]['lib_size'].div(ref).to_list()
        elif options.scalesample == 'raw':
            libScaleList = [1.0, 1.0]
        ## matrixdf header: id,library,condition,label,replicate,bam,bai,lib_size,symlink_bam,symlink_bai,lib_scale,paired_lib_scale
        options.matrixdf.loc[labelList, 'paired_lib_scale'] = libScaleList
    return options

def creatSymlink(targetFile, symlinkFile):
    try:
        os.symlink(targetFile, symlinkFile)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(symlinkFile)
            os.symlink(targetFile, symlinkFile)
        else:
            raise e

def bamToSymlink(options):
    for label in options.matrixdf.index:
        bam = options.matrixdf.at[label, 'bam']
        bai = options.matrixdf.at[label, 'bai']
        sbam = options.matrixdf.at[label, 'symlink_bam']
        sbai = options.matrixdf.at[label, 'symlink_bai']
        creatSymlink(bam, sbam)
        creatSymlink(bai, sbai)

def getCellByBam(options, bam, column):
    ## bam is the soft symbolic bam
    bamid = options.bamdict[bam]
    cell = options.matrixdf.at[bamid, column]
    return cell

def getBamidList(options, bamList):
    bamidList = list(map(lambda x: options.bamdict[x], bamList))
    return bamidList

def getBamidFromDf(df, filterList2d, sortList, ascending=True):
    ##filterList2d = [['library', 'input'], ['condition', 'control']]
    ##sortList = ['condition', 'replicate']
    ## start to filter
    subDf = df.copy()
    for filterList in filterList2d:
        condition, value = filterList
        subDf = subDf[subDf[condition] == value]
    ##sort and convert to list
    bamidList = subDf.sort_values(by=sortList, ascending=ascending).index.to_list()
    return bamidList

def removeDupBam(options, bamList):
    ## bamList is the soft symbolic bam
    bamidList = getBamidList(options, bamList)
    subMatrixDf = options.matrixdf.loc[bamidList, ]
    subMatrixDf = subMatrixDf[subMatrixDf['bam_unique'] == 1]
    uniqueBamList = subMatrixDf['symlink_bam'].to_list()
    return uniqueBamList

def generateSampleMtxFile(options, bamidList, sampleMtxFile):
    matrixDf = options.matrixdf.loc[bamidList, ]
    ## exclude unwanted columns
    excludeColNameList = ['bam', 'binary', 'bai', 'lib_size', 'label']
    excludeColNameList += ['symlink_bam', 'symlink_bai', 'bam_unique', 'whole_lib_scale', 'paired_lib_scale']
    remainMatrixDf = matrixDf.loc[:, ~matrixDf.columns.isin(excludeColNameList)]
    ## output to sampleMtxFile
    remainMatrixDf.to_csv(sampleMtxFile, sep='\t', header=True, index=True)

def computeChunksize(options, count, sliceNum=4):
    chunksize = max(1, int(count / (options.thread * sliceNum)))
    return chunksize

def getLoopByChrom(options, chromTxDict, chromSet, maxLoop=5):
    ## split 
    chromTxCountDict = {}
    totalTxCount = 0
    for chrom in sorted(chromTxDict.keys()):
        chromSize = options.chrsizedict[chrom]
        if chrom not in chromSet:
            continue
        txCount = len(sorted(chromTxDict[chrom]))
        if txCount > 0:
            chromTxCountDict[chrom] = txCount
            totalTxCount += txCount
    expectLoopTxCount = int(totalTxCount / maxLoop)
    loopDict = defaultdict(dict)
    loop = 0
    for chrom in sorted(chromTxCountDict.keys()):
        txCount = chromTxCountDict[chrom]
        if txCount > expectLoopTxCount:
            loop += 1
            loopDict[loop]['chrom'] = [chrom]
            loopDict[loop]['count'] = txCount
            loop += 1
        else:
            if loop not in loopDict:
                loopDict[loop]['chrom'] = list()
                loopDict[loop]['count'] = 0
            if (loopDict[loop]['count'] + txCount) < expectLoopTxCount:
                loopDict[loop]['chrom'].append(chrom)
                loopDict[loop]['count'] += txCount
            else:
                loop += 1
                loopDict[loop]['chrom'] = [chrom]
                loopDict[loop]['count'] = txCount
    loopChromList = [ loopDict[i]['chrom'] for i in sorted(loopDict.keys()) ]
    loopChunksizeList = [ computeChunksize(options, loopDict[i]['count'], sliceNum=2) for i in sorted(loopDict.keys()) ]
    return [loopChromList, loopChunksizeList]

## split large intervals
def splitCovArrayCount(txBed, maxSize, optSize):
    size = txBed.exonlength
    if size > maxSize:
        ## how many sub-arrays should be splitted
        count = int(size // maxSize)
        if (size % maxSize) >= optSize:
            count += 1
    else:
        count  = 1
    return count

def splitCovArray(ipCovArr, inputCovArr, ipMeanCov, maxSize, optSize):
    size = ipCovArr.size
    if size > maxSize:
        ## how many sub-arrays should be splitted
        count = int(size // maxSize)
        if (size % maxSize) >= optSize:
            count += 1
        if count > 1:
            ##np.where():(array([ 2,  3,  4,  5,  9, 12, 14, 15, 16, 18, 19]),)
            belowMeanIndexArr = np.where(ipCovArr <= ipMeanCov)[0]
            ## filter out empty and single-element sub-array
            indexSplitArrayList = list(filter(lambda x:x.size > 1, np.array_split(belowMeanIndexArr, count)))
            splitCount = len(indexSplitArrayList)
            if splitCount <= 1 :
                ipCovArrayList = [ipCovArr]
                inputCovArrayList = [inputCovArr]
                indexList = [[0, size]]
            else:
                ## determin start and end index for each sub-arrays
                indexList = []
                for i in range(splitCount):
                    if i == 0:
                        start = 0
                        end = indexSplitArrayList[i][-1]
                    else:
                        start = indexList[i-1][1]
                        if i == splitCount - 1:
                            end = size
                        else:
                            end = indexSplitArrayList[i][-1]
                    indexList.append([start, end])
                ## split IP and input array into N sections
                ipCovArrayList = []
                inputCovArrayList = []
                for x in indexList:
                    ipCovArrayList.append(ipCovArr[x[0]:x[1]])
                    inputCovArrayList.append(inputCovArr[x[0]:x[1]])
        else:
            ipCovArrayList = [ipCovArr]
            inputCovArrayList = [inputCovArr]
            indexList = [[0, size]]
    else:
        ipCovArrayList = [ipCovArr]
        inputCovArrayList = [inputCovArr]
        indexList = [[0, size]]
    return [ipCovArrayList, inputCovArrayList, indexList]

## smooth
def smoothMove(valueList, method, span=10, loop=1, backward=False):
    if method == 'none':
        smoothValList = valueList
    elif method == 'move':
        smoothValList = valueList
        for i in range(loop):
            if backward is True:
                ## get forward moving average
                smoothForw = bn.move_mean(smoothValList, window=span, min_count = 1)
                ## get backward moving average
                smoothBackw = bn.move_mean(smoothValList[::-1], window=span, min_count = 1)[::-1]
                ## take average
                smoothValList = np.add(smoothForw, smoothBackw) / 2
            else:
                smoothValList = bn.move_mean(smoothValList, window=span, min_count = 1)
    return smoothValList

def smoothCsaps(options, npArr):
    spanmethod = options.spanmethod
    spanloop = options.spanloop
    csapsp = options.csapsp
    maxSpan = options.spandict['max']
    minSpan = options.spandict['min']
    spanStep = options.spandict['step']
    ## make span not exceed array length
    optSpan = min(maxSpan, max(minSpan, int(npArr.size / spanStep)))
    indexArr = np.arange(npArr.size)
    ## estimate weights for each point
    weights = preprocessing.normalize([npArr], norm="l2")[0]
    weights[weights < csapsp] = weights[weights < csapsp] + csapsp
    weights[weights > 1] = 1
    smooth = 1 / math.log(indexArr.size) * csapsp
    try:
        csapsSmoothArr = csaps(indexArr, npArr, indexArr, weights=weights, smooth=smooth)
        ## smooth again with move average
        npSmoothArr = smoothMove(csapsSmoothArr, 'move', span=optSpan, loop=spanloop, backward=True)
    except RuntimeError as e:
        npSmoothArr = smoothMove(npArr, 'move', span=optSpan, loop=3, backward=True)
    return npSmoothArr

def findConGroup(npArr, stepSize=1):
    ##a = np.array([0, 47, 48, 49, 50, 97, 98, 99])
    ## return [array([0]), array([47, 48, 49, 50]), array([97, 98, 99])]
    return np.split(npArr, np.where(np.diff(npArr) != stepSize)[0] + 1)

def findLagestGapInArr(npArr):
    diffArr = np.diff(npArr)
    diffMax = diffArr.max()
    sindex = np.where(diffArr == diffMax)[0][0]
    eindex = sindex + 1
    return [sindex, eindex]

def findOverIndex(npArr, cutoff):
    overIndexArr =  np.where(npArr >= cutoff)[0]
    if overIndexArr.size > 0:
        ## find continuous group
        sindex = overIndexArr.min()
        eindex = overIndexArr.max()
    else:
        sindex = 0
        eindex = npArr.size - 1
    indexLen = eindex - sindex
    return [sindex, eindex, indexLen]

def estimateRegionCompexity(npArr):
    #unique, counts = np.unique(npArr, return_counts=True)
    uniqueArr = np.unique(npArr)
    complexityRate = uniqueArr.size / npArr.size
    return complexityRate
