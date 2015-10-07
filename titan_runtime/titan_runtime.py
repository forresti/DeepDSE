import time 
import conf_rt as conf
import parse_logs
import os
import subprocess
from IPython import embed
import time
import xml.etree.ElementTree as ET 
from parse_logs import get_latest_snapshot
from pbs_template import pbs_template

#check whether I already have a PBS allocation queued or running
#@return: false if I already have an allocation queued/running.
#         true if I do not have an allocation queued/running.
def is_pbs_ready():
    #qstat_str = "qstat -u %s" %conf.uname
    qstat_str = "qstat -x" #get xml
    pbs_out = subprocess.check_output(qstat_str, shell=True)

    root = ET.fromstring(pbs_out)
    for job in root:
        username = job.find('euser').text
        job_state = job.find('job_state').text

        if (username == conf.uname) and (job_state != 'C'):
            #I already have a job queued or running
            return False

    return True #I don't have any jobs running.

def parse_job_status(job_dir):
    job_path = conf.net_dir + '/' + job_dir

    started = parse_logs.isStarted(job_path)
    if not started:
        return 'not_started'
   
    done = parse_logs.isDone(job_path)
    if done:
        return 'done' 

    crashed = parse_logs.isCrashed(job_path)
    if crashed:
        return 'crashed'

    else:
        return 'paused'

#@return list of eligible jobs (each entry is the relative path of a training run)
def get_eligible_jobs():
        #list of jobs
        jobs = sorted(os.listdir(conf.net_dir))

        #collect eligible jobs by parsing job status
        eligible_jobs = []    
        for j in jobs: #list of job subdirectory names
            status = parse_job_status(j)
            #print status
            if (status == 'not_started') or (status == 'paused'): # or (status == 'crashed'):
                eligible_jobs.append(j)

            elif (status == 'done') or (status == 'crashed'):
                continue

            else:
                print "unknown job status:", status

        return eligible_jobs

#@param eligible_jobs = list of job relative paths
#@return eligible_job_dicts = [{path, snapshot}, ...]
def get_snapshots(eligible_jobs):
    eligible_job_dicts = []
    for j in eligible_jobs:
        snapshot = get_latest_snapshot(conf.net_dir + '/' + j)
        eligible_job_dicts.append({'path':j, 'snapshot':snapshot})
    return eligible_job_dicts

#@param eligible_jobs = [{'path'...}, {'path'...}, ...]
#add n_gpu to each job dict
def get_n_gpu(eligible_jobs):
    for i in xrange( 0, len(eligible_jobs) ):
        n_gpu_f = conf.net_dir + '/' + eligible_jobs[i]['path'] + '/n_gpu.txt'
        with open(n_gpu_f,'r') as f:
            n_gpu = int(f.read())
        eligible_jobs[i]['n_gpu']=n_gpu
    return eligible_jobs 

#@return relative path to new PBS script
def pbs_template_wrapper(n_jobs, eligible_jobs):
    time_str = time.strftime("%a_%Y_%m_%d__%H_%M_%S")
    pbs_F = 'pbs_scripts/%s.pbs' %time_str
    pbs_str = pbs_template(n_jobs, eligible_jobs) #THE CRUX
    f = open(pbs_F, 'w')
    f.write(pbs_str)
    f.close()
    return pbs_F

# a "job" is a Caffe training run.
def schedulerLoop():

    unfinishedJobs = True #are there Caffe nets that need more training?
    
    while unfinishedJobs is True:

        #step 1: check for queued/running allocations (and wait for them to finish)
        isReady = is_pbs_ready()
        print "isReady: ", isReady 
        #   TODO: loop over isReady, with a 1-5min timeout.
        if not isReady:
            time.sleep(60) #1 minute
            continue

        #step 2: collect eligible jobs by parsing job status
        eligible_jobs = get_eligible_jobs()

        if len(eligible_jobs) == 0:
            unfinishedJobs = False
            break

        #  prune down to max_jobs
        n_jobs = min( len(eligible_jobs), conf.max_jobs )
        eligible_jobs = eligible_jobs[0:n_jobs] #eligible_jobs is a list of strings
        eligible_jobs = get_snapshots(eligible_jobs) #now, eligible_jobs is a list of {path, snapshot} dicts.
        eligible_jobs = get_n_gpu(eligible_jobs)

        #step 3: create PBS script of eligible jobs
        pbs_F = pbs_template_wrapper(n_jobs, eligible_jobs)
        print pbs_F

        #step 4: launch allocation
        pbs_out = subprocess.call('qsub %s' %pbs_F, shell=True)
        
        #step 5: remove old model snapshots (only keep newest snapshot)

        #unfinishedJobs = False #for debugging (TODO: remove)

if __name__ == "__main__":
    schedulerLoop()

