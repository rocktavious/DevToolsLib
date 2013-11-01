from DTL.qt import QtGui

from DTL.gui.base import BaseGUI

#------------------------------------------------------------
#------------------------------------------------------------
class Window(QtGui.QMainWindow, BaseGUI):
    #------------------------------------------------------------
    def __init__(self, *a, **kw):
        self._qtclass = QtGui.QMainWindow
        BaseGUI.__init__(self, *a, **kw)
    
