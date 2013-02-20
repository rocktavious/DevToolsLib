import json
from PyQt4 import QtXml

from .properties import StringProperty, FloatProperty, IntegerProperty, BooleanProperty
from .. import InternalError

RESERVED_PROPERTY_NAME = re.compile('^__.*__$')

RESERVED_WORDS = ['addChild',
                  'asJson',
                  'asXml',
                  'child',
                  'childCount',
                  'insertChild',
                  'parent',
                  'properties',
                  'removeChild',
                  'resource',
                  'row',
                  'typeInfo',
                  '']

#------------------------------------------------------------
#------------------------------------------------------------
class ReservedWordError(InternalError):
    """Raised when a property is defined for a reserved word."""


#------------------------------------------------------------
def check_reserved_word(attr_name):
    """Raise an exception if attribute name is a reserved word.

    Args:
      attr_name: Name to check to see if it is a reserved word.

    Raises:
      ReservedWordError when attr_name is determined to be a reserved word.
    """
    if RESERVED_PROPERTY_NAME.match(attr_name):
        raise ReservedWordError(
            "Cannot define property.  All names both beginning and "
            "ending with '__' are reserved.")

    if attr_name in RESERVED_WORDS or attr_name in dir(Model):
        raise ReservedWordError(
            "Cannot define property using reserved word '%(attr_name)s'. "
            "If you would like to use this name in the datastore consider "
            "using a different name like %(attr_name)s_ and adding "
            "name='%(attr_name)s' to the parameter list of the property "
            "definition." % locals())


#------------------------------------------------------------
#------------------------------------------------------------
class PropertiedClass(type):
    #------------------------------------------------------------
    def __init__(cls, name, bases, dct):
        super(PropertiedClass, cls).__init__(name, bases, dct)
        cls._properties = {}
        for base in bases:
            if hasattr(base, '_properties'):
                property_keys = set(base._properties.keys())
                if property_keys:
                    cls._properties.update(base.properties())
                    
        for name, attr in dct.items():
            if isinstance(attr, Property):
                check_reserved_word(name)
                cls._properties[name] = attr
                attr.__property_config__(cls, name)


#------------------------------------------------------------
#------------------------------------------------------------
class BaseData(object):
    __metaclass__ = PropertiedClass
    #------------------------------------------------------------
    def __init__(self, parent=None):
        super(BaseData, self).__init__()
        self._parent = parent
        self._children = []
        
        if parent is not None:
            parent.addChild(self)
    
    #------------------------------------------------------------
    def __repr__(self):
        output = self.__class__.__name__ + '( '
        for key, prop in sorted(self.properties().items()):
            output += str(key) + '=' + str(prop.get_value(self)) + ', '
        output = output[:-2] + ' )'
        return str(output)
            
    #------------------------------------------------------------
    def addChild(self, child):
        self._children.append(child)
        child._parent = self
        
    #------------------------------------------------------------
    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False
        
        self._children.insert(position, child)
        child._parent = self
        return True
    
    #------------------------------------------------------------
    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False
        
        child = self._children.pop(position)
        child._parent = None

        return True
    
    #------------------------------------------------------------
    def child(self, row):
        return self._children[row]
    
    #------------------------------------------------------------
    def childCount(self):
        return len(self._children)
    
    #------------------------------------------------------------
    def parent(self):
        return self._parent
    
    #------------------------------------------------------------
    def typeInfo(self):
        return self.__class__.__name__
    
    #------------------------------------------------------------
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
        
    #------------------------------------------------------------
    def resource(self):
        return None
    
    #------------------------------------------------------------
    def asXml(self):
        doc = QtXml.QDomDocument()
        node = doc.createElement(self.typeInfo())
        doc.appendChild(node)
       
        for i in self._children:
            i._recurseXml(doc, node)

        return doc.toString(indent=4)
    
    #------------------------------------------------------------
    def _recurseXml(self, doc, parent):
        node = doc.createElement(self.typeInfo())
        parent.appendChild(node)

        for k, v in self.properties_dict().items():
            node.setAttribute(k, v)

        for i in self._children:
            i._recurseXml(doc, node)
    
    #------------------------------------------------------------
    def asJson(self):
        dictionary = self.properties_dict()
        dictionary['type'] = self.typeInfo()
        children_data = list()
        for i in self._children:
            children_data.append(i._recuresJson())
        
        dictionary['children'] = children_data

        return json.dumps(dictionary, sort_keys=True, indent=4)
    
    #------------------------------------------------------------
    def _recurseJson(self):
        dictionary = self.properties_dict()
        dictionary['type'] = self.typeInfo()
        children_data = list()
        for i in self._children:
            children_data.append(i._recuresJson())
        
        dictionary['children'] = children_data
        
        return dictionary
    
    #------------------------------------------------------------
    @classmethod
    def properties(cls):
        """Returns a dictionary of all the properties defined for this model."""
        return dict(cls._properties)
    
    #------------------------------------------------------------
    def properties_dict(self):
        dictionary = dict()
        for key, prop in sorted(self.properties().items()):
            dictionary[key] = prop.get_value(self)
        
        return dictionary

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



        
        
        
        

        
