"""
Dev Tools Library (DTL) multiplatform, multiapplication tools suite.
"""
import os
import sys
import imp
import getpass

def mainIsFrozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze

def getcwd():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""
    if mainIsFrozen():
        return os.path.dirname(sys.executable)
    if sys.argv[0] == '' :
        return os.getcwdu()
    return os.path.dirname(sys.argv[0])

def cleanup():
    """ Util method to clean up all the pyc files"""
    from DTL.api.path import Path
    local_path = Path.getcwd()
    for file_path in local_path.walk('*.pyc') :
        file_path.remove()

__version__ = '1.0.2'
__company__ = 'Cloud Imperium'
__user__ = getpass.getuser()
__authors__ = ['Kyle Rockman', 'John Crocker']
__docformat__ = 'restructuredtext en'
__pkgdir__ = os.path.dirname(getcwd())
__pkgname__ = os.path.basename(__pkgdir__)
__pkgresources__ = os.path.join(__pkgname__, 'resources')
__installers__ = os.path.join(__pkgname__,'installers')


if sys.platform == 'win32' :
    __appdata__ = os.path.join(os.environ['APPDATA'], __company__)
else:
    __appdata__ = os.path.join(os.environ['HOME'], 'Documents', __company__)



