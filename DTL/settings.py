import os
import sys
import imp
import getpass

from DTL.api.jsondocument import JsonDocument
from DTL.api.path import Path

#------------------------------------------------------------
#------------------------------------------------------------
class Settings(JsonDocument):

    #------------------------------------------------------------
    def __init__(self):
        super(Settings, self).__init__()
        
        self._setup()
        
    #------------------------------------------------------------
    def _setup(self):
        self._findOS()
        self._findPkgVars()
        self._readGlobalSettings()
        self._readLocalSettings()
        self._applyOSSettings()
    
    #------------------------------------------------------------
    def _findOS(self):
        key = 'OS_TYPE'
        if ( os.name == 'posix' ):
            self[key] = 'Linux'
        elif ( os.name == 'nt' ):
            self[key] = 'Windows'
        elif ( os.name == 'osx' ):
            self[key] = 'MacOS'
        else:
            self[key] = None
    
    #------------------------------------------------------------
    def _findPkgVars(self):
        self['PKG_DIR'] = self.getPkgDir()
        self['PKG_NAME'] = self['PKG_DIR'].name
        
        self['PKG_DATA_DIR'] = Path('~').join('.' + self['PKG_NAME']).expand()
        if not self['PKG_DATA_DIR'].exists :
            self['PKG_DATA_DIR'].makedirs()
        
        self['GLOBAL_SETTINGS_PATH'] = self['PKG_DIR'].join('settings.json')
        self['LOCAL_SETTINGS_PATH'] = self['PKG_DATA_DIR'].join('settings.json')
        self['RESOURCE_PATH'] = self['PKG_DIR'].join('resources')
    
    #------------------------------------------------------------
    def _applyOSSettings(self):
        for k,v in self[self['OS_TYPE']].items():
            self.__setitem__(k,v)
        
        self.pop('Windows')
        self.pop('MacOS')
        self.pop('Linux')
    
    #------------------------------------------------------------
    def _readGlobalSettings(self):
        self.setFilePath(self['GLOBAL_SETTINGS_PATH'])
        self.read()
    
    #------------------------------------------------------------
    def _readLocalSettings(self):
        self.setFilePath(self['LOCAL_SETTINGS_PATH'])
        self.read()
    
    #------------------------------------------------------------
    def mainIsFrozen(self):
        """Returns whether we are frozen via py2exe.
        This will affect how we find out where we are located."""
        return (hasattr(sys, "frozen") or # new py2exe
                hasattr(sys, "importers") # old py2exe
                or imp.is_frozen("__main__")) # tools/freeze
    
    #------------------------------------------------------------
    def getPkgDir(self):
        """ This will get us the program's directory,
        even if we are frozen using py2exe"""
        if self.mainIsFrozen():
            return Path(sys.executable).parent
        if '__file__' in globals():
            return Path(__file__).parent
        if sys.argv[0] == '' :
            return Path(os.getcwdu())
        return Path(sys.argv[0]).parent
    
    #------------------------------------------------------------
    def getTempPath(self):
        temp_path = Settings['PKG_DATA_DIR'].join('tmp')
        temp_path.makedirs()
        return temp_path
    
    #------------------------------------------------------------
    def getResourcePath(self):
        return self['RESOURCE_PATH']

#------------------------------------------------------------
Settings = Settings() 


if __name__ == '__main__':
    for k,v in Settings.items(): print k,':',v