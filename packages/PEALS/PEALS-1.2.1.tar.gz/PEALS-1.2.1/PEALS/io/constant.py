# CONSTANT VALUE
VERSION = '1.2.1'
BUFFER_SIZE = 10000000
THREAD = 10
THREAD_START_METHOD="fork"
MATH_RELTOL = 0.05
MOVE_METHOD = "move"
SMOOTH_LOOP = 1
SMOOTH_SPAN = 25
PEAK_SIZE = 35
EXT_SIZE = 0
LOOK_AHEAD = 25
CSAPS_SMOOTH = 0.005
IP_RATIO = 1.25
CENTER = 0.25
COMPLEXITY_RATE = 0.05
SPAN_DICT = {'max':200, 'min':5, 'step':80}
TX_SPLIT_MAX_SIZE=50000
TX_SPLIT_OPT_SIZE=int(TX_SPLIT_MAX_SIZE * 0.3)
THIRD_PARTY_SOFTWARE = {'bedtools':['bash', '2.30.0'], \
                        'featureCounts':['bash', '2.0.2'], \
                        'samtools':['bash', '1.14'], \
                        'DESeq2':['R', '1.32.0'], \
                        'ashr':['R', '2.2.54'], \
                        'apeglm':['R', '1.14.0'], \
                        'ggplot2':['R', '3.4.1'],}
#identifier
ID_SEP_DICT={'labeltxid':'#=',\
             'txinfo':':=', \
             'genetx':'::', \
             'peakid':'|=', \
             'bedutils':'==', \
             'peakid_out':'|'}
##prefix and appendix
REF_PEAK_LABEL = 'PEALS_POOL_REF'
BINARY_APPENDIX = '.pb'
# CONSTANT TEMP NAME
TEMP_PREFIX = "peals_tmp"
# CONSTANT HELP
EPILOG_CALL_PEAK = """
Examples:
Peak calling for MeRIP-seq:
    $ peals callpeak -i <bam directory> -m <sample matrix> -P <prefix> -o <output directory>
"""

EPILOG_DIFF_PEAK = """
Examples:
Differential peak calling for MeRIP-seq:
    $ peals diffpeak -i <bam directory> -m <sample matrix> -P <prefix> -o <output directory>
"""

# CONSTANT LOGGING MESSAGE
RUNNING_TIME = "Total execution time for the whole analysis was: {}."
GET_GENE_EXP_LOG = "Obtaining gene expression..."
GET_TX_EXP_LOG = "Obtaining trascript expression..."
SUBSAMPLE_BAM_LOG = "Subsampling input bams with seed {}..."
BAM_TO_COVERAGE_LOG = "Preparing genome-wide reads coverage..."
DECODE_ANNO_LOG = "Decoding and building annotation information from {}..."
CALL_PEAK_LOG = "Calling peak candidates on ip ({}) and input ({})..."
CALL_PEAK_DONE_LOG = "Calling peak candidates on ip ({}) and input ({}) done."
READ_BINARY_LOG = "Reading binary files from specified input ({})..."
