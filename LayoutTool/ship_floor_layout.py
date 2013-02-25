import os.path, json
from functools import partial
import random
from PyQt4.QtCore import QObject, QPoint, QString, QRectF, Qt
from PyQt4.QtGui import QGraphicsView, QGraphicsScene, QColor, QSizePolicy, QGraphicsItem, QGraphicsRectItem, QGraphicsItemGroup, QInputDialog, QMatrix, \
     QPainter, QCursor, QFileDialog, QMessageBox, QPixmap, QBrush

from DTL.api import Path, MainTool, Utils, Start

from models import Map, Object, Tile
from objects import ObjectsDock
from layers import LayersDock
from tile import Tile
from export import convert_map, save_doc


objects_data_list = {"Square":{"rect":QRectF(0,0,10,10)},
                     "Bench":{"rect":QRectF(0,0,5,1)},
                     "Rect":{"rect":QRectF(0,0,20,5)}
                     }

class ShipFloorLayout(MainTool):
    def onInit(self):
        self.ui_file = __file__.replace('.pyc','.ui').replace('.py','.ui')

    def onFinalize(self):
        self.model = None
        self.model_file = None
        self.view = GraphicsView(self)
        self.main_layout.addWidget(self.view)
        self.layers_dock = LayersDock(self, self.view)
        self.editors_layout.addWidget(self.layers_dock)
        self.objects_dock = ObjectsDock(self, self.view)
        self.editors_layout.addWidget(self.objects_dock)
        self.new()
        self.objects_dock.load(self.model, objects_data_list)
                
        self.toolbar.addAction(self.action_New)
        self.toolbar.addAction(self.action_Open)
        self.toolbar.addAction(self.action_Save)
        self.toolbar.addSeparator()
        
        self.action_New.triggered.connect(self.new)
        self.action_Open.triggered.connect(self.open)
        self.action_Save.triggered.connect(self.save)
        self.action_Save_As.triggered.connect(self.save)
        self.action_Export_Cry_Layout.triggered.connect(self.export_cry_layout)

        self.toolbar.addAction(self.action_Select)
        self.toolbar.addAction(self.action_Place)
        self.toolbar.addAction(self.action_Draw)
        self.action_Select.triggered.connect(partial(self.change_tool,1))
        self.action_Place.triggered.connect(partial(self.change_tool,2))
        self.action_Draw.triggered.connect(partial(self.change_tool,3))
        self.action_Draw.setChecked(True)
        self.view.active_tool = 3
        
        self.action_View_Walls.toggled.connect(self.toggle_view_walls)

        self.action_Zoom_In.triggered.connect(partial(self.zoom,2))
        self.action_Zoom_Out.triggered.connect(partial(self.zoom,0.5))
        
        self.action_Rotate_90_CW.triggered.connect(partial(self.rotate,90))
        self.action_Rotate_90_CCW.triggered.connect(partial(self.rotate,-90))   
        
    def zoom(self, value):
        matrix = self.view.matrix()
        matrix.scale(value, value)
        self.view.setMatrix(matrix)
        
    def rotate(self, value):
        self.view.rotate(value)
        
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
            
        self.view.set_active_tool(active_tool)
        
    def toggle_view_walls(self, value):
        self.view.set_show_walls(value)
            
    def new(self):
        self.check_save()
        self.model = Map('New',10,10)
        self.model.add_layer('Default')
        self.layers_dock.load_map(self.model)          
    
    def open(self):
        self.check_save()
        new_model = Map()
        new_model.readJson()
        
        self.layers_dock.load_map(new_model)
        self.model = new_model

    def check_save(self):
        if self.model :
            if Utils.getConfirmDialog("Do you want to save the current map file?") :
                self.save()           
    
    def save(self):
        self.model.saveXml()  
    
    def export_cry_layout(self):
        ###This should get moved into the map model and export.py should be merged into it too
        selected_file = Utils.getSaveFileFromUser()
        if selected_file is None :
            return
        selected_file = os.path.splitext(selected_file.path)[0] + '.xml'
        doc = convert_map(self.model)
        save_doc(doc, selected_file)

    def close_event(self):
        self.check_save()
        pass

    def save_settings(self, settings):
        pass

    def read_settings(self, settings):
        pass

    def shutdown(self):
        pass
    
