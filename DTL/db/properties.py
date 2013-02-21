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
    def _attr_name(self):
        """Attribute name we use for this property in model instances."""
        return '_' + self.name


#------------------------------------------------------------
#------------------------------------------------------------
class StringProperty(BaseProperty):
    """A textual property, which can be multi- or single-line."""
    MAX_LENGTH = 500
    data_type = basestring
    #------------------------------------------------------------
    def __init__(self, multiline=False, **kwds):
        super(StringProperty, self).__init__(**kwds)
        self.multiline = multiline
    
    #------------------------------------------------------------
    def validate(self, value):
        value = super(StringProperty, self).validate(value)
        if value is not None and not isinstance(value, basestring):
            raise ValueError(
                'Property %s must be a str or unicode instance, not a %s'
                % (self.name, type(value).__name__))
        if not self.multiline and value and value.find('\n') != -1:
            raise ValueError('Property %s is not multi-line' % self.name)
        if value is not None and len(value) > self.MAX_LENGTH:
            raise ValueError(
                'Property %s is %d characters long; it must be %d or less.'
                % (self.name, len(value), self.MAX_LENGTH))
        return value


#------------------------------------------------------------
#------------------------------------------------------------
class IntegerProperty(BaseProperty):
    data_type = int
    #------------------------------------------------------------
    def validate(self, value):
        value = super(IntegerProperty, self).validate(value)
        if value is None:
            return value

        if not isinstance(value, (int, long)) or isinstance(value, bool):
            raise ValueError('Property %s must be an int or long, not a %s'
                             % (self.name, type(value).__name__))
        if value < -0x8000000000000000 or value > 0x7fffffffffffffff:
            raise ValueError('Property %s must fit in 64 bits' % self.name)
        return value
    
    #------------------------------------------------------------
    def empty(self, value):
        """0 is not an empty value."""
        return value is None


#------------------------------------------------------------
#------------------------------------------------------------
class FloatProperty(BaseProperty):
    data_type = float
    #------------------------------------------------------------
    def validate(self, value):
        value = super(FloatProperty, self).validate(value)
        if value is not None and not isinstance(value, float):
            raise ValueError('Property %s must be a float' % self.name)
        return value
    
    #------------------------------------------------------------
    def empty(self, value):
        """0.0 is not an empty value."""
        return value is None


#------------------------------------------------------------
#------------------------------------------------------------
class BooleanProperty(BaseProperty):
    data_type = bool
    #------------------------------------------------------------
    def validate(self, value):
        value = super(BooleanProperty, self).validate(value)
        if value is not None and not isinstance(value, bool):
            raise ValueError('Property %s must be a bool' % self.name)
        return value
    
    #------------------------------------------------------------
    def empty(self, value):
        """False is not an empty value."""
        return value is None