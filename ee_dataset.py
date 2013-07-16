#######################################################
#                                                     #
# Author: George Dietz                                #
#                                                     #
# Description: Underlying data model for OpenMEE data #
#                                                     #
#######################################################



from sets import Set

from globals import *



class EEDataSet():
    def __init__(self):
        self.study_collection = StudyCollection()
        
        # dictionary of variable information indexed by variable name:
        # variable_name: {attr1: X, attr2: Y, etc}
        self.variable_info = {}
        
        
    ############## Methods for manipulating studies ###################
    def make_study(self, label=None, study_id=None, **variables):
        ''' Returns a reference to the newly created study '''
        return self.study_collection.make_study(label=label, study_id=study_id, **variables)
    
    def add_existing_study(self, study):
        return self.study_collection.add_existing_study(study)
        
    def remove_study(self, study):
        self.study_collection.remove_study(study)
    
    def get_study_by_id(self, study_id):
        return self.study_collection.get_study_by_id(study_id)
        
    def get_studies_by_name(self, name):
        return self.study_collection.get_studies_by_name(name)
    
    def get_studies_by_var_value(self, var_name, var_val):
        return self.study_collection.get_studies_by_var_value(var_name, var_val)
    
    def get_studies_with_data_for_var(self, var_name):
        return self.study_collection.get_studies_with_data_for_var(var_name)
    
    def get_all_studies(self):
        return self.study_collection.get_all_studies()
    
    def get_all_study_labels(self):
        return self.study_collection.get_all_study_labels()
    ########### End methods for manipulating studies ##################
    
    ############### Methods for manipulating variables #################
    def add_variable(self, var_name, var_type=CATEGORICAL):
        ''' Adds variable and type to self.variable_info '''
        if var_name in self.variable_info.keys():
            raise ValueError("Variable names must be unique")
        
        if var_type not in VARIABLE_TYPES:
            raise ValueError("Type not in allowed types")
        
        self.variable_info[var_name] = {'type':var_type}
        
    def get_variable_type(self, name):
        if name not in self.variable_info.keys():
            raise KeyError("No such variable exists in the dataset")
        return self.variable_info[name]['type']
        
    def change_variable_type(self, var_name, new_type, precision=DEFAULT_PRECISION):
        '''
        1. Recasts all the stored values for that variable type in the studies
        2. Changes the variable type in self.variable info.
        '''
        
        # verification
        if var_name not in self.variable_info.keys():
            raise KeyError("No such variable exists in the dataset")
        if new_type not in VARIABLE_TYPES:
            raise ValueError("Type not in allowed types")
        if not self.can_convert_variable_to_type(var_name, new_type):
            raise ConversionError("Unable to convert '%s' to type '%s'" % (var_name, VARIABLE_TYPE_STRING_REPS[new_type]))
        
        old_type = self.get_variable_type(var_name)
        for study in self.get_studies_with_data_for_var(var_name):
            value = study.get_var(var_name)
            converted_value = self.convert_var_value_to_type(old_type, new_type, value, precision)
            study.set_var(var_name, converted_value)
        
        # change variable type in self.variable_info
        self.variable_info[var_name]['type'] = new_type
    
    def can_convert_var_value_to_type(self, new_type, value):
        # TODO: remember to warn user if converting to integer from continuous that they will lose precision
        
        if new_type == CATEGORICAL:
            pass
        elif new_type == CONTINUOUS:
            try:
                float(value)
            except ValueError:
                return False
        elif new_type == INTEGER:
            try:
                int(float(value))
            except ValueError:
                return False
        return True
            
    def convert_var_value_to_type(self, old_type, new_type, value,
                                   precision=DEFAULT_PRECISION):
        ''' Converts a variable of type old_type to a variable of type new_type
        Doesn't do any verification (assume this has already been done) '''
        
        
        if value is None:
            return None
        
        if new_type == CATEGORICAL:
            if old_type == CONTINUOUS:
                fmt_str = "{:.%df}" % precision
                return fmt_str.format(value)
            else:
                return str(value)
        elif new_type == CONTINUOUS:
            return float(value)
        elif new_type == INTEGER:
            return int(float(value))
        
    def can_convert_variable_to_type(self, var_name, new_type):
        '''
        Returns True if it is possible to convert the type of variable called
        var_name to the new_type for all studies
        '''
        
        old_type = self.get_variable_type(var_name)
        for study in self.get_studies_with_data_for_var(var_name):
            value = study.get_var(var_name)
            # verification
            if not self.can_convert_var_value_to_type(new_type, value):
                return False
        return True


    def remove_variable(self, var_name):
        '''
        1. Remove entry for variable in all the studies
        2. Delete the variable from variable_info
        '''
        
        if var_name not in self.variable_info.keys():
            raise ValueError("Attempted to delete non-existing variable")
        
        for study in self.get_studies_with_data_for_var(var_name):
            study.remove_variable(var_name)
        del self.variable_info[var_name]
        


    def change_variable_name(self, old_name, new_name):
        '''
        1. Changes the name in all the studies
        2. changes the variable name in self.varable_info
        '''
        
        var_type = self.get_variable_type(old_name)
        
        #verification
        if new_name in self.variable_info.keys():
            raise ValueError("Cannot change to name to existing variable name")
        
        for study in self.get_studies_with_data_for_var(old_name)[:]:
            value = study.get_var(old_name)
            study.set_var(new_name, value) # create entry for new name
            study.remove_variable(old_name)  # remove entry for old name
        
        # adjust info in self.variable_info
        self.add_variable(new_name, var_type)
        self.remove_variable(old_name)
    
    def get_all_variable_names(self):
        return self.variable_info.keys()
    
    
    def __str__(self):
        return self._get_studies_summary()
        
        
    def _get_variables_summary(self):
        ''' Retuns a string summarizing info about the variables '''
        
        variables_summary_str = "Summary of Variables:\n"
        variables_summary = ["Variable","Type"]
        
        sorted_variable_names = sorted(self.get_all_variable_names())
        types = [VARIABLE_TYPE_STRING_REPS[self.variable_info[var_name]['type']] for var_name in sorted_variable_names]
        names_types = zip(sorted_variable_names,types)
        variables_summary.extend([(var_name, var_type) for var_name,var_type in names_types])
        
        # convert to string
        variables_summary = table_as_str(variables_summary)
        variables_summary_str += variables_summary
        
        return variables_summary_str
        
    def _get_studies_summary(self):
        ''' Returns a string summarizing info about the studies '''
        
        sorted_study_ids = sorted(self.study_collection.get_study_ids())
        sorted_studies = [self.get_study_by_id(study_id) for study_id in sorted_study_ids]
        
        sorted_variable_names = sorted(self.get_all_variable_names())
        sorted_variable_types = [VARIABLE_TYPE_STRING_REPS[self.variable_info[var_name]['type']] for var_name in sorted_variable_names]
        
        studies_summary_str = "Summary of Studies:\n"
        
        summary_table_header0 = ["",""]
        summary_table_header0.extend(sorted_variable_types)
        summary_table_header1 = ['study id','study label']
        summary_table_header1.extend(sorted_variable_names)
        summary_table_header1 = tuple(summary_table_header1)
        
        study_summaries = [summary_table_header0, summary_table_header1]
        for study in sorted_studies:
            info = [study.get_id(), study.get_label()]
            info.extend([study.get_var(var_name) for var_name in sorted_variable_names])
            f = lambda x: str(x) if x is not None else ""
            info = [f(x) for x in info]
            study_summaries.append(info)
        
        studies_summary_str += table_as_str(study_summaries)
        return studies_summary_str
    
    

    
        
    ####### End methods for manipulating variables ##########

