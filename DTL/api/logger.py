import os
import logging
import logging.handlers
import threading
import time

#------------------------------------------------------------
#------------------------------------------------------------
class Logger(type):
    """
    Metaclass for Logging, will add self.logger to the class
    """
    #------------------------------------------------------------
    def __init__(cls, name, bases, attrs):
        super(Logger, cls).__init__(name, bases, attrs)
        cls.logger = logging.getLogger('{0}.{1}'.format(attrs['__module__'], name))


#------------------------------------------------------------
#------------------------------------------------------------
class SafeRotatingFileHandler (logging.handlers.RotatingFileHandler):
    """
    RotatingFileHandler that works even if log file is locked.
    When we try to rename the file it fails until that subprocess complete.
    So, wait for a while before you rotate.
    """
    #------------------------------------------------------------
    def __init__(self, *pargs, **kwargs):
        self._lock = threading.Lock()
        logging.handlers.RotatingFileHandler.__init__(self, *pargs, **kwargs)

    #------------------------------------------------------------
    def emit(self, record):
        with self._lock:
            return logging.handlers.RotatingFileHandler.emit(self, record)

    #------------------------------------------------------------
    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        name = threading.current_thread().name
        #------------------------------------------------------------
        def rename (sfn, dfn):
            for i in range(20):
                if os.path.exists(dfn):
                    os.remove(dfn)
                try:
                    os.rename(sfn, dfn)
                    break
                except:
                    time.sleep(0.5)

        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            fname, ext = os.path.splitext(self.baseFilename)
            for i in range(self.backupCount - 1, 0, -1):
                sfn = "%s.%d%s" % (fname, i, ext)
                dfn = "%s.%d%s" % (fname, i + 1, ext)
                if os.path.exists(sfn):
                    rename (sfn, dfn)
            dfn = "%s.%d%s" % (fname, 1, ext)
            rename (self.baseFilename, dfn)
        self.mode = 'w'
        self.stream = self._open()


def setupLogging():
    formatter = logging.Formatter('[%(levelname)s]%(asctime)s | %(message)s', '%b %d %I:%M:%S %p')
    logfile = os.path.join(os.path.dirname(__file__),'logs','Output.log')
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    #Stream Out
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    #File Out
    kwargs = dict(maxBytes = 1024*1024, backupCount=64, delay=True)
    handler = SafeRotatingFileHandler(logfile, **kwargs)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
setupLogging()