class GraphicsScene(QGraphicsScene):
    
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent=parent)
        self.layer_rect = None
        
    def keyPressEvent(self, event):
        if not self.selectedItems():
            super(GraphicsScene, self).keyPressEvent(event)
            return
        for item in self.selectedItems():
            if event.modifiers() & Qt.SHIFT :
                move_amount = 16
            else:
                move_amount = 1
            if event.key() == Qt.Key_Down:
                item.moveBy(0, move_amount)
            if event.key() == Qt.Key_Up:
                item.moveBy(0, move_amount * -1)
            if event.key() == Qt.Key_Left:
                item.moveBy(move_amount * -1, 0)
            if event.key() == Qt.Key_Right:
                item.moveBy(move_amount, 0)


class GraphicsView(QGraphicsView):
    
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent=parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setRenderHint(QPainter.Antialiasing)
        self.setScene(GraphicsScene(self))
        self.scene().layer_rect = self.scene().sceneRect()
        
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        
        matrix = self.matrix()
        matrix.scale(1, 1)
        self.setMatrix(matrix)   
        
        self.active_tool = 1
        self.view_walls = False
        self.obj_cmd = None
        self.obj_stamp = None
        
    def set_active_tool(self, value):
        self.active_tool = value
        if self.active_tool == 2 :
            self.setObjectVis(True)
        else:
            self.setObjectVis(False)
        
        self.update_cursors()
        
    def set_show_walls(self, value):
        self.view_walls = value
        for tile_model in self.active_layer.Tiles:
            tile_model.graphic.show_walls(self.view_walls)
        
    def set_active_layer(self, layer_model):
        self.active_layer = layer_model
        self.load_layer(layer_model)
        
    def set_active_object(self, model):
        if self.obj_stamp :
            self.scene().removeItem(self.obj_stamp)
        self.obj_cmd = partial(ObjectGraphic, model)
        self.obj_stamp = self.obj_cmd()
        self.obj_stamp.setVisible(False)
        self.scene().addItem(self.obj_stamp)
        
    def clear(self):
        self.scene().clear()
        
        #Re-setup the cursor following objects
        if self.obj_cmd :
            self.obj_stamp = self.obj_cmd()
            self.scene().addItem(self.obj_stamp)
            self.setObjectVis(False)
        
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space :
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        super(GraphicsView, self).keyPressEvent(event)
        
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)
                self.active_layer.del_object(item.model)
                del item        
        
    def keyReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.RubberBandDrag)
        super(GraphicsView, self).keyReleaseEvent(event)
        
    def mousePressEvent(self, event):
        if self.active_tool == 1 or self.dragMode() == QGraphicsView.ScrollHandDrag:
            super(GraphicsView, self).mousePressEvent(event)
        elif self.active_tool == 3:
            item = self.get_item_under_cursor()
            if item :
                if event.buttons() & Qt.LeftButton :
                    item.setActive(True)
                if event.buttons() & Qt.RightButton:
                    item.setActive(False)
        
        self.update_cursors()
        
    def mouseReleaseEvent(self, event):
        if self.active_tool == 1 or self.dragMode() == QGraphicsView.ScrollHandDrag:
            super(GraphicsView, self).mouseReleaseEvent(event)
        elif self.active_tool == 2:
            self.active_layer.add_object(self.obj_stamp.model)
            self.obj_stamp = self.obj_cmd()
            self.scene().addItem(self.obj_stamp)
            print "Placed"            
        
        self.update_cursors()

                
    def mouseMoveEvent(self, event): 
        self.update_cursors()
        if self.active_tool == 1 or self.dragMode() == QGraphicsView.ScrollHandDrag:
            super(GraphicsView, self).mouseMoveEvent(event)
        elif self.active_tool == 3:
            item = self.get_item_under_cursor()
            if item :
                if event.buttons() & Qt.LeftButton :
                    item.setActive(True)
                if event.buttons() & Qt.RightButton:
                    item.setActive(False)
                    
        self.update_cursors()
        self.update()
        
    def wheelEvent(self, event):
        if event.modifiers() & Qt.CTRL :
            factor = 1.41 ** (event.delta() / 240.0)
            self.scale(factor, factor)
        else:
            super(GraphicsView, self).wheelEvent(event)
            
    def setObjectVis(self, value):
        if not self.obj_stamp :
            return
        if self.active_tool == 2:
            self.obj_stamp.setVisible(value)
        else:
            self.obj_stamp.setVisible(False)        
            
    def get_item_under_cursor(self):
        self.setObjectVis(False)
        item = self.scene().itemAt(self.position()) or None

        self.setObjectVis(True)

        return item
        
    def update_cursors(self):
        if self.obj_stamp and self.obj_stamp.isVisible():
            self.obj_stamp.setPos(self.obj_stamp.test_pos(self.position()))
                
    def load_layer(self, layer_model):
        for item in layer_model.children():
            if isinstance(item.__class__, Tile.__class__):
                new_obj = TileGraphic(item)
                self.scene().addItem(new_obj)
            #if isinstance(item.__class__, Object.__class__):
            #    new_obj = ObjectGraphic(item)
            #    self.scene().addItem(new_obj)
            
        self.scene().layer_rect = self.scene().itemsBoundingRect()
        
    def position(self):
        point = self.mapFromGlobal(QCursor.pos())
        if not self.geometry().contains(point):
            coord = random.randint(36,144)
            point = QPoint(coord, coord)
        return self.mapToScene(point)

        
        
