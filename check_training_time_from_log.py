from titan_runtime.parse_logs import get_time_per_iter
from titan_runtime.parse_logs import get_latest_log
#import titan_runtime.conf_rt as conf
import os


#ASSUME: we have time_training_<datetime>.log in some of the net_dir subdirectories

if __name__ == "__main__":

  log_fnames = []

  #log_fnames.append('/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_64_64_64_incr_64_64_64_freq_2/train_Mon_2015_12_14__16_07_30.log')
  #log_fnames.append('/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_r_64_64_incr_r_64_64_CEratio_1.000_freq_2/train_Sun_2015_12_20__19_35_20.log')
  #log_fnames.append('/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/FireNet_8_fireLayers_base_r_64_64_incr_r_64_64_CEratio_0.125_freq_2/train_Thu_2015_12_17__21_30_39.log')

  #log_fnames.append('/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/microbenchmark_1gpu/FireNet_8_fireLayers_base_64_64_64_incr_64_64_64_freq_2/train_Tue_2016_01_05__21_21_07.log')
  #log_fnames.append('/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/microbenchmark_1gpu/FireNet_8_fireLayers_base_r_64_64_incr_r_64_64_CEratio_0.125_freq_2/train_Tue_2016_01_05__21_15_36.log')

  net_dir = '/lustre/atlas/scratch/forresti/csc103/dnn_exploration/nets_nov2015_done/'
  for d in os.listdir(net_dir):
    #TODO: possibly replace the following with 'get_latest_log'
    train_dir = net_dir + '/' + d
    for f in os.listdir(train_dir):
      if 'time_training' in f:
        log_fnames.append(train_dir + '/' + f)
  print log_fnames

  for log_fname in log_fnames:
    print log_fname
    time_stats = get_time_per_iter(log_fname)
    #print time_stats
    print '  ', time_stats['mean'], 'sec per iter'
    print '' #newline

