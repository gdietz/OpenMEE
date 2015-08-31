'''
Created on Jul 27, 2015

@author: george
'''

import rpy2, rpy2.rinterface
from rpy2 import robjects as ro
from rpy2.robjects.vectors import FloatVector
#from rpy2.robjects.vectors.Vector

def rvector_to_pystruct(rvector):
    '''
    Converts an a vector in R to a python list or dictionary
    
    If the vector doesn't have names, convert the rvector to a simple python list
    If the vector has names, convert the vector to a python dictionary
    
    Arguments:
        rvector - an rvector in rpy2 format
    '''
    
    values = list(rvector)
    if rvector.names == rpy2.rinterface.NULL:
        names = None
    else:
        names = list(rvector.names)
        
    if names:
        return dict(zip(names, values))
    else:
        return values

def named_rlist_to_pydict(rlist):
    '''
    Converts a named R list vector to a python dictionary. It is assumed that each element is named

    Arguments:
        rlist - an rlist in rpy2 format
    '''
    values = list(rlist)
    if rlist.names == rpy2.rinterface.NULL:
        names = []
    else:
        names = list(rlist.names)

    if len(values) != len(names):
        raise Exception("Number of names doesn't match number of values")

    return dict(zip(names, values))

def parse_r_struct(rstruct):
    '''
    Parses an r structure (nested list) into a purely python structure
    '''

    if isinstance(rstruct, rpy2.robjects.vectors.ListVector):
        pyobj = named_rlist_to_pydict(rstruct)
        for k,v in pyobj.items():
            pyobj[k] = parse_r_struct(v)
    elif isinstance(rstruct, rpy2.robjects.vectors.Vector):
        pyobj = rvector_to_pystruct(rstruct)
    else:
        pyobj = rstruct

    return pyobj

def singletonlists_to_scalars(pydict):
    '''
    Iterates over a nested dictionary. For values which are singleton lists,
    convert them to scalars matching the first element in the list.
    e.g.:
        {
            'FOO': {
                'BAR': ['hello']
            }
        }

        turns into 

        {
            'FOO': {
                'BAR': 'hello'
            }
        }

        Does not modify input dictionary.
    '''

    result = {}
    for key, value in pydict.items():
        if isinstance(value, dict):
            result[key] = singletonlists_to_scalars(value)
        elif (isinstance(value, list) or isinstance(value, tuple)) and len(value) == 1:
            result[key] = value[0]
        else:
            result[key] = value
    return result
    

if __name__ == '__main__':
    pass