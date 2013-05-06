from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from DTL.gui.base import BaseGUI

#------------------------------------------------------------
#------------------------------------------------------------
class Widget(QtGui.QWidget, BaseGUI):
    #------------------------------------------------------------
    def __init__(self, *args, **kwds):
        self._qtclass = QtGui.QWidget
        BaseGUI.__init__(self, *args, **kwds)