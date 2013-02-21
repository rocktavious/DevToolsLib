from PyQt4 import QtCore, QtGui

from DTL.api import Tool, Start


class SampleTool(Tool):
    
    def onInit(self):
        QtGui.QPushButton(parent=self)
        self.setObjectName('Sample 1')
        self.setWindowTitle('Sample 1')
        SampleTool2()
        

        
class SampleTool2(Tool):
    
    def onInit(self):
        QtGui.QPushButton(parent=self)
        QtGui.QPushButton(parent=self)
        self.setObjectName('Sample 2')
        self.setWindowTitle('Sample 2')
        SampleTool3()
        
    def isModal(self):
        return True    
        
class SampleTool3(Tool):
    
    def onInit(self):
        QtGui.QPushButton(parent=self)
        QtGui.QPushButton(parent=self)
        QtGui.QPushButton(parent=self)
        self.setObjectName('Sample 3')
        self.setWindowTitle('Sample 3')

if __name__ == '__main__':
    SampleTool()
    Start()