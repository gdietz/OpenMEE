#########################
#                       #
# Author: George Dietz  #
#                       #
#########################

from globals import *
import study_collection
import variable_collection


class ConversionError(Exception):
    def __init__(self, arg):
        self.args = arg


class EEDataSet():
    def __init__(self):
        self.study_collection = study_collection.StudyCollection()
        self.variable_collection = variable_collection.VariableCollection()
        
        
    ################ Methods for manipulating studies only ################
    # This section is a wrapper to the study collection interface
    def add_existing_study(self, study):
        return self.study_collection.add_existing_item(study)
    
    def get_study_ids(self):
        return self.study_collection.get_ids()
    
    def get_study_by_id(self, study_id):
        return self.study_collection.get_item_by_id(study_id)
    
    def get_studies(self):
        return self.study_collection.get_items()
    
    def get_studies_by_label(self, label):
        return self.study_collection.get_items_by_label(label)

    def get_study_labels(self):
        return self.study_collection.get_labels()

    def make_new_study(self, label=None):
        return self.study_collection.make_item(label)

    def remove_study(self, study):
        self.study_collection.remove_item(study)
    ############## End methods for manipulating studies only ###############
    
    ################ Methods for manipulating variables only #################
    # This section is a wrapper to the variable collection interface
    def add_existing_variable(self, var):
        return self.variable_collection.add_existing_item(var)
    
    def get_variable_ids(self):
        return self.variable_collection.get_ids() 
    
    def get_variable_by_id(self, var_id):
        return self.variable_collection.get_item_by_id(var_id)
    
    def get_variables(self):
        return self.variable_collection.get_items()
    
    def get_variables_by_label(self, label):
        return self.variable_collection.get_items_by_label(label)
    
    def get_variable_labels(self):
        return self.variable_collection.get_labels()

    def make_new_variable(self, label=None, var_type=CATEGORICAL):
        var = self.variable_collection.make_item(label)
        var.set_type(var_type)
        return var
    
    ################# End methods for manipulating variables #################
    
    ######### Methods which manipulate both variables and studies  ##########
    def change_variable_type(self, var, new_type, precision=DEFAULT_PRECISION):
        '''
        1. Recasts all the stored values for that variable type in the studies
        2. Changes the variable type for the variable itself
        '''
        
        # verification
        if new_type not in VARIABLE_TYPES:
            raise ValueError("Type not in allowed types")
        if not self.can_convert_variable_to_type(var, new_type):
            raise ConversionError("Unable to convert '%s' to type '%s'" % (var.get_label(), VARIABLE_TYPE_STRING_REPS[new_type]))
        
        old_type = var.get_type()
        for study in self.study_collection.get_studies_with_variable(var):
            value = study.get_var(var)
            converted_value = self.convert_var_value_to_type(old_type, new_type, value, precision)
            study.set_var(var, converted_value)
        
        # change variable type in the variable itself
        var.set_type(new_type)
    
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
        ''' Returns value converted from old_type to new_type
        Doesn't do any verification (assumes this has already been done) '''
        
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
        
    def can_convert_variable_to_type(self, var, new_type):
        '''
        Returns True if it is possible to convert the type of variable called
        var_name to the new_type for all studies (examines the values it takes
        in the studies)
        '''
        
        old_type = var.get_type()
        for study in self.study_collection.get_studies_with_variable(var):
            value = study.get_var(var)
            # verification
            if not self.can_convert_var_value_to_type(new_type, value):
                return False
        return True


    def remove_variable(self, var):
        '''
        1. Remove entry for variable in all the studies
        2. Delete the variable from the variable collection
        '''
        
        # verification
        if var not in self.variable_collection.get_items():
            raise ValueError("Attempted to delete non-existing variable")
        
        for study in self.study_collection.get_studies_with_variable(var):
            study.remove_variable(var)
        self.variable_collection.remove_item(var)

    
    ####### End methods for manipulating variables ##########
    
    
    def __str__(self):
        return self._get_studies_summary() + "\n" + self._get_variables_summary()
    
    def _get_variables_summary(self):
        output_str = "Variables Summary:\n"
        variables_summary = [["ID:","Label:", "Type:"],]
        
        for var in self.variable_collection.get_items():
            variables_summary.append([str(var.get_id()), str(var.get_label()), str(var.get_type())])
        return output_str+table_as_str(variables_summary)
        
    def _get_studies_summary(self):
        ''' Returns a string summarizing info about the studies '''
        
        sorted_study_ids = sorted(self.study_collection.get_ids())
        sorted_studies = [self.study_collection.get_item_by_id(study_id) for study_id in sorted_study_ids]
                
        sorted_variables = sorted(self.variable_collection.get_items(), key=lambda var: var.get_label())
        sorted_variable_names = [var.get_label() for var in self.variable_collection.get_items()]
        sorted_variable_types = [VARIABLE_TYPE_STRING_REPS[var.get_type()] for var in sorted_variables]
        
        studies_summary_str = "Summary of Studies:\n"
        
        summary_table_header0 = ["",""]
        summary_table_header0.extend(sorted_variable_types)
        summary_table_header1 = ['study id','study label']
        summary_table_header1.extend(sorted_variable_names)
        summary_table_header1 = tuple(summary_table_header1)
        
        study_summaries = [summary_table_header0, summary_table_header1]
        for study in sorted_studies:
            info = [study.get_id(), study.get_label()]
            info.extend([study.get_var(var) for var in sorted_variables])
            f = lambda x: str(x) if x is not None else ""
            info = [f(x) for x in info]
            study_summaries.append(info)
        
        studies_summary_str += table_as_str(study_summaries)
        return studies_summary_str