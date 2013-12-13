#################
#               #
# George Dietz  #
# CEBM@Brown    #
#               #
#################

class Study:
    # Study holds a collection of variables
    # Invariant: 'None' as variable values are not stored, just implied
    #            "" i.e. empty strings are not stored
    def __init__(self, study_id=None, label=None):
        if study_id is None:
            raise ValueError("Study MUST have an id")
        self.study_id = study_id
        self.label = label
        
        # each variable value is a scalar
        self.variables = {}
        
    def get_id(self):
        return self.study_id
    # No set_id method because the only time an item_id should ever be set
    # is when it is created
        
    def get_label(self, none_to_empty_string=False):
        if none_to_empty_string and self.label is None:
            return ''
        return self.label
    
    def set_label(self, label):
        self.label = label
        
    
    # Since not every study will have data for all variables, return None for
    # missing variables
    def get_var(self, var):
#         if var not in self.variables:
#             return None
        try:
            return self.variables[var]
        except KeyError:
            return None
    
    def set_var(self, var, var_value):
        self.variables[var] = var_value
        if var_value in [None,""]: # we do implied Nones, not explicit Nones
            del self.variables[var]
    
    def remove_variable(self, var):
        # Trying to set value to None removes the reference to the variable
        self.set_var(var, None)
        
        
    def is_totally_blank(self):
        ''' returns True if the study contains no information i.e. if the label
        is blank, and it stores no data for any variables '''
        
        if self.label or len(self.variables) > 0:
            return False
        return True
        
        
    def __str__(self):
        indentation_level = 2
        variables = self.variables.keys()[:]
        variables.sort(key=lambda var: var.get_label())
        
        output = ["Study info:",]
        study_summary = ["id: %s" % str(self.get_id()),
         "label: %s" % str(self.get_label()),
         "Variables"]
        study_summary = [" "*indentation_level + x for x in study_summary]
        var_info = [" "*2*indentation_level + "%s: %s" % (var.get_label(), self.get_var(var)) for var in variables]
        
        output.extend(study_summary)
        output.extend(var_info)
        
        return "\n".join(output)