import conf_rt as conf

def pbs_template(n_jobs, job_dirs):
    st = """#!/bin/bash
#PBS -A csc103
#PBS -l walltime=2:00:00
#PBS -q batch
#PBS -l gres=atlas1%atlas2"""
    st += "\n#PBS -l nodes=%d" %n_jobs

    st += """\n\n#compute nodes do NOT look at ~/.bashrc
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MEMBERWORK/csc103/dnn_exploration/forrest_usr_local/lib"""
    st += '\nCAFFE_ROOT=%s' %conf.caffe_root
    st += '\nCAFFE_BIN_COMPUTENODE=%s' %conf.caffe_bin_computenode
    st += '\ncp $CAFFE_ROOT/build/tools/caffe $CAFFE_BIN_COMPUTENODE'
    st += '\nNETDIR=%s' %conf.net_dir
    st += '\ncd $NETDIR'
    st += '\nnow=`date +%a_%Y_%m_%d__%H_%M_%S`'

    n_jobs = min(n_jobs, len(job_dirs)) # making sure we're not going beyond our allocation
    for j in job_dirs:
        st += '\n\ncd %s' %j
        st += '\naprun -n 1 -d 16 $CAFFE_ROOT/build/tools/caffe $CAFFE_BIN_COMPUTENODE/caffe train -solver=solver.prototxt -gpu=0 > train_$now.log 2>&1 &'
        st += '\ncd ..'
    return st

if __name__ == "__main__":
    st = pbs_template(2, ['run1', 'run2'])
    print st

