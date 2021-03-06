from pprint import pprint
import os
import time
import datetime
import re
from IPython import embed

def isStarted(logdir):
    logF = get_latest_log(logdir)
    if logF is None:
        return False
    else:
        return True

#TODO: code de-duplication across isDone() and isCrashed()
def isDone(logdir):
    goodStr = 'Optimization Done.'
    logF = get_latest_log(logdir)
    if goodStr in open(logF).read():
        return True
    else:
        return False

def isCrashed(logdir):
    goodStr = 'Check failed:' #should capture any LOG(FATAL) situation.
    logF = get_latest_log(logdir)
    if goodStr in open(logF).read():
        return True
    else:
        return False

'''
#e.g. scheduler ended the job, but there's more training to do
def isPaused(logDir):
    #there is no defining characteristic of "Titan scheduler killed the job,"
    # other than "the log file ends abruptly without any error messages."
''' 
#@param netDir = absolute path to place where solverstate files are located
def get_latest_snapshot(netDir):
    files = os.listdir(netDir)
    files = [f for f in files if f.endswith('.solverstate')]
    if len(files) == 0:
        return None

    max_iter = 0
    max_iter_file = None

    for f in files:
        f_iter = f.split('.solverstate')[0] #trim extension
        f_iter = f_iter.split('_')[-1] #googlenet_iter_160000 -> 160000
        f_iter = int(f_iter)

        if f_iter > max_iter:
            max_iter = f_iter
            max_iter_file = f

    return max_iter_file
    
#@param netID = random seed for this net (e.g. 3 -> ./nets/3)
def get_forward_time(netDir):
    #dir = './nets/%d' %netID
    f = open(netDir + '/timing.log')

    time_str = None
    line = f.readline()
    while line:
        if "Forward pass: " in line:
            time_str = line #I1220 20:47:35.469178  2823 caffe.cpp:247] Forward pass: 1940.47 milliseconds.
        line = f.readline()
    f.close()
    if time_str is None:
        return None
    time_substr = time_str.split("Forward pass: ")[1] #1940.47 milliseconds.
    time_float = float(time_substr.split(' ')[0]) #1940.47 
    return time_float


#get the filename of the latest training log, e.g. "train_Sun_2014_12_21__16_01_39.log"
#@param for_timing is a hack to look for time_training*.log instead of just train*.log
def get_latest_log(logdir, for_timing=False):
    #logdir = './nets/%d' %netID
    allfiles = os.listdir(logdir)

    files_with_time = []

    searchstr = 'train_'
    if for_timing:
      searchstr =  'time_training_'

    for f in allfiles:
        #if not (f.startswith('train_') and f.endswith('.log')):
        if not (f.startswith(searchstr) and '.log' in f):
            continue
        timeOnly = f[len(searchstr):]
        #timeOnly = timeOnly[:-len('.log')]
        timeOnly = timeOnly.split('.log')[0]
        timeOnly = time.strptime(timeOnly, '%a_%Y_%m_%d__%H_%M_%S')
        files_with_time.append({'filename':f, 'time':timeOnly})

    if len(files_with_time) == 0:
        return None

    files_with_time = sorted(files_with_time, key=lambda f:f['time']) #sort from old to new
    #pprint(files_with_time)
    return logdir + '/' + files_with_time[-1]['filename']

#@param log_filename: e.g. './nets/0/train_Sun_2014_12_21__16_01_39.log'
#@return num iter and accuracy
def get_current_accuracy(log_filename):
    '''
    look latest one of these:
    I1221 22:31:42.642572 23298 solver.cpp:247] Iteration 34000, Testing net (#0)
    I1221 22:34:36.420714 23298 solver.cpp:298]     Test net output #0: accuracy = 0.11198
    '''

    f = open(log_filename)
    test_results = [] #results for every time we test the net

    line = f.readline()
    while line:
        if "Testing net" in line:
            iter_str = line #...solver.cpp:247] Iteration 34000, Testing net (#0)
            accuracy_str = f.readline() #...solver.cpp:298]     Test net output #0: accuracy = 0.11198

            iter = iter_str.split("Iteration ")[1].split(',')[0]
            iter = int(iter)
          
            ''' 
            if("Test net output #0: " in accuracy_str): #is occasionally missing, e.g. if job dies while writing output to disk 
                accuracy = accuracy_str.split("Test net output #0: ")[1].split('= ')[1]
                accuracy = float(accuracy)
                test_results.append({'accuracy':accuracy, 'iter':iter})
            '''
            #top-1
            if "accuracy = " in accuracy_str:
                accuracy = accuracy_str.split('= ')[1]
                accuracy = float(accuracy)
                test_results.append({'accuracy':accuracy, 'iter':iter})

            #top-5 (if available)
            try:
                accuracy_top5_str = f.readline()
                if "accuracy_top5 = " in accuracy_top5_str:
                    accuracy_top5 = accuracy_top5_str.split('= ')[1]
                    accuracy_top5 = float(accuracy_top5)
                    test_results[-1]['accuracy_top5'] = accuracy_top5
            except:
                pass

        if "error" in line:
            return "error"

        line = f.readline()


    #print '      test_results: ', test_results
    #test_results is already sorted, since we read the log file in order
    return test_results[-1]
   
