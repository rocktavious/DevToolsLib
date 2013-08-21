import sys
import logging
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from DTL.api import Enum, Path, apiUtils, loggingUtils
from DTL.settings import Settings

#------------------------------------------------------------
#------------------------------------------------------------
class Core(object):
    '''Tool Environment Core'''
    __metaclass__ = loggingUtils.LoggingMetaclass
    EnvironmentTypes = Enum("External","Maya","Max","MotionBuilder")
    
    _instance = None
    #------------------------------------------------------------
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    #------------------------------------------------------------
    @staticmethod
    def getAppSettings():
        return QtCore.QSettings(Settings['COMPANY'], Settings['PKG_NAME'])
    
    #------------------------------------------------------------
    @staticmethod
    def getStyleSheet():
        ss_file = Settings['RESOURCE_PATH'].join('darkorange.stylesheet')
        data = ''
        with open(ss_file, 'r') as file_handle :
            data = file_handle.read()
        return '%s' % data
    
    #------------------------------------------------------------
    @staticmethod
    def getApp():
        app = QtGui.QApplication.instance()
        if not app :
            app = QtGui.QApplication(sys.argv)
            app.setStyle( 'Plastique' )
            #app.setStyleSheet(Core.getStyleSheet())
        
        return app

    #------------------------------------------------------------
    def __init__(self):
        self.setupLogging()
        
        apiUtils.synthesize(self, 'environment', Core.EnvironmentTypes.External)
        apiUtils.synthesize(self, 'mfcApp', False)
        apiUtils.synthesize(self, 'app', None)
        
        app = Core.getApp()
        self.setApp(app)
        self._readSettings()
        self.app().aboutToQuit.connect(self._saveSettings)


    #------------------------------------------------------------
    def _saveSettings(self):        
        settings = Core.getAppSettings()
        settings.beginGroup(apiUtils.getClassName(self))
        
        self.saveSettings(settings)

        settings.endGroup()

    #------------------------------------------------------------
    def _readSettings(self):        
        settings = Core.getAppSettings()
        settings.beginGroup(apiUtils.getClassName(self))
        
        self.readSettings(settings)

        settings.endGroup()
        
    #------------------------------------------------------------
    @staticmethod
    def Start():
        if Core.instance().app() :
            Core.instance().app().exec_()
            
    #------------------------------------------------------------
    @staticmethod
    def Stop():
        if Core.instance().app() :
            Core.instance().app().closeAllWindows()
            Core.instance().app().quit()
        
    #------------------------------------------------------------
    # Begin Overriable methods
    #------------------------------------------------------------
    def setupLogging(self):
        pass
        #Setup Defaults
        #Logger.setupFileLogger()
        #Logger.setupDatabaseLogger()
        #Logger.setupStreamLogger()
        

    #------------------------------------------------------------
    def rootWindow(self):
        """returns the current applications root window"""
        from PyQt4 import QtGui
        window = None
        
        #MFC apps there should be no root window
        if self.mfcApp():
            return window
        
        if QtGui.QApplication.instance():
            window = QtGui.QApplication.instance().activeWindow()
            # grab the root window
            if window:
                while window.parent():
                    window = window.parent()

        return window
    
    #------------------------------------------------------------
    def getFileFromUser(self, parent=None, ext=''):
        file_dialog = QtGui.QFileDialog(parent)
        file_dialog.setViewMode(QtGui.QFileDialog.Detail)
        file_dialog.setNameFilter(ext)
        return _return_file(file_dialog)
    
    #------------------------------------------------------------
    def getDirFromUser(self, parent=None):
        file_dialog = QtGui.QFileDialog(parent)
        file_dialog.setFileMode(QtGui.QFileDialog.Directory)
        file_dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        file_dialog.setViewMode(QtGui.QFileDialog.Detail)
        return self._return_file(file_dialog)    
    
    #------------------------------------------------------------
    def getSaveFileFromUser(self, parent=None, ext=[]):
        file_dialog = QtGui.QFileDialog(parent)
        file_dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        file_dialog.setViewMode(QtGui.QFileDialog.Detail)
        return self._return_file(file_dialog)
        
    #------------------------------------------------------------
    def _return_file(self, file_dialog):
        if file_dialog.exec_():
            returned_file = str(file_dialog.selectedFiles()[0])
            return Path(returned_file).expand()
        return Path()    
    
    #------------------------------------------------------------
    def saveSettings(self, settings):
        pass
    
    #------------------------------------------------------------
    def readSettings(self, settings):
        pass
