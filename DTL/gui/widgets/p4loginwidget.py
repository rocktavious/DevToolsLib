import os.path
import subprocess
import base64
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from DTL.api import Path, JsonDocument, apiUtils
from DTL.gui import Dialog, guiUtils
    
#------------------------------------------------------------
#------------------------------------------------------------
class P4LoginWidget(Dialog):
    loginSubmitted = QtCore.pyqtSignal(QtCore.QString, QtCore.QString, QtCore.QString, QtCore.QString)
    
    #------------------------------------------------------------
    def onFinalize(self, loginMsg='Login', credentialsFile=''):
        apiUtils.synthesize(self, 'loginMsg', loginMsg)
        apiUtils.synthesize(self, 'credentialsFile', Path(credentialsFile))
        apiUtils.synthesize(self, 'submitted', False)
        
        self.setModal(True)
        
        self.ui_loginMessage.setText(self.loginMsg())
        self.ui_submit.clicked.connect(self.emitLoginSubmitted)
        self.ui_username.returnPressed.connect(self.emitLoginSubmitted)
        self.ui_password.returnPressed.connect(self.emitLoginSubmitted)
        self.ui_port.returnPressed.connect(self.emitLoginSubmitted)
        self.ui_client.returnPressed.connect(self.emitLoginSubmitted)
        self.ui_password.setEchoMode(QtGui.QLineEdit.Password)
        
        self.center()
        
        if self.credentialsFile() :
            self._readCredentials()
            
        
    #------------------------------------------------------------
    def emitLoginSubmitted(self):
        if not self.signalsBlocked():
            username = self.ui_username.text()
            password = self.ui_password.text()
            port = self.ui_port.text()
            client = self.ui_client.text()            
            
            self._saveCredentials(username, password, port, client)
            self.loginSubmitted.emit(username, password, port, client)
            self.setSubmitted(True)
            self.close()
    
    #------------------------------------------------------------
    def _saveCredentials(self, username, password, port, client):
        if self.ui_saveOption.checkState() :
            
            if not self.credentialsFile() :
                self.setCredentialsFile(apiUtils.getTempFilepath('p4_login.dat'))
            data = JsonDocument(file_path=self.credentialsFile())
            data['Username'] = base64.b64encode(str(username))
            data['Password'] = base64.b64encode(str(password))
            data['Port'] = base64.b64encode(str(port))
            data['Client'] = base64.b64encode(str(client))
            data.save()
            
    #------------------------------------------------------------
    def _readCredentials(self):
        if self.credentialsFile() and self.credentialsFile().exists() :
            data = JsonDocument(file_path=self.credentialsFile())
            self.ui_username.setText(base64.b64decode(data['Username']))
            self.ui_password.setText(base64.b64decode(data['Password']))
            self.ui_port.setText(base64.b64decode(data['Port']))
            self.ui_client.setText(base64.b64decode(data['Client']))
            self.ui_saveOption.setCheckState(True)
            self.setSubmitted(True)
        
            
    #------------------------------------------------------------
    @staticmethod
    def getCredentials(*args, **kwds):
        success, username, password, port, client = False, '', '', '', ''
        widget = P4LoginWidget(*args, **kwds)
        if not widget.submitted() :
            widget.exec_()
        success = widget.submitted()
        if success :
            username = widget.ui_username.text()
            password = widget.ui_password.text()
            port = widget.ui_port.text()
            client = widget.ui_client.text()            
        
        return success, str(username), str(password), str(port), str(client)
    

#------------------------------------------------------------
if __name__ == "__main__":
    credentialsFile = apiUtils.getTempFilepath('p4_login.dat')
    print credentialsFile
    print P4LoginWidget.getCredentials(loginMsg='This is my test message.', credentialsFile=credentialsFile)
    
    
