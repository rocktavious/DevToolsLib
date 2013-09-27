import os.path
import subprocess
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from DTL.api import apiUtils, Path, Enum
from DTL.gui import Core, Widget, guiUtils


#------------------------------------------------------------
#------------------------------------------------------------
class PathWidget(Widget):
    pickerTypes = Enum('File','Folder','Node')
    
    pathChanged	= QtCore.pyqtSignal(QtCore.QString)
    editingFinished = QtCore.pyqtSignal()
    
    #------------------------------------------------------------
    def onFinalize(self, pickerType=None, ext='', label='', field=''):
        apiUtils.synthesize(self, 'pickerType', PathWidget.pickerTypes.File)
        self.setPickerType(pickerType)
        apiUtils.synthesize(self, 'ext', ext)
        self.setLabel(label)
        self.setField(field)
        
        self.ui_Field.contextMenuEvent = self.extendContextMenuEvent
        self.actionShow_in_explorer.triggered.connect(self.openPath)
        self.ui_Picker.clicked.connect(self.pickFile)
        self.ui_Field.textChanged.connect(self.emitPathChanged)
        self.ui_Field.editingFinished.connect(self.editingFinished)
    
    #------------------------------------------------------------
    def extendContextMenuEvent(self, event):
        menu = self.ui_Field.createStandardContextMenu();
        menu.addAction(self.actionShow_in_explorer)
        menu.exec_(event.globalPos())
        del menu
        
    #------------------------------------------------------------
    def openPath(self):
        userInputPath = Path(str(self.ui_Field.text()))
        if userInputPath :
            subprocess.call('explorer ' + userInputPath.dir().caseSensative())
        
    #------------------------------------------------------------
    def pickFile(self):
        picked = None       
        if self.pickerType() == PathWidget.pickerTypes.Node :
            if Core.environment() == Core.EnvironmentTypes.Maya :
                picked = Core.getMayaSelection()[0]
            if picked is None:
                return
        else: #Begin Testing for path types
            if self.pickerType() == PathWidget.pickerTypes.File :
                picked = guiUtils.getFileFromUser(ext=self.ext)
            if self.pickerType() == PathWidget.pickerTypes.Folder :
                picked = guiUtils.getDirFromUser()
            if not picked :
                return
        
        self.ui_Field.setText(picked)
        
    #------------------------------------------------------------
    def setPickerType(self, pickerType):
        temp = None
        if isinstance(pickerType, str):
            temp = PathWidget.pickerTypes.names.index(pickerType)
        else:
            temp = pickerType
        
        if temp and PathWidget.pickerTypes.names[temp]:
            self._pickerType = temp
    
    #------------------------------------------------------------
    def setLabel(self, label):
        self.ui_Label.setText(label)
        
    #------------------------------------------------------------
    def setField(self, field):
        self.ui_Field.setText(field)

    #------------------------------------------------------------
    def emitPathChanged(self, path):
        if not self.signalsBlocked():
            self.pathChanged.emit(QtCore.QString(path))



if ( __name__ == '__main__' ):
    from PyQt4.QtGui import QVBoxLayout
    from DTL.gui import Core, Dialog
    from functools import partial
    
    dlg = Dialog()
    dlg.setWindowTitle( 'Pathwidget Test' )
    
    layout = QVBoxLayout()
    pathWidget = PathWidget(ext='*.py',
                            label='Pick File',
                            parent=dlg)
    layout.addWidget(pathWidget)
    
    pathWidget = PathWidget(label='Pick Folder',
                            pickerType=PathWidget.pickerTypes.Folder,
                            field='c:/test/my/path',
                            parent=dlg)
    layout.addWidget(pathWidget)
    
    dlg.setLayout(layout)
    dlg.show()
    
    
    Core.Start()