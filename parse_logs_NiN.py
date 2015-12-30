from titan_runtime.parse_logs import get_latest_log
from titan_runtime.parse_logs import get_current_accuracy
import titan_runtime.conf_rt as conf
import os

if __name__ == "__main__":

  jobs = os.listdir(conf.net_dir)
  #jobs = [j for j in jobs if 'NiN' in j]
  jobs = [j for j in jobs if not j.startswith('googlenet')]
  jobs = sorted(jobs)
  for logdir in jobs:
    logF = get_latest_log(conf.net_dir + '/' + logdir)
    if logF is None:
      continue
    accuracy_dict = get_current_accuracy(logF)
    if accuracy_dict is not 'error':
      if 'accuracy_top5' in accuracy_dict.keys():
        print '  net: %s, top1: %f, top5: %f, at iter %d' %(logdir, accuracy_dict['accuracy'], accuracy_dict['accuracy_top5'], accuracy_dict['iter'])
      else:
        print '  net: %s, top1: %f, at iter %d' %(logdir, accuracy_dict['accuracy'], accuracy_dict['iter'])
