import logging
import logging.handlers
import os
import threading
import time

from . import Settings, Enum


LogTypes = Enum('Info','Testing','Timing','Warning','Errors')

#------------------------------------------------------------
#------------------------------------------------------------
class Logger(object):
    _log_dir = None
    _log_types = ['[Info]','[Testing]','[Timing]','[Warning]','[Errors]']
    
    _instance = None
    #------------------------------------------------------------
    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance  
    
    #------------------------------------------------------------
    def __init__(self):
        super(Logger, self).__init__()
        if not Settings.ENABLERLOGGER :
            return
        self._log_dir = Settings._appdata.new_path_join('Log')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        """
        # stream handler for application output
        filter = Multifilter([LOGGER_ERROR])
        formatter = logging.Formatter('%(message)s')
        handler = logging.StreamHandler()
        handler.setLevel(0)# allow all messages
        handler.setFormatter(formatter)
        handler.addFilter(filter)
        logger.addHandler(handler)
        """
    
        # setup file handlers
        logger.addHandler(self._make_file_handler('verbose.log',
                                                  self._log_types))
        logger.addHandler(self._make_file_handler('errors.log',
                                                  [self._log_types[-2],
                                                   self._log_types[-1]]))
        logger.addHandler(self._make_file_handler('timing.log',
                                                  [self._log_types[2]]))
    
    #------------------------------------------------------------
    def _make_file_handler(self, filename, loggers):
        logFile = self._log_dir.new_path_join(filename)
        
        formatter = logging.Formatter('%(asctime)s %(name)s %(message)s', Settings.TIMEFORMAT)
        kwargs = dict(maxBytes = 1024*1024, backupCount=64, delay=True)
        handler = SafeRotatingFileHandler(logFile.path, **kwargs)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        filter = Multifilter(loggers)
        for logger in loggers:
            filter.setLevel(logger, logging.DEBUG)
        handler.addFilter(filter)
    
        return handler
    
    #------------------------------------------------------------
    def log(self, *a):
        '''This first arg can be a number for the log type otherise
        we compile all the args into a single string'''
        if not Settings.ENABLERLOGGER :
            return
        try:
            log_type = self._log_types[a[0]]
            msg_list = a[1:]
        except:
            log_type = self._log_types[0]
            msg_list = a
        
        logger = logging.getLogger(log_type)
        
        msg = ''
        for item in msg_list :
            msg += str(item) + ' '
        if log_type is self._log_types[-1] :
            msg += '\n'
            logger.exception(msg)
        else:
            logger.info(msg)

#------------------------------------------------------------
#------------------------------------------------------------
class Multifilter(object):
    """
    Replacement for logging.Filter that allows multiple loggers.

    Multifilter contains a set of subfilters; if any of those filters want the
    record, then the record will be logged.
    """
    #------------------------------------------------------------
    class LevelFilter(logging.Filter):
        """
        Logging Filter which allows filtering on level as well as logger name.
        """
        #------------------------------------------------------------
        def __init__(self, *pargs, **kwargs):
            self._level = logging.INFO
            logging.Filter.__init__(self, *pargs, **kwargs)
        
        #------------------------------------------------------------
        def filter(self, record):
            return (record.levelno >= self._level and
                logging.Filter.filter(self, record))
        
        #------------------------------------------------------------
        def setLevel(self, level):
            self._level = logging._checkLevel(level)

    #------------------------------------------------------------
    def __init__(self, loggers):
        """
        Initialize Multifilter with a list of loggers.

        Args:
            loggers: an iterable of strings with the names of loggers that will
                pass the Multifilter.
        """
        self._loggers = {}
        for l in loggers:
            self.enable(l)

    #------------------------------------------------------------
    def enable(self, loggerName):
        """
        Allow messages from loggers with the given name to pass.

        Args:
            loggerName: string containing the name of the logger
        """
        self._loggers[loggerName] = Multifilter.LevelFilter(loggerName)

    #------------------------------------------------------------
    def disable(self, loggerNames):
        """
        Prevent messages from loggers with the given name from passing.

        Args:
            loggerName: string containing the name of the logger
        """
        try: del self._loggers[loggerName]
        except KeyError: pass

    #------------------------------------------------------------
    def filter(self, record):
        """
        Determine if the specified record is to be logged.

        Models the logging.Filter.record() function.  The record passes if ANY
        of the Multifilters subFilters want the record.

        Args:
            record: record to check

        Returns:
            whether to log the given record.
        """
        return any(f.filter(record) for f in self._loggers.itervalues())

    #------------------------------------------------------------
    def setLevel(self, loggerName, level):
        """
        Set a logger to a level.

        Args:
            loggerName: name of the logger to set
            level: logging level to set it to

        Returns:
            None
        """
        try: self._loggers[loggerName].setLevel(level)
        except KeyError: pass


#------------------------------------------------------------
#------------------------------------------------------------
class SafeRotatingFileHandler (logging.handlers.RotatingFileHandler):
    """
    RotatingFileHandler that works even if log file is locked.

    The subprocess that is spawned in builder.py inherits all open file
    handles, including the log file.  When we try to rename the file it
    fails until that subprocess complete.  So, wait for a while.
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

