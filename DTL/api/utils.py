'''
Utility Funcs for DTL

These are imported into the DTL namespace upon import
'''
import os
import sys
import imp
import types
import re
import subprocess

from DTL import __pkgname__, __company__, __pkgresources__
from DTL.api.path import Path

#------------------------------------------------------------
def mainIsFrozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze

#------------------------------------------------------------
def getMainDir():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""
    if mainIsFrozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])

#------------------------------------------------------------
def quickReload(modulename):
    """
    Searches through the loaded sys modules and looks up matching module names 
    based on the imported module.
    """
    expr = re.compile( str(modulename).replace( '.', '\.' ).replace( '*', '[A-Za-z0-9_]*' ) )

    # reload longer chains first
    keys = sys.modules.keys()
    keys.sort()
    keys.reverse()

    for key in keys:
        module = sys.modules[key]
        if ( expr.match(key) and module != None ):
            print 'reloading', key
            reload( module )



#------------------------------------------------------------
def synthesize(object, name, value):
    """
    Convenience method to create getters and setters for a instance. 
    Should be called from within __init__. Creates [name], set[Name], 
    _[name] on object.

    :param object: An instance of the class to add the methods to.
    :param name: The base name to build the function names, and storage variable.
    :param value: The initial state of the created variable.

    """
    storageName = '_%s' % name
    setterName = 'set%s%s' % (name[0].capitalize(), name[1:])
    if hasattr(object, name):
        raise KeyError('The provided name already exists')
    # add the storeage variable to the object
    setattr(object, storageName, value)
    # define the getter
    def customGetter(self):
        return getattr(self, storageName)
    # define the Setter
    def customSetter(self, state):
        setattr(self, storageName, state)
    # add the getter to the object, if it does not exist
    if not hasattr(object, name):
        setattr(object, name, types.MethodType(customGetter, object))
    # add the setter to the object, if it does not exist
    if not hasattr(object, setterName):
        setattr(object, setterName, types.MethodType(customSetter, object))

#------------------------------------------------------------
def runFile( filepath, basePath=None, cmd=None, debug=False ):
    """
    Runs the filepath in a shell with proper commands given, or passes 
    the command to the shell. (CMD in windows) the current platform

    :param filepath: path to the file to execute
    :param basePath: working directory where the command should be called
    from.  If omitted, the current working directory is used.

    """
    status = False
    filepath = Path(filepath)

    # make sure the filepath we're running is a file 
    if not filepath.isFile:
        return status

    # determine the base path for the system
    if basePath is None:
        basePath = filepath.dir

    options = { 'filepath': filepath.path, 'basepath': basePath }

    if cmd == None :
        if filepath.ext in ['.py','.pyw']:
            if debug:
                cmd = 'python.exe "%s"' % filepath.path
            else:
                cmd = 'pythonw.exe "%s"' % filepath.path

            status = subprocess.Popen( cmd, stdout=sys.stdout, stderr=sys.stderr, shell=debug, cwd=basePath)

    if not status :
        try:
            status = os.startfile(filepath.path)
        except:
            print 'Core.runFile Cannot run type (*%s)' % filepath.ext

    return status
