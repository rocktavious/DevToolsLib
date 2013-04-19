"""
Custom Xml document class

Description
=============
    Contains both the dictionary of data and the filepath for ease of saving, reading and accessing

Usage Example
=============
    >>> xml_doc = XmlDocument('c:/temp/test.xml')
    >>> print xml_doc['Node Tag']['@Nodes Attribute Name']
    >>> print xml_doc['Node Tag']['#Nodes Text']

"""

from xml.parsers import expat
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesImpl
from xml.dom.minidom import parseString
try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
try:
    from collections import OrderedDict
except ImportError :
    OrderedDict = dict

try:
    _basestring = basestring
except NameError:
    _basestring = str
try:
    _unicode = unicode
except NameError:
    _unicode = str
    
import path

#------------------------------------------------------------
#------------------------------------------------------------
class dotdictify(dict):
    #------------------------------------------------------------
    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError, 'expected dict'
    
    #------------------------------------------------------------
    def __setitem__(self, key, value):
        if '.' in key:
            myKey, restOfKey = key.split('.', 1)
            target = self.setdefault(myKey, dotdictify())
            if not isinstance(target, dotdictify):
                raise KeyError, 'cannot set "%s" in "%s" (%s)' % (restOfKey, myKey, repr(target))
            target[restOfKey] = value
        else:
            if isinstance(value, dict) and not isinstance(value, dotdictify):
                value = dotdictify(value)
            dict.__setitem__(self, key, value)
    
    #------------------------------------------------------------
    def __getitem__(self, key):
        if '.' not in key:
            return dict.__getitem__(self, key)
        myKey, restOfKey = key.split('.', 1)
        target = dict.__getitem__(self, myKey)
        if not isinstance(target, dotdictify):
            raise KeyError, 'cannot get "%s" in "%s" (%s)' % (restOfKey, myKey, repr(target))
        return target[restOfKey]
    
    #------------------------------------------------------------
    def __contains__(self, key):
        if '.' not in key:
            return dict.__contains__(self, key)
        myKey, restOfKey = key.split('.', 1)
        target = dict.__getitem__(self, myKey)
        if not isinstance(target, dotdictify):
            return False
        return restOfKey in target
    
    #------------------------------------------------------------
    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default
        except Exception, e:
            raise Exception(e)
    
    #------------------------------------------------------------
    def setdefault(self, key, default):
        if key not in self:
            self[key] = default
        return self[key]
    
    #------------------------------------------------------------
    __setattr__ = __setitem__
    __getattr__ = __getitem__



#------------------------------------------------------------
#------------------------------------------------------------
class ParsingInterrupted(Exception): pass


#------------------------------------------------------------
#------------------------------------------------------------
class _DictSAXHandler(object):
    """Written by: Martin Blech  -  Integrated by: Kyle Rockman"""
    def __init__(self,
                 item_depth=0,
                 item_callback=lambda *args: True,
                 xml_attribs=True,
                 attr_prefix='@',
                 cdata_key='#text',
                 force_cdata=True,
                 cdata_separator='',
                 postprocessor=None,
                 dict_constructor=OrderedDict,
                 strip_whitespace=True):
        self.path = []
        self.stack = []
        self.data = None
        self.item = None
        self.item_depth = item_depth
        self.xml_attribs = xml_attribs
        self.item_callback = item_callback
        self.attr_prefix = attr_prefix
        self.cdata_key = cdata_key
        self.force_cdata = force_cdata
        self.cdata_separator = cdata_separator
        self.postprocessor = postprocessor
        self.dict_constructor = dict_constructor
        self.strip_whitespace = strip_whitespace
    
    #------------------------------------------------------------
    def startElement(self, name, attrs):
        attrs = self.dict_constructor(zip(attrs[0::2], attrs[1::2]))
        self.path.append((name, attrs or None))
        if len(self.path) > self.item_depth:
            self.stack.append((self.item, self.data))
            if self.xml_attribs:
                attrs = self.dict_constructor(
                    (self.attr_prefix+key, value)
                    for (key, value) in attrs.items())
            else:
                attrs = None
            self.item = attrs or None
            self.data = None
    
    #------------------------------------------------------------
    def endElement(self, name):
        if len(self.path) == self.item_depth:
            item = self.item
            if item is None:
                item = self.data
            should_continue = self.item_callback(self.path, item)
            if not should_continue:
                raise ParsingInterrupted()
        if len(self.stack):
            item, data = self.item, self.data
            self.item, self.data = self.stack.pop()
            if self.strip_whitespace and data is not None:
                data = data.strip() or None
            if data and self.force_cdata and item is None:
                item = self.dict_constructor()
            if item is not None:
                if data:
                    self.push_data(item, self.cdata_key, data)
                self.item = self.push_data(self.item, name, item)
            else:
                self.item = self.push_data(self.item, name, data)
        else:
            self.item = self.data = None
        self.path.pop()
    
    #------------------------------------------------------------
    def characters(self, data):
        if not self.data:
            self.data = data
        else:
            self.data += self.cdata_separator + data
    
    #------------------------------------------------------------
    def push_data(self, item, key, data):
        if self.postprocessor is not None:
            result = self.postprocessor(self.path, key, data)
            if result is None:
                return item
            key, data = result
        if item is None:
            item = self.dict_constructor()
        try:
            value = item[key]
            if isinstance(value, list):
                value.append(data)
            else:
                item[key] = [value, data]
        except KeyError:
            item[key] = data
        return item


