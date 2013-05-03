from DTL.api import InternalError, Path, Utils
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
        
        self.setColumnMap([self.name])


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
        
        self.columnMap().append(self.x)
        self.columnMap().append(self.y)
        self.columnMap().append(self.z)
        

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
    
        self.columnMap().append(self.x)
        self.columnMap().append(self.y)
        self.columnMap().append(self.z)


#------------------------------------------------------------
#------------------------------------------------------------
class Layer(Node):
    index = IntegerProperty(default=0)
    #------------------------------------------------------------
    def __init__(self, index=0, **kwds):
        super(Layer, self).__init__(**kwds)
        self.index = index
    
        self.columnMap().append(self.index)       
    

#------------------------------------------------------------
#------------------------------------------------------------
class Progress(Node):
    total = IntegerProperty(default=1)
    current = IntegerProperty(default=0)
    message = StringProperty(default='Loading...')
    
    #------------------------------------------------------------
    def __init__(self, total=1, current=0, message='Loading...', **kwds):
        super(Progress, self).__init__(**kwds)
        self.total = total
        self.current = current
        self.message = message
                
        self.columnMap().append(self.total) 
        self.columnMap().append(self.current)
        
    #------------------------------------------------------------
    def increment(self):
        self.current += 1
    
    #------------------------------------------------------------
    def percent(self):
        return 1.0 / self.total
    
    #------------------------------------------------------------
    def value(self, recursive=True):
        return (100 * self.current * self.percent())
        