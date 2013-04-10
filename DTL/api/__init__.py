import sys

from .exceptions import InternalError
from .enum import Enum
from .version import Version
from .path import Path
from .logger import Logger
from .rollbackimporter import RollbackImporter
from .commandticker import CommandTicker
from .jsondocument import JsonDocument
from .xmldocument import XmlDocument
from . import utils as Utils
if sys.platform == 'win32' :
    from . import envUtils

from .stopwatch import Stopwatch
from .decorators import SafeCall, TimerDecorator
#from .daemon import Daemon, DaemonThread
#from .mailer import Mailer
from .cores import Core
#from .tool import Tool


#------------------------------------------------------------
def Start():
    if Core.instance().app :
        Core.instance().app.exec_()

#------------------------------------------------------------
def Run(modulename):
    import sys
    tool_mod = sys.modules.get(modulename, None)
    if tool_mod is None :
        __import__(modulename)
        tool_mod = sys.modules.get(modulename, None)
    else:
        tool_mod.mainUI.instance().close()
        Utils.quickReload(modulename)
        tool_mod = sys.modules.get(modulename, None)
    
    Launch(tool_mod.mainUI.instance)

#------------------------------------------------------------
def Launch(ctor, modal=False):
    """
    This method is used to create an instance of a widget (dialog/window) to 
    be run inside the blurdev system.  Using this function call, blurdev will 
    determine what the application is and how the window should be 
    instantiated, this way if a tool is run as a standalone, a new 
    application instance will be created, otherwise it will run on top 
    of a currently running application.

    :param ctor: callable object that will return a widget instance, usually
    			 a :class:`QWidget` or :class:`QDialog` or a function that
    			 returns an instance of one.
    :param modal: If True, widget will be created as a modal widget (ie. blocks
    			  access to calling gui elements).
    """
    from PyQt4.QtGui import QWizard

    # always run wizards modally
    try:
        modal = issubclass(ctor, QWizard)
    except:
        pass

    # create the output instance from the class
    widget = ctor(None)

    # check to see if the tool is running modally and return the result
    if modal:
        return widget.exec_()
    else:
        widget.show()
        # run the application if this item controls it and it hasnt been run before
        Start()
        return widget


#------------------------------------------------------------
def Stop():
    if Core.instance().app :
        Core.instance().app.closeAllWindows()
        Core.instance().app.quit()