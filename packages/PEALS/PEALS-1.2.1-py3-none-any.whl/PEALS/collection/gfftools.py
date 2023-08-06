# -*- coding: utf-8 -*-
##########################################
#           peakutils                    #
#          2023.02.23                    #
##########################################
__author__ = "Keren Zhou"
__version__ = "v2.0"

import re
from collections import defaultdict
from copy import copy
import tempfile
from multiprocessing import get_context
from contextlib import closing

# own module
from PEALS.collection import bedutils
from PEALS.collection import functools
from PEALS.collection import bamtool

def gffFeatureDict(gffType, source = 'GENCODE'):
    featureDict = defaultdict(dict)
    featureDict['gene'] = ['gene']
    featureDict['start_codon'] = ['start_codon']
    featureDict['stop_codon'] = ['stop_codon']
    featureDict['transcript'] = ['transcript']
    featureDict['exon'] = ['exon']
    featureDict['CDS'] = ['CDS']
    if gffType == 'GFF3' and source == 'ENSEMBL':
        featureDict['transcript'] = ['mRNA', 'ncRNA', 'lnc_RNA', 'pre_miRNA', 'RNase_MRP_RNA', 'rRNA', 'snoRNA', 'snRNA', 'SRP_RNA', 'tRNA']
    ## create blockdict
    blockNameList = ['start_codon', 'stop_codon', 'CDS', 'exon']
    for block in blockNameList:
        for value in featureDict[block]:
            featureDict['block'][value] = block
    return featureDict

def gffIdentifier(gffType):
    if gffType == 'GTF':
        identifier = 'transcript_id,transcript_id'
    elif gffType == 'GFF3':
        identifier = 'Parent,ID'
    return identifier

def gffAttParser(attribute, gffType):
    listA = []
    if gffType == 'GFF3':
        listA = re.split('=|;', attribute)
    elif gffType == 'GTF':
        listA = re.split('\s"|";\s|";', attribute)
    return functools.list2Dict(listA)

def getAttVal(attDict, attid):
    if attid in attDict:
        val = attDict[attid]
    else:
        val = 'NA'
    return val

