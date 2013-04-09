import time
from DTL.api.stopwatch import Stopwatch
from DTL.api.logger import Logger

#------------------------------------------------------------
#------------------------------------------------------------
class SafeCall(object):
    __metaclass__ = Logger.getMetaClass()
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
        self._stopwatch = None

    #------------------------------------------------------------
    def pre_call(self, *a, **kw):
        self._stopwatch = Stopwatch(self.func.__name__)

    #------------------------------------------------------------
    def post_call(self, *a, **kw):
        self._stopwatch.stop()

## {{{ http://code.activestate.com/recipes/577817/ (r1)
"""
A profiler decorator.

Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
License: MIT
"""
try:
    import cProfile
    import tempfile
    import pstats
    def profile(sort='cumulative', lines=50, strip_dirs=False, fileName=r'c:\temp\profile.profile'):
        """A decorator which profiles a callable. This uses cProfile which is not in Python2.4.
        Example usage:

        >>> @profile
        	def factorial(n):
        		n = abs(int(n))
        		if n < 1:
        				n = 1
        		x = 1
        		for i in range(1, n + 1):
        				x = i * x
        		return x
        ...
        >>> factorial(5)
        Thu Jul 15 20:58:21 2010    c:\temp\profile.profile

        		 4 function calls in 0.000 CPU seconds

           Ordered by: internal time, call count

        	ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        		1    0.000    0.000    0.000    0.000 profiler.py:120(factorial)
        		1    0.000    0.000    0.000    0.000 {range}
        		1    0.000    0.000    0.000    0.000 {abs}

        120
        >>>
        """
        def outer(fun):
            def inner(*args, **kwargs):
                prof = cProfile.Profile()
                ret = prof.runcall(fun, *args, **kwargs)

                prof.dump_stats(fileName)
                stats = pstats.Stats(fileName)
                if strip_dirs:
                    stats.strip_dirs()
                if isinstance(sort, (tuple, list)):
                    stats.sort_stats(*sort)
                else:
                    stats.sort_stats(sort)
                stats.print_stats(lines)
                return ret
            return inner

        # in case this is defined as "@profile" instead of "@profile()"
        if hasattr(sort, '__call__'):
            fun = sort
            sort = 'cumulative'
            outer = outer(fun)
        return outer
    ## end of http://code.activestate.com/recipes/577817/ }}}
except ImportError:
    def profile(sort='cumulative', lines=50, strip_dirs=False, fileName=r'c:\temp\profile.profile'):
        def outer(fun):
            def inner(*args, **kwargs):
                print 'cProfile is unavailable in this version of python. Use Python 2.5 or later.'
                return fun(*args, **kwargs)
            return inner
        # in case this is defined as "@profile" instead of "@profile()"
        if hasattr(sort, '__call__'):
            fun = sort
            sort = 'cumulative'
            outer = outer(fun)
        return outer


if __name__ == "__main__":
    @TimerDecorator
    def TestTime():
        time.sleep(2)

    @SafeCall
    def TestError():
        1/0

    myTime = TestTime()
    myError = TestError()