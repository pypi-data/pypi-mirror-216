# ------------------------------------
# python modules
# ------------------------------------

import os
import sys
import logging

def glue(param, value):
    report = '{}={}'.format(param, value)
    return report

def log(options):
    inputParamDict = {'inputdir':'input', 'matrix':'matrix', 'binarydir':'binary-dir', \
                      'binary':'call-with-binary', 'recursive':'recursive', 'rnatype':'type', \
                      'sample':'sample', \
                     }
    outputParamDict = {'outputdir':'output', 'tempdir':'temp', 'prefix':'prefix', \
                      'nobwtrack':'no-bwtrack', 'keeptemp':'keep-temp', 'verbose':'verbose', \
                     }
    libraryParamDict = {'library':'library', 'estlibsize':'estlib-size', 'extsize':'extsize', \
                      'pairend':'pairend', \
                     }
    normalizeParamDict = {'expmethod':'exp-method', 'peaksizefactor':'estpeak-sizefactor', 'bwscale':'bw-scale', \
                          'estipeff':'estip-eff', \
                     }
    bamParamDict = {'scalesample':'scale-sample', 'sortbam':'sortbam', 'nofraction':'no-fraction', \
                    'fracoverlap':'frac-overlap', 'ignoredup':'ignore-dup', 'expcutoff':'exp-cutoff', \
                    }
    constantParamDict = {'thread':'thread', 'threadstart':'thread-start', 'reltol':'reltol', \
                    'buffer':'buffer', \
                    }
    annoParamDict = {'gsize':'gsize', 'gff':'gff', 'gfftype':'gff-type', \
                    'gffsource':'gff-source', 'identifier':'identifier', \
                    }
    peakParamDict = {'txsizemax':'split', 'spanmethod':'span-method', 'span':'span', \
                    'spanloop':'span-loop', 'comprate':'complexity-rate', 'lookahead':'lookahead', \
                    'csapsp':'csaps-p', 'csapsnor':'csaps-normalize', 'peaksize':'peak-size', \
                    'ipratio':'ipratio', 'center':'center', \
                    }
    modelParamDict = {'fittype':'fit-type', 'shrink':'shrink', 'test':'test', \
                    'formula':'formula', \
                    }
    filterParamDict = {'pvalcutoff':'pval', 'padjcutoff':'padj', 'padjmethod':'padj-method', \
                         'foldcutoff':'fold', 'difffoldcutoff':'diff-fold', 'diffpvalcutoff':'diff-pval', \
                         'diffpadjcutoff':'diff-padj', \
                    }
    paramGoupList = ['input', 'output', 'library', 'normalize', 'bam', \
                     'constant', 'annotation', 'peak', 'model', 'filter']
    paramMergeList = [inputParamDict, outputParamDict, libraryParamDict, normalizeParamDict, bamParamDict, \
                      constantParamDict, annoParamDict, peakParamDict, modelParamDict, filterParamDict]
    ## get the parameter dict
    optionDict = options.__dict__
    logging.info('PEALS (v{}) is running with following parameters:'.format(options.version))
    for i in range(len(paramGoupList)):
        groupName = paramGoupList[i]
        paramDict = paramMergeList[i]
        ## loop the parameters
        glueList = []
        for param in sorted(paramDict.keys()):
            if param not in optionDict:
                continue
            value = optionDict[param]
            param = paramDict[param]
            glueList.append(glue(param, value))
        glueVal = ', '.join(glueList)
        report = '[{}] parameter group: {}'.format(groupName, glueVal)
        logging.info(report)