#------------------------------------------------------------
#------------------------------------------------------------
class XmlDocument(dict):
    '''Custom Dictionary class that has an associated xml file for easy saving/reading'''
    #------------------------------------------------------------
    def __init__(self, file_path=None):
        super(XmlDocument, self).__init__()
        self.setFilePath(file_path)
        self.read()
        
    #------------------------------------------------------------
    def filePath(self):
        return self._file.path

    #------------------------------------------------------------
    def setFilePath(self, file_path):
        if isinstance(file_path, Path):
            self._file = file_path
        else :
            self._file = Path(file_path)
            
    #------------------------------------------------------------
    def prettyprint(self):
        print self._unparse(self)

    #------------------------------------------------------------
    def save(self):
        '''Writes the dict data to the xml file'''
        data = self._unparse(self)
        with open(self._file.path,'wb') as xml_file :
            xml_file.write(data)
    
    #------------------------------------------------------------
    def read(self):
        '''Reads from a xml file the dictionary data'''
        if not self._file.exists :
            return
        with open(self._file.path,'r') as xml_file :
            data = self._parse(xml_file.read())
        for key, value in data.items():
            self.__setitem__(key, value)

    #------------------------------------------------------------
    def defaults(self, defaults={}):
        '''Allows the user to specify default values that should appear in the data'''
        for key, value in defaults.items():
            if not self.has_key(key):
                self.__setitem__(key, value)
    
    #------------------------------------------------------------
    def _emit(self, key, value, content_handler,
              attr_prefix='@',
              cdata_key='#text',
              root=True,
              preprocessor=None):
        if preprocessor is not None:
            result = preprocessor(key, value)
            if result is None:
                return
            key, value = result
        if not isinstance(value, (list, tuple)):
            value = [value]
        if root and len(value) > 1:
            raise ValueError('document with multiple roots')
        for v in value:
            if v is None:
                v = OrderedDict()
            elif not isinstance(v, dict):
                v = _unicode(v)
            if isinstance(v, _basestring):
                v = OrderedDict(((cdata_key, v),))
            cdata = None
            attrs = OrderedDict()
            children = []
            for ik, iv in v.items():
                if ik == cdata_key:
                    cdata = iv
                    continue
                if ik.startswith(attr_prefix):
                    attrs[ik[len(attr_prefix):]] = iv
                    continue
                children.append((ik, iv))
            content_handler.startElement(key, AttributesImpl(attrs))
            for child_key, child_value in children:
                self._emit(child_key, child_value, content_handler,
                      attr_prefix, cdata_key, False, preprocessor)
            if cdata is not None:
                content_handler.characters(cdata)
            content_handler.endElement(key)
                
    #------------------------------------------------------------
    def _parse(self, xml_input, encoding='utf-8', **kw):
        handler = _DictSAXHandler(**kw)
        parser = expat.ParserCreate()
        parser.ordered_attributes = True
        parser.StartElementHandler = handler.startElement
        parser.EndElementHandler = handler.endElement
        parser.CharacterDataHandler = handler.characters
        try:
            parser.ParseFile(xml_input)
        except (TypeError, AttributeError):
            if isinstance(xml_input, _unicode):
                xml_input = xml_input.encode(encoding)
            parser.Parse(xml_input, True)
        return handler.item   
    
    #------------------------------------------------------------
    def _unparse(self, dict_input, output=None, encoding='utf-8', **kwargs):
        ((key, value),) = dict_input.items()
        must_return = False
        if output == None:
            output = StringIO()
            must_return = True
        content_handler = XMLGenerator(output, encoding)
        content_handler.startDocument()
        self._emit(key, value, content_handler, **kwargs)
        content_handler.endDocument()
        if must_return:
            value = output.getvalue()
            try:
                value = value.decode(encoding)
            except AttributeError:
                pass
            return parseString(value).toprettyxml(indent="\t")
    
    #------------------------------------------------------------
    @staticmethod
    def getValuesAsList(dictionary, keyList, allowNone=True, keyErrorMsg='Unable to find key'):
        dotified = dotdictify(dictionary)
        dot_key = '.'.join(keyList[:-1])
        if len(keyList) == 1 :
            data = dictionary
        else:
            data = dotified.get(dot_key, None)
            if data is None:
                if allowNone :
                    return []
                raise KeyError(keyErrorMsg)
        if not isinstance(data[keyList[-1]], list):
            data = [data[keyList[-1]]]
        else:
            data = data[keyList[-1]]
        
        return data        



def remove_whilespace_nodes(node, unlink=False):
    """Removes all of the whitespace-only text decendants of a DOM node.

    When creating a DOM from an XML source, XML parsers are required to
    consider several conditions when deciding whether to include
    whitespace-only text nodes. This function ignores all of those
    conditions and removes all whitespace-only text decendants of the
    specified node. If the unlink flag is specified, the removed text
    nodes are unlinked so that their storage can be reclaimed. If the
    specified node is a whitespace-only text node then it is left
    unmodified."""

    remove_list = []
    for child in node.childNodes:
        if child.nodeType == Node.TEXT_NODE and \
           not child.data.strip():
            remove_list.append(child)
        elif child.hasChildNodes():
            remove_whilespace_nodes(child, unlink)
    for node in remove_list:
        node.parentNode.removeChild(node)
        if unlink:
            node.unlink()
