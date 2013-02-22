from copy import deepcopy

from DTL.api import Path
from DTL.db.data import BaseData, JsonData
from DTL.db.properties import StringProperty, IntegerProperty, FloatProperty, BooleanProperty, ListProperty, CustomProperty

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
    Name = StringProperty(default='')
    Id = StringProperty(default='')
    X = FloatProperty(default=0.0)
    Y = FloatProperty(default=0.0)
    
    def dup_object(self):
        new_object = Object()
        new_object.X = self.X
        new_object.Y = self.Y
        new_object.Id = self.Id
        new_object.Name = self.Name
        
        return new_object


class Layer(BaseData):
    Name = StringProperty(default='Default')
    Width = IntegerProperty(default=5)
    Height = IntegerProperty(default=5)
    Index = IntegerProperty(default=0)
    Tiles = ListProperty(Tile)
    Objects = ListProperty(Object)
    
    def __init__(self, name='Default', width=5, height=5, index=0, **kw):
        super(Layer, self).__init__(**kw)
        self.Name = name
        self.Width = width
        self.Height = height
        self.Index = index
 
        for x in range(width):
            for y in range(height):
                self.Tiles = Tile(x,y)
                
    def get_tile(self, x, y):
        found_tiles = [tile for tile in self.Tiles if tile.x == x and tile.y == y]
        if found_tiles :
            return found_tiles[0]
        else:
            return None
                
    def add_object(self, new_obj):
        ids_list = list()
        count = 1
        for obj in [obj for obj in self.Objects if obj.Name == new_obj.Name]:
            ids_list.append(obj.Id)
        
        new_obj.Id = new_obj.Name + '_' + str(count)
        while new_obj.Id in ids_list :
            count += 1
            new_obj.Id = new_obj.Name + '_' + str(count)
        
        self.Objects = new_obj
        
    def del_object(self, rmv_obj):
        self.Objects = [obj for obj in self.Objects if obj.Id is not rmv_obj.Id]
                
    def dup_layer(self):
        new_layer = Layer()
        for tile in self.Tiles:
            new_tile = Tile()
            new_tile.x = tile.x
            new_tile.y = tile.y
            new_tile.Active = tile.Active
            new_layer.Tiles = new_tile
        
        for obj in self.Objects:
            new_obj = Object()
            new_obj.X = obj.X
            new_obj.Y = obj.Y
            new_obj.Name = obj.Name   
            new_obj.Id = obj.Id
            new_layer.Objects = new_obj
        
        return new_layer
    

class Map(JsonData):
    Name = StringProperty(default='New')
    Width = IntegerProperty(default=5)
    Height = IntegerProperty(default=5)
    
    Layers = ListProperty(Layer)
    
    def __init__(self, name='New', width=5, height=5, **kw):
        super(Map, self).__init__(**kw)
        self.Name = name
        self.Width = width
        self.Height = height
        
        self.add_layer('Default')
    
    def check_layer_name(self, name):
        for layer in self.Layers :
            if layer.Name == name:
                return True
        return False
    
    def get_layer(self, name):
        for layer in self.Layers:
            if layer.Name == name:
                return layer
            
    def add_object(self, name):
        new_obj = Object()
        new_obj.Name = name
        return new_obj
    
    def add_layer(self, name):
        new_layer = Layer(name, self.Width, self.Height, len(self.Layers))
        self.Layers = new_layer
        return new_layer
    
    def dup_layer(self, name, new_name):
        cur_layer = self.get_layer(name)
        new_layer = cur_layer.dup_layer()
        new_layer.Name = new_name
        new_layer.Index = len(self.Layers)
        self.Layers = new_layer
        return new_layer
    
    def del_layer(self, name):
        cur_layer = self.get_layer(name)
        self.Layers = [x for x in self.Layers if x is not cur_layer]
        
