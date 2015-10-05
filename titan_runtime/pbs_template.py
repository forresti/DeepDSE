import conf_rt as conf

#@param job_dicts = [{'path':..., 'snapshot':...}, ...]
# where path is relative to conf.net_dir
def pbs_template(n_jobs, job_dicts):
    n_gpus = sum( [j['n_gpu'] for j in job_dicts] )

    st = """#!/bin/bash
#PBS -A csc103
#PBS -l walltime=2:00:00
#PBS -q batch
#PBS -l gres=atlas1%atlas2"""
    st += "\n#PBS -l nodes=%d" %n_gpus #%n_jobs
    st += '\nCAFFE_ROOT=%s' %conf.caffe_root

    st += '\n\nCAFFE_BIN_COMPUTENODE=%s' %conf.caffe_bin_computenode
    st += '\ncp $CAFFE_ROOT/build/tools/caffe $CAFFE_BIN_COMPUTENODE'

    st += '\n\nCAFFE_LIB_COMPUTENODE=%s' %conf.caffe_lib_computenode
    st += '\ncp $CAFFE_ROOT/build/lib/libcaffe.so $CAFFE_LIB_COMPUTENODE'
    st += '\nLD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MEMBERWORK/csc103/dnn_exploration/forrest_usr_local/lib:$CAFFE_LIB_COMPUTENODE'

    st += '\n\nNETDIR=%s' %conf.net_dir
    st += '\ncd $NETDIR'
    st += '\nnow=`date +%a_%Y_%m_%d__%H_%M_%S`'

    n_jobs = min(n_jobs, len(job_dicts)) # making sure we're not going beyond our allocation
    for j in job_dicts:

        if j['snapshot'] is None:
            snapshot_str = ''
        else:
            snapshot_str = '-snapshot=%s' %j['snapshot']

        st += '\n\ncd %s' %j['path']
        st += '\naprun -n %d -d 16 $CAFFE_BIN_COMPUTENODE/caffe train -solver=solver.prototxt %s -gpu=0 > train_$now.log 2>&1 &' %(j['n_gpu'], snapshot_str)
        st += '\ncd ..'

    st += '\nsleep 2h #otherwise, this script returns immediately'
    return st

if __name__ == "__main__":
    #st = pbs_template(2, ['run1', 'run2'])
    st = pbs_template(2, [{'path':'run1', 'snapshot':'train_iter_25000.solverstate'}, {'path':'run2', 'snapshot':None}])
    print st

