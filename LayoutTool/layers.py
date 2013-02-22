from functools import partial
from operator import attrgetter
from PyQt4.QtCore import QSize, QString, pyqtSignal
from PyQt4.QtGui import QWidget, QToolBar, QListWidgetItem, QInputDialog
from PyQt4.uic import loadUi

from DTL.api import Utils


class LayersDock(QWidget):
    def __init__(self, parent, view):
        super(LayersDock, self).__init__(parent=parent)
        self.setObjectName("ShipFloorLayoutLayers")
        self.setWindowTitle("Layers")
        
        self = loadUi(__file__.replace('.pyc','.ui').replace('.py','.ui'), self)
        
        self.toolbar = QToolBar()
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(16, 16))
        
        self.toolbar.addAction(parent.action_Add_Layer)
        self.toolbar.addAction(parent.action_Raise_Layer)
        self.toolbar.addAction(parent.action_Lower_Layer)
        self.toolbar.addAction(parent.action_Duplicate_Layer)
        self.toolbar.addSeparator()
        self.toolbar.addAction(parent.action_Remove_Layer)
        
        self.main_layout.addWidget(self.toolbar)
        
        parent.action_Raise_Layer.triggered.connect(partial(self.move_layer,-1))
        parent.action_Lower_Layer.triggered.connect(partial(self.move_layer,1))
        parent.action_Add_Layer.triggered.connect(self.add_layer)
        parent.action_Remove_Layer.triggered.connect(self.del_layer)
        parent.action_Duplicate_Layer.triggered.connect(self.dup_layer)
        
        self.layers_list.itemSelectionChanged.connect(self.show_layer)
        
        self.view = view
        self.model = None
 
    def load_map(self, map_model):
        self.layers_list.clear()
        self.view.clear()
        self.model = None
        self.model = map_model
         
        for layer_model in sorted(self.model.Layers, key=attrgetter('Index')) :
            self.layers_list.addItem(QListWidgetItem(layer_model.Name))
        
        
        self.layers_list.setCurrentRow(0)
        
    def move_layer(self, value):
        cur_row = self.layers_list.currentRow()
        new_row = cur_row + value
        #Check if top or bottom and just ingore the command
        if cur_row == self.layers_list.count() -1 and value == 1:
            return
        if cur_row == 0 and value == -1:
            return
        
        cur_item = self.layers_list.takeItem(cur_row)
        self.layers_list.insertItem(new_row, cur_item)
        self.layers_list.setCurrentRow(new_row)
        self.reindex_layers()
        
    def add_layer(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 
            'Enter new layer name:')
        
        if ok:
            new_layer_name = str(text)
            if self.model.check_layer_name(new_layer_name):
                Utils.notifyUser('Duplicate Layer Name!', self)
                return
            new_layer_model = self.model.add_layer(new_layer_name)    
            self.layers_list.addItem(QListWidgetItem(new_layer_model.Name))
            self.layers_list.setCurrentRow(self.layers_list.count() - 1)
            self.reindex_layers()
            
    def del_layer(self):
        cur_row_count = self.layers_list.count() -1
        cur_row = self.layers_list.currentRow()
        cur_list_item = self.layers_list.takeItem(cur_row)
        cur_layer_name = str(cur_list_item.text())
        
        if cur_row == cur_row_count:
            self.layers_list.setCurrentRow(cur_row - 1)
        if cur_row == 0:
            self.layers_list.setCurrentRow(0)
        
        self.model.del_layer(cur_layer_name)
        
        del cur_list_item
        
        self.reindex_layers()
    
    def dup_layer(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 
            'Enter new layer name:')
        
        if ok:
            new_layer_name = str(text)
            if self.model.check_layer_name(new_layer_name):
                Utils.notifyUser('Duplicate Layer Name!', self)
                return
            cur_layer_name = str(self.layers_list.currentItem().text())
            new_layer_model = self.model.dup_layer(cur_layer_name, new_layer_name)
            self.layers_list.addItem(QListWidgetItem(new_layer_model.Name))
            self.layers_list.setCurrentRow(self.layers_list.count() - 1)
            self.reindex_layers()
    
    def reindex_layers(self):
        for row in range(self.layers_list.count()):
            item = self.layers_list.item(row)
            layer_model = self.model.get_layer(str(item.text()))
            layer_model.Index = row
        
    def show_layer(self):
        self.view.clear()
        cur_item = self.layers_list.currentItem()
        if cur_item :
            layer_model = self.model.get_layer(str(cur_item.text()))
            self.view.set_active_layer(layer_model)
        