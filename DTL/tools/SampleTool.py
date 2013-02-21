from PyQt4 import QtCore, QtGui

from DTL.api import Utils, SubTool, Start


class SampleTool(SubTool):
    
    def onInit(self):
        self.ui_file = 'c:\\dev-tools\\DTL\\tools\\SampleTool.ui'
        
    def onFinalize(self):
        self.pushButton.clicked.connect(self.test)
        
    def test(self):
        user_file = Utils.getDirFromUser(self)
        print user_file
    

if __name__ == '__main__':
    SampleTool()
    Start()