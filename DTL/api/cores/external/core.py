from PyQt4 import QtCore, QtGui

from ... import Settings, Utils

#------------------------------------------------------------
#------------------------------------------------------------
class Core(QtCore.QObject):
    '''Tool Environment Core'''
    _instance = None
    #------------------------------------------------------------
    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance    
    
    #------------------------------------------------------------
    def __init__(self):
        super(Core, self).__init__()
        self.setObjectName(Settings['COMPANY'] + ' Tools Environment Core')
        self._tools = list()

    #------------------------------------------------------------
    def init(self):
        app = QtGui.QApplication.instance()
        if not app :
            app = QtGui.QApplication([])

        self._readSettings()
        app.setStyle( 'Plastique' )
        app.setStyleSheet(Utils.getStyleSheet())
        app.addLibraryPath(Settings._resources_dir.new_path_join('images').path)
        app.aboutToQuit.connect(self._saveSettings)
        
        return app
            
    #------------------------------------------------------------
    def registerTool(self, tool):
        self._tools.append(tool)
            
    #------------------------------------------------------------
    def runTools(self):
        for tool in self._tools :
            if tool.isModal() :
                return tool.exec_()
            else:
                tool.show()

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
    
