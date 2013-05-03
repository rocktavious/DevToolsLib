import os.path
import subprocess
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from DTL.api import Utils, Path, Enum
from DTL.gui import Core, guiUtils
from DTL.gui.base import BaseGUI


#------------------------------------------------------------
#------------------------------------------------------------
class PathWidget(QtGui.QWidget, BaseGUI):
    pickerTypes = Enum('File','Folder','Node')
    
    pathChanged	= QtCore.pyqtSignal(QtCore.QString)
    editingFinished = QtCore.pyqtSignal()
    
    #------------------------------------------------------------
    def __init__(self, pickerType=None, ext='', **kwds):
        self._qtclass = QtGui.QWidget
        BaseGUI.__init__(self, **kwds)
        if pickerType is None :
            pickerType = PathWidget.pickerTypes.File
        
        Utils.synthesize(self, 'pickerType', pickerType)
        Utils.synthesize(self, 'ext', ext)
        
    #------------------------------------------------------------
    def onFinalize(self):
        self.widgetField.contextMenuEvent = self.extendContextMenuEvent
        self.actionShow_in_explorer.triggered.connect(self.openPath)
        self.widgetFieldPicker.clicked.connect(self.pickFile)
        self.widgetField.textChanged.connect(self.emitPathChanged)
        self.widgetField.editingFinished.connect(self.editingFinished)
    
    #------------------------------------------------------------
    def extendContextMenuEvent(self, event):
        menu = self.widgetField.createStandardContextMenu();
        menu.addAction(self.actionShow_in_explorer)
        menu.exec_(event.globalPos())
        del menu
        
    #------------------------------------------------------------
    def openPath(self):
        userInputPath = Path(str(self.widgetField.text()))
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
                picked = guiUtils.getFileFromUser(ext=self._ext)
            if self.pickerType() == PathWidget.pickerTypes.Folder :
                picked = guiUtils.getDirFromUser()
            if not picked :
                return
        
        self.widgetField.setText(picked)
        
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
    pathWidget = PathWidget(ext='*.py', parent=dlg)
    pathWidget.widgetField.setText("c:/test/my/path.db")
    layout.addWidget(pathWidget)
    
    pathWidget = PathWidget(parent=dlg)
    pathWidget.widgetLabel.setText("Pick a Folder")
    pathWidget.widgetField.setText("c:/test/my/path")
    pathWidget.setPickerType(PathWidget.pickerTypes.Folder)
    layout.addWidget(pathWidget)
    
    dlg.setLayout(layout)
    dlg.show()
    
    Core.Start()