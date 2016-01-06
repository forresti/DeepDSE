#!/bin/bash
#PBS -A csc103
#PBS -q batch
#PBS -e /dev/null
#PBS -o /dev/null
#PBS -l gres=atlas1%atlas2
#PBS -l walltime=00:05:00
#PBS -l nodes=512
#this is to be called by DeepDSE/time_training_runs/time_training_runs.py
# assume are running from an allocated node, not a titan-ext node.

d=/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_r_64_64_incr_r_64_64_CEratio_0.125_freq_2
#d=/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_64_64_64_incr_64_64_64_freq_2

#pbs doesn't like stdin
#d=$1
n_gpu=512

CAFFE_ROOT=/ccs/home/forresti/FireCaffe_batchreduce
CAFFE_BIN_COMPUTENODE=/lustre/atlas/scratch/forresti/csc103/dnn_exploration/bin
cp $CAFFE_ROOT/build/tools/caffe $CAFFE_BIN_COMPUTENODE
CAFFE_LIB_COMPUTENODE=/lustre/atlas/scratch/forresti/csc103/dnn_exploration/lib
cp $CAFFE_ROOT/build/lib/libcaffe.so $CAFFE_LIB_COMPUTENODE
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MEMBERWORK/csc103/dnn_exploration/forrest_usr_local/lib:$CAFFE_LIB_COMPUTENODE

now=`date +%a_%Y_%m_%d__%H_%M_%S`
export MPICH_ALLREDUCE_NO_SMP=1
export APRUN_BALANCED_INJECTION=80

cd $d
 #just run 'till the job gets killed. (then, we'll parse the log file in the interactive shell.)
aprun -n $n_gpu -d 16 $CAFFE_BIN_COMPUTENODE/caffe train -solver=solver.prototxt  -gpu=0 > time_training_${n_gpu}_gpu_${APRUN_BALANCED_INJECTION}_APRUN_BALANCED_INJECTION_$now.log 2>&1 
cd ..

