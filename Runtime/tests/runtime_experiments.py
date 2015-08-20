import threading
import subprocess


def onExit(idx):
    print "finished subprocess %d. TODO: update training database" %idx

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
    for i in xrange(0,3):
        jobDict = {'cmd': 'sleep 10', 'idx':i}
        popenAndCall(onExit, jobDict)


