import sys
import json
import re
from PyQt4 import QtXml

from DTL.api import InternalError, Utils, Path

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
def obj_for_name(module_name, class_name):
    try:
        return getattr(sys.modules[module_name], class_name)
    except KeyError:
        module = __import__(module_name, globals(), locals(), class_name)
        return getattr(module, class_name)
    except Exception, e:
        raise Exception(e)

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
    def __init__(self, parent=None, filepath=None):
        super(BaseData, self).__init__()
        self._filepath = Path(filepath)
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
    def children(self):
        return self._children
    
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
    def moduleInfo(self):
        return self.__class__.__module__
    
    #------------------------------------------------------------
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
        
    #------------------------------------------------------------
    def resource(self):
        return None
    
    #------------------------------------------------------------
    def _getFile(self, ext=[]):
        if self._filepath.isEmpty :
            self._filepath = Utils.getFileFromUser(ext=ext)
            if self._filepath.isEmpty :
                return False
        return True
    
    #------------------------------------------------------------
    def _getSaveFile(self, ext=[]):
        if self._filepath.isEmpty :
            self._filepath = Utils.getSaveFileFromUser(ext=ext)
            if self._filepath.isEmpty :
                return False
        return True        
    
    #------------------------------------------------------------
    def readXml(self):
        if self._getFile(ext=['.xml']) is False:
            return
        with open(self._filepath.path,'r') as xml_file :
            xml_data = xml_file.read()
        
        xml_doc = QtXml.QDomDocument()
        xml_doc = xml_doc.documentElement()
        xml_doc.setContent(xml_data)
        self._readXml(doc_element.firstChild())
        
    #------------------------------------------------------------
    def saveXml(self):
        if self._getSaveFile(ext=['.xml']) is False :
            return        
        self._filepath.validate_dirs()
        xml_data = self._asXml(QtXml.QDomDocument(), None)
        with open(self._filepath.path,'wb') as xml_file :
            xml_file.write(xml_data)
    
    #------------------------------------------------------------
    def readJson(self):
        if self._getFile(ext=['.json']) is False:
            return        
        with open(self._filepath.path,'r') as json_file :
            json_data = json.load(json_file)
        
        self._readJson(json_data)
        
    #------------------------------------------------------------
    def saveJson(self):
        '''Writes the dict data to the json file'''
        if self._getSaveFile(ext=['.json']) is False:
            return           
        self._filepath.validate_dirs()
        with open(self._filepath.path,'wb') as json_file :
            json_data = json.dumps(self._asJson(), sort_keys=True, indent=4, cls=JsonModelEncoder)
            json_file.write(json_data)
    
    #------------------------------------------------------------
    def _readXML(self, current_node):
        for prop in self.properties().values():
            if current_node.hasAttribute(prop.name):
                attr_value = current_node.attribute(prop.name)
                prop.__set__(self, attr_value)        

        
        for child in current_node.childNodes():
            module_name = child.attribute('module_name')
            class_name = child.attribute('class_name')
            child_class = obj_for_name(module_name, class_name)
            new_child = child_class(parent=self)
            new_child._readXML(child)        
    
    #------------------------------------------------------------
    def _asXml(self, xml_doc, parent):
        node = xml_doc.createElement(self.typeInfo())
        if parent :
            parent.appendChild(node)
        else:
            xml_doc.appendChild(node)
       
        for k, v in self.properties_dict().items():
            node.setAttribute(k, v)
        
        node.setAttribute('module_name', self.typeInfo())
        node.setAttribute('class_name', self.moduleInfo())

        for i in self._children:
            i._asXml(xml_doc, node)

        return xml_doc.toString(indent=4)
    
    #------------------------------------------------------------
    def _readJson(self, json_data):
        for prop in self.properties().values():
            if prop.name in json_data:
                prop_data = json_data[prop.name]
                prop.__set__(self, prop_data)        

        for child in json_data.get('children',[]):
            module_name = child.pop('module_name')
            class_name = child.pop('class_name')
            child_class = obj_for_name(module_name, class_name)
            new_child = child_class(parent=self)
            new_child._readJson(child)
    
    #------------------------------------------------------------
    def _asJson(self):
        dictionary = self.properties_dict()
        dictionary['class_name'] = self.typeInfo()
        dictionary['module_name'] = self.moduleInfo()
        children_data = list()
        for i in self._children:
            children_data.append(i._asJson())
        
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