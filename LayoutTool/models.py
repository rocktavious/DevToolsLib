import os.path
from functools import partial
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from DTL.api import Utils
from DTL.db.models import GraphicsSceneModel, GraphicsItemModel

from data import TileLayer, Tile

#------------------------------------------------------------
#------------------------------------------------------------
class GraphicsScene(GraphicsSceneModel):

    #------------------------------------------------------------
    def populateScene(self, parent=QtCore.QModelIndex()):
        count = self.model.rowCount(parent=parent)
        for i in reversed(range(count)):
            index = self.model.index(i, 0, parent)
            if index : 
                self.addIndex(index, False)
                self.populateScene(index)
    
    #------------------------------------------------------------
    def setActiveLayer(self, parent=QtCore.QModelIndex()):
        for item in self.items() :
            item.setEnabled(False)
            item.setVisible(False)
        
        for i in range(self.model.rowCount(QtCore.QModelIndex())):
            newLayer = self.model.index(i, 0, QtCore.QModelIndex())
            if i == parent.row():
                for j in range(self.model.rowCount(parent=newLayer)):
                    index = self.model.index(j, 0, newLayer)
                    if index : 
                        item = self.modelIndexToSceneItem(index)
                        if item :
                            item.setEnabled(True)
                            item.setVisible(True)
                            item.setOpacity(1.0)
            
            #This enables one layer ghosting which is really slow right now for larger maps
            #if i == parent.row() + 1:
                #for j in range(self.model.rowCount(parent=newLayer)):
                    #index = self.model.index(j, 0, newLayer)
                    #if index : 
                        #item = self.modelIndexToSceneItem(index)
                        #if item :
                            #item.setEnabled(False)
                            #item.setVisible(True)
                            #item.setOpacity(0.3)
        
    #------------------------------------------------------------
    def addIndex(self, index, selected=True):
        if isinstance(index.internalPointer(), Tile) :
            new_item = TileGraphic(index)
            self.addItem(new_item)
            new_item.setSelected(selected)
    
    #------------------------------------------------------------
    def removeIndex(self, index):
        if isinstance(index.internalPointer(), Tile) :
            item = self.modelIndexToSceneItem(index)
            item = self.removeItem(item)
            del item
    
    #------------------------------------------------------------
    def setSelectionArea(self, selectionRect, selectionMode, deviceTransform, currentSelection):
        self.blockSignals(True)
        path = QtGui.QPainterPath()
        path.addRect(selectionRect.boundingRect())
        super(GraphicsScene, self).setSelectionArea(path, selectionMode, deviceTransform)
        for item in currentSelection :
            item.setSelected(True)
        self.blockSignals(False)
        self.selectionChanged.emit()


#------------------------------------------------------------
#------------------------------------------------------------
class TileGraphic(GraphicsItemModel):
    tile_size = 30
    #------------------------------------------------------------
    def onInit(self):
        self.rect = QtCore.QRectF(self.tile_size * -0.5,
                                  self.tile_size * -0.5,
                                  self.tile_size,
                                  self.tile_size)
        self.brush.setStyle(Qt.SolidPattern)
        self.shape.addRect(self.rect)
        self.setFlags(self.ItemIsSelectable | self.ItemIsFocusable | self.ItemIsMovable)
            
    #------------------------------------------------------------
    def paint(self, painter, option, widget):
        #**********
        #Hack
        #**********
        if not self.scene().views()[0].busy :
            self.setPos(self.data(2) * self.tile_size, self.data(3) * self.tile_size)
            self.setZValue(self.data(4))
        
        super(TileGraphic, self).paint(painter, option, widget)