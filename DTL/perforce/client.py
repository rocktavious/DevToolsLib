import sys
import traceback
from functools import partial
from P4 import P4, P4Exception

from DTL.api import Path, Logger, apiUtils
from DTL.gui.widgets import P4LoginWidget

from functools import wraps  # use this to preserve function signatures and docstrings

#------------------------------------------------------------
def requiresP4Conn(func):
    '''Decorator for P4Client functions to require a test of the p4Connection'''
    #------------------------------------------------------------
    @wraps(func)
    def inner(*args, **kwargs):
        args[0]._connect()
        return func(*args, **kwargs)
    return inner

#------------------------------------------------------------
#------------------------------------------------------------
class P4Client(object):
    #------------------------------------------------------------
    def __init__(self, verbose=False):
        apiUtils.synthesize(self, 'p4Conn', None)
        apiUtils.synthesize(self, 'p4Info', {})
        apiUtils.synthesize(self, 'verbose', verbose)
            
    #------------------------------------------------------------
    def _setupConnection(self):
        success, user, password, port, client = P4LoginWidget.getCredentials(loginMsg='P4 Login', credentialsFile=apiUtils.getTempFilepath('p4_login.dat'))
        if not success:
            raise ValueError('Invalid Login Infomation!')
        p4conn = P4()
        p4conn.port = port
        p4conn.user = user
        p4conn.password = password
        p4conn.client = client
        p4conn.connect()
        p4conn.prog = "DTL Perforce Python Tools"
        p4conn.exception_level = 1 # ignore warnings

            
        p4info = p4conn.run("info")[0] # Run "p4 info" (returns a dict)
        if self.verbose() :
            for key, value in p4info.items() :
                print key, '\t', value
        #Test Connection
        if not p4conn.connected() :
            raise P4Exception('Unable to validate connection')
        
        self.setP4Conn(p4conn)
        self.setP4Info(p4info)
    
    #------------------------------------------------------------
    def _connect(self):
        try:
            if self.p4Conn().connected() :
                return
        except AttributeError:
            #If unable to check connected then we don't have a P4 Obj so 
            self._setupConnection()
        except Exception, e:
            raise Exception(e)
        
    #------------------------------------------------------------
    @requiresP4Conn
    def run(self, *args, **kwds):
        return partial(self.p4Conn().run, *args, **kwds)()
    
    #------------------------------------------------------------
    @requiresP4Conn
    def test_connection(self):
        return self.p4Info()

    #------------------------------------------------------------
    @requiresP4Conn
    def getWorkspacePath(self, path):
        return Path(path.replace("//" + self.p4Info()['clientName'],
                                 self.p4Info()['clientRoot']))
    
    #------------------------------------------------------------
    @requiresP4Conn
    def getChangeDescription(self, cl):
        return self.p4Conn().fetch_changelist(cl)
    
    #------------------------------------------------------------
    @requiresP4Conn
    def makeClientSpec(self, name, root, view):
        client_spec = self.p4Conn().fetch_client(name)
        client_spec['Root'] = root
        client_spec['View'] = view
        self.p4Conn().save_client(client_spec)
    
if __name__ == '__main__':
    test_client = P4Client()
    print test_client.test_connection()