from .base import BaseData, BaseProperty


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


#------------------------------------------------------------
#------------------------------------------------------------
class CustomProperty(BaseProperty):
    data_type = object
    #------------------------------------------------------------
    def __init__(self, reference_class, default=None, **kwds):
        if not isinstance(reference_class, type) or issubclass(reference_class, self.data_type.__class__):
            raise ValueError('reference_class must be object or type')
        self.reference_class = reference_class
        
        if default is None:
            raise ValueError('Default must have a value of the type given')
        
        super(CustomProperty, self).__init__(default=default,
                                             **kwds)
        
    #------------------------------------------------------------
    def validate(self, value):
        """
        Raises:
          ValueError if property is not an instance of
          the reference_class given to the constructor.
        """
        value = super(CustomProperty, self).validate(value)

        if not isinstance(value, self.reference_class) and not issubclass(value.__class__, self.reference_class):
            raise ValueError('Value %s of property must be instance of %s' % (value, self.reference_class.__class__.__name__))
        return value
    
    #------------------------------------------------------------
    def empty(self, value):
        """[] is not an empty value."""
        return value is None


#------------------------------------------------------------
#------------------------------------------------------------
class ListProperty(CustomProperty):
    data_type = list
    #------------------------------------------------------------
    def __init__(self, reference_class, default=None, **kwds):
        if default is None:
            default = []

        super(ListProperty, self).__init__(reference_class=reference_class,
                                           default=default,
                                           **kwds)
        
    #------------------------------------------------------------
    def __set__(self, model_instance, value):
        if not isinstance(value, list):
            if self.__get__(model_instance, model_instance.__class__):
                new_value = [value] + self.__get__(model_instance, model_instance.__class__)
            else:
                new_value = [value]
        else:
            new_value = value
            
        super(ListProperty, self).__set__(model_instance, new_value)
        
    #------------------------------------------------------------
    def validate(self, value):
        """
        Raises:
          ValueError if property is not a list whose items are instances of
          the reference_class given to the constructor.
        """
        #value = super(ListProperty, self).validate(value)
        if value is not None:
            if not isinstance(value, list):
                raise ValueError('Property %s must be a list' % self.name)

            value = self.validate_list_contents(value)
        return value
    
    #------------------------------------------------------------
    def validate_list_contents(self, value):
        """Validates that all items in the list are of the correct type.
        Raises:
          ValueError if the list has items are not instances of the
          reference_class given to the constructor.
        """
        for item in value:
            if not isinstance(item, self.reference_class) and not issubclass(item.__class__, self.reference_class.__class__):
                raise ValueError('Items in the %s list must all be %s instances' %
                                 (self.name, self.reference_class.__class__.__name__))
        return value
    
    #------------------------------------------------------------
    def empty(self, value):
        """[] is not an empty value."""
        return value is None
    
    #------------------------------------------------------------
    def default_value(self):
        """Because the property supplied to 'default' is a static value,
        that value must be shallow copied to prevent all fields with
        default values from sharing the same instance.

        Returns:
          Copy of the default value.
        """
        return list(super(ListProperty, self).default_value())