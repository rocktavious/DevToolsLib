from PyQt4 import QtCore, QtGui

from . import Core, Utils

class Tool(QtGui.QWidget):
    
    _instance = None
    #------------------------------------------------------------
    @classmethod
    def instance(cls, parent=None):
        if not cls._instance:
            cls._instance = cls(parent=parent)
        return cls._instance    
    
    #------------------------------------------------------------
    def __init__(self, parent=None):
        super(Tool, self).__init__(parent=parent)
        self.ui_file = None
        self.onInit()
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
        
    
