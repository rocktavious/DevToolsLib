from DTL.qt import QtGui
from DTL.gui.base import BaseGUI

#------------------------------------------------------------
#------------------------------------------------------------
class Dialog(QtGui.QDialog, BaseGUI):
    #------------------------------------------------------------
    def __init__(self, *args, **kwds):
        self._qtclass = QtGui.QDialog
        BaseGUI.__init__(self, *args, **kwds)
        # set this property to true to properly handle tracking events to control keyboard overrides
        self.setMouseTracking(True)
