# -*- coding: utf-8 -*-
##########################################
#           optioncheck                  #
#          2023.02.23                    #
##########################################
__author__ = "Keren Zhou"
__version__ = "v1.1"

"""Module Description
This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file LICENSE included with
the distribution).
"""

# ------------------------------------
# python modules
# ------------------------------------
import sys
import os
import re
import logging
import pandas as pd
import psutil

from PEALS.collection import functools
from PEALS.io.constant import *
from PEALS.io import paramlog

cpuCount = psutil.cpu_count()

def exitError(message):
    logging.error(message)
    sys.exit(1)

def parseError(option):
    message = "Error when parssing '--{}' option.".format(option)
    return message

def parseAvail(values):
    optionValue = "{}".format(', '.join(map(str, values)))
    message = "Available values will be one of ({})".format(optionValue)
    return message

def checkArgsEqual(option1, option2, optionName1, optionName2):
    if len(option1) != len(option2):
        logging.error("Error when parssing '--{}' and '--{}' option.".format(optionName1, optionName2))
        exitError("The number of input arguments of '--{}' and '--{}' option should be the same!".format(optionName1, optionName2))

def checkThirdParty(options):
    logging.info("Checking whether required third party software are properly installed...")
    installFlag = True
    failureList = []
    for software in sorted(options.thirdparty.keys()):
        env = options.thirdparty[software]
        install = functools.checkSoftware(software, env)
        if install is False:
            failureList.append(software)
    if len(failureList) > 1:
        softwares = ', '.join(failureList)
        exitError("The following third party sofware is not installed or not found in your path environment: ({}).".format(softwares))
    else:
        logging.info("Congratulations! All required third party software are properly installed!")

def checkThead(options):
    if options.thread > 64:
        ## Value for argumant -T is out of range: 1 to 64, limited by featureCounts
        options.thread = 64
    elif options.thread <= 0:
        options.thread = 1
    return options

def checkSample(options):
    inforDict = functools.decodeSample(options)
    count = len(inforDict['value'])
    if options.subprogram == 'callpeak':
        ##key: column,value
        if count != 1:
            exitError(parseError('sample'))
    elif options.subprogram == 'diffpeak':
        ##key: column,value,control,treated
        keyList = sorted(inforDict.keys())
        if 'control' not in keyList or 'treated' not in keyList:
            exitError(parseError('sample'))
        if count != 2:
            exitError(parseError('sample'))
    return inforDict

def checkSplitSize(options):
    ## Value for split a transcript
    if options.txsizemax < 5000:
        options.txsizemax = 5000
    elif options.txsizemax > 50000:
        options.txsizemax = 50000
    return options

def checkVerbose(options):
    if options.verbose > 3:
        logging.error(parseError('verbose'))
        exitError(parseAvail([0, 1, 2, 3]))

def chekFolder(folder, default, optionName):
    if folder is None:
        if default == 'cwd':
            folder = os.path.realpath(os.getcwd())
        else:
            folder = default
    else:
        try:
            os.makedirs(folder, exist_ok=True)
        except:
            logging.error(parseError(optionName))
            exitError("Output directory ({}) could not be created. Terminating program.".format(folder))

def checkArgsIsFile(*argsFiles, optionName):
    for argsFile in argsFiles:
        if os.path.isfile(argsFile) is False:
            logging.error(parseError(optionName))
            exitError("At least one invalid file detected in '--{}' option!".format(optionName))

def readInputFromFile(fileList, optionName, extension):
    parsedFileList = []
    isFlag = True
    if len(fileList) == 1:
        ## check whether input is a valid file
        checkArgsIsFile(*fileList, optionName)
        with open(fileList[0], 'r') as f:
            for file in f:
                file = file.strip()
                fextend = os.path.splitext(os.path.basename(file))[-1]
                if fextend == extension:
                    parsedFileList.append(file)
                else:
                    isFlag = False
                    break
        ## isFlag is True, then return decode files
        if isFlag is True:
            ## check whether files in input is valid files
            checkArgsIsFile(*parsedFileList, optionName)
            return parsedFileList
        else:
            logging.error(parseError(optionName))
            logging.error("At least one file in the input is not with '{}' extension.".format(extension))
            sys.exit(1)
    else:
        logging.error(parseError(optionName))
        exitError("The input should be files with '{}' extension.".format(extension))

def checkInputFileOption(fileList, optionName, extension, readFlag=False):
    isFlag = True
    for File in fileList:
        ## check the extension
        fextend = os.path.splitext(os.path.basename(File))[-1]
        if fextend != extension:
            isFlag = False
            break
    if isFlag is False:
        ## try to get input from a file
        parsedFileList = readInputFromFile(fileList, optionName, extension)
        return parsedFileList
    else:
        return fileList

