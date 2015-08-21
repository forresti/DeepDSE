from IPython import embed
import shelve
import os
import conf_rt #config file for user to edit


#valid statuses (should make these enums):
# 'not-started', 'pruned', 'running', 'done'

# possibly add these statuses:
# 'too-slow', 

## nothing in this file is threadsafe.
def initDB(db_path, net_dir):
    db = shelve.open(db_path)
    for net_name in os.listdir(net_dir):
        net = dict()
        net['status'] = 'not-started'
        net['accuracy'] = 0
        net['iter'] = 0
        net['batchsize'] = None #stub for now
        net['epochs'] = None #stub for now
        net['dataset'] = 'imagenet-1k' #TODO: Sports-1M
        net['experimentGroup'] = 'warmup' #TODO lowParams
        db[net_name] = net 

    db.close()
 
if __name__ == "__main__":
    db_path = conf_rt.db_path
    net_dir = conf_rt.net_dir
    initDB(db_path, net_dir)

