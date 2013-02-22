from functools import partial
from operator import attrgetter
from PyQt4.QtCore import QSize, QString, QRectF, QPoint, pyqtSignal
from PyQt4.QtGui import QWidget, QToolBar, QListWidgetItem, QInputDialog
from PyQt4.uic import loadUi

class ObjectsDock(QWidget):
    def __init__(self, parent, view):
        super(ObjectsDock, self).__init__(parent=parent)
        self.setObjectName("ShipFloorLayoutObjects")
        self.setWindowTitle("Objects")
        
        self = loadUi(__file__.replace('.pyc','.ui').replace('.py','.ui'), self)
        
        self.toolbar = QToolBar()
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(16, 16))
        
        self.main_layout.addWidget(self.toolbar)
        
        self.objects_list.itemSelectionChanged.connect(self.set_active_object)
            
        
        self.view = view
        self.model = None
        self.layers = dict()
 
    def load(self, model, objects_data_list):
        self.model = model
        
        for name in sorted(objects_data_list.keys()):
            self.objects_list.addItem(QListWidgetItem(name))
        
        
        self.objects_list.setCurrentRow(0)
        self.set_active_object()
    
    def set_active_object(self):
        cur_obj_name = str(self.objects_list.currentItem().text())
        new_obj_model = self.model.add_object(cur_obj_name)
        self.view.set_active_object(new_obj_model)
        