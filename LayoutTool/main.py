import os.path
from functools import partial
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from DTL.api import MainTool, Utils, Start
from DTL.db.models import SceneGraphModel

from controllers import GraphicsView, LayoutPropertiesEditor
from models import GraphicsScene
from data import Map, TileLayer, Tile
from export import exportMap


#------------------------------------------------------------
#------------------------------------------------------------
class MainWindow(MainTool):
    #------------------------------------------------------------
    def onInit(self):
        self.ui_file = os.path.join(os.path.dirname(__file__),'views','main_window.ui')
        self._data = None
        self.model = None
        self.busy = False  
        self.scene = GraphicsScene()
        self.view = GraphicsView()
        self.view.setScene(self.scene)
        self.treeview = QtGui.QTreeView()
        self.treeview.setSelectionMode(self.treeview.ExtendedSelection)
        self.layersview = QtGui.QListView()       
        self.propertyEditor = LayoutPropertiesEditor()        

    #------------------------------------------------------------
    def onFinalize(self):
        self.setupUI()
        self.new()
        self.setupActions()

        self.model.dataChanged.connect(self.view.dataChanged)
        self.scene.selectionChanged.connect(self.sceneSelectionChanged)
        
    #------------------------------------------------------------
    def setupUI(self):
        main_splitter = QtGui.QSplitter()
        editors_splitter = QtGui.QSplitter(Qt.Vertical)

        editors_splitter.addWidget(self.layersview)
        editors_splitter.addWidget(self.propertyEditor)

        main_splitter.addWidget(self.view)
        main_splitter.addWidget(editors_splitter)
        main_splitter.addWidget(self.treeview)

        self.main_layout.addWidget(main_splitter)
        main_splitter.setSizes([300,250,100])        
        
    #------------------------------------------------------------
    def setupActions(self):
        self.action_New.triggered.connect(self.new)
        self.action_Open.triggered.connect(self.open)
        self.action_Save.triggered.connect(self.save)
        self.action_Save_As.triggered.connect(self.save)
        self.action_Export_Cry_Layout.triggered.connect(self.export_cry_layout)
        
        self.action_Select.triggered.connect(partial(self.change_tool,1))
        self.action_Drag.triggered.connect(partial(self.change_tool,2))
        self.action_Draw.triggered.connect(partial(self.change_tool,3))
        self.action_Place.triggered.connect(partial(self.change_tool,4))
        
        self.action_Add_Layer.triggered.connect(self.addLayer)
        #This is not working
        #self.action_Remove_Layer.triggered.connect(self.removeLayer)
        self.action_Add_Tile.triggered.connect(self.addTile)
    
    
    #------------------------------------------------------------
    def change_tool(self, value):
        if value == 1 :
            self.action_Select.setChecked(True)
            active_tool = 1
        else:
            self.action_Select.setChecked(False)
            
        if value == 2 :
            self.action_Place.setChecked(True)
            active_tool = 2
        else:
            self.action_Place.setChecked(False)
            
        if value == 3 :
            self.action_Draw.setChecked(True)
            active_tool = 3
        else:
            self.action_Draw.setChecked(False)
            
        self.view.setTool(active_tool)
        
    #------------------------------------------------------------
    def setupModel(self):
        if self.model :
            self.model.deleteLater()
        self.model = SceneGraphModel(self._data, self)
        
        self.layersview.setModel(self.model)
        self.treeview.setModel(self.model)
        self.propertyEditor.setModel(self.model)
        self.scene.setModel(self.model)
        
        self.treeview.selectionModel().selectionChanged.connect(self.smSelectionChanged)
        #self.layersview.setSelectionModel(self.treeview.selectionModel())
        self.layersview.selectionModel().selectionChanged.connect(self.layersSelectionChanged)
        
    #------------------------------------------------------------
    def new(self):
        self.checkSave()
        
        self._data = Map()        
        
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
        if self.model :
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
        exportMap(self._data, selected_file)
        
    #------------------------------------------------------------
    def addTile(self):
        new_tile = None
        selectedIndexes = self.layersview.selectionModel().selectedIndexes()
        if len(selectedIndexes) == 1:
            new_tile = Tile()
            self.scene.insertNode(new_tile, selectedIndexes[0])
        
        return new_tile
    
    #------------------------------------------------------------
    def addLayer(self, name=None):
        name, success = Utils.getUserInput('Enter new layer name:')
        
        if success:
            layer_count = self.model.rowCount(QtCore.QModelIndex())
            new_layer = TileLayer(index=layer_count,
                                  name=name)
                   
            new_index = self.scene.insertNode(new_layer, QtCore.QModelIndex())
            self.layersview.selectionModel().select(new_index, QtGui.QItemSelectionModel.ClearAndSelect)
            for x in range(5):
                for y in range(5):
                    new_tile = self.addTile()
                    new_tile.x = x
                    new_tile.y = y

        return success
    
    #------------------------------------------------------------
    def removeLayer(self):
        selectedIndexes = self.layersview.selectionModel().selectedIndexes()
        for index in selectedIndexes :
            self.scene.removeNode(index.row(), index)
        
    #------------------------------------------------------------
    def close_event(self):
        self.checkSave()
        
    #------------------------------------------------------------
    def layersSelectionChanged(self):
        if not self.busy:
            self.busy = True
            
            selectedIndexes = self.layersview.selectionModel().selectedIndexes()
            self.scene.clearSelection()
            self.propertyEditor.clearSelection()
            if len(selectedIndexes) == 1:
                self.scene.setActiveLayer(selectedIndexes[0])
                self._activeLayerIndex = QtCore.QPersistentModelIndex(selectedIndexes[0])
                self.propertyEditor.setSelection(selectedIndexes[0]) 
            
            self.busy = False

    #------------------------------------------------------------
    def smSelectionChanged(self):
        if not self.busy:
            self.busy = True

            selectedIndexes = self.treeview.selectionModel().selectedIndexes()
            self.scene.clearSelection()
            self.propertyEditor.clearSelection()         
            for index in selectedIndexes :
                self.scene.setSelection(index)
            if len(selectedIndexes) == 1:
                self.propertyEditor.setSelection(selectedIndexes[0])
                

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
                pass
                #This seems to really slow the selection update
                #selectionModel.select(item.getIndex(), QtGui.QItemSelectionModel.Select)
            if len(selectedItems) == 1:
                self.propertyEditor.setSelection(selectedItems[0].getIndex())
            
            self.busy = False
            
    #------------------------------------------------------------
    def getModelIndex(self, item):
        persistentIndex = item.index
        if not persistentIndex.isValid() :
            raise Exception('Persistent Model Index is not Valid!')
        return self.model.index(persistentIndex.row(), persistentIndex.column(),persistentIndex.parent())


#------------------------------------------------------------
#------------------------------------------------------------
if __name__ == '__main__':
    MainWindow()
    Start()