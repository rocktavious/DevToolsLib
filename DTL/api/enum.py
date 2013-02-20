"""
Python based enumartion type

Usage Example
=============
    >>> Colors = Enum("Red","Yellow","Blue")
    >>> print Colors.Red
    0
    >>> print Colors.Yellow
    1
    >>> print 2 == Colors.Blue
    True
    >>> print Colors.names[2]
    Blue
    >>> print Colors.names.index('Blue')
    2
    
"""

def Enum(*enumerated):
    enums = dict(zip(enumerated, range(len(enumerated))))
    enums["names"] = enumerated
    return type('Enum', (), enums)

