from titan_runtime.parse_logs import get_latest_log
from titan_runtime.parse_logs import get_time_per_iter
import titan_runtime.conf_rt as conf
import os

###  GLOBALS (may move to a conf file) ###
solver_rel_path = 'tmp_solver.prototxt'
log_prefix = 'time_training'
net_dir = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done' #TODO: perhaps make a dedicated directory for stuff I want to time?


#essentially a 'normal' solver, but with very few iterations ... just to do a quick training run
def gen_solver_prototxt(train_dir, n_gpu):
  #maxiter = n_gpu*10
  max_iter = 100
  out_st = '#temporary solver file for TIMING the training of a DNN\n'
  out_st += 'max_iter: %d\n' %max_iter
  #most the following is boilderplate (only a couple of these fields affect speed) 

  out_st += '\
display: 1 \n\
net: "trainval.prototxt" \n\
snapshot_prefix: "train" \n\
solver_mode: GPU \n\
\n#the following is not relevant to our timing runs\n\
test_iter: 49 \n\
test_interval: 1000 \n\
base_lr: 0.08 \n\
lr_policy: "poly" \n\
power: 0.5 \n\
momentum: 0.9 \n\
weight_decay: 0.0002 \n\
snapshot: 1000 \n\
random_seed: 42 \n\
test_initialization: false \n\
average_loss: 40\n'

  f = open(train_dir + '/' + solver_rel_path, 'w')
  f.write(out_st)
  f.close()

if __name__ == "__main__":

  '''
  #TODO: 100-iteration solver
  cp 100 iteration solver to directory to evaluate
  run 100-iterations solver (for various numbers of GPUs)
  parse results

  '''

  #train_dir = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_r_64_64_incr_r_64_64_CEratio_0.125_freq_2'
  train_dir = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_64_64_64_incr_64_64_64_freq_2/'
  n_gpu = 32
  gen_solver_prototxt(train_dir, n_gpu)

  training_cmd = './do_training.sh %s %d' %(train_dir, n_gpu)
  os.system(training_cmd)

  #TODO: parse results.
  latest_log = get_latest_log(train_dir, for_timing=True)
  time_stats = get_time_per_iter(latest_log)


  '''
  log_fname = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_64_64_64_incr_64_64_64_freq_2/train_Mon_2015_12_14__16_07_30.log'

  time_stats = get_time_per_iter(log_fname)
  print time_stats
  '''
