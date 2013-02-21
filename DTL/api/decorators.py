from . import Logger

#------------------------------------------------------------
#------------------------------------------------------------
class SafeCall(object):
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
        Logger.instance().log(-1)

        