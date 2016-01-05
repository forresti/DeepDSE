
#this is to be called by DeepDSE/time_training_runs/time_training_runs.py
# assume are running from an allocated node, not a titan-ext node.

d=$1
n_gpu=$2

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
aprun -n $n_gpu -d 16 $CAFFE_BIN_COMPUTENODE/caffe train -solver=tmp_solver.prototxt  -gpu=0 > time_training_$now.log 2>&1 
cd ..

