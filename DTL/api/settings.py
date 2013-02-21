import os
import sys
import getpass

from .. import __pkgdir__, __pkgname__
from . import default_user_settings, Version, Path, JsonDocument

#------------------------------------------------------------
#------------------------------------------------------------
class Settings(JsonDocument):
    #------------------------------------------------------------
    def __init__(self):
        pkg_defaults = dict()
        for setting in dir(default_user_settings):
            if setting == setting.upper():
                pkg_defaults[setting] = getattr(default_user_settings, setting)
        
        self._pkg = __pkgname__
        self._version = Version((1,0,0,0))
        self._username = getpass.getuser()
        self._resources_dir = Path(__pkgdir__).new_path_join('resources')
        
        if sys.platform == 'darwin' :
            self._appdata = Path(os.path.join(os.environ['HOME'], 'Documents', default_user_settings.COMPANY, self._pkg))
        else :
            self._appdata = Path(os.path.join(os.environ['APPDATA'], default_user_settings.COMPANY, self._pkg))
        
        self._appdata.validate_dirs()
        super(Settings, self).__init__(self._appdata.new_path_join('local_settings.json'))    
        self.defaults(pkg_defaults)
        self.save()
        
Settings = Settings()
            
