#################
#               #
# George Dietz  #
# CEBM@Brown    #
#               #
#################

from globals import *

class Variable:
    def __init__(self, var_id, var_label, var_type=CATEGORICAL, sub_type=None):
        if var_id is None:
            raise ValueError("variable MUST have an id")
        self.var_id = var_id
        self.label = var_label
        
        self.set_type(var_type) # self.var_type
        self.set_subtype(sub_type)
        
    def get_id(self):
        return self.var_id
    # No set_id method because the only time an item_id should ever be set
    # is when it is created
        
    def get_label(self):
        return self.label
    
    def set_label(self, label):
        self.label = label
        
    def get_type(self):
        return self.var_type
    
    def set_type(self, new_type):
        if new_type not in VARIABLE_TYPES:
            raise ValueError("Unrecognized variable type")
        self.var_type = new_type
        
    def set_subtype(self, subtype):
        self.sub_type = subtype
    
    def get_subtype(self):
        try:
            return self.sub_type
        except AttributeError:
            self.sub_type = None
            return None
            
    
    def get_type_as_str(self):
        return VARIABLE_TYPE_STRING_REPS[self.var_type]
    
        
