'''
Created on Jul 8, 2013

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *


import pdb
import string

# handrolled
from ee_dataset import EEDataSet
from globals import *

# Some constants
ADDITIONAL_ROWS = 100
ADDITIONAL_COLS = 40

# Forbidden variable names
LABEL_PREFIX_MARKER  = "*lbl*" # marker placed at start of a label(but is not displayed)
FORBIDDEN_VARIABLE_NAMES = [LABEL_PREFIX_MARKER,]

# TODO:
# * Don't show option to change the format of a column marked as label
# * Add options to mark/unmark column as label ----> categorical

class EETableModel(QAbstractTableModel):
    def __init__(self, undo_stack):
        super(EETableModel, self).__init__()
        
        # Give model access to undo_stack
        self.undo_stack = undo_stack
        self.dataset = EEDataSet()
        
        
        ###self.filename = filename
        self.precision = DEFAULT_PRECISION
        self.dirty = False
        
        self.default_headers = self._generate_header_string(ADDITIONAL_COLS)
    
        # mapping rows to studies
        # For each variable name, store its column location
        #    the label column (if it exists) is included here even though it
        #    is not really a variable
        self.rows_2_studies = self._make_arbitrary_mapping_of_rows_to_studies()
        (self.cols_2_vars, self.label_column) = self._make_arbitrary_mapping_of_cols_to_variables()
        
    def __str__(self):
        rows_2_study_ids = dict([(row, study.get_id()) for (row, study) in self.rows_2_studies.items()])
        
        
        summary_str = "Dataset Info: %s\n" % str(self.dataset)
        model_info = "  ".join(["Model Info:\n",
                                "Precision: %d\n" % self.precision,
                                "Dirty: %s\n" % str(self.dirty),
                                "Label Column: %s\n" % self.label_column,
                                "Rows-to-study ids: %s\n" % str(rows_2_study_ids),
                                "Columns to variables: %s\n" % str(self.cols_2_vars)])
        return summary_str + model_info
    
    def get_study_by_id(self, study_id):
        return self.dataset.get_study_by_id(study_id)
    
    def _make_arbitrary_mapping_of_rows_to_studies(self):
        studies = self.dataset.get_all_studies()
        return dict(enumerate(studies))

    def _make_arbitrary_mapping_of_cols_to_variables(self):
        variable_names = self.dataset.get_all_variable_names()
        labeled_studies_present = len(self.dataset.get_all_study_labels()) != 0

        cols2vars = {}
        # just set the first column as label if there are labeled studies
        if labeled_studies_present:
            label_column = 0
            cols2vars[0] = "Study Labels"
            cols2vars.update(enumerate(variable_names, start=1))
        else:
            label_column = None
            cols2vars.update(enumerate(variable_names, start=0))
        return (cols2vars, label_column)
    
    def get_label_column(self):
        return self.label_column
        
        
    def rowCount(self, index=QModelIndex()):
        max_occupied_row = self._get_max_occupied_row()
        if max_occupied_row is None:
            return ADDITIONAL_ROWS
        return max_occupied_row + ADDITIONAL_ROWS
    
    
    def columnCount(self, index=QModelIndex()):
        occupied_cols = self.cols_2_vars.keys()
        max_occupied_col = max(occupied_cols) if len(occupied_cols) != 0 else None
        if max_occupied_col is None:
            return ADDITIONAL_COLS
        return max_occupied_col + ADDITIONAL_COLS
    
    def _get_max_occupied_row(self):
        ''' Returns the highest numbered row index of the occupied rows
            returns None if no rows are occupied '''
        
        occupied_rows = self.rows_2_studies.keys()
        if len(occupied_rows) == 0:
            return None
        else:
            return max(occupied_rows)


    def change_variable_name(self, old_name, new_name):
        ''' Change the name of a variable '''
        
        # change name in dataset and in the mapping from column names to
        # variable names
        self.beginResetModel()
        column = self._get_column_assigned_to_variable(old_name)
        self.dataset.change_variable_name(old_name, new_name)
        self.cols_2_vars[column] = new_name
        self.endResetModel()
        
        print("After changing variable %s to %s:" % (old_name,new_name))
        print(self)


    def _get_column_assigned_to_variable(self, var_name):
        ''' Returns the index of the column assigned to the variable with name
        var_name '''
        
        return self._get_key_for_value(self.cols_2_vars, var_name)
    
        
    def _get_key_for_value(self, adict, value):
        '''
        * Returns a list of keys that point to given value if the there are
        more than one such key.
        * Returns a single key (scalar) if there is only one key pointing to
        the given value
        * Returns None if there are no such keys '''
        
        keylist = []
        for k,v in adict.items():
            if v == value:
                keylist.append(k)
        if len(keylist) == 1:
            return keylist[0]
        elif len(keylist) == 0:
            return None
        else:
            return keylist
            
        
    
    def change_label_column_name(self, new_name):
        ''' Changes the name of the label column '''
        
        if new_name in self.dataset.get_all_variable_names():
            raise Exception("Cannot change label column name to existing variable column name")
        
        self.rows_2_studies[self.label_column] = new_name
        
    def get_column_name(self, column_index):
        ''' Returns the column name if we store a reference to it,
            raises an error otherwise'''
        
        return self.cols_2_vars[column_index]
    
    def get_variable_type(self, var_name):
        return self.dataset.get_variable_type(var_name)
    
    def can_convert_variable_to_type(self, var_name, new_type):
        return self.dataset.can_convert_variable_to_type(var_name, new_type)
    
    def change_variable_type(self, var_name, new_type, precision):
        self.beginResetModel()
        self.dataset.change_variable_type(var_name, new_type, precision)
        self.endResetModel()
        
    def get_all_variable_names(self):
        return self.dataset.get_all_variable_names()
        
    def mark_column_as_label(self, column_index):
        ''' Sets the contents of this column as the labels for the studies in the column '''
        
        # Only one column can be set as the label column at a time
        if self.label_column:
            raise Exception("Only one column can be set as the label column at a time")
        
        
        variable_name = self.get_column_name(column_index)
        
        # Set values from column to be the study labels
        # Delete references to that column in the studies
        # Mark the column as the label column
        studies = self.dataset.get_all_studies()
        for study in studies:
            label = str(study.get_var(variable_name))
            study.set_label(label)
        self.dataset.remove_variable(variable_name)
        self.label_column = column_index
         
    def unmark_column_as_label(self, column_index):
        '''
        Unmark the column as the label column.
        Turns the column into a categorical variable '''
        
        # verification
        if self.label_column != column_index:
            raise Exception("This is not the label column!")
        
        # Add new variable with 'categorical' type (the most general)
        variable_name = self.get_column_name(column_index)
        self.dataset.add_variable(variable_name, CATEGORICAL)
        
        # Set values from label column to be the values of the variable
        # Set labels to None
        # Un-mark label column
        studies = self.dataset.get_all_studies()
        for study in studies:
            value = study.get_label()
            # converts the value from a string to a string (overkill but whatever)
            value = self.dataset.convert_var_value_to_type(CATEGORICAL, CATEGORICAL, value)
            study.set_var(variable_name, value)
            study.set_label(None)
        self.label_column = None
        
        
    def set_precision(self, new_precision):
        ''' Sets precision (# of decimals after the decimal point for continuous)
        variable values '''
        
        self.precision = new_precision
        
        
    def get_precision(self):
        return self.precision
        
        
    def _var_value_for_display(self, value, var_type):
        ''' Converts the variable value to a suitable string representation
        according to its type '''
        
        old_type = var_type
        # This just properly formats the value with the right precision
        # We're not actually saving a converted value in the dataset
        # TODO: should probably make this function static in the dataset
        return self.dataset.convert_var_value_to_type(old_type, CATEGORICAL, value, precision=self.precision)
            
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        max_occupied_row = self._get_max_occupied_row()
        if max_occupied_row and not (0 <= index.row() <= max_occupied_row):
            return QVariant()
        
        row, col = index.row(), index.column()
        is_study_row = row in self.rows_2_studies
        is_label_col = col == self.label_column
        
        
        
        if role == Qt.DisplayRole:         
            if not is_study_row: # no study for this row, no info to display
                return QVariant()
            
            # Get the study this to which this row refers
            study = self.rows_2_studies[row]
            
            if is_label_col:
                label = study.get_label()
                if label is None: # no label
                    return QVariant()
                return QVariant(QString(label))
            else: # is a variable column
                if not self.column_assigned_to_variable(col):
                    return QVariant()
                
                # the column is assigned to a variable
                var_name = self.cols_2_vars[col]
                var_type = self.dataset.get_variable_type(var_name)
                var_value = study.get_var(var_name)
                if var_value is None: # don't display Nones
                    return QVariant()
                return QVariant(QString(self._var_value_for_display(var_value, var_type)))
            
        return QVariant()

    def _variable_exists(self, var_name):
        return var_name in self.cols_2_vars.values()
    def column_assigned_to_variable(self, column_index):
        return column_index in self.cols_2_vars.keys()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        
        if orientation == Qt.Horizontal:
            #default case
            unassigned_column = section not in self.cols_2_vars
            if unassigned_column:
                return QVariant(self.get_default_header(int(section)))
            
            # there is a study label or variable assignment to the column
            is_label_col = section == self.label_column
            col_name = self.cols_2_vars[section]
            if is_label_col:
                suffix = " (label)"
            else: # is a variable column
                var_type = self.dataset.get_variable_type(col_name)
                suffix = " (%s)" % VARIABLE_TYPE_SHORT_STRING_REPS[var_type]
            return QVariant(QString(col_name + suffix))
            
        elif orientation == Qt.Vertical:
            return QVariant(int(section + 1))
        


    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() and not (0 <= index.row() < self.columnCount()):
            return False
        if role != Qt.EditRole:
            print("No implementation written when role != Qt.EditRole")
            return False
        
        row, col = index.row(), index.column()
        row_has_study = row in self.rows_2_studies
        is_label_col = col == self.label_column
        
        value_blank = value is None or str(value.toString()) == ""
        
        def cancel_macro_creation_and_revert_state():
            ''' Ends creation of macro (in progress) and reverts the state of
            the model to before the macro began to be created '''
            
            #print("Cancelling macro creation and reverting")
            self.undo_stack.endMacro()
            self.undo_stack.undo()
        
        # For doing/undoing all the sub_actions in one go
        # The emit data changed is so that it will be called LAST when the
        # macro is undone
        self.undo_stack.beginMacro(QString("SetDataMacro: (%d,%d), value: '%s'" % (row,col, value.toString())))
        self.undo_stack.push(EmitDataChangedCommand(model=self, index=index))
        
        if not row_has_study: # no study on this row yet, we will make one
            if value_blank:
                cancel_macro_creation_and_revert_state()
                return False
            self.undo_stack.push(MakeStudyCommand(model=self, row=row))
            
        study = self.rows_2_studies[row]
        
        if is_label_col:
            existing_label = study.get_label()
            proposed_label = str(value.toString())
            if proposed_label != existing_label:
                self.undo_stack.push(SetStudyLabelCommand(study=study, new_label=proposed_label))
            else:
                cancel_macro_creation_and_revert_state()
                return False
        else: # we are in a variable column (initialized or not)
            make_new_variable = not self.column_assigned_to_variable(col)
            if make_new_variable: # make a new variable and give it the default column header name
                if value_blank:
                    cancel_macro_creation_and_revert_state()
                    return False
                new_var_name = str(self.get_default_header(col))
                self.undo_stack.push(MakeNewVariableCommand(model=self, var_name=new_var_name, col=col))

            
            var_name = self.cols_2_vars[col]
            var_type = self.dataset.get_variable_type(var_name)
            
            value_as_string = str(value.toString())
            # Set value in study for variable
            can_convert_value_to_desired_type = self.dataset.can_convert_var_value_to_type(var_type, value_as_string)
            # TODO: finish this when a value that doesn't match the type of the variable is entered
            #if not can_convert_value_to_desired_type:
            #    emit(SIGNAL("WrongDataType"), 
            
            formatted_value = self._convert_input_value_to_correct_type_for_assignment(value_as_string, var_type)
            self.undo_stack.push(SetVariableValueCommand(study=study, variable_name=var_name, value=formatted_value))
            
            # TODO:
            # 1. check if variables and label for this study are all blank
            # if so, remove the study from the dataset
        
        # End of the macro for undo/redo
        self.undo_stack.push(EmitDataChangedCommand(model=self, index=index))
        self.undo_stack.endMacro()
        
        self.dirty = True
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                  index, index)
        
        return True
    
    def _emitdatachanged(self, model, index):
        model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                  index, index)
        
    def _convert_input_value_to_correct_type_for_assignment(self, value, var_type):
        ''' Converts input value (assumged to a be a string) to the correct type
        required by a variable of type var_type '''
        
        return self.dataset.convert_var_value_to_type(CATEGORICAL,
                                                      var_type,
                                                      value,
                                                      precision=self.precision)


    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|
                            Qt.ItemIsEditable)
        
        
        
    #def insertRows()
    #def removeRows()


    
    def get_default_header(self, col):
        if col > len(self.default_headers):
            self._generate_header_string(col*2)
        return self.default_headers[col]
    
    def get_default_header_string(self):
        return self.default_headers
    
    def _generate_header_string(self, length):
        self.default_headers = []
        for i,label in zip(range(length), excel_column_headers()):
            self.default_headers.append(QString(label))
        return self.default_headers
    
    
        
##generate_blank_list = lambda length: [None for x in range(length)]
########### Generate Excel-style default headers #############################
# inspired by: http://thinkpython.blogspot.com/2006/10/working-with-excel-column-labels.html" '''
def excel_column_headers():
    alphabet = string.ascii_uppercase
    for x in alphabet:
        yield x
    for exCh in excel_column_headers():
        for x in alphabet:
            yield exCh + x
##############################################################################


############################# Undo Command Classes ###########################
class MakeStudyCommand(QUndoCommand):
    ''' Makes a new study at the specified row in the model'''
    
    def __init__(self, model, row):
        super(MakeStudyCommand, self).__init__()
        
        self.setText(QString("MakeStudy @ Row %d" % row))
        
        self.model = model
        self.row = row
        
        self.study = None
        
        
        
    def redo(self):
        model = self.model
        if self.study is None: # this should only execute once
            self.study = model.dataset.make_study()
        else:            # we should always be here on subsequent runs of redo
            model.dataset.add_existing_study(self.study)
        model.rows_2_studies[self.row] = self.study
        
    
    def undo(self):
        ''' Remove study at the specified row in the model '''
        
        model = self.model
        model.dataset.remove_study(self.study)
        del model.rows_2_studies[self.row]
        
class SetStudyLabelCommand(QUndoCommand):
    ''' Sets/unsets the label of the given study '''
    
    def __init__(self, study, new_label):
        super(SetStudyLabelCommand, self).__init__()
        self.study = study
        self.new_label = new_label
        self.old_label = study.get_label()
        
        self.setText(QString("set study label from '%s' to '%s" % (self.old_label, self.new_label)))
        
    def redo(self):
        self.study.set_label(self.new_label)
        
    def undo(self):
        self.study.set_label(self.old_label)
        

class MakeNewVariableCommand(QUndoCommand):
    ''' Creates/Deletes a new variable and assigns it to the given column '''
    
    def __init__(self, model, var_name, col, var_type=CATEGORICAL):
        super(MakeNewVariableCommand, self).__init__()
        
        self.model = model
        self.var_name = var_name
        self.col = col
        self.var_type = var_type
        
        self.setText(QString("Created variable '%s'" % self.var_name))
        
        
    def redo(self):
        self.model.dataset.add_variable(self.var_name, self.var_type)
        self.model.cols_2_vars[self.col] = self.var_name
        
    def undo(self):
        self.model.dataset.remove_variable(self.var_name)
        del self.model.cols_2_vars[self.col]
        

class SetVariableValueCommand(QUndoCommand):
    ''' Sets/unsets the value of the variable for the given study'''
    
    def __init__(self, study, variable_name, value):
        super(SetVariableValueCommand, self).__init__()
        
        self.study = study
        self.variable_name = variable_name
        self.new_value = value
        self.old_value = self.study.get_var(variable_name)
        
        self.setText(QString("Set '%s' from '%s' to '%s' for a study" % (self.variable_name, str(self.old_value), str(self.new_value))))
        
    def redo(self):
        self.study.set_var(self.variable_name, self.new_value)

    def undo(self):
        self.study.set_var(self.variable_name, self.old_value)

class EmitDataChangedCommand(QUndoCommand):
    ''' Not really a command, just the last thing called @ the end of the macro
    in setData in order to notify the view that the model has changed '''
    
    def __init__(self, model, index):
        super(EmitDataChangedCommand, self).__init__()
        
        self.model = model
        self.index = index
        
        self.setText(QString("Data changed emission"))
    
    def undo(self):
        self.model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
          self.index, self.index)
        
    def redo(self):
        self.model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
          self.index, self.index)