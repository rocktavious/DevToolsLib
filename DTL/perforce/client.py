import os
import sys
import traceback
from functools import partial
from P4 import P4, P4Exception

from DTL.settings import Settings
from DTL.api import Path, apiUtils
from DTL.gui import guiUtils
from DTL.gui.widgets import LoginWidget

from functools import wraps  # use this to preserve function signatures and docstrings

#------------------------------------------------------------
def requiresP4Conn(func):
    '''Decorator for P4Client functions to require a test of the p4Connection'''
    #------------------------------------------------------------
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            args[0]._connect()
            return func(*args, **kwargs)
        except P4Exception:
            for e in args[0].p4Conn().errors:
                print e
        except:
            traceback.print_exc()
    return inner

#------------------------------------------------------------
#------------------------------------------------------------
class P4Client(object):
    #------------------------------------------------------------
    def __init__(self, username=None, password=None, client=None, port=None, verbose=False):
        apiUtils.synthesize(self, 'p4Conn', None)
        apiUtils.synthesize(self, 'p4Info', {})
        apiUtils.synthesize(self, 'verbose', verbose)
        apiUtils.synthesize(self, 'p4User', username or os.getenv('P4USER'))
        apiUtils.synthesize(self, 'p4Password', password or os.getenv('P4PASSWD'))
        apiUtils.synthesize(self, 'p4Client', client or os.getenv('P4CLIENT'))
        apiUtils.synthesize(self, 'p4Port', port or os.getenv('P4PORT'))
    
    #------------------------------------------------------------
    def _setupConnection(self):
        #Validate Credentials
        if self.p4User() is None or self.p4Password() is None:
            success, user, password = LoginWidget.getCredentials(loginMsg='P4 Login',
                                                                 credentialsFile=Settings.getTempPath().join('p4_login.dat'))
            if not success:
                raise ValueError('Invalid Login Infomation!')
            self.setP4User(user)
            self.setP4Password(password)
            #Set the env's for next time
        apiUtils.setEnv('P4USER', self.p4User())
        apiUtils.setEnv('P4PASSWD', self.p4Password())
        
        #Validate Client Workspace
        if self.p4Client() is None:
            success, client = guiUtils.getUserInput(msg='Please Enter P4CLIENT:')
            if not success :
                raise P4Exception('Unable to determine P4CLIENT')
            self.setP4Client(client)
            #Set the env's for next time
        apiUtils.setEnv('P4CLIENT', self.p4Client())
        
        #Validate P4 Port
        if self.p4Port() is None:
            success, port = guiUtils.getUserInput(msg='Please Enter P4PORT:')
            if not success :
                raise P4Exception('Unable to determine P4PORT')
            self.setP4Port(port)
            #Set the env's for next time
        apiUtils.setEnv('P4PORT', self.p4Port())
        

        #Try Connecting
        self.setP4Conn(P4())
        self.p4Conn().user = self.p4User()
        self.p4Conn().password = self.p4Password()
        self.p4Conn().client = self.p4Client()
        self.p4Conn().port = self.p4Port()
        
        self.p4Conn().connect()
        self.p4Conn().prog = "DTL Perforce Python Tools"
        self.p4Conn().exception_level = 1 # ignore warnings

        #Grab p4Info
        p4info = self.p4Conn().run("info")[0] # Run "p4 info" (returns a dict)
        if self.verbose() :
            for key, value in p4info.items() :
                print key, '\t', value
        #Test Connection
        if not self.p4Conn().connected() :
            raise P4Exception('Unable to validate connection')
        
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