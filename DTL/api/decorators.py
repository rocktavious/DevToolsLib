import time
from DTL.api.logger import Logger

#------------------------------------------------------------
#------------------------------------------------------------
class SafeCall(object):
    __metaclass__ = Logger
    #------------------------------------------------------------
    def __init__(self, func):
        self.func = func

    #------------------------------------------------------------
    def __get__(self, obj, type=None):
        return self.__class__(self.func.__get__(obj, type))

    #------------------------------------------------------------
    def __call__(self, *a, **kw):
        retval = None
        try:
            self.pre_call(*a, **kw)
            retval = self.func(*a, **kw)
        except:
            self.error(retval, *a, **kw)
        finally:
            try:
                self.post_call(retval, *a, **kw)
            except:
                self.error(retval, *a, **kw)
            return retval

    #------------------------------------------------------------
    def pre_call(self, *a, **kw):
        pass

    #------------------------------------------------------------
    def post_call(self, *a, **kw):
        pass

    #------------------------------------------------------------
    def error(self, retval, *a, **kw):
        self.logger.exception("")


#------------------------------------------------------------
#------------------------------------------------------------
class TimerDecorator(SafeCall):
    #------------------------------------------------------------
    def __init__(self, func):
        super(TimerDecorator, self).__init__(func)
        self._time = None
    
    #------------------------------------------------------------
    def pre_call(self, *a, **kw):
        self._time = time.time()
    
    #------------------------------------------------------------
    def post_call(self, *a, **kw):
        elapsed  = (time.time() - self._time)
        self.logger.info("{0} took {1} seconds".format(self.func.__name__,
                                                       elapsed))


if __name__ == "__main__":
    class TestTime(object):
        @TimerDecorator
        def __init__(self):
            time.sleep(2)
    
    class TestError(object):
        @SafeCall
        def __init__(self):
            1/0
    
    myTime = TestTime()
    myError = TestError()