"""
Dev Tools Library (DTL) multiplatform, multiapplication tools suite.
"""
import os.path
__docformat__ = 'restructuredtext en'
__pkgdir__ = os.path.dirname(__file__)
__pkgname__ = 'DTL'

try:
    from PyQt4 import QtCore, QtGui, uic
except:
    raise Exception('DTL Module Requires PyQt4!')

from . import api, db

