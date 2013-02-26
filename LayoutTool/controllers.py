import os.path
from PyQt4 import QtCore, QtGui
from DTL.api import MainTool, Start
from DTL.db.models import SceneGraphModel
from DTL.db.controllers import PropertiesEditor

from data import Map

class MainWindow(MainTool):
    def onInit(self):
        self.ui_file = os.path.join(os.path.dirname(__file__),'views','main_window.ui')
        
    def onFinalize(self):
        
        main_splitter = QtGui.QSplitter()
        
        view = GraphicsView()
        
        
        editors_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        layers = QtGui.QTreeView()
        objects = LayoutPropertiesEditor()
        editors_splitter.addWidget(layers)
        editors_splitter.addWidget(objects)
        
        main_splitter.addWidget(view)
        main_splitter.addWidget(editors_splitter)
        
        
        self.main_layout.addWidget(main_splitter)
        main_splitter.setSizes([300,250])
        
        
        self._data = Map()
        self._data.add_layer()
        self._data.add_layer()
        self._model = SceneGraphModel(self._data, self)
        layers.setModel(self._model)
        objects.setModel(self._model)
        view.setModel(self._model)
        
        QtCore.QObject.connect(layers.selectionModel(),
                               QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"),
                               objects.setSelection)
        
class GraphicsScene(QtGui.QGraphicsScene):
    
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent=parent)
        self.layer_rect = None
        
    def keyPressEvent(self, event):
        if not self.selectedItems():
            super(GraphicsScene, self).keyPressEvent(event)
            return
        for item in self.selectedItems():
            if event.modifiers() & QtCore.Qt.SHIFT :
                move_amount = 16
            else:
                move_amount = 1
            if event.key() == QtCore.Qt.Key_Down:
                item.moveBy(0, move_amount)
            if event.key() == QtCore.Qt.Key_Up:
                item.moveBy(0, move_amount * -1)
            if event.key() == QtCore.Qt.Key_Left:
                item.moveBy(move_amount * -1, 0)
            if event.key() == QtCore.Qt.Key_Right:
                item.moveBy(move_amount, 0)


class GraphicsView(QtGui.QGraphicsView):
    
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent=parent)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setScene(GraphicsScene(self))
        self.scene().layer_rect = self.scene().sceneRect()
        
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        matrix = self.matrix()
        matrix.scale(1, 1)
        self.setMatrix(matrix)
        
    def setModel(self, model):
        print model


class LayoutPropertiesEditor(PropertiesEditor):
    
    def setEditors(self):
        super(LayoutPropertiesEditor, self).setEditors()

if __name__ == '__main__':
    MainWindow()
    Start()