def get_current_accuracy_googlenet(log_filename):
    '''
    I1015 14:09:41.126691 18569 solver.cpp:275] Iteration 50000, Testing net (#0)
    I1015 14:09:55.964213 18569 solver.cpp:339]     Test net output #7: loss3/top-1 = 0.597995
    I1015 14:09:55.964251 18569 solver.cpp:339]     Test net output #8: loss3/top-5 = 0.830497
    '''
    f = open(log_filename)
    test_results = [] #results for every time we test the net

    line = f.readline()
    while line:
        if "Testing net" in line:
            iter_str = line #...solver.cpp:247] Iteration 34000, Testing net (#0)

            iter = iter_str.split("Iteration ")[1].split(',')[0]
            iter = int(iter)

            accuracy = -1.0 #if you see this, then the job was killed while Testing net
            accuracy_str = f.readline()
            while "loss3/top-1" not in accuracy_str:
                accuracy_str = f.readline()
            #split... ...loss3/top-1 = 0.597995
            accuracy = accuracy_str.split('= ')[1]
            accuracy = float(accuracy)
            test_results.append({'accuracy':accuracy, 'iter':iter})

        if "error" in line:
            return "error"

        line = f.readline()
    return test_results[-1] 

#@param [{elapsed_time_sec, elapsed_iter}, ...]
def time_per_iter_stats(time_per_iter_dicts):
    time_per_iter_list = [d['elapsed_time_sec'] / d['elapsed_iter'] for d in time_per_iter_dicts]
    out = dict()
    out['min'] = min(time_per_iter_list)
    out['max'] = max(time_per_iter_list)
    out['mean'] = sum(time_per_iter_list) / float(len(time_per_iter_list))
    return out 

#@param log_filename = e.g. path/to/train_Mon_2015_12_14__16_07_30.log
#@return {min, max, mean} time (in seconds) per iter of training
def get_time_per_iter(log_filename):
    '''
    I1221 14:27:37.733464 24560 solver.cpp:558] Iteration 13120, lr = 0.0735673
    I1221 14:28:02.202710 24560 solver.cpp:558] Iteration 13160, lr = 0.0735468
    #Lmmdd hh:mm:ss.uuuuuu
    '''
    f = open(log_filename)
    line = f.readline()

    prev_timestamp = None
    curr_timestamp = None

    prev_iter = None
    curr_iter = None

    result_dicts = []

    while line:
        if 'lr =' in line:
            #print line

            # PARSE TIMESTAMP from google-logging message
            prev_timestamp = curr_timestamp

            time_re = r'\d{4} \d{2}:\d{2}:\d{2}.\d{6}'
            time_format = '%m%d %H:%M:%S.%f'

            time_to_parse = re.search(time_re, line).group() #whole line -> 1221 14:27:37.733464
            curr_timestamp = datetime.datetime.strptime(time_to_parse, time_format)

            # PARSE ITERATION 
            prev_iter = curr_iter
            curr_iter = int(re.search('Iteration \d+', line).group().split(' ')[1])

            # ELAPSED QUANTITIES
            if prev_timestamp is not None:
                elapsed_time = curr_timestamp - prev_timestamp
                elapsed_iter = curr_iter - prev_iter

                #print elapsed_time.total_seconds()
                result_dicts.append({'elapsed_time_sec':elapsed_time.total_seconds(), 'elapsed_iter':elapsed_iter})

        line = f.readline()

    stats = time_per_iter_stats(result_dicts)
    return stats

