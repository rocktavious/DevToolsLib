import os.path
from DTL.qt import QtGui

from DTL.conf import settings
from DTL.gui.base import BaseGUI

#------------------------------------------------------------
#------------------------------------------------------------
class Wizard(QtGui.QWizard, BaseGUI):
    #------------------------------------------------------------
    def __init__(self, *a, **kw):
        self._qtclass = QtGui.QWizard
        BaseGUI.__init__(self, *a, **kw)
        # set this property to true to properly handle tracking events to control keyboard overrides
        self.setMouseTracking( True )
        self.initWizardPages()
    
    #------------------------------------------------------------
    def setupStyle(self):
        self.setWizardStyle( QtGui.QWizard.ModernStyle )
        imgfilepath = Path(settings.PKG_RESOURCE_PATH).join('images', 'Logo_lg.png' )
        self.setPixmap( QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(imgfilepath))

    #------------------------------------------------------------
    def initWizardPages( self ):
        pass
    
    #------------------------------------------------------------
    @classmethod
    def runWizard( cls, parent = None ):
        if ( cls(parent).exec_() ):
            return True
        return False

#------------------------------------------------------------
#------------------------------------------------------------
class WizardPage(QtGui.QWizardPage, BaseGUI):
    #------------------------------------------------------------
    def __init__(self, *a, **kw):
        self._qtclass = QtGui.QWizard
        BaseGUI.__init__(self, *a, **kw)
        