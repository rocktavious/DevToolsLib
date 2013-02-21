import os.path
from PyQt4 import QtCore, QtGui, uic

from . import Core, Utils


#------------------------------------------------------------
#------------------------------------------------------------
class Tool(object):  
    #------------------------------------------------------------
    def init(self):
        self.ui_file = None
        self.onInit()
        if self.ui_file :
            if os.path.exists(self.ui_file):
                self = uic.loadUi(self.ui_file, self)
            else:
                raise ValueError('Ui Files does not exist: %s' % self.ui_file)
        self.onFinalize()
        Core.instance().registerTool(self)
        
    #------------------------------------------------------------
    def _saveSettings(self):
        settings = Utils.getAppSettings()
        settings.beginGroup(self.objectName())        
        
        settings.endGroup()
    
    #------------------------------------------------------------
    def _readSettings(self):
        settings = Utils.getAppSettings()
        settings.beginGroup(self.objectName())     
        
        settings.endGroup()
        
    #------------------------------------------------------------
    def isModal(self):
        return False
    
    #------------------------------------------------------------
    def onInit(self):
        pass
    
    #------------------------------------------------------------
    def onFinalize(self):
        pass
        

class MainTool(QtGui.QMainWindow, Tool):
    """Tool for ui files the inherit from QMainWindow"""
    #------------------------------------------------------------
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__()
        self.init()
        
class SubTool(QtGui.QWidget, Tool):
    """Tool for ui files that inherit from QWidget"""
    #------------------------------------------------------------
    def __init__(self, parent=None):
        super(QtGui.QWidget, self).__init__(parent=parent)
        self.init()
        
        


    
