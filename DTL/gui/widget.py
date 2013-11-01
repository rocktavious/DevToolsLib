from DTL.qt import QtGui

from DTL.gui.base import BaseGUI

#------------------------------------------------------------
#------------------------------------------------------------
class Widget(QtGui.QWidget, BaseGUI):
    #------------------------------------------------------------
    def __init__(self, *args, **kwds):
        self._qtclass = QtGui.QWidget
        BaseGUI.__init__(self, *args, **kwds)