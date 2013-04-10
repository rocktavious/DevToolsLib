import sys
import __builtin__
import copy

BLACKLIST = ["unittest", "logging", "warnings"]

class RollbackImporter(object):
    '''RollbackImporter installs itself as a proxy for the built-in __import__ function
    that lies behind the 'import' statement. Once installed,
    they note all imported modules, and when uninstalled or restarted,
    they delete those modules from the system module list;
    this ensures that the modules will be freshly loaded from their source code when next imported.
    '''
    _instance = None
    #------------------------------------------------------------
    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance   
    
    #------------------------------------------------------------
    def __init__(self):
        "Creates and installs as the global importer"
        self.install()
        
    #------------------------------------------------------------
    def _import(self, name, globals=None, locals=None, fromlist=[], level = -1):
        result = apply(self.realImport, (name, globals, locals, fromlist))
        
        if len(name) <= len(result.__name__):
            name = copy.copy(result.__name__)
        
        for b in BLACKLIST:
            if b in name.lower():
                return result        
        
        # Remember import in the right order
        if name not in self.previousModules:
            # Only remember once
            if name not in self.newModules:                            
                self.newModules += [name]
        
        return result

    #------------------------------------------------------------
    def install(self):
        self.previousModules = sys.modules.copy()
        self.realImport = __builtin__.__import__
        __builtin__.__import__ = self._import
        self.newModules = []
    
    #------------------------------------------------------------
    def uninstall(self):
        for modname in self.newModules:
            if not self.previousModules.has_key(modname):
                # Force reload when modname next imported
                del(sys.modules[modname])
        __builtin__.__import__ = self.realImport
    
    #------------------------------------------------------------
    def restart(self):
        RollbackImporter.instance().uninstall()
        RollbackImporter.instance().install()