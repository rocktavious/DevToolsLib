import json
import re
from PyQt4 import QtXml

from DTL.api import InternalError

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

    if attr_name in RESERVED_WORDS or attr_name in dir(BaseData):
        raise ReservedWordError(
            "Cannot define property using reserved word '%(attr_name)s'. "
            "If you would like to use this name in the datastore consider "
            "using a different name like %(attr_name)s_ and adding "
            "name='%(attr_name)s' to the parameter list of the property "
            "definition." % locals())


#------------------------------------------------------------
#------------------------------------------------------------
class BaseProperty(object):
    #------------------------------------------------------------
    def __init__(self, default=None, name=None, required=False, choices=None):
        self.default = default
        self.name = name
        self.required = required
        self.choices = choices
    
    #------------------------------------------------------------
    def __property_config__(self, property_name):
        """Configure property, connecting it to its data instance."""
        super(BaseProperty, self).__init__()
        if self.name is None:
            self.name = property_name
        
    #------------------------------------------------------------
    def __get__(self, instance, cls):
        if instance is None:
            return self
        try:
            return getattr(instance, self._attr_name())
        except AttributeError:
            self.__set__(instance, self.default)
            return self.default       
    
    #------------------------------------------------------------
    def __set__(self, instance, new_value):
        new_value = self.validate(new_value)
        setattr(instance, self._attr_name(), new_value)
    
    #------------------------------------------------------------
    def get_value(self, model_instance):
        """Looks for this property in the given model instance, and returns the value"""
        return self.__get__(model_instance, model_instance.__class__)
        
    #------------------------------------------------------------
    def empty(self, value):
        """Determine if value is empty in the context of this property.
        For most kinds, this is equivalent to "not value", but for kinds like
        bool, the test is more subtle, so subclasses can override this method
        if necessary."""
        return not value
    
    #------------------------------------------------------------
    def validate(self, value):
        """Assert that provided value is compatible with this property."""
        if self.empty(value):
            if self.required:
                raise ValueError('Property %s is required' % self.name)
        else:
            if self.choices:
                if value not in self.choices:
                    raise ValueError('Property %s is %r; must be one of %r' %
                                     (self.name, value, self.choices))
        return value
    
    #------------------------------------------------------------
    def default_value(self):
        return self.default
    
    #------------------------------------------------------------
    def _attr_name(self):
        """Attribute name we use for this property in model instances."""
        return '_' + self.name


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
            if isinstance(attr, BaseProperty) or issubclass(attr.__class__, BaseProperty):
                check_reserved_word(name)
                cls._properties[name] = attr
                attr.__property_config__(name)


#------------------------------------------------------------
#------------------------------------------------------------
class JsonModelEncoder(json.JSONEncoder):
    #------------------------------------------------------------
    def default(self, obj):
        if issubclass(obj.__class__, BaseData):
            return obj.properties_dict()
        return json.JSONEncoder.default(self, obj)


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
    def readJson(self, dictionary):
        for prop in self.properties().values():
            if prop.name in dictionary:
                data = dictionary[prop.name]
                if prop.data_type is list :
                    for item in data:
                        print item
                        new_model = prop.reference_class()
                        new_model.readJson(item)
                        prop.__set__(self, new_model)
                elif prop.data_type is object :
                    new_obj = prop.reference_class(data)
                    prop.__set__(self, new_obj)
                else:
                    prop.__set__(self, data)
            
    #------------------------------------------------------------
    def asJson(self):
        dictionary = self.properties_dict()
        dictionary['type'] = self.typeInfo()
        children_data = list()
        for i in self._children:
            children_data.append(i._recuresJson())
        
        dictionary['children'] = children_data

        return json.dumps(dictionary, sort_keys=True, indent=4, cls=JsonModelEncoder)
    
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