def parssingMatrixError(message):
    logging.error(parseError('matrix'))
    exitError(message)

def checkMatrixFile(options):
    ## check the header
    headerList = []
    idColValList = []
    with open(options.matrix, 'r') as f:
        headerList = f.readline().strip().split('\t')
        for line in f:
            row = line.strip().split('\t')
            idColValList.append(row[0])
    ## check whether the first column is id
    if headerList[0] != 'id':
        parssingMatrixError("The name of first column should be 'id'.")
    ## check whether id in 'id' column is unique
    if len(idColValList) != len(set(idColValList)):
        parssingMatrixError("The value of 'id' column should be unique.")
    ## check header
    #requiredColNameList = ["id", "library", "condition", "replicate", "label", "bam", "binary"]
    requiredColNameList = ["id", "library", "condition", "replicate", "label", "bam"]
    for colName in requiredColNameList:
        if colName not in headerList:
            parssingMatrixError("The column ({}) is required!".format(colName))
    ##parsing sample matrix
    matrixDf = pd.read_csv(options.matrix, header=0, sep="\t", index_col=0, skiprows=0)
    ## if needs to sample subset
    if options.sample is not None:
        inforDict = checkSample(options)
        subsetCol = inforDict['column']
        subsetValList = inforDict['value']
        ## whether the column in matrix
        if subsetCol not in matrixDf.columns:
            parssingMatrixError("The column ({}) is not in sample matrix!".format(subsetCol))
        ## subset the matrix
        matrixDf = matrixDf.loc[matrixDf[subsetCol].isin(subsetValList)]
        ## whether the subet matrix is empty
        if matrixDf.empty is True:
            values = ','.join(subsetValList)
            parssingMatrixError("Values ({}) is not found in the column ({})in sample matrix!".format(values, subsetCol))
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
    ### check condition
    conditionList = sorted(matrixDf['condition'].unique())
    conditionCount = len(conditionList)
    if conditionCount == 1:
        if conditionList[0] != 'control' and conditionList[0] != 'treated':
            parssingMatrixError("The value  in column 'condition' should be either 'control' or 'treated' when running 'callpeak' subcommand!")
    elif conditionCount == 2:
        if conditionList != ['control', 'treated']:
            parssingMatrixError("The values in column 'condition' should be 'control' and 'treated' when running 'diffpeak' subcommand!")
    else:
        parssingMatrixError("Currently only support at most 2 conditions in a test ('control' and 'treat').")
    ## check library
    libraryList = sorted(matrixDf['library'].unique())
    if len(libraryList) == 2:
        for condition in conditionList:
            libraryList = sorted(matrixDf[ matrixDf['condition'] == condition ]['library'].unique())
            if libraryList != ['input', 'ip']:
                parssingMatrixError("The values in column 'library' should be 'input' and 'ip' in conditon ({})!".format(condition))
    else:
        parssingMatrixError("Currently only support with ('input' and 'ip')!")
    ### check replicate, label & binary
    if pd.api.types.is_int64_dtype(matrixDf['replicate']) is False:
        parssingMatrixError("The column 'replicate' should be integers!")
    ### check other
    for condition in conditionList:
        inputDf = matrixDf[ (matrixDf['condition'] == condition) & (matrixDf['library'] == 'input') ].sort_values(by=['replicate'], ascending=True)
        ipDf = matrixDf[ (matrixDf['condition'] == condition) & (matrixDf['library'] == 'ip') ].sort_values(by=['replicate'], ascending=True)
        ### check replicate
        inputRepList = inputDf['replicate'].to_list()
        ipRepList = ipDf['replicate'].to_list()
        if inputRepList != ipRepList:
            parssingMatrixError("The corresponidng values in 'replicate' column must be the same in the condition ({})!".format(condition))
        if len(set(ipRepList)) != len(ipRepList):
            parssingMatrixError("The values in 'replicate' column should be unique in 'input' or 'ip' in the condition ({})!".format(condition))
        ### check label
        inputLabelList = inputDf['label'].to_list()
        ipLabelList = ipDf['label'].to_list()
        if inputLabelList != ipLabelList:
            parssingMatrixError("The corresponidng values in 'label' column must be the same in the condition ({})!".format(condition))
        if len(set(ipLabelList)) != len(ipLabelList):
            parssingMatrixError("The values in 'label' column should be unique in 'input' or 'ip' in the condition ({})!".format(condition))
        ## check binary if neccesary
        if options.binary is True:
            inputBinaryList = inputDf['binary'].to_list()
            ipBinaryList = ipDf['binary'].to_list()
            if inputBinaryList != ipBinaryList:
                parssingMatrixError("The corresponidng values in 'binary' column must be the same in the condition ({})!".format(condition))
            if len(set(ipBinaryList)) != len(ipBinaryList):
                parssingMatrixError("The values in 'binary' column should be unique in 'input' or 'ip' in the condition ({})!".format(condition))

