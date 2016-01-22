from titan_runtime.parse_logs import get_latest_log
from titan_runtime.parse_logs import get_current_accuracy
import titan_runtime.conf_rt as conf
import os

if __name__ == "__main__":

  jobs = os.listdir(conf.net_dir)
  #jobs = [j for j in jobs if 'NiN' in j]
  #jobs = [j for j in jobs if not j.startswith('googlenet')]
  jobs = [j for j in jobs if not 'googlenet' in j]
  jobs = sorted(jobs)
  for logdir in jobs:
    logF = get_latest_log(conf.net_dir + '/' + logdir)
    if logF is None:
      continue
    accuracy_dict = get_current_accuracy(logF)
    if accuracy_dict is not 'error':
      if 'accuracy_top5' in accuracy_dict.keys():
        print '  net: %s, top1: %0.1f, top5: %0.1f, at iter %d' %(logdir, accuracy_dict['accuracy']*100, accuracy_dict['accuracy_top5']*100, accuracy_dict['iter'])
      else:
        print '  net: %s, top1: %0.1f, at iter %d' %(logdir, accuracy_dict['accuracy']*100, accuracy_dict['iter'])
