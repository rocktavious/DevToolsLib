import os
import sys
import imp
import getpass

from DTL.api import JsonDocument, Path

class _Settings(JsonDocument):

    #------------------------------------------------------------
    def __init__(self, *args, **kwds):
        super(_Settings, self).__init__(*args, **kwds)
        
        self._setup()
        
    #------------------------------------------------------------
    def _setup(self):
        self._findOS()
        
        self['USERNAME'] = getpass.getuser()
        self['PKG_DIR'] = self.getPkgDir()
        self['PKG_NAME'] = os.path.basename(self['PKG_DIR'])
        self['PKG_RESOURCE_PATH'] = os.path.join(self['PKG_DIR'],'resources')
        
        if self['OS_TYPE'] == 'Windows' :
            self['PKG_DATA_DIR'] = os.path.join(os.environ['LOCALAPPDATA'], self['PKG_NAME'])
        else:
            self['PKG_DATA_DIR'] = os.path.join(os.environ['HOME'], '.' + self['PKG_NAME'])
        if not os.path.exists(self['PKG_DATA_DIR']) :
            os.makedirs(self['PKG_DATA_DIR'])
        
        self['PKG_SETTINGS_PATH'] = os.path.join(self['PKG_RESOURCE_PATH'],'settings.json')
        self['LOCAL_SETTINGS_PATH'] = os.path.join(self['PKG_DATA_DIR'], 'settings.json')


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
    def _unparse(self, data_dict):
        return json.dumps(data_dict, sort_keys=True, indent=4, cls=self.encoder())
    
    #------------------------------------------------------------
    def _parse(self, file_handle):
        return json.load(file_handle)
    
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
            return os.path.dirname(sys.executable)
        if '__file__' in dir():
            return os.path.dirname(__file__)
        if sys.argv[0] == '' :
            return os.getcwdu()
        return os.path.dirname(sys.argv[0])

#------------------------------------------------------------
Settings = _Settings()

if __name__ == '__main__':

    for k,v in Settings.items(): print k,':',v