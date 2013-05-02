from PyQt4 import QtCore, QtGui

from DTL.api import Path
from DTL.gui import Core
from DTL.gui.base import BaseGUI

LOCALPATH = Path.getMainDir()

#------------------------------------------------------------
#------------------------------------------------------------
class ProgressWidget(QtGui.QDialog, BaseGUI):
    #------------------------------------------------------------
    def __init__( self, progress, *a, **kw):
        self._qtclass = QtGui.QDialog
        self._progress = progress
        BaseGUI.__init__(self, *a, **kw)
        self.center()
        
    #------------------------------------------------------------
    def update(self):
        self.progressBar.setValue(self._progress.value())

#------------------------------------------------------------
#------------------------------------------------------------
class Progress(object):
    #------------------------------------------------------------
    def __init__(self, total, parent=None):
        self._parent = parent
        self._total = total
        self._index = 0
        self._ui = None
        
    #------------------------------------------------------------
    def update(self):
        self._ui.update()
    
    #------------------------------------------------------------
    def increment(self):
        self._index += 1
        self.update()
    
    #------------------------------------------------------------
    def index(self):
        return self._index
    
    #------------------------------------------------------------
    def isValid(self):
        return self._total != None
    
    #------------------------------------------------------------
    def parent(self):
        return self._parent
    
    #------------------------------------------------------------
    def percent(self, recursive=True):
        outPercent = 1.0

        if self._total:
            outPercent /= self._total

        if recursive:
            section = self.parent()

            while section:
                outPercent *= section.percent()
                section = section.parent()

            return outPercent
    
    #------------------------------------------------------------
    def value(self, recursive=True):
        if recursive:
            outValue = 0
            section = self.parent()
            while section:
                outValue += 100 * (section.index() * section.percent())
                section	= section.parent()

            return outValue + (100 * self.index() * self.percent())
        else:
            return (100 * self.index() * self.percent(recursive=False))
    
    #------------------------------------------------------------
    def start(self):
        if not self._ui :
            self._ui = ProgressWidget(self)
            self._ui.show()
        
        self.update()
    
    #------------------------------------------------------------
    def end(self):
        if self._ui :
            self._ui.close()


#------------------------------------------------------------
if __name__ == '__main__':
    import time
    prg = Progress(5)
    prg.start()
    
    for i in range(5):
        time.sleep(1)    
        prg.increment()
