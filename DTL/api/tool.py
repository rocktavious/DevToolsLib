from PyQt4 import QtCore, QtGui, uic

from . import Path, Core, Utils


#------------------------------------------------------------
#------------------------------------------------------------
class Tool(object):
    
    #------------------------------------------------------------
    def init(self, register=True):
        self.ui_file = None
        self.onInit()
        self.ui_file = Path(self.ui_file)
        if self.ui_file.isEmpty :
            raise Exception('No UI File was specified in onInit()')
        if not self.ui_file.exists :
            raise ValueError('Ui Files does not exist: %s' % self.ui_file.path)
        
        self = uic.loadUi(self.ui_file.path, self)
        self.onFinalize()
        if register :
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
    def __init__(self, register=True):
        super(QtGui.QMainWindow, self).__init__()
        self.init(register=register)
        
class SubTool(QtGui.QWidget, Tool):
    """Tool for ui files that inherit from QWidget"""
    #------------------------------------------------------------
    def __init__(self, parent=None, register=True):
        super(QtGui.QWidget, self).__init__(parent=parent)
        self.init(register=register)
        
        


    
