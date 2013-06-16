import inspect

#------------------------------------------------------------
#------------------------------------------------------------
class BaseStruct(object):
    #------------------------------------------------------------
    def __init__(self, *args, **kwds):
        self.__set(*args, **kwds)
    
    #------------------------------------------------------------
    def __get_repr_format(self):
        return '{0}({1})'.format(type(self).__name__, self.__get_init_params_format())
    
    #------------------------------------------------------------
    def __get_init_params_format(self):
        param_format = ''
        params = inspect.getargspec(self.__init__)[0]
        params_count = len(params[1:])
        for i in range(params_count):
            param_format += '{0}='.format(params[i+1]) +'{'+str(i)+'}'
            if i != params_count-1:
                param_format += ', '
        return param_format
    
    #------------------------------------------------------------
    def __get_repr(self):
        try:
            return self.__get_repr_format().format(*self.serialize())
        except:
            return '{0}({1})'.format(type(self).__name__, *self.serialize())
    
    #------------------------------------------------------------
    def __str__(self):
        return self.__get_repr()
    
    #------------------------------------------------------------
    def __repr__(self):
        return self.__get_repr()
    
    #------------------------------------------------------------
    def __eq__(self, other):
        if not isinstance(other, type(self)) :
            return False
        
        return True
    
    #------------------------------------------------------------
    def __ne__(self, other):
        return not self.__eq__(other)
    
    #------------------------------------------------------------
    def serialize(self):
        '''When subclassing get should return a format that __set can read to re-setup the object'''
        return None
    
    #------------------------------------------------------------
    def __set(self, *args, **kwds):
        '''When sublclassing this method should setup the object'''
        pass


if __name__ == "__main__":
    base1 = BaseStruct()
    base2 = BaseStruct()
    print base1
    print base1 == None
    print base1 == base2