def validateCallpeakArgs(options):
    """Validate options from argparser.parse_args().
    Ret: Validated options object.
    """
    # check verbose, thread, split size for sub-transcirpt
    checkVerbose(options)
    options = checkThead(options)
    options = checkSplitSize(options)
    # setting logging object
    logging.basicConfig(level=(4-options.verbose)*10,
                        format='%(levelname)-5s @ %(asctime)s: %(message)s ',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        stream=sys.stderr,
                        filemode="w"
                        )
    ## subprogram
    options.subprogram = 'callpeak'
    # function alias
    options.error = logging.error
    options.warn  = logging.warning
    options.debug = logging.debug
    options.info  = logging.info
    ## binary
    options.reuse = False
    options.binary = False
    options.binaryapp = BINARY_APPENDIX
    options.binarydir = None
    ## check sample matrix
    checkMatrixFile(options)
    # determin outputdir
    chekFolder(options.outputdir, 'cwd', 'output')
    # determin temdir
    chekFolder(options.tempdir, options.outputdir, 'temp')
    # determin binarydir
    chekFolder(options.binarydir, options.outputdir, 'binary')
    ## constant
    options.idsepdict = ID_SEP_DICT
    options.tempre = TEMP_PREFIX
    options.labelref = REF_PEAK_LABEL
    options.txoptsize = int(options.txsizemax * 0.2)
    options.spandict = SPAN_DICT
    options.version = VERSION
    ## construct peak regex
    peakidsep = options.idsepdict['peakid'].replace('|', '\\|')
    options.peakregex = r'{0}\d+{0}T$'.format(peakidsep)
    ##
    if options.peaksize is None:
        options.peaksize = max([int(options.extsize / 2), PEAK_SIZE])
    ## 
    if options.thread >= cpuCount:
        options.thread = max(cpuCount, 1)
    ## print the running parameters
    paramlog.log(options)
    ## check requried third party software
    options.thirdparty = THIRD_PARTY_SOFTWARE
    checkThirdParty(options)
    return options

def validateDiffpeakArgs(options):
    """Validate options from argparser.parse_args().
    Ret: Validated options object.
    """
    # check verbose, thread, split size for sub-transcirpt
    checkVerbose(options)
    options = checkThead(options)
    options = checkSplitSize(options)
    # setting logging object
    logging.basicConfig(level=(4-options.verbose)*10,
                        format='%(levelname)-5s @ %(asctime)s: %(message)s ',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        stream=sys.stderr,
                        filemode="w"
                        )
    ## subprogram
    options.subprogram = 'diffpeak'
    # function alias
    options.error = logging.error
    options.warn  = logging.warning
    options.debug = logging.debug
    options.info  = logging.info
    ## binary
    options.reuse = False
    options.binary = False
    options.binaryapp = BINARY_APPENDIX
    options.binarydir = None
    ## check sample matrix
    checkMatrixFile(options)
    # determin outputdir
    chekFolder(options.outputdir, 'cwd', 'output')
    # determin temdir
    chekFolder(options.tempdir, options.outputdir, 'temp')
    # determin binarydir
    chekFolder(options.binarydir, options.outputdir, 'binary')
    ## constant
    options.idsepdict = ID_SEP_DICT
    options.tempre = TEMP_PREFIX
    options.labelref = REF_PEAK_LABEL
    options.txoptsize = int(options.txsizemax * 0.3)
    options.spandict = SPAN_DICT
    options.version = VERSION
    ## construct peak regex
    peakidsep = options.idsepdict['peakid'].replace('|', '\\|')
    options.peakregex = r'{0}\d+{0}T$'.format(peakidsep)
    ##
    if options.peaksize is None:
        options.peaksize = max([int(options.extsize / 2), PEAK_SIZE])
    ## 
    if options.thread >= cpuCount:
        options.thread = max(cpuCount, 1)
    ## print the running parameters
    paramlog.log(options)
    ## check requried third party software
    options.thirdparty = THIRD_PARTY_SOFTWARE
    checkThirdParty(options)
    return options
