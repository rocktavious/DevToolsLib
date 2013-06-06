
#------------------------------------------------------------
#------------------------------------------------------------
class BaseStruct(object):
    #------------------------------------------------------------
    def __init__(self, attitude=None):
        self.__set(attitude)
    
    #------------------------------------------------------------
    def __str__(self):
        return '{0}({1})'.format(type(self).__name__, self.__get())
    
    #------------------------------------------------------------
    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, self.__get())
    
    #------------------------------------------------------------
    def __eq__(self, other):
        if not isinstance(other, type(self)) :
            return False
        if not self.get() == other.get() :
            return False
        
        return True
    
    #------------------------------------------------------------
    def __ne__(self, other):
        return not self.__eq__(other)
    
    #------------------------------------------------------------
    def __get(self):
        return None
    
    #------------------------------------------------------------
    def __set(self, value):
        pass


if __name__ == "__main__":
    base1 = BaseStruct()
    base2 = BaseStruct()
    print base1
    print base1 == None
    print base1 == base2