##
def gffparser(bulkArgs):
    options, chromosome, featureDict, expTxidDict = bulkArgs
    parserDict = defaultdict(dict)
    #options.debug('Decoding gene annotations in chromosome:{}'.format(chromosome))
    ## format of featureDict
    '''
    {'chrom':chr1, 'strand', 'exon':['exon'], 'CDS':['CDS'], ...}
    '''
    ## identifier: 'transcript_id,transcript_id' or 'Parent,ID'
    skipRegex = re.compile(r'(^#.*)|(^$)')
    ## transcript_id, transcript_id or ## Parent:ID
    identifier = gffIdentifier(options.gfftype)
    txidName, featureidName = identifier.split(',')
    with open(options.gff, 'r', buffering=options.buffer) as f:
        for line in f:
            if bool(skipRegex.match(line)) is True:
                continue
            row = line.rstrip('\n').split('\t')
            feature = row[2]  # gene, transcript, exon, CDS...
            ## record coordniates of features
            if feature in featureDict['block']:
                ## skip chrom
                chrom = row[0]
                if chrom != chromosome:
                    continue
                ## get attribute value
                attributeDict = gffAttParser(row[-1], options.gfftype)
                ## determin feature
                feature = featureDict['block'][feature]
                txid = attributeDict[txidName]
                ## skip non-expessed transcripts
                if txid not in expTxidDict:
                    continue
                start = int(row[3]) - 1
                end = int(row[4])
                strand = row[6]
                ## record chromosomes and strand
                if 'chrom' not in parserDict[txid]:
                    parserDict[txid]['chrom'] = row[0]
                    parserDict[txid]['strand'] = row[6]
                # if feature not in parserDict.get(txid, {}):
                if feature not in parserDict[txid]:
                    parserDict[txid][feature] = [[], []]
                parserDict[txid][feature][0].append(start)
                parserDict[txid][feature][1].append(end)
    ## decode parserDict to bed12 row
    bed12RowList = []
    for txid in sorted(parserDict.keys()):
        chrom = parserDict[txid]['chrom']
        strand = parserDict[txid]['strand']
        start = min(parserDict[txid]['exon'][0])
        end = max(parserDict[txid]['exon'][1])
        bcount = len(parserDict[txid]['exon'][0])
        ## if rnatype is mature, then decode transcripts into mature RNA
        if (options.rnatype == 'mature' or options.rnatype == 'mixture'):
            bstartList = sorted(parserDict[txid]['exon'][0])
            bendList = sorted(parserDict[txid]['exon'][1])
            thickStart = start
            thickEnd = start
            bcount = len(bstartList)
            bsize = ','.join(functools.list2Str([bendList[i] - bstartList[i] for i in range(bcount)]))
            bstart = ','.join(functools.list2Str([x - thickStart for x in bstartList]))
            ## label thickModifiedFlag
            thickStartFlag = False
            thickEndFlag = False
            if 'CDS' in parserDict[txid]:
                if 'start_codon' in parserDict[txid]:
                    if strand == '+':
                        thickStart = min(parserDict[txid]['start_codon'][0])
                        thickStartFlag = True
                    else:
                        thickEnd = max(parserDict[txid]['start_codon'][1])
                        thickEndFlag = True
                if 'stop_codon' in parserDict[txid]:
                    if strand == '+':
                        thickEnd = max(parserDict[txid]['stop_codon'][1])
                        thickEndFlag = True
                    else:
                        thickStart = min(parserDict[txid]['stop_codon'][0])
                        thickStartFlag = True
                ## continue to change
                if thickStartFlag is False:
                    thickStart = min(parserDict[txid]['CDS'][0])
                if thickEndFlag is False:
                    thickEnd = max(parserDict[txid]['CDS'][1])
            ## construct bed12
            labelTxid = options.idsepdict['labeltxid'].join([txid, 'mature'])
            bed12Row = [chrom, start, end, labelTxid, 0, strand, thickStart, thickEnd, 0, bcount, bsize, bstart]
            bed12RowList.append(bed12Row)
        ## if rnatype is primary, then decode transcripts into primary RNA
        if (options.rnatype == 'primary' or options.rnatype == 'mixture'):
            if options.rnatype == 'mixture' and bcount == 1:
                continue
            labelTxid = options.idsepdict['labeltxid'].join([txid, 'primary'])
            txLen = end - start
            bed12Row = [chrom, start, end, labelTxid, 0, strand, start, end, 0, 1, str(txLen), '0']
            bed12RowList.append(bed12Row)
    return bed12RowList

def prepareGffpaserBulkArgs(options, featureDict, expTxidDict):
    skipRegex = re.compile(r'(^#.*)|(^$)')
    ## transcript_id, transcript_id or ## Parent:ID
    identifier = gffIdentifier(options.gfftype)
    txidName, featureidName = identifier.split(',')
    chromDict = {}
    with open(options.gff, 'r', buffering=options.buffer) as f:
        for line in f:
            if bool(skipRegex.match(line)) is True:
                continue
            row = line.rstrip('\n').split('\t')
            feature = row[2]  # gene, transcript, exon, CDS...
            ## record coordniates of features
            if feature in featureDict['block']:
                attributeDict = gffAttParser(row[-1], options.gfftype)
                ## determin feature
                feature = featureDict['block'][feature]
                txid = attributeDict[txidName]
                ## skip non-expessed transcripts
                if txid not in expTxidDict:
                    continue
                chrom = row[0]
                chromDict[chrom] = 1
    paramList = []
    for chrom in sorted(chromDict.keys()):
        paramList.append([ options, chrom, featureDict, expTxidDict ])
    return paramList

