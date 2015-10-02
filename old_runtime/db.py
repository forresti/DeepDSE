from IPython import embed
import shelve
import os
import conf_rt #config file for user to edit

## NOTHING IN THIS FILE IS THREADSAFE.

#valid statuses (should make these enums):
# 'not-started', 'pruned', 'running', 'done'

# possibly add these statuses:
# 'too-slow', 

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

#TODO: implement refreshDB(), to run after a Titan job is killed, and the next one starts.
# do NOT run refreshDB while caffe is actually running, because refreshDB will 
#    change all 'running' states to 'paused'
'''
def refreshDB(db_path, net_dir):
    db = shelve.open(db_path)
    for k in db.keys():
        net = db[k]
        if net['status'] == 'running':
            #Titan's scheduler killed the meta-job, and we didn't get a chance to refresh the DB.
            net['status'] = 'paused'
            log_fname = get_latest_log(net_dir + '/' + k) #TODO: use path.join
            accuracy_dict = get_current_accuracy(net_dir + '/' + log_fname)
            net['accuracy'] = accuracy_dict['accuracy']
            net['iter'] = accuracy_dict['iter']
            db[k] = net #TODO: figure out of I actually need to do this (is 'net' a deepcopy or not?) 

'''

if __name__ == "__main__":
    db_path = conf_rt.db_path
    net_dir = conf_rt.net_dir
    initDB(db_path, net_dir)

