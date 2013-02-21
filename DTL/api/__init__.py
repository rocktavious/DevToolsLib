from .exceptions import InternalError
from .enum import Enum
from . import constants as Constants
from .version import Version
from .path import Path
from .jsondocument import JsonDocument
from .settings import Settings
from .logger import Logger
from .decorators import SafeCall
from .thread_helpers import DaemonThread
from .mailer import Mailer
from .timer import TimerDecorator
from . import utils as Utils
from .cores import Core
from .tool import Tool

_appHasExec = False
_app = Core.instance().init()


#------------------------------------------------------------
def Start():
    global _appHasExec, _app
    
    if _app and not _appHasExec :
        #print "QT App Started!"
        _appHasExec = True
        Core.instance().runTools()
        _app.exec_()
        #print "QT App Finished!"
        
#------------------------------------------------------------
def Stop(self):
    global _app
    
    if _app and _appHasExec :
        _app.closeAllWindows()
        _app.quit()