"""
Dev Tools Library (DTL) multiplatform, multiapplication tools suite.

Usage
=====
    import DTL
    
    From there a number of processes will be spawned based on the environment you have imported into


:author: Kyle Rockman
"""
import os.path
import traceback
__docformat__ = 'restructuredtext en'

__pkgdir__ = os.path.dirname(__file__)
__pkgname__ = 'DTL'

try:
    from .resources import internal_resources
    from .api import *

    from .cores import Core
    core = Core()
    core.start()
    #from .tool import *
    
except:
    traceback.print_exc()
    raw_input()
