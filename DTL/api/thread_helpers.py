import threading
import Queue


#------------------------------------------------------------
#------------------------------------------------------------
class DaemonThread(threading.Thread):
    """
    Thread class that is a daemon by default.  (Normal threading.Thread
    objects are not daemons by default.)
    """
    #------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True