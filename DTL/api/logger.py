import os
import logging
import logging.handlers
import sqlite3
import threading
import time

from DTL import __pkgname__, __appdata__
from DTL.api.path import Path

#------------------------------------------------------------
#------------------------------------------------------------
class Logger(object):
    LOGFILE = os.path.join(__appdata__,'logs',__pkgname__ + '.log')
    DATABASEFILE = os.path.join(__appdata__,'logs',__pkgname__ + '.db')
    
    VERBOSE = logging.Formatter('[%(levelname)s]%(asctime)s | [%(name)s][%(module)s][%(funcName)s][line:%(lineno)s] \n\t %(message)s', '%b %d %I:%M:%S %p')
    SIMPLE = logging.Formatter('[%(levelname)s] %(message)s')
    
    #------------------------------------------------------------
    @staticmethod
    def getMetaClass():
        return LoggerMetaclass
    
    #------------------------------------------------------------
    @staticmethod
    def getLogger():
        return logging.getLogger(__pkgname__)
    
    #------------------------------------------------------------
    @staticmethod
    def getSubLogger(name):
        return logging.getLogger('{0}.{1}'.format(__pkgname__, name))
    
    #------------------------------------------------------------
    @staticmethod
    def addHandler(handler):
        logger = Logger.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    
    #------------------------------------------------------------
    @staticmethod
    def setupFileLogger(filepath=None, level=None, formatter=None):
        filepath = filepath or Logger.LOGFILE
        level = level or logging.INFO
        formatter = formatter or Logger.VERBOSE
        
        kwargs = dict(maxBytes = 1024*1024, backupCount=64, delay=True)
        handler = SafeRotatingFileHandler(filepath, **kwargs)
        handler.setFormatter(formatter)
        handler.setLevel(level)
    
    #------------------------------------------------------------
    @staticmethod
    def setupDatabaseLogger(filepath=None, level=None):
        filepath = filepath or Logger.LOGFILE
        level = level or logging.WARNING
        
        handler = SQLiteHandler(filepath)
        handler.setLevel(level)
        Logger.addHandler(handler)
    
    #------------------------------------------------------------
    @staticmethod
    def setupStreamLogger(level=None, formatter=None):
        level = level or logging.INFO
        formatter = formatter or Logger.SIMPLE
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(level)
        Logger.addHandler(handler) 


#------------------------------------------------------------
#------------------------------------------------------------
class LoggerMetaclass(type):
    """
    Metaclass for Logging, will add self.logger to the class
    """
    #------------------------------------------------------------
    def __init__(cls, name, bases, attrs):
        super(LoggerMetaclass, cls).__init__(name, bases, attrs)
        cls.logger = Logger.getLogger()


#------------------------------------------------------------
#------------------------------------------------------------
class SQLiteHandler(logging.Handler):
    """
    Logging handler for SQLite.

    Based on Vinay Sajip's DBHandler class (http://www.red-dove.com/python_logging.html)

    This version sacrifices performance for thread-safety:
    Instead of using a persistent cursor, we open/close connections for each entry.

    AFAIK this is necessary in multi-threaded applications, 
    because SQLite doesn't allow access to objects across threads.
    """

    initial_sql = """CREATE TABLE IF NOT EXISTS log(
                        Created text,
                        Name text,
                        LogLevel int,
                        LogLevelName text,    
                        Message text,
                        Args text,
                        Module text,
                        FuncName text,
                        LineNo int,
                        Exception text,
                        Process int,
                        Thread text,
                        ThreadName text
                   )"""

    insertion_sql = """INSERT INTO log(
                        Created,
                        Name,
                        LogLevel,
                        LogLevelName,
                        Message,
                        Args,
                        Module,
                        FuncName,
                        LineNo,
                        Exception,
                        Process,
                        Thread,
                        ThreadName
                   )
                   VALUES (
                        '%(dbtime)s',
                        '%(name)s',
                        %(levelno)d,
                        '%(levelname)s',
                        '%(msg)s',
                        '%(args)s',
                        '%(module)s',
                        '%(funcName)s',
                        %(lineno)d,
                        '%(exc_text)s',
                        %(process)d,
                        '%(thread)s',
                        '%(threadName)s'
                   );
                   """

    #------------------------------------------------------------
    def __init__(self, db=None):

        logging.Handler.__init__(self)
        if db is None:
            self.db = ':memory:Temp.db'
        else:
            self.db = Path(db)
            self.db.makedirs()
            self.db = self.db.path
        # Create table if needed:
        conn = sqlite3.connect(self.db)
        conn.execute(SQLiteHandler.initial_sql)
        conn.commit()

    #------------------------------------------------------------
    def formatDBTime(self, record):
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

    #------------------------------------------------------------
    def emit(self, record):

        # Use default formatting:
        self.format(record)
        # Set the database time up:
        self.formatDBTime(record)
        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ""
        # Insert log record:
        sql = SQLiteHandler.insertion_sql % record.__dict__
        conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()



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
