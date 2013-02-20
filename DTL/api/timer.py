import time
from . import Logger, SafeCall

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
        Logger().log(2,
                     self.func.__name__,
                     elapsed)