def table_as_str(table):
    ''' Returns a string formatted as a pretty table. 'table' is a list of
    tuples, one tuple per row '''
    
    if len(table) == 0:
        raise ValueError("Table cannot be empty")
    
    output_str = ""
    num_cols = len(table[0])
    row_fmt = "{:>15}"*num_cols
    row_fmt += "\n"
    for row in table:
        output_str += row_fmt.format(*row)
    return output_str

class DuplicateItemError(Exception):
    def __init__(self, arg):
        self.args = arg

class ConversionError(Exception):
    def __init__(self, arg):
        self.args = arg
    
class Study:
    # Study holds a collection of variables
    # Invariant: 'None' as variable values are not stored, just implied
    #            "" i.e. empty strings are not stored
    def __init__(self, study_id=None, label=None):
        if study_id is None:
            return ValueError("Study MUST have an id")
        self.study_id = study_id
        
        self.label = label
        # each variable is a scalar
        self.variables = {}
        
    def get_id(self):
        return self.study_id
    # No set_id method because the only time a study_id should ever be set
    # is when it is created
        
    def get_label(self):
        return self.label
    
    def set_label(self, label):
        self.label = label
    
    # Since not every study will have data for all variables, return None for
    # missing variable
    def get_var(self, varname):
        if varname not in self.variables:
            return None
        return self.variables[varname]
    
    def set_var(self, var_name, var_value):
        self.variables[var_name] = var_value
        if var_value in [None,""]: # we do implied Nones, not explicit Nones
            del self.variables[var_name]
    
    def remove_variable(self, var_name):
        # Trying to set value to None removes the reference to the variable
        self.set_var(var_name, None)
        
        
    def is_totally_blank(self):
        ''' returns True if the study contains no information i.e. if the label
        is blank, and it stores no data for any variables '''
        
        if self.get_label():
            return False
        if len(self.variables) > 0:
            return False
        return True
        
        
    def __str__(self):
        indentation_level = 2
        var_names = self.variables.keys()
        var_names = sorted(var_names)
        output = ["Study info:",]
        study_summary = ["id: %s" % str(self.get_id()),
         "label: %s" % str(self.get_label()),
         "Variables"]
        study_summary = [" "*indentation_level + x for x in study_summary]
        var_info = [" "*2*indentation_level + "%s: %s" % (var_name, self.get_var(var_name)) for var_name in var_names]
        
        output.extend(study_summary)
        output.extend(var_info)
        
        return "\n".join(output)
    
         
        
    
    

