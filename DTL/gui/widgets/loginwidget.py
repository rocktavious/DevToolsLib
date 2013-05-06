import os.path
import subprocess
import base64
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from DTL.api import Path, JsonDocument, Utils
from DTL.gui import Dialog, guiUtils

#------------------------------------------------------------
#------------------------------------------------------------
class LoginWidget(Dialog):
    loginSubmitted = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
    
    #------------------------------------------------------------
    def onFinalize(self, loginMsg='Login', credentialsFile=''):
        Utils.synthesize(self, 'loginMsg', loginMsg)
        Utils.synthesize(self, 'credentialsFile', Path(credentialsFile))
        Utils.synthesize(self, 'submitted', False)
        
        self.setModal(True)
        
        
        self.ui_loginMessage.setText(self.loginMsg())
        self.ui_submit.clicked.connect(self.emitLoginSubmitted)
        self.ui_username.returnPressed.connect(self.emitLoginSubmitted)
        self.ui_password.returnPressed.connect(self.emitLoginSubmitted)
        self.ui_password.setEchoMode(QtGui.QLineEdit.Password)
        
        self.center()
        
        if self.credentialsFile() :
            self._readCredentials()
            
        
    #------------------------------------------------------------
    def emitLoginSubmitted(self):
        if not self.signalsBlocked():
            username = self.ui_username.text()
            password = self.ui_password.text()
            if self.ui_saveOption.checkState() :
                self._saveCredentials(username, password)
            self.loginSubmitted.emit(username, password)
            self.setSubmitted(True)
            self.close()
    
    #------------------------------------------------------------
    def _saveCredentials(self, username, password):
        if self.credentialsFile() :
            data = JsonDocument(self.credentialsFile())
            data['Username'] = base64.b64encode(str(username))
            data['Password'] = base64.b64encode(str(password))
            data.save()
            
    #------------------------------------------------------------
    def _readCredentials(self):
        if self.credentialsFile() and self.credentialsFile().exists() :
            data = JsonDocument(self.credentialsFile())
            self.ui_username.setText(base64.b64decode(data['Username']))
            self.ui_password.setText(base64.b64decode(data['Password']))
            self.ui_saveOption.setCheckState(True)
            self.setSubmitted(True)
        
            
    #------------------------------------------------------------
    @staticmethod
    def getCredentials(*args, **kwds):
        success, username, password = False, '', ''
        widget = LoginWidget(*args, **kwds)
        if not widget.submitted() :
            widget.exec_()
        success = widget.submitted()
        if success :
            username = widget.ui_username.text()
            password = widget.ui_password.text()
        
        return success, str(username), str(password)
    

if __name__ == "__main__":
    from DTL.api import Utils
    print Utils.getTempFilepath('code_review_crucible_login.dat')
    print LoginWidget.getCredentials(loginMsg='This is my test message.')
    
    