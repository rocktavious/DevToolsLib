from copy import deepcopy

from DTL.api import Path
from DTL.db.data import Node, FloatTransformNode, IntTransformNode, Layer
from DTL.db.properties import StringProperty, IntegerProperty, FloatProperty, BooleanProperty, ListProperty, CustomDataProperty


#------------------------------------------------------------
#------------------------------------------------------------
class Tile(IntTransformNode):    
    #------------------------------------------------------------
    def __init__(self, active=False, name='Tile', **kwds):
        super(Tile, self).__init__(name=name,
                                   **kwds)
        self.name += "_%i_%i" %(self.x, self.y)
        
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
class Map(Node):
    
    #------------------------------------------------------------
    def __init__(self, name='Map', **kwds):
        super(Map, self).__init__(name=name,
                                  **kwds)
    
    #------------------------------------------------------------
    def add_layer(self, name='Layer'):
        new_layer = Layer(index=self.childCount(),
                          name=name,
                          parent=self)
        
        Tile(x=0, y=0, parent=new_layer)
        Tile(x=1, y=0, parent=new_layer)
        
        return new_layer
        
