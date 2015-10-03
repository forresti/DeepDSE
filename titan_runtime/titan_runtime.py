import conf_rt as conf
import parse_logs
import os
import subprocess
from IPython import embed
import time
import xml.etree.ElementTree as ET 
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
 
        #step 2: list of jobs
        jobs = sorted(os.listdir(conf.net_dir))

        #step 3: collect eligible jobs by parsing job status
        eligible_jobs = []    
        for j in jobs: #list of job subdirectory names
            status = parse_job_status(j)
            #print status
            if (status == 'not_started') or (status == 'paused'):
                eligible_jobs.append(j)

            elif (status == 'done') or (status == 'crashed'):
                continue

            else:
                print "unknown job status:", status

        #  prune down to max_jobs
        n_jobs = min( len(eligible_jobs), conf.max_jobs )
        eligible_jobs = eligible_jobs[0:n_jobs]

        #step 4: create PBS script of eligible jobs
        pbs_F = pbs_template_wrapper(n_jobs, eligible_jobs)
        print pbs_F

        #step 5: launch allocation

        #step 6: remove old model snapshots (only keep newest snapshot)

        unfinishedJobs = False #for debugging (TODO: remove)

if __name__ == "__main__":
    schedulerLoop()

