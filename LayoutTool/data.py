from copy import deepcopy

from DTL.api import Path
from DTL.db.data import Node, TransformNode, Layer
from DTL.db.properties import StringProperty, IntegerProperty, FloatProperty, BooleanProperty, ListProperty, CustomDataProperty


#------------------------------------------------------------
#------------------------------------------------------------
class Tile(TransformNode):
    active = BooleanProperty(default=False)
    
    #------------------------------------------------------------
    def __init__(self, active=False, name='Tile', **kwds):
        super(Tile, self).__init__(name=name,
                                   **kwds)
        self.name += "_%i_%i" %(self.x, self.y)
        self.active = active
        
    #------------------------------------------------------------
    def data(self, column):
        r = super(Tile, self).data(column)
        
        if   column is 5: r = self.active
        
        return r
    
    #------------------------------------------------------------
    def setData(self, column, value):
        super(Tile, self).setData(column, value)
        
        if   column is 5: self.active = value.toPyObject()


#------------------------------------------------------------
#------------------------------------------------------------
class Object(TransformNode):
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
    width = IntegerProperty(default=5)
    height = IntegerProperty(default=5)
    
    #------------------------------------------------------------
    def __init__(self, width=5, height=5, name='Map', **kwds):
        super(Map, self).__init__(name=name,
                                  **kwds)
        self.width = width
        self.height = height
        
    #------------------------------------------------------------
    def data(self, column):
        r = super(Map, self).data(column)
        
        if   column is 2: r = self.width
        elif column is 3: r = self.height
        
        return r
    
    #------------------------------------------------------------
    def setData(self, column, value):
        super(Map, self).setData(column, value)
        
        if   column is 2: self.width = value.toPyObject()
        elif column is 3: self.height = value.toPyObject()
    
    #------------------------------------------------------------
    def check_layer_name(self, name):
        for layer in self.children() :
            if layer.Name == name:
                return True
        return False
    
    #------------------------------------------------------------
    def get_layer(self, name):
        for layer in self.children():
            if layer.Name == name:
                return layer
    
    #------------------------------------------------------------
    def add_object(self, name):
        new_obj = Object()
        new_obj.Name = name
        return new_obj
    
    #------------------------------------------------------------
    def add_layer(self, name='Layer'):
        new_layer = Layer(index=self.childCount(),
                          name=name,
                          parent=self)
        
        for x in range(self.width):
            for y in range(self.height):
                Tile(x=float(x), y=float(y), parent=new_layer)
        
        return new_layer
    
    #------------------------------------------------------------
    def del_layer(self, name):
        cur_layer = self.get_layer(name)
        pass #self.Layers = [x for x in self.Layers if x is not cur_layer]
        
