from DTL.api import InternalError, Path
from DTL.db.base import BaseData
from DTL.db.properties import StringProperty, FloatProperty, IntegerProperty, BooleanProperty, ListProperty, CustomDataProperty


#------------------------------------------------------------
#------------------------------------------------------------
class Node(BaseData):
    name = StringProperty(default='Node')
    #------------------------------------------------------------
    def __init__(self, name='Node', **kwds):
        super(Node, self).__init__(**kwds)
        self.name = name
        
        self.setColumnMap([self.properties()['name']])


#------------------------------------------------------------
#------------------------------------------------------------
class FloatTransformNode(Node):
    x = FloatProperty(default=0.0)
    y = FloatProperty(default=0.0)
    z = FloatProperty(default=0.0)
    #------------------------------------------------------------
    def __init__(self, x=0.0, y=0.0, z=0.0, **kwds):
        super(FloatTransformNode, self).__init__(**kwds)
        self.x = x
        self.y = y
        self.z = z
        
        self.columnMap().append(self.properties()['x'])
        self.columnMap().append(self.properties()['y'])
        self.columnMap().append(self.properties()['z'])
        

#------------------------------------------------------------
#------------------------------------------------------------
class IntTransformNode(Node):
    x = IntegerProperty(default=0)
    y = IntegerProperty(default=0)
    z = IntegerProperty(default=0)
    #------------------------------------------------------------
    def __init__(self, x=0, y=0, z=0, **kwds):
        super(IntTransformNode, self).__init__(**kwds)
        self.x = x
        self.y = y
        self.z = z
    
        self.columnMap().append(self.properties()['x'])
        self.columnMap().append(self.properties()['y'])
        self.columnMap().append(self.properties()['z'])


#------------------------------------------------------------
#------------------------------------------------------------
class Layer(Node):
    index = IntegerProperty(default=0)
    #------------------------------------------------------------
    def __init__(self, index=0, **kwds):
        super(Layer, self).__init__(**kwds)
        self.index = index
    
        self.columnMap().append(self.properties()['index'])
