from copy import deepcopy

from DTL.api import Path
from DTL.db.data import Node, FloatTransformNode, IntTransformNode, Layer
from DTL.db.properties import StringProperty, IntegerProperty, FloatProperty, BooleanProperty, ListProperty, CustomDataProperty


#------------------------------------------------------------
#------------------------------------------------------------
class Tile(IntTransformNode):
    #Enum properties for wall types
    
    #------------------------------------------------------------
    def __init__(self, active=False, name='Tile', **kwds):
        super(Tile, self).__init__(name=name,
                                   **kwds)
    
    #------------------------------------------------------------
    def data(self, column):
        r = super(Tile, self).data(column)
        
        #if   column is 5: r = self.active
        
        return r
    
    #------------------------------------------------------------
    def setData(self, column, value):
        super(Tile, self).setData(column, value)
        
        #if   column is 5: self.active = value.toPyObject()


#------------------------------------------------------------
#------------------------------------------------------------
class Object(FloatTransformNode):
    objId = StringProperty(default='', required=True)
    
    #------------------------------------------------------------
    def __init__(self,objId, name='Object', **kwds):
        super(Object, self).__init__(name=name,
                                     **kwds)
        self.objId = objId
        
    #------------------------------------------------------------
    def data(self, column):
        r = super(Object, self).data(column)
        
        if   column is 5: r = self.objId
        
        return r
    
    #------------------------------------------------------------
    def setData(self, column, value):
        super(Object, self).setData(column, value)
        
        if   column is 5: self.objId = value.toPyObject()


#------------------------------------------------------------
#------------------------------------------------------------
class TileLayer(Layer):

    def get_tile(self, x, y, z=0):
        if z == 0 :
            found_tiles = [item for item in self.children() if isinstance(item, Tile)]
            found_tiles = [tile for tile in found_tiles if tile.x == x and tile.y == y]
            if found_tiles :
                return found_tiles[0]
            else:
                return None
        else:
            map_data = self.parent()
            other_layer = map_data.getLayer(self.index + z)
            if other_layer:
                return other_layer.get_tile(x,y)
            else:
                return None


#------------------------------------------------------------
#------------------------------------------------------------
class Map(Node):
    
    #------------------------------------------------------------
    def __init__(self, name='Map', **kwds):
        super(Map, self).__init__(name=name,
                                  **kwds)
        TileLayer(index=0,
                  name='Default',
                  parent=self)
    
    #
    def getLayer(self, index):
        found_layers = [item for item in self.children() if isinstance(item, TileLayer)]
        found_layers = [layer for layer in found_layers if layer.index == index]
        if found_layers :
            return found_layers[0]
        else:
            return None        

