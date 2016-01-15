from titan_runtime.parse_logs import get_latest_log
from titan_runtime.parse_logs import get_current_accuracy_googlenet
import titan_runtime.conf_rt as conf
import os

if __name__ == "__main__":

  jobs = os.listdir(conf.net_dir)
  jobs = [j for j in jobs if 'googlenet' in j]
  jobs = sorted(jobs)
  for logdir in jobs:
    logF = get_latest_log(conf.net_dir + '/' + logdir)
    if logF is None:
      continue
    accuracy_dict = get_current_accuracy_googlenet(logF)
    print '  net: %s, accuracy: %0.1f, at iter %d' %(logdir, accuracy_dict['accuracy']*100, accuracy_dict['iter'])