def gffToTxBedDict(options, txidList):
    ## build gene->tx->bedutils.buildbed(row).decode() from gff
    ## return a dictionary
    ## convert gff to bed12
    expTxidDict = {}
    for txid in txidList:
        expTxidDict[txid] = 1
    ## essential values
    gff = options.gff
    gfftype = options.gfftype
    gffsource = options.gffsource
    txDict = defaultdict(dict)
    _geneid, _geneName, _geneType, _txid, _txName, _txType = options.identifier.split(':')
    skipRegex = re.compile(r'(^#.*)|(^$)')
    ## prepearing feature
    featureDict = gffFeatureDict(gfftype, gffsource)
    with open(options.gff, 'r', buffering=options.buffer) as f:
        for line in f:
            if bool(skipRegex.match(line)) is True:
                continue
            row = line.strip().split('\t')
            attributeDict = gffAttParser(row[-1], gfftype)
            #txid = re.findall(r'transcript_id "(.+?)";', row[-1])[0]
            if _txid not in attributeDict or _geneid not in attributeDict:
                continue
            txid = attributeDict[_txid]
            ## skip non-expressed transcripts
            if txid not in expTxidDict:
                continue
            if txid not in txDict:
                geneid = attributeDict[_geneid]
                geneName = getAttVal(attributeDict, _geneName)
                geneType = getAttVal(attributeDict, _geneType)
                txName = getAttVal(attributeDict, _txName)
                txType = getAttVal(attributeDict, _txType)
                txDict[txid]['gene_id'] = geneid
                txDict[txid]['gene_name'] = geneName
                txDict[txid]['gene_type'] = geneType
                txDict[txid]['transcript_name'] = txName
                txDict[txid]['transcript_type'] = txType
    ## start to pool
    ## convert gff to bed12
    ## return a list contain bed12 rows
    ## generate txdict
    resultList = []
    with closing(get_context(options.threadstart).Pool(options.thread)) as pool:
        #options.debug('Identifing peak candidates on chromosomes ({})...'.format( ','.join(chromList)))
        ## prepare chromosomes
        options.debug('Prepearing chromosomes for decoding annotations.')
        paramList = prepareGffpaserBulkArgs(options, featureDict, expTxidDict)
        chromosomes = ','.join(map(lambda x:x[1], paramList))
        options.debug('Transcripts from following chromosomes will be decoded:({})'.format(chromosomes))
        options.debug('Decoding annotations in parrallel...')
        imapUnordered = pool.imap_unordered(gffparser, paramList)
        for i, result in enumerate(imapUnordered):
            if bool(result):
                resultList.append(result)
    ## generate bed12 from gff
    #bed12RowList = gffparser(options, featureDict, expTxidDict)
    ## construct the txBedDict
    txBedDict = {}
    for bed12RowList in resultList:
        ## [ ['chr7', 127588410, 127591700, 'ENST00000000233.10#mature', 0, '+', 127588498, 127591299, 255, 6, '155,81,110,72,126,488', '0,672,1074,1655,2552,2802'], ... ]
        ## annotate generated bed12 with gff
        for row in bed12RowList:
            labelTxid = row[3]
            txid = labelTxid.split(options.idsepdict['labeltxid'])[0]
            if txid in txDict:
                geneid = txDict[txid]['gene_id']
                geneName = txDict[txid]['gene_name']
                geneType = txDict[txid]['gene_type']
                txName = txDict[txid]['transcript_name']
                txType = txDict[txid]['transcript_type']
                ## reconstruct the 4th column
                ## row[3], ENSG00000237613.2:FAM138A:lncRNA:ENST00000461467.1#mature:FAM138A-202:lncRNA
                ## geneid:geneName:geneType:labelTxid:txName:txType
                row[3] = options.idsepdict['txinfo'].join([geneid, geneName, geneType, labelTxid, txName, txType])
                txBed = bedutils.buildbed(row).decode()
                txBedDict[labelTxid] = txBed
    return txBedDict

def getChromTxDict(options, txBedDict, ipBam, inputBam):
    thread = max(1, int(options.thread / 2))
    bulkArgsList = [[options, thread, txBedDict, inputBam], [options, thread, txBedDict, ipBam]]
    chromTxDictList = []
    with Pool(2) as pool:
        imap = pool.imap(bamtool.bamToExpFilter, bulkArgsList)
        for result in imap:
            if bool(result):
                chromTxDictList.append(result)
    inputChromTxDict, inputtxidExpDict = chromTxDictList[0]
    ipChromTxDict, iptxidExpDict = chromTxDictList[1]
    chromTxDict = {}
    for chrom in ipChromTxDict.keys():
        txidList = list(filter(lambda x: x in inputChromTxDict[chrom], ipChromTxDict[chrom]))
        chromTxDict[chrom] = txidList
    return [chromTxDict, inputtxidExpDict]
