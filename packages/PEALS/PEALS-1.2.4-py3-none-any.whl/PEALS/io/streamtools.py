# -*- coding: utf-8 -*-
##########################################
#           streamtool                   #
#          2022.3.24                     #
##########################################
__author__ = "Keren Zhou"
__version__ = "v1.0"

import os
import pickle
from PEALS.collection import bedutils

def readPickle(pfile, bufferSize=1000):
    return pickle.load( open(pfile, 'rb', buffering=bufferSize) )

def readPeakFromFile(peakFileList, bufferSize=1000, bed12Plus=True, folder=None):
    ## read peak outputs to peakRowList
    peakRowList = []
    if folder is not None:
        peakFileList = list(map(lambda x:os.path.join(folder, x), peakFileList))
    for peakFile in peakFileList:
        with open(peakFile, 'r', buffering=bufferSize) as f:
            for line in f:
                row = line.strip().split('\t')
                if bed12Plus is True:
                    row[12] = True if row[12] == 'True' else False
                    row[13] = float(row[13])
                    row[14] = float(row[14])
                buildbed = bedutils.buildbed(row)
                row = buildbed.list
                peakRowList.append(row)
    return peakRowList

def dumpPeakToMbb(peakRowList, mbbFile, folder=None):
    if folder is not None:
        mbbFile = os.path.join(folder, mbbFile)
    pickle.dump( peakRowList, open(mbbFile, "wb"))

def readPeakFromMbb(mbbFileList, bufferSize=1000, folder=None):
    peakRowList = []
    if folder is not None:
        mbbFileList = list(map(lambda x:os.path.join(folder, x), mbbFileList))
    for mbbFile in mbbFileList:
        perPeakRowList = readPickle(mbbFile, bufferSize=1000)
        peakRowList.extend(perPeakRowList)
    return peakRowList

def peakToFile(peakRowList, file, bed12=False, folder=None):
    if folder is not None:
        file = os.path.join(folder, file)
    with open(file, 'w') as out:
        for peakRow in peakRowList:
            if bed12 is True:
                out.write('\t'.join(map(str, peakRow[0:12])) + '\n')
            else:
                out.write('\t'.join(map(str, peakRow)) + '\n')
