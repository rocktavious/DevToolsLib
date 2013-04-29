import os.path
import subprocess
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from DTL.gui.base import BaseGUI
from DTL.gui import utils as guiUtils

#------------------------------------------------------------
#------------------------------------------------------------
class LoginWidget(QtGui.QDialog, BaseGUI):
    loginSubmitted = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
    
    #------------------------------------------------------------
    def __init__(self, msg, *a, **kw):
        self._qtclass = QtGui.QDialog
        self._msg = msg
        self._submitted = False
        BaseGUI.__init__(self, *a, **kw)
        self.setModal(True)
        self.center()
        
        
    #------------------------------------------------------------
    def onFinalize(self):
        self.message.setText(self._msg)
        self.submit.clicked.connect(self.emitLoginSubmitted)
        self.username.returnPressed.connect(self.emitLoginSubmitted)
        self.password.returnPressed.connect(self.emitLoginSubmitted)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        
    #------------------------------------------------------------
    def emitLoginSubmitted(self):
        if not self.signalsBlocked():
            username = self.username.text()
            password = self.password.text()
            self.loginSubmitted.emit(username, password)
            self._submitted = True
            self.close()
    
    #------------------------------------------------------------
    def show(self):
        self.exec_()
            
    #------------------------------------------------------------
    @staticmethod
    def getCredentials(msg):
        success, username, password = False, '', ''
        widget = LoginWidget(msg)
        widget.show()
        success = widget._submitted
        if success :
            username = widget.username.text()
            password = widget.password.text()
        
        return success, username, password
    

if __name__ == "__main__":      
    print LoginWidget.getCredentials('This is my test message.')
    
    
