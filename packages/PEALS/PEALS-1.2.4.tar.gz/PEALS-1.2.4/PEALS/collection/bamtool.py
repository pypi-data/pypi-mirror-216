# -*- coding: utf-8 -*-
##########################################
#           peakutils                    #
#          2023.02.23                    #
##########################################
__author__ = "Keren Zhou"
__version__ = "v1.1"

import os
import sys
import shutil
import re
import numpy as np
import pandas as pd
from collections import defaultdict
import tempfile
import pysam
from multiprocessing import get_context
from contextlib import closing

# own module
from PEALS.collection import functools

def fileFromBam(options, bam, ftype):
    ## bamList is the soft symbolic bam
    bamBaseName = os.path.splitext(os.path.basename(bam))[0]
    ## remove "tmp_"
    bamBaseName = bamBaseName.replace('tmp_', '')
    if ftype == 'bw':
        if options.library == 0:
            forward = '_'.join([bamBaseName + '.bw'])
            reverse = '_'.join([bamBaseName + '.bw'])
        else:
            forward = '_'.join([bamBaseName + '.forward.bw'])
            reverse = '_'.join([bamBaseName + '.reverse.bw'])
        value = list(map(lambda x: os.path.join(options.outputdir, x), [forward, reverse]))
    return value

def tempfileFromBam(options, bam, ftype):
    ## bamList is the soft symbolic bam
    bamBaseName = os.path.splitext(os.path.basename(bam))[0]
    if ftype == 'bg':
        if options.library == 0:
            forward = '_'.join([options.tempre, bamBaseName + '.bedGraph'])
            reverse = '_'.join([options.tempre, bamBaseName + '.bedGraph'])
        else:
            forward = '_'.join([options.tempre, bamBaseName + '.forward.bedGraph'])
            reverse = '_'.join([options.tempre, bamBaseName + '.reverse.bedGraph'])
        value = list(map(lambda x: os.path.join(options.tempdir, x), [forward, reverse]))
    elif ftype == 'subam':
        name = '_'.join(['tmp', bamBaseName + '.sub.bam'])
        value = os.path.join(options.tempdir, name)
    return value

def convertBamToBg(bulkArgs):
    ## bamList is the soft symbolic bam
    options, bam, strand = bulkArgs
    tempdir = options.tempdir
    pairendFlag = options.pairend
    extsize = options.extsize
    library = options.library
    forwardBgFile, reverseBgFile = tempfileFromBam(options, bam, 'bg')
    bamName = os.path.basename(bam)
    ## only used for bedtools
    if options.ignoredup is True:
        command = 'samtools view -bh -F 1024 {} | '.format(bam)
        bam = 'stdin'
    else:
        command = ''
    if options.extsize == 0:
        fsArgs = ""
    else:
        fsArgs = "-fs {}".format(options.extsize)
    if pairendFlag is False:
        command += 'bedtools genomecov -ibam {} {} -split {} -bg > {}'
    else:
        command += 'bedtools genomecov -ibam {} {} -split {} -du -bg > {}'
    if library == 0:
        command = command.format(bam, fsArgs, '', forwardBgFile)
    else:
        if library == 1:
            forwardStrand = "-strand +"
            reverseStrand ="-strand -"
        else:
            forwardStrand = "-strand -"
            reverseStrand ="-strand +"
        if strand == '+':
            command = command.format(bam, fsArgs, forwardStrand, forwardBgFile)
        else:
            command = command.format(bam, fsArgs, reverseStrand, reverseBgFile)
    ## debug
    options.debug('Generating genome-wide coverage for bam ({}) with command: {}'.format(bamName, command))
    ## running
    __ = functools.subprocessToList(command, False)
    ## degug
    if options.library == 0:
        options.debug('Generating genome-wide coverage for bam ({}) done.'.format(bamName))
    else:
        options.debug('Generating genome-wide coverage for bam ("{}" strand, {}) done.'.format(strand, bamName))
    return True

