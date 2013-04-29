import os.path
import subprocess
import base64
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from DTL.api import Path, JsonDocument
from DTL.gui.base import BaseGUI
from DTL.gui import guiUtils

#------------------------------------------------------------
#------------------------------------------------------------
class LoginWidget(QtGui.QDialog, BaseGUI):
    loginSubmitted = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
    
    #------------------------------------------------------------
    def __init__(self, msg, credentialsFile='', *a, **kw):
        self._qtclass = QtGui.QDialog
        self._msg = msg
        self._credentialsFile = Path(credentialsFile)
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
        if self._credentialsFile :
            self._readCredentials()
            
        
    #------------------------------------------------------------
    def emitLoginSubmitted(self):
        if not self.signalsBlocked():
            username = self.username.text()
            password = self.password.text()
            if self.saveCredentials.checkState() :
                self._saveCredentials(username, password)
            self.loginSubmitted.emit(username, password)
            self._submitted = True
            self.close()
    
    #------------------------------------------------------------
    def _saveCredentials(self, username, password):
        if self._credentialsFile :
            data = JsonDocument(self._credentialsFile)
            data['Username'] = base64.b64encode(str(username))
            data['Password'] = base64.b64encode(str(password))
            data.save()
            
    #------------------------------------------------------------
    def _readCredentials(self):
        if self._credentialsFile and self._credentialsFile.exists() :
            data = JsonDocument(self._credentialsFile)
            self.username.setText(base64.b64decode(data['Username']))
            self.password.setText(base64.b64decode(data['Password']))
            self.saveCredentials.setCheckState(True)
        
            
    #------------------------------------------------------------
    @staticmethod
    def getCredentials(*args, **kwds):
        success, username, password = False, '', ''
        widget = LoginWidget(*args, **kwds)
        widget.exec_()
        success = widget._submitted
        if success :
            username = widget.username.text()
            password = widget.password.text()
        
        return success, str(username), str(password)
    

if __name__ == "__main__":
    from DTL.api import Utils
    print Utils.getTempFilepath('code_review_crucible_login.dat')
    print LoginWidget.getCredentials('This is my test message.',
                                     Utils.getTempFilepath('code_review_crucible_login.dat'))
    
    
