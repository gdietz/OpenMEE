#################
#               #
# George Dietz  #
# CEBM@Brown    #
#               #
#################

from sets import Set

from ome_globals import *
from variable import Variable
from managed_collection import ManagedCollection

class VariableCollection(ManagedCollection):
    # Holds a collection of variables that all have unique ids
    # The variables are not ordered in any way

    def __init__(self):
        super(VariableCollection, self).__init__(Variable)

    def data_item_name(self, plural=False):
        if plural:
            return "variables"
        return "variable"

    def get_variables_by_type(self, var_type):
        var_list = []
        for var in self.get:
            if var.get_type() == var_type:
                var_list.append(var)
        return var_list

    def make_new_variable(self, var_label, var_type=CATEGORICAL):
        ''' Makes new variable in the collection of the given type '''

        if var_type not in VARIABLE_TYPES:
            raise ValueError("Type not in allowed types")

        new_variable = self.make_item(label=var_label)
        new_variable.set_type(var_type)
        return new_variable

