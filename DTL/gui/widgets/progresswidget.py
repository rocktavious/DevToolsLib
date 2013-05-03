from PyQt4 import QtGui

from DTL.api import Utils
from DTL.db.data import Progress
from DTL.gui.base import BaseGUI
from DTL.gui import Core

#------------------------------------------------------------
#------------------------------------------------------------
class ProgressWidget(QtGui.QDialog, BaseGUI):
    #------------------------------------------------------------
    def __init__( self, progress, **kwds):
        self._qtclass = QtGui.QDialog
        Utils.synthesize(self, 'progress', progress)
        BaseGUI.__init__(self, **kwds)
        self.center()
        
    #------------------------------------------------------------
    def onFinalize(self):
        self.message.setText(self.progress().message)
        self.progressBar.setValue(10)
        
    #------------------------------------------------------------
    def update(self):
        self.progressBar.setValue(self.progress().value())
        self.progressBar.update()
        super(ProgressWidget, self).update()
    
    #------------------------------------------------------------
    def increment(self):
        self.progress().increment()
        self.update()
    
    #------------------------------------------------------------
    @staticmethod
    def start(parent=None, flags=0, *args, **kwds):
        new_progress = Progress(*args, **kwds)
        new_widget = ProgressWidget(progress=new_progress, flags=flags, parent=parent)
        new_widget.show()
        return new_widget


#------------------------------------------------------------
if __name__ == '__main__':
    import time
    prg = ProgressWidget.start(total=5)
    
    for i in range(5):
        time.sleep(1)    
        prg.increment()
        
    prg.close()

