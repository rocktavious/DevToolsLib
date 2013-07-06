import math

#------------------------------------------------------------
def clamp(v, minvalue=0, maxvalue=1):
    return max(minvalue, min(v, maxvalue))

#------------------------------------------------------------
def clamp_array(v, minvalue=0, maxvalue=1):
    return [clamp(v[i], minvalue, maxvalue) for i in range(len(v))]
    
#------------------------------------------------------------
def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))
    
#------------------------------------------------------------
def normalize(v):
    vmag = magnitude(v)
    if vmag == 0 :
        vmag = 0.0001
    return [ v[i]/vmag for i in range(len(v)) ]

#------------------------------------------------------------
def linear_srgb(v):
    return [ math.pow(v[i],1/2.2) if v[i] <= 1 else v[i] for i in range(len(v))]

#------------------------------------------------------------
def srgb_linear(v):
    return [ math.pow(v[i],2.2) if v[i] <= 1 else v[i] for i in range(len(v))]