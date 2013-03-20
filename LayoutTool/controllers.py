import time

import os.path
from functools import partial
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from DTL.db.controllers import PropertiesEditor, Editor


#------------------------------------------------------------
#------------------------------------------------------------
class GraphicsView(QtGui.QGraphicsView):
    #------------------------------------------------------------
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent=parent)
        self.setDragMode(QtGui.QGraphicsView.NoDrag)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setInteractive(True)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.busy = False
        
        self.rubberBanding = False
        self.rubberBand = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle, self)
        self.rubberBandStart = QtCore.QPoint(0,0)
        self.rubberBandRect = QtCore.QRect(self.rubberBandStart, QtCore.QSize())
        self.rubberBandCurrentSelection = list()
        
        self.scrollStart = QtCore.QPoint(0,0)

        matrix = self.matrix()
        matrix.scale(1, 1)
        self.setMatrix(matrix)
        
    def dataChanged(self, current, old):
        if not self.busy :
            self.repaint()
            
    def setTool(self, value):
        if value == 1 :
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)           
                
        if value == 2 :
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
                
        if value == 3 :
            self.setDragMode(QtGui.QGraphicsView.NoDrag) 

    def keyPressEvent(self, event):
        self.busy = True
        super(GraphicsView, self).keyPressEvent(event)
        key_pressed = event.key()

        for item in self.scene().selectedItems():
            
            if event.key() == Qt.Key_Down:
                currentValue = item.data(3)
                item.setData(3, currentValue + 1)
            if event.key() == Qt.Key_Up:
                currentValue = item.data(3)
                item.setData(3, currentValue + -1)
            if event.key() == Qt.Key_Left:
                currentValue = item.data(2)
                item.setData(2, currentValue + -1)            
            if event.key() == Qt.Key_Right:
                currentValue = item.data(2)
                item.setData(2, currentValue + 1)  
            item.ensureVisible()
        
        if key_pressed == Qt.Key_Plus or key_pressed == Qt.Key_Equal:
            self.zoom(1.2)
        if key_pressed == Qt.Key_Minus :
            self.zoom(1.0/1.2)
        if key_pressed == Qt.Key_BracketLeft :
            self.rotate(45)
        if key_pressed == Qt.Key_BracketRight :
            self.rotate(-45)
            
        if key_pressed & Qt.Key_Shift :
            self.setDragMode(self.RubberBandDrag)        
        
        self.busy = False
        self.repaint()

    def keyReleaseEvent(self, event):
        super(GraphicsView, self).keyReleaseEvent(event)
        self.setDragMode(self.NoDrag)
            
    def mousePressEvent(self, event):
        self.busy = True
        if event.buttons() & Qt.RightButton:
            self.setFocus(True)
        elif self.dragMode() == self.RubberBandDrag :
            self.rubberBanding = True
            self.rubberBandStart = event.pos()
            if event.modifiers() & Qt.ControlModifier :
                self.rubberBandCurrentSelection = self.scene().selectedItems()
            self.rubberBandRect = QtCore.QRect(self.rubberBandStart, QtCore.QSize()).normalized()
            self.rubberBand.setGeometry(self.rubberBandRect)
            self.rubberBand.show()
        else:
            if self.dragMode() == self.ScrollHandDrag :
                item = self.scene().itemAt(self.mapToScene(event.pos()))
                if item :
                    currentFlags = item.flags()
                    item.setFlag(item.ItemIsSelectable, False)
                    item.setFlag(item.ItemIsFocusable, False)
                    item.setFlag(item.ItemIsMovable, False)
            super(GraphicsView, self).mousePressEvent(event)
            if self.dragMode() == self.ScrollHandDrag :
                item.setFlags(currentFlags)
                
                
                
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.RightButton :
            pass
        elif self.dragMode() == self.RubberBandDrag and self.rubberBanding :
            self.rubberBandRect = QtCore.QRect(self.rubberBandStart, event.pos()).normalized()
            self.rubberBand.setGeometry(self.rubberBandRect)
        else:
            super(GraphicsView, self).mouseMoveEvent(event)
            
            for item in self.scene().selectedItems():
                point = item.pos()
                newX = divmod(point.x() + 10, item.tile_size)[0]
                newY = divmod(point.y() + 10, item.tile_size)[0]                
                item.setData(2, newX)
                item.setData(3, newY)
            

    def mouseReleaseEvent(self, event):
        if event.buttons() & Qt.RightButton:
            pass
        elif self.dragMode() == self.RubberBandDrag and self.rubberBanding:
            self.rubberBanding = False
            self.rubberBand.hide()
            selectionRect = self.mapToScene(self.rubberBandRect)
            self.scene().setSelectionArea(selectionRect, self.rubberBandSelectionMode(), self.viewportTransform(), self.rubberBandCurrentSelection)
            if self.viewportUpdateMode() != self.NoViewportUpdate :
                self.update()
            self.rubberBandCurrentSelection = list()        
        else:
            super(GraphicsView, self).mouseReleaseEvent(event)
             
        self.busy = False
        self.repaint()

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ShiftModifier :
            super(GraphicsView, self).wheelEvent(event)
        else:
            factor = 1.41 ** (event.delta() / 240.0)
            self.zoom(factor)

    def zoom(self, factor):
        self.scale(factor, factor)
        
    def paintEvent(self, event):
        super(GraphicsView, self).paintEvent(event)
        if not self.busy :
            self.scene().setSceneRect(self.scene().itemsBoundingRect())



#------------------------------------------------------------
class LayoutPropertiesEditor(PropertiesEditor):
    #------------------------------------------------------------
    def setEditors(self):
        super(LayoutPropertiesEditor, self).setEditors()
        self._editors['Tile'] = TileEditor()

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




        



