from titan_runtime.parse_logs import get_latest_log
from titan_runtime.parse_logs import get_current_accuracy
import titan_runtime.conf_rt as conf
import os

if __name__ == "__main__":

  jobs = os.listdir(conf.net_dir)
  jobs = [j for j in jobs if 'NiN' in j]
  jobs = sorted(jobs)
  for logdir in jobs:
    logF = get_latest_log(conf.net_dir + '/' + logdir)
    accuracy_dict = get_current_accuracy(logF)
    print '  net: %s, accuracy: %f, at iter %d' %(logdir, accuracy_dict['accuracy'], accuracy_dict['iter'])
