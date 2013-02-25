from copy import deepcopy

from DTL.api import Path
from DTL.db.data import BaseData
from DTL.db.properties import StringProperty, IntegerProperty, FloatProperty, BooleanProperty, ListProperty, CustomDataProperty

class Tile(BaseData):
    active = BooleanProperty(default=False)
    x = IntegerProperty(default=0)
    y = IntegerProperty(default=0)
    z = IntegerProperty(default=0)
    
    def __init__(self, x=0, y=0, z=0, active=False, **kw):
        super(Tile, self).__init__(**kw)
        self.x = x
        self.y = y
        self.z = z
        self.active = active

class Object(BaseData):
    name = StringProperty(default='')
    objId = StringProperty(default='')
    x = FloatProperty(default=0.0)
    i = FloatProperty(default=0.0)
    
    def __init__(self, x=0.0, y=0.0, objId='', name='', **kw):
        super(Object, self).__init__(**kw)
        self.x = x
        self.y = y
        self.objId = objId
        self.name = name
    
    def dup_object(self):
        new_object = Object(self.x, self.y, self.objId, self.name)
        return new_object


class Layer(BaseData):
    Name = StringProperty(default='Default')
    Width = IntegerProperty(default=5)
    Height = IntegerProperty(default=5)
    Index = IntegerProperty(default=0)
    
    def __init__(self, name='Default', width=5, height=5, index=0, **kw):
        super(Layer, self).__init__(**kw)
        self.Name = name
        self.Width = width
        self.Height = height
        self.Index = index
 
        for x in range(width):
            for y in range(height):
                Tile(x,y, parent=self)
                
    def get_tile(self, x, y):
        found_tiles = [tile for tile in self.Tiles if tile.x == x and tile.y == y]
        if found_tiles :
            return found_tiles[0]
        else:
            return None
                
    def add_object(self, new_obj):
        ids_list = list()
        count = 1
        for obj in [obj for obj in self.children() if obj.Name == new_obj.Name]:
            ids_list.append(obj.Id)
        
        new_obj.Id = new_obj.Name + '_' + str(count)
        while new_obj.Id in ids_list :
            count += 1
            new_obj.Id = new_obj.Name + '_' + str(count)
        
        self.addChild(new_obj)
        
    def del_object(self, rmv_obj):
        pass #self.Objects = [obj for obj in self.Objects if obj.Id is not rmv_obj.Id]
                
    def dup_layer(self):
        new_layer = Layer()
        for tile in self.Tiles:
            Tile(tile.x, tile.y, 0, tile.active, parent=self)
        
        for obj in self.Objects:
            Object(obj.x, obj.y, obj.objId, obj.name, parent=self)
        
        return new_layer
    

class Map(BaseData):
    Name = StringProperty(default='New')
    Width = IntegerProperty(default=5)
    Height = IntegerProperty(default=5)
    
    def __init__(self, name='New', width=5, height=5, **kw):
        super(Map, self).__init__(**kw)
        self.Name = name
        self.Width = width
        self.Height = height
    
    def check_layer_name(self, name):
        for layer in self.children() :
            if layer.Name == name:
                return True
        return False
    
    def get_layer(self, name):
        for layer in self.children():
            if layer.Name == name:
                return layer
            
    def add_object(self, name):
        new_obj = Object()
        new_obj.Name = name
        return new_obj
    
    def add_layer(self, name):
        new_layer = Layer(name, self.Width, self.Height, self.childCount())
        self.addChild(new_layer)
        return new_layer
    
    def dup_layer(self, name, new_name):
        cur_layer = self.get_layer(name)
        new_layer = cur_layer.dup_layer()
        new_layer.Name = new_name
        new_layer.Index = len(self.Layers)
        self.addChild(new_layer)
        return new_layer
    
    def del_layer(self, name):
        cur_layer = self.get_layer(name)
        pass #self.Layers = [x for x in self.Layers if x is not cur_layer]
        
