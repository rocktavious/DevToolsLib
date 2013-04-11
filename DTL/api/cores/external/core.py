import logging

from DTL import __company__
from DTL.api.logger import Logger
from DTL.api import utils as Utils
from DTL.api.enum import Enum

#------------------------------------------------------------
#------------------------------------------------------------
class Core(object):
    '''Tool Environment Core'''
    __metaclass__ = Logger.getMetaClass()
    EnvironmentTypes = Enum("External","Maya","Max","MotionBuilder")
    
    _instance = None
    #------------------------------------------------------------
    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance    

    #------------------------------------------------------------
    def __init__(self):
        self.setupLogging()
        
        Utils.synthesize(self, 'environment', Core.EnvironmentTypes.External)
        Utils.synthesize(self, 'mfcApp', False)
        Utils.synthesize(self, 'app', None)
        
        try:
            from DTL.gui import guiUtils
            app = guiUtils.getApp()
            self.setApp(app)
            self._readSettings()
            self.app.aboutToQuit.connect(self._saveSettings)
        except:
            pass

    #------------------------------------------------------------
    def _saveSettings(self):
        from DTL.gui import guiUtils
        
        settings = guiUtils.getAppSettings()
        settings.beginGroup(self.objectName())
        
        self.saveSettings(settings)

        settings.endGroup()

    #------------------------------------------------------------
    def _readSettings(self):
        from DTL.gui import guiUtils
        
        settings = guiUtils.getAppSettings()
        settings.beginGroup(self.objectName())
        
        self.readSettings(settings)

        settings.endGroup()
        
    #------------------------------------------------------------
    # Begin Overriable methods
    #------------------------------------------------------------
    def setupLogging(self):
        #Setup Defaults
        Logger.setupFileLogger()
        Logger.setupDatabaseLogger()
        Logger.setupStreamLogger()
        


    #------------------------------------------------------------
    def rootWindow(self):
        """returns the current applications root window"""
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
    def saveSettings(self, settings):
        pass
    
    #------------------------------------------------------------
    def readSettings(self, settings):
        pass
