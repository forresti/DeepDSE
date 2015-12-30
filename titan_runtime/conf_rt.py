
#cachedir=#TODO
#db_path = cachedir + '/experiment_db.shelve'
#net_dir = cachedir + '/fake_nets'
#db_path = 'experiment_db.shelve'

#where are the nets to train?
#net_dir = 'tests/fake_nets'
#net_dir = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_batchsize_sweep'
net_dir = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015'
#net_dir = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_debug_batchreduce'

#titan user ID (for tracking the PBS scheduling)
uname = 'forresti'
#uname = 'worley'

caffe_root = '/ccs/home/forresti/FireCaffe_batchreduce'
caffe_bin_computenode = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/bin'
caffe_lib_computenode = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/lib'
#max_jobs = 1000
max_jobs = 3

walltime=2