class TileGraphic(QGraphicsItem):
    inactive_color = QColor(100,100,100)
    active_color = QColor(190,210,250)
    selected_color = QColor(100,250,100)
    tile_size = 30
    def __init__(self, model=None):
        super(TileGraphic, self).__init__()
        
        self.model = model
        self.active = model.active
        self.setAcceptsHoverEvents(True)
        self.rect = QRectF(0,0,self.tile_size,self.tile_size)
        self.brush = QBrush()
        self.brush.setColor(self.active_color)
        self.brush.setStyle(Qt.SolidPattern)
        self.setPos(model.x * self.tile_size, model.y * self.tile_size)
        self.setVisible(True)        
        self.setZValue(0)
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsFocusable)
        self.isTile = True
        
    def setActive(self, new_value):
        self.model.active = new_value
        self.active = new_value
        self.update()
        
    def boundingRect(self):
        return self.rect
    
    def paint(self, painter, option, widget):
        if self.active:
            self.brush.setColor(self.active_color)
        else:
            self.brush.setColor(self.inactive_color)
        painter.setBrush(self.brush)
        painter.drawRect(self.rect)


class ObjectGraphic(QGraphicsItem):
    active_color = QColor(200,50,50)
    def __init__(self, model=None):
        super(ObjectGraphic, self).__init__()
        
        self.model = model.copy()
        self.rect = QRectF(0,0,10,10)
        self.brush = QBrush()
        self.brush.setColor(self.active_color)
        self.brush.setStyle(Qt.SolidPattern)
        self.setPos(model.x, model.y)
        self.setVisible(True)        
        self.setZValue(2)
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable|QGraphicsItem.ItemIsFocusable|QGraphicsItem.ItemSendsGeometryChanges)
        self.isObject = True
    
    def itemChange(self, change_type, value):
        if change_type == QGraphicsItem.ItemPositionChange and self.scene():
            new_pos = value.toPointF()
            return self.test_pos(new_pos)

        return super(ObjectGraphic, self).itemChange(change_type, value)
    
    def test_pos(self, new_pos):
        rect = QRectF(new_pos.x(), new_pos.y(), self.rect.width(), self.rect.height())
        scene_rect = self.scene().layer_rect
        if not scene_rect.contains(rect): 
            new_x = min(max(new_pos.x(), scene_rect.left()), scene_rect.right() - 10.0)
            new_y = min(max(new_pos.y(), scene_rect.top()), scene_rect.bottom() - 10.0)
            new_pos = QPoint(new_x, new_y)     
        
        self.model.X = float(new_pos.x())
        self.model.Y = float(new_pos.y())
            
        return new_pos
        
    def boundingRect(self):
        return self.rect
    
    def paint(self, painter, option, widget):
        if self.isSelected() or self.hasFocus():
            self.brush.setColor(self.active_color.light())
        else:
            self.brush.setColor(self.active_color)
        painter.setBrush(self.brush)
        painter.drawRect(self.rect)
    


if __name__ == '__main__':
    ShipFloorLayout()
    Start()