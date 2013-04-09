import os.path
import subprocess
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from DTL.gui.base import BaseGUI
from DTL.api import Utils, Path, Enum, Core

#------------------------------------------------------------
#------------------------------------------------------------
class PathWidget(QtGui.QWidget, BaseGUI):
    pickerTypes = Enum('File','Folder','Node')
    
    pathChanged	= QtCore.pyqtSignal( QtCore.QString )
    editingFinished = QtCore.pyqtSignal()
    
    #------------------------------------------------------------
    def __init__(self, *a, **kw):
        self._qtclass = QtGui.QWidget
        BaseGUI.__init__(self, *a, **kw)

        self._pickerType = PathWidget.pickerTypes.File
        self._ext = ''
        
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
        userInputPath = Path(self.widgetField.text())
        if userInputPath.isEmpty :
            return
        subprocess.call('explorer ' + userInputPath.dir.path)
        
    #------------------------------------------------------------
    def pickFile(self):
        picked = None       
        if self.pickerType() == PathWidget.pickerTypes.Node :
            if Core.instance().environment() == Core.CoreEnvironments.Maya :
                picked = Core.instance().getMayaSelection()[0]
            if picked is None:
                return
        else: #Begin Testing for path types
            picked = Path()
            if self.pickerType() == PathWidget.pickerTypes.File :
                picked = Utils.getFileFromUser(ext=self._ext)
            if self.pickerType() == PathWidget.pickerTypes.Folder :
                picked = Utils.getDirFromUser()
            if picked.isEmpty :
                return
            picked = picked.path
            
        self.widgetField.setText(picked)
        
    #------------------------------------------------------------
    def pickerType(self):
        return self._pickerType
        
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
    def setExtFilter(self, ext):
        self._ext = ext

    #------------------------------------------------------------
    def emitPathChanged(self, path):
        if not self.signalsBlocked():
            self.pathChanged.emit(QtCore.QString(path))

if ( __name__ == '__main__' ):
    from PyQt4.QtGui import QVBoxLayout
    import DTL.all as DTL
    from functools import partial
    
    dlg = DTL.Dialog()
    dlg.setWindowTitle( 'Color Test' )
    
    layout = QVBoxLayout()
    pathWidget = PathWidget(dlg)
    #pathWidget.widgetLabel.setText("Pick a File")
    pathWidget.widgetField.setText("c:/test/my/path.db")
    layout.addWidget(pathWidget)
    
    pathWidget = PathWidget(dlg)
    pathWidget.widgetLabel.setText("Pick a Folder")
    pathWidget.widgetField.setText("c:/test/my/path")
    pathWidget.setPickerType(PathWidget.pickerTypes.Folder)
    layout.addWidget(pathWidget)
    
    dlg.setLayout(layout)
    dlg.show()
    
    DTL.Start()