class StudyCollection:
    # Holds a collection of studies that all have unique ids
    # The studies are not ordered in any way
    
    def __init__(self):
        self.studies = Set()
        self.study_ids = Set()  # for now just simple integers
        
    def _acquire_unique_id(self):
        ''' 1. Creates a unique study id
            2. Adds it to the study id pool
            3. Returns the new id
            
            Make sure you use the returned id, otherwise there will be be
            study ids that refer to no study
        '''
    
        if len(self.study_ids) == 0:
            new_id = 0
        else:
            max_id = max(self.study_ids)
            new_id = max_id + 1
        
        # Should never be raised but is a good check to make sure the ids are
        # uniquely assigned
        if new_id in self.study_ids:
            raise DuplicateItemError("The id '%s' is already in the set of used ids!" % str(id))
            
        self.study_ids.add(new_id)
        return new_id
        
    def get_study_ids(self):
        return self.study_ids
    
    def get_study_by_id(self, study_id):
        ''' Returns a single study since study ids are always unique '''
        
        # improvement could be made by using a sorted list with the bisect module
        for study in self.studies:
            if study.get_id() == study_id:
                return study
        return ValueError("Study with id: '%s' not found" % str(study_id))
    
    def get_studies_by_name(self, name):
        ''' Returns a list of studies since studies MAY not have unique names '''
        
        studylist = []
        for study in self.studies:
            if study.get_name() == name:
                studylist.append(study)
        return studylist
    
    def get_studies_with_data_for_var(self, var_name):
        studylist = []
        for study in self.studies:
            if study.get_var(var_name) != None:
                studylist.append(study)
        return studylist
    
    def get_studies_by_var_value(self, var_name, var_val):
        '''
        Returns a list of studies by which have a value of var_val for
        var_name
        '''
        
        studylist = []
        for study in self.studies:
            if study.get_var('varname') == var_val:
                studylist.append(study)
        return studylist
    
    def get_all_studies(self):
        return self.studies
    
    def get_all_study_labels(self):
        # Exclude None labels
        labels = [study.get_label() for study in self.studies if study.get_label() is not None]
        return labels

    def make_study(self, label=None, new_study_id=None, **variables):
        ''' Makes a new study  and returns reference to newly created study '''
        
        if new_study_id is None:
            # creates new study_id and add it to the set of used study_ids
            new_study_id = self._acquire_unique_id()
        
        if label:
            study = Study(study_id=new_study_id, label=label)
        else:
            study = Study(study_id=new_study_id) # use default label
        
        # assign variables
        for var_name, var_val in variables.items():
            study.set_var(var_name, var_val)
            
        # Add the study to the collection
        self.studies.add(study)
        
        return study
    
    def add_existing_study(self, study):
        ''' Adds a study object that was created elsewhere to the collection
            (i.e. from an Undo Command) '''
        
        study_id = study.get_id()
        # verification
        if study is None:
            raise Exception("Study is None!")
        if study_id is None:
            raise Exception("Study must have an id!")
        if study in self.studies:
            raise Exception("Study already in collection of studies!")
        if study_id in self.study_ids:
            raise Exception("Study id already in collection of study ids!")
        
        # Add the study to the set of studies and to the set of study ids
        self.studies.add(study)
        self.study_ids.add(study_id)
        return study
        
        
        
    
    def remove_study(self, study):
        # Just need to remove the study itself and then the study id from the
        # pool of used ids
        study_id = study.get_id()
        self.studies.remove(study)
        self.study_ids.remove(study_id)
