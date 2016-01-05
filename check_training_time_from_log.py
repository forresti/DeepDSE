from titan_runtime.parse_logs import get_time_per_iter
import titan_runtime.conf_rt as conf
import os

if __name__ == "__main__":

  '''
  #TODO: 100-iteration solver
  cp 100 iteration solver to directory to evaluate
  run 100-iterations solver (for various numbers of GPUs)
  parse results

  '''

  #log_fname = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_64_64_64_incr_64_64_64_freq_2/train_Mon_2015_12_14__16_07_30.log'
  log_fname = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_r_64_64_incr_r_64_64_CEratio_0.125_freq_2'
  time_stats = get_time_per_iter(log_fname)
  print time_stats

