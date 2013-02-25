import json
import re
from PyQt4 import QtXml

from DTL.api import InternalError, Path


from .base import BaseData
from .properties import StringProperty, FloatProperty, IntegerProperty, BooleanProperty, ListProperty, CustomDataProperty


#------------------------------------------------------------
#------------------------------------------------------------
class Node(BaseData):
    name = StringProperty(default='',required=True)
    #------------------------------------------------------------
    def __init__(self, name, *a):
        super(Node, self).__init__(*a)
        self.name = name
    
    #------------------------------------------------------------
    def name():
        def fget(self): return self._name
        def fset(self, value): self._name = value
        return locals()
    name = property(**name())
    
    #------------------------------------------------------------
    def data(self, column):
        if   column is 0: return self.name
        elif column is 1: return self.typeInfo()
    
    #------------------------------------------------------------
    def setData(self, column, value):
        if   column is 0: self.name = value.toPyObject()
        elif column is 1: pass


#------------------------------------------------------------
#------------------------------------------------------------
class TransformNode(Node):
    x = FloatProperty(default=0.0)
    y = FloatProperty(default=0.0)
    z = FloatProperty(default=0.0)
    #------------------------------------------------------------
    def __init__(self, x=0.0, y=0.0, z=0.0, *a):
        super(TransformNode, self).__init__(*a)
        self.x = x
        self.y = y
        self.z = z
    
    #------------------------------------------------------------
    def data(self, column):
        r = super(TransformNode, self).data(column)
        
        if   column is 2: r = self.x
        elif column is 3: r = self.y
        elif column is 4: r = self.z
        
        return r
    
    #------------------------------------------------------------
    def setData(self, column, value):
        super(TransformNode, self).setData(column, value)
        
        if   column is 2: self.x = value.toPyObject()
        elif column is 3: self.y = value.toPyObject()
        elif column is 4: self.z = value.toPyObject()



        
        
        
        

        