def runConvertBamToBgParallel(options, bamList):
    ## convert bam to bedgraph by using bedtools
    ## bamList is the soft symbolic bam
    if options.library == 0:
        loopCount = len(bamList)
    else:
        loopCount = len(bamList) * 2
    if loopCount > options.thread:
        thread = options.thread
    else:
        thread = loopCount
    ## prepare arguments for parallel
    bulkArgsList = []
    for bam in bamList:
        if options.library == 0:
            bulkArgsList.append([options, bam, '+'])
        else:
            bulkArgsList.append([options, bam, '+'])
            bulkArgsList.append([options, bam, '-'])
    ## run in paralell
    resultList = []
    with closing(get_context(options.threadstart).Pool(thread)) as pool:
        imap = pool.imap_unordered(convertBamToBg, bulkArgsList)
        for result in imap:
            resultList.append(result)

def doMergeBam(bulkArgs):
    options, bamList, mergeBam, thread = bulkArgs
    inputBams = ' '.join(bamList)
    command = "samtools merge -o {} -f --threads {} {}".format(mergeBam, thread, inputBams)
    options.debug("Merging bams from inputs with command: {}".format(command))
    __ = functools.subprocessToList(command, False)
    ## sort output bam
    command = "samtools index {}".format(mergeBam)
    __ = functools.subprocessToList(command, False)
    return True

def runMergeBamParallel(options, bamGroupList, mergeBamList):
    ## merge input bamgroup
    ## bamGroupList = [[bam1, bam2], [bam3, bam4]]
    ## mergeBamList = [mergeBam1, mergeBam2]
    groupNum = len(bamGroupList)
    ## except the bam with fraction 1
    threadEach = int(max(options.thread / groupNum, 1))
    if threadEach == 1:
        thread = options.thread
    else:
        thread = groupNum
    bulkArgsList = []
    for i in range(groupNum):
        bamList = bamGroupList[i]
        mergeBam = mergeBamList[i]
        bulkArgsList.append([options, bamList, mergeBam, threadEach])
    ## run in paralell
    resultList = []
    with closing(Pool(thread)) as pool:
        imap = pool.imap_unordered(doMergeBam, bulkArgsList)
        for result in imap:
            if bool(result):
                resultList.append(result)

def getLibSize(bulkArgs):
    options, bam, runThread = bulkArgs
    ## get the total mapped reads from an indexed bam file
    ## by using flagstat instead of idxstats to avoid repeatedly counting of multiple mapping reads
    regex = re.compile(r'\s?\(.+\)')
    mapCountDict = {}
    command = "samtools flagstat --threads {} {}".format(runThread, bam)
    resList = functools.subprocessToList(command)
    for line in resList:
        ## eg. 40362505 + 0 primary mapped (98.16% : N/A)
        row = line[0].strip().split(' ')
        count = row[0]
        field = regex.sub('', ' '.join(row[3:]))
        mapCountDict[field] = count
    ## get primary mapped read count
    if options.estlibsize == "primary_mapped":
        libSize = mapCountDict["primary mapped"]
    elif options.estlibsize == "mapped":
        libSize = mapCountDict["mapped"]
    elif options.estlibsize == "primary":
        if options.pairend is False:
            libSize = mapCountDict["primary"]
    return int(libSize)

def getLibSizeParallel(options, bamList):
    ## convert bam to bedgraph by using bedtools
    ## bamList is the soft symbolic bam
    bamCount = len(bamList)
    if options.thread > bamCount:
        runThread = int(options.thread / bamCount)
        thread = bamCount
    else:
        runThread = 1
        thread = options.thread
    ## prepare arguments for parallel
    bulkArgsList = []
    for bam in bamList:
        bulkArgsList.append([options, bam, runThread])
    ## run in paralell
    resultList = []
    with closing(get_context(options.threadstart).Pool(thread)) as pool:
        imap = pool.imap(getLibSize, bulkArgsList)
        for result in imap:
            resultList.append(result)
    return resultList

def getPairLibScale(options, ipBamList, inputBamList):
    ## allways down-scaling
    ## determin the libSize of input relative to ip
    ipLibSize = sum(map(lambda x: functools.getCellByBam(options, x, 'lib_size'), ipBamList)) / len(ipBamList)
    inputLibSize = sum(map(lambda x: functools.getCellByBam(options, x, 'lib_size'), inputBamList)) / len(inputBamList)
    ## the libSize is ip bam relative to input bam,reads(ip)/reads(input)
    if ipLibSize > inputLibSize:
        ipLibScale = ipLibSize / inputLibSize
        inputLibScale = 1
    else:
        ipLibScale = 1
        inputLibScale = inputLibSize / ipLibSize
    return [ipLibScale, inputLibScale]
