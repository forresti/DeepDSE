import threading
import subprocess


def onExit():
    print "finished subprocesses. TODO: update training database"

#thanks: http://stackoverflow.com/questions/2581817/python-subprocess-callback-when-cmd-exits
def popenAndCall(onExit, popenArgs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that 
    would give to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs):
        #proc = subprocess.Popen(*popenArgs, shell=False)
        #proc.wait()
        subprocess.call(popenArgs, shell=True) #TODO: make sure popenArgs is just a string.
        onExit()
        return
    thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    thread.start()
    # returns immediately after the thread starts
    return thread


if __name__ == "__main__":
    #subprocess.Popen("sleep 10", shell=True) #this works. (doesn't have callback, of course.)

    popenAndCall(onExit, "sleep 10") #error: bufsize must be an integer


