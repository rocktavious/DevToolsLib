import os.path
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from DTL.api import MainTool, Utils, Start
from DTL.db.data import Layer
from DTL.db.controllers import PropertiesEditor, Editor

from data import Map, Tile
from models import MapModel


#------------------------------------------------------------
#------------------------------------------------------------
class MainWindow(MainTool):
    #------------------------------------------------------------
    def onInit(self):
        self.ui_file = os.path.join(os.path.dirname(__file__),'views','main_window.ui')
        self._data = None
        self._model = None  
        self.busy = False  
        self.scene = GraphicsScene()
        self.view = GraphicsView()
        self.view.setScene(self.scene)
        self.treeview = QtGui.QTreeView()
        self.treeview.setSelectionMode(self.treeview.ExtendedSelection)
        self.propertyEditor = LayoutPropertiesEditor()        

    #------------------------------------------------------------
    def onFinalize(self):        
        
        self.setupUI()
        self.new()
        self.setupActions()

        
        self.scene.selectionChanged.connect(self.sceneSelectionChanged)
        
    #------------------------------------------------------------
    def setupUI(self):
        main_splitter = QtGui.QSplitter()
        editors_splitter = QtGui.QSplitter(Qt.Vertical)

        editors_splitter.addWidget(self.treeview)
        editors_splitter.addWidget(self.propertyEditor)

        main_splitter.addWidget(self.view)
        main_splitter.addWidget(editors_splitter)

        self.main_layout.addWidget(main_splitter)
        main_splitter.setSizes([300,250])        
        
    #------------------------------------------------------------
    def setupActions(self):
        self.action_New.triggered.connect(self.new)
        self.action_Open.triggered.connect(self.open)
        self.action_Save.triggered.connect(self.save)
        self.action_Save_As.triggered.connect(self.save)
        self.action_Export_Cry_Layout.triggered.connect(self.export_cry_layout)
        
        self.action_Add_Layer.triggered.connect(self._model.addLayer)
        self.action_Add_Tile.triggered.connect(self._model.addTile)
        
    def setupModel(self):
        if self._model :
            self._model.deleteLater()
        self._model = MapModel(self._data, self)
        
        self.treeview.setModel(self._model)
        self.propertyEditor.setModel(self._model)
        self.scene.setModel(self._model)
        
        self.treeview.selectionModel().selectionChanged.connect(self.smSelectionChanged)
        
    #------------------------------------------------------------
    def new(self):
        self.checkSave()
        
        self._data = Map()
        self._data.add_layer()
        
        self.setupModel()
        
    #------------------------------------------------------------
    def open(self):
        self.checkSave()
        
        self._data = Map()
        self._data.readXml()
        
        print self._data
        
        self.setupModel()
    
    #------------------------------------------------------------
    def checkSave(self):
        if self._model :
            if Utils.getConfirmDialog("Do you want to save the current map file?") :
                self.save()           
    
    #------------------------------------------------------------
    def save(self):
        self._data.saveXml()  
    
    #------------------------------------------------------------
    def export_cry_layout(self):
        ###This should get moved into the map model and export.py should be merged into it too
        selected_file = Utils.getSaveFileFromUser()
        if selected_file is None :
            return
        selected_file = os.path.splitext(selected_file.path)[0] + '.xml'
        doc = convert_map(self._data)
        save_doc(doc, selected_file)
        
    #------------------------------------------------------------
    def close_event(self):
        self.checkSave()

    #------------------------------------------------------------
    def smSelectionChanged(self):
        if not self.busy:
            self.busy = True

            selectedIndexes = self.treeview.selectionModel().selectedIndexes()
            self.scene.clearSelection()
            for index in selectedIndexes :
                self.scene.setSelection(index)
            self.propertyEditor.setSelection(selectedIndexes[-1])

            self.busy = False
    
    #------------------------------------------------------------
    def sceneSelectionChanged(self):
        if not self.busy:
            self.busy = True
            selectionModel = self.treeview.selectionModel()
            
            selectedItems = self.scene.selectedItems()
            selectionModel.clearSelection()
            self.propertyEditor.clearSelection()
            index = None
            for item in selectedItems:
                index = self.getModelIndex(item)
                selectionModel.select(index, QtGui.QItemSelectionModel.Select)
            
            if index :
                self.propertyEditor.setSelection(index)                 
            self.busy = False
            
    #------------------------------------------------------------
    def getModelIndex(self, item):
        persistentIndex = item.index
        if not persistentIndex.isValid() :
            raise Exception('Persistent Model Index is not Valid!')
        return self._model.index(persistentIndex.row(), persistentIndex.column(),persistentIndex.parent())


