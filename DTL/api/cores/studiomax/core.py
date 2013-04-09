import Py3dsMax
from Py3dsMax import mxs

from DTL.api.logger import Logger
from DTL.api import utils as Utils
from DTL.api.cores.external.core import Core

#------------------------------------------------------------
#------------------------------------------------------------
class StudioMaxCore(Core):
    '''Tool Environment Core for 3dsMax'''
    #------------------------------------------------------------
    def __init__(self):
        super(StudioMaxCore, self).__init__()
        self.setEnvironment(Core.CoreEnvironments.Max)
    
    #------------------------------------------------------------
    def setupLogging(self):
        Logger.setupLogger()
