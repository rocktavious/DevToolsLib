import sys
import traceback
from functools import partial
from P4 import P4, P4Exception

from DTL.api import Path, Logger

P4CONN = None
P4CLIENT = ''
P4INFO = dict()

def P4SetClient(client):
    global P4CLIENT
    P4CLIENT = client

#------------------------------------------------------------
#------------------------------------------------------------
class P4Wrapper(object):
    __metaclass__ = Logger.getMetaClass()
    '''Decorator to help with safely calling a function and logging usage and errors'''
    #------------------------------------------------------------
    def __init__(self,function, client=None):
        self.function = function
        if client:
            global P4CLIENT
            P4CLIENT = client

    #------------------------------------------------------------
    def __get__(self, obj, type=None):
        return self.__class__(self.function.__get__(obj, type))

    #------------------------------------------------------------
    def __call__(self, *args, **kwds):
        try:
            self.connect()
            return self.function(*args, **kwds)
        except Exception, e:
            #This gets us the traceback from inside the function call
            etype, value, tb = sys.exc_info()
            excData = traceback.format_exception(etype, value, tb)
            self.logger.exception(''.join(excData))

    #------------------------------------------------------------
    def connect(self):
        global P4CONN, P4INFO
        try:
            if P4CONN.connected() :
                return
        except AttributeError: #If unable to check connected then we don't have a P4 Obj
            pass
        except Exception, e:
            raise Exception(e)
        
        P4CONN = P4()
        P4CONN.client = P4CLIENT
        
        
        P4CONN.connect()
        P4CONN.prog = "DTL Perforce Python Tools"
        P4CONN.exception_level = 1 # ignore warnings

            
        P4INFO = P4CONN.run("info")[0] # Run "p4 info" (returns a dict)
        for key, value in P4INFO.items() :
            print key, '\t', value
        #Test Connection
        if not P4CONN.connected() :
            raise P4Exception('Unable to validate connection')

#------------------------------------------------------------
@P4Wrapper
def P4Run(*args, **kwargs):
    return partial(P4CONN.run,*args,**kwargs)()

#------------------------------------------------------------
@P4Wrapper
def P4GetWorkspaceRoot():
    return P4INFO['clientRoot']

#------------------------------------------------------------
@P4Wrapper
def P4GetClientRoot():
    return "//" + P4INFO['clientName']

#------------------------------------------------------------
def P4GetWorkspacePath(path):
    P4CONN.fetch_changelists
    return Path(path.replace(P4GetClientRoot(),
                             P4GetWorkspaceRoot()))

#------------------------------------------------------------
@P4Wrapper
def P4GetChangeDescription(cl):
    return P4CONN.fetch_changelist(cl)