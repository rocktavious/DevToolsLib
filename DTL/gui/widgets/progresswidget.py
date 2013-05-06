from PyQt4 import QtGui

from DTL.api import Utils
from DTL.gui import Core, Dialog

#------------------------------------------------------------
#------------------------------------------------------------
class ProgressWidget(Dialog):
    #------------------------------------------------------------
    def onFinalize(self, total=1, current=0, message='Loading...'):
        Utils.synthesize(self, 'total', total)
        Utils.synthesize(self, 'current', current)
        Utils.synthesize(self, 'message', message)
        
        self.ui_ProgressBar.setValue(1)
        self.ui_Label.setText(self.message())
        
        self.center()
        self.show()
        self.update()
        
    #------------------------------------------------------------
    def update(self):
        self.ui_ProgressBar.setValue(self.value())
        self.ui_Label.setText(self.message())
        super(ProgressWidget, self).update()
    
    #------------------------------------------------------------
    def increment(self):
        self.setCurrent(self.current() + 1)
        self.update()
    
    #------------------------------------------------------------
    def percent(self):
        return 1.0 / self.total()
    
    #------------------------------------------------------------
    def value(self, recursive=True):
        return (100 * self.current() * self.percent())


#------------------------------------------------------------
if __name__ == '__main__':
    import time
    prg = ProgressWidget(total=5, message='Test Loading...')
    
    for i in range(5):
        time.sleep(1)
        prg.setMessage(str(i))
        prg.increment()
        
        
    prg.close()

