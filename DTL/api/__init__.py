import sys

#Bases
from DTL.api.exceptions import InternalError, DeprecatedError
from DTL.api.bases import BaseStruct

#Structures
from DTL.api.enum import Enum
from DTL.api.version import Version
from DTL.api.path import Path
from DTL.api.dotifydict import DotifyDict
from DTL.api.document import Document

#I don't currently like this implementation but i'm not sure how to handle utils and other things like the functions below
from DTL.api import utils as Utils

#Objects
from DTL.api.logger import Logger
from DTL.api.importlib import ImportModule
from DTL.api.rollbackimporter import RollbackImporter
from DTL.api.commandticker import CommandTicker
from DTL.api.jsondocument import JsonDocument
from DTL.api.xmldocument import XmlDocument
from DTL.api.stopwatch import Stopwatch
from DTL.api.decorators import SafeCall, TimerDecorator
from DTL.api.threadlib import Process, ThreadedProcess, ThreadedProcessWithPrompt


###
# Things that need to be fixed
###
#from DTL.api.daemon import Daemon, DaemonThread
#from DTL.api.mailer import Mailer
#if sys.platform == 'win32' :
#    from DTL.api import envUtils

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
        return widget
        
#------------------------------------------------------------
def CheckVersion(matching):
    from DTL import __version__
    
    if __version__ != matching :
        msg = 'You currently have version {0} of Dev Tools.  Please update to at least version {1}'.format(__version__, matching)
        try:
            from DTL.gui import utils as guiUtils
            guiUtils.notifyUser(msg)
            sys.exit(1)
        except:
            raise ValueError(msg)
        
        