#------------------------------------------------------------
#------------------------------------------------------------
class GraphicsScene(QtGui.QGraphicsScene):
    #------------------------------------------------------------
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent=parent)
        self._model = None
        self._index_list = list()

    #------------------------------------------------------------
    def setModel(self, model):
        self.clear()
        self._model = model
        model.dataChanged.connect(self.dataChanged)
        self.populate()
        
    #------------------------------------------------------------
    def setSelection(self, index):
        item = self.modelIndexToSceneItem(QtCore.QPersistentModelIndex(index))
        if item :
            print item
            item.setSelected(True)

    #------------------------------------------------------------
    def mousePressEvent(self, event):
        super(GraphicsScene, self).mousePressEvent(event)
        #self.updateItems()

    #------------------------------------------------------------
    def keyPressEvent(self, event):
        super(GraphicsScene, self).keyPressEvent(event)
        for item in self.selectedItems():
            item.keyPressEvent(event)
        self.update()

    #------------------------------------------------------------
    def dataChanged(self, index1, index2):
        self.populate()        
        
    #------------------------------------------------------------
    def modelIndexToSceneItem(self, index):
        index = QtCore.QPersistentModelIndex(index)
        for item in self.items() :
            if self.compareIndexes(index, item.index) :
                return item
        
        return None
    
    #------------------------------------------------------------
    def compareIndexes(self, index1, index2):
        if not index1.isValid() or not index2.isValid() :
            return False
        if index1.row() != index2.row() :
            return False
        if index1.data() != index2.data() :
            return False
        return True

    #------------------------------------------------------------
    def populate(self, parent=QtCore.QModelIndex()):
        count = self._model.rowCount(parent=parent)
        for i in range(count):
            index = self._model.index(i, 0, parent)
            if index : 
                self.addIndex(index)
                self.populate(index)
    
    #------------------------------------------------------------
    def addIndex(self, index):
        if isinstance(index.internalPointer(), Tile) :
            print "Making Tile", index.internalPointer()
            new_item = TileGraphic(index)
            self.addItem(new_item)        


#------------------------------------------------------------
#------------------------------------------------------------
class GraphicsView(QtGui.QGraphicsView):
    #------------------------------------------------------------
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent=parent)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        matrix = self.matrix()
        matrix.scale(1, 1)
        self.setMatrix(matrix)

    def keyPressEvent(self, event):
        super(GraphicsView, self).keyPressEvent(event)
        key_pressed = event.key()
        if key_pressed == Qt.Key_Space:
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        if key_pressed == Qt.Key_Plus or key_pressed == Qt.Key_Equal:
            self.zoom(1.2)
        if key_pressed == Qt.Key_Minus :
            self.zoom(1.0/1.2)
        if key_pressed == Qt.Key_BracketLeft :
            self.rotate(45)
        if key_pressed == Qt.Key_BracketRight :
            self.rotate(-45)

    def keyReleaseEvent(self, event):
        super(GraphicsView, self).keyReleaseEvent(event)
        if event.key() == Qt.Key_Space:
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

    def wheelEvent(self, event):
        factor = 1.41 ** (event.delta() / 240.0)
        self.zoom(factor)
        super(GraphicsView, self).wheelEvent(event)

    def zoom(self, factor):
        self.scale(factor, factor)
        
    def paintEvent(self, event):
        super(GraphicsView, self).paintEvent(event)
        self.scene().setSceneRect(self.scene().itemsBoundingRect())



#------------------------------------------------------------
class LayoutPropertiesEditor(PropertiesEditor):
    #------------------------------------------------------------
    def setEditors(self):
        super(LayoutPropertiesEditor, self).setEditors()
        #self._editors['Tile'] = TileEditor()

#------------------------------------------------------------
#------------------------------------------------------------
class TileEditor(Editor):
    #------------------------------------------------------------
    def onInit(self):
        super(TileEditor, self).onInit()
        self.ui_file = os.path.join(os.path.dirname(__file__),'views','tile_editor.ui')

    #------------------------------------------------------------
    def setMappings(self):
        self._dataMapper.addMapping(self.prop_active, 5)


#------------------------------------------------------------
#------------------------------------------------------------
class TileGraphic(QtGui.QGraphicsItem):
    unselected_color = QtGui.QColor(100,100,100)
    selected_color = QtGui.QColor(100,250,100)
    tile_size = 30
    #------------------------------------------------------------
    def __init__(self, index):
        super(TileGraphic, self).__init__()
        self.index = QtCore.QPersistentModelIndex(index)
        self.model = index.internalPointer()
        self.rect = QtCore.QRectF(self.tile_size * -0.5,
                                  self.tile_size * -0.5,
                                  self.tile_size,
                                  self.tile_size)
        self.brush = QtGui.QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.setFlags(self.ItemIsSelectable)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            self.model.y += 1
        if event.key() == Qt.Key_Up:
            self.model.y += -1
        if event.key() == Qt.Key_Left:
            self.model.x += -1
        if event.key() == Qt.Key_Right:
            self.model.x += 1        

    def boundingRect(self):
        return self.rect

    def shape(self):
        path=QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        if self.isSelected() :
            self.brush.setColor(self.selected_color)
        else:
            self.brush.setColor(self.unselected_color)            
        self.setPos(self.model.x * self.tile_size, self.model.y * self.tile_size)
        self.setZValue(self.model.z)        
        painter.setBrush(self.brush)
        painter.drawRect(self.rect)


#------------------------------------------------------------
#------------------------------------------------------------
if __name__ == '__main__':
    MainWindow()
    Start()