from IPython import embed
import threading
from threading import Lock
import subprocess
import shelve

#mutexes for 'shelve' thread safety": georg.io/2014/06/Python-Shelve-Thread-Safety

db_path = 'experiment_db.shelve' #'shelve' db file location
mutex = Lock()

def onExit(idx):
    print "finished subprocess %d. TODO: update training database" %idx

    mutex.acquire()
    db = shelve.open(experiment_shelve)

    # write to db
    db[str(idx)] = 'hello'

    db.close()
    mutex.release()


#thanks: http://stackoverflow.com/questions/2581817/python-subprocess-callback-when-cmd-exits
def popenAndCall(onExit, jobDict):
    """
    Runs the given args in a subprocess.call, and then calls the function
    onExit when the subprocess completes.
    """
    def runInThread(onExit, jobDict):
        #TODO: make sure popenArgs is just a string.
        subprocess.call(jobDict['cmd'], shell=True) #this is supposed wait for subprocess to complete.
        onExit(jobDict['idx'])
        return

    thread = threading.Thread(target=runInThread, args=(onExit, jobDict))
    thread.start()
    # returns immediately after the thread starts
    return thread


if __name__ == "__main__":
    #n_concurrent = 1
    n_concurrent = 5

    for i in xrange(0, n_concurrent):
        cmd = 'sleep 2'
        #cmd = '~/__caffe_allreduce/build/tools/caffe'
        jobDict = {'cmd': cmd, 'idx':i}
        t = popenAndCall(onExit, jobDict)
        #TODO: look at what 't' can do
