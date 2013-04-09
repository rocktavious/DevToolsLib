"""
Dev Tools Library (DTL) multiplatform, multiapplication tools suite.
"""
import os
import sys
import getpass

__versiontuple__ = (1,0,0)
__version__ = '.'.join(str(x) for x in __versiontuple__)
__company__ = 'Cloud Imperium'
__user__ = getpass.getuser()
__authors__ = ['Kyle Rockman', 'John Crocker']
__docformat__ = 'restructuredtext en'
__pkgdir__ = os.path.dirname(sys.argv[0])
__pkgname__ = os.path.basename(__pkgdir__)
__pkgresources__ = os.path.join(__pkgdir__, 'resources')
__installers__ = os.path.join(__pkgdir__,'installers')

if sys.platform == 'win32' :
    __appdata__ = os.path.join(os.environ['APPDATA'], __company__, __pkgname__)
else:
    __appdata__ = os.path.join(os.environ['HOME'], 'Documents', __company__, __pkgname__)
    
try:
    os.makedirs(__appdata__,0777)
except:
    pass
