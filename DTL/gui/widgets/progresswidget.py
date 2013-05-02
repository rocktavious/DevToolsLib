from PyQt4 import QtGui

from DTL.api import Utils
from DTL.gui.base import BaseGUI

#------------------------------------------------------------
#------------------------------------------------------------
class ProgressWidget(QtGui.QDialog, BaseGUI):
    #------------------------------------------------------------
    def __init__( self, progress, *args, **kwds):
        self._qtclass = QtGui.QDialog
        Utils.synthesize(self, 'progress', progress)
        BaseGUI.__init__(self, *args, **kwds)
        self.center()
        
    #------------------------------------------------------------
    def onFinalize(self):
        self.message.setText(self.progress().msg())
        self.progressBar.setValue(1)
        
    #------------------------------------------------------------
    def update(self):
        self.progressBar.setValue(self.progress().value())


#------------------------------------------------------------
#------------------------------------------------------------
class Progress(object):
    #------------------------------------------------------------
    def __init__(self, total=1, index=0, msg='Loading...', *args, **kwds):
        Utils.synthesize(self, 'total', total)
        Utils.synthesize(self, 'index', index)
        Utils.synthesize(self, 'msg', msg)
        Utils.synthesize(self, 'ui', ProgressWidget(self))
        
    #------------------------------------------------------------
    def update(self):
        self.ui().update()
    
    #------------------------------------------------------------
    def increment(self):
        self.setIndex(self.index() + 1)
        self.update()
    
    #------------------------------------------------------------
    def percent(self):
        return 1.0 / self.total()
    
    #------------------------------------------------------------
    def value(self, recursive=True):
        return (100 * self.index() * self.percent())
    
    #------------------------------------------------------------
    def start(self):
        self.ui().show()        
        self.update()
    
    #------------------------------------------------------------
    def end(self):
        self.ui().close()


#------------------------------------------------------------
if __name__ == '__main__':
    import time
    prg = Progress(5)
    prg.start()
    
    for i in range(5):
        time.sleep(1)    
        prg.increment()
