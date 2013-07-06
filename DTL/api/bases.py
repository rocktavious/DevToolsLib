import inspect

#------------------------------------------------------------
#------------------------------------------------------------
class BaseStruct(object):
    #------------------------------------------------------------
    def __init__(self, *args, **kwds):
        self.deserialize(*args, **kwds)
    
    #------------------------------------------------------------
    def _get_repr_format(self):
        return '{0}({1})'.format(type(self).__name__, self._get_init_params_format())
    
    #------------------------------------------------------------
    def _get_init_params_format(self):
        param_format = ''
        params = inspect.getargspec(self.deserialize)[0]
        params_count = len(params[1:])
        for i in range(params_count):
            param_format += '{0}='.format(params[i+1]) +'{'+str(i)+'}'
            if i != params_count-1:
                param_format += ', '
        return param_format
    
    #------------------------------------------------------------
    def _get_repr(self):
        try:
            return self._get_repr_format().format(*self.serialize())
        except:
            return '{0}({1})'.format(type(self).__name__, self.serialize())
    
    #------------------------------------------------------------
    def __str__(self):
        return self._get_repr()
    
    #------------------------------------------------------------
    def __repr__(self):
        return self._get_repr()
    
    #------------------------------------------------------------
    def __eq__(self, other):
        if not isinstance(other, type(self)) :
            return False
        
        return True
    
    #------------------------------------------------------------
    def __ne__(self, other):
        return not self.__eq__(other)
    
    #------------------------------------------------------------
    def add_quotes(self, data):
        '''Convenience method to help in serialization of strings'''
        return "'{0}'".format(data)
    
    #------------------------------------------------------------
    def serialize(self):
        '''Returns the arg list in which deserialize can recreate this object'''
        return (None,)
    
    #------------------------------------------------------------
    def deserialize(self, *args, **kwds):
        '''If provided the info from serialize, this should should beable to construct the object
        deserialize must provide all of the args for the spec because the format is pulled from this function'''
        pass


#------------------------------------------------------------
#------------------------------------------------------------
class BaseDict(BaseStruct, dict):
    #------------------------------------------------------------
    def __init__(self, *args, **kwds):
        super(BaseDict, self).__init__(*args, **kwds)
        
    #------------------------------------------------------------
    def _set_data(self, data_dict):
        for key, value in data_dict.items():
            self.__setitem__(key, value)
            
    #------------------------------------------------------------
    def set_default(self, default={}):
        '''Allows the user to specify default values that should appear in the data'''
        for key, value in default.items():
            if not self.has_key(key):
                self.__setitem__(key, eval(value))
                
    #------------------------------------------------------------
    def serialize(self):
        return (dict(self),)
    
    #------------------------------------------------------------
    def deserialize(self, data_dict={}):
        self._set_data(data_dict=data_dict)


#------------------------------------------------------------
#------------------------------------------------------------
if __name__ == "__main__":
    base1 = BaseStruct()
    base2 = BaseStruct()
    print base1
    print base1 == None
    print base1 == base2