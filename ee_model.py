'''
Created on Jul 8, 2013

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *


import pdb
import string
from sets import Set
from functools import partial

# handrolled
from dataset.ee_dataset import EEDataSet
from globals import *

DEBUG = False

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
        self.label_column_name_label = "Study Labels"
        
        # for rowCount() and colCount()
        self.rowlimit = ADDITIONAL_ROWS
        self.collimit = ADDITIONAL_COLS
        
    def get_studies_in_current_order(self):
        studies = [self.rows_2_studies[row] for row in sorted(self.rows_2_studies.keys())]
        return studies
        
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
    
    
    ################ Get columns of a particular type ########################
    def get_catergorical_columns(self):
        return self._get_columns_of_type(CATEGORICAL)
    
    def get_continuous_columns(self):
        
        ''' returns a list of column indices with variables that have continuous data'''
        return self._get_columns_of_type(CONTINUOUS)
    
    def get_count_columns(self):
        return self._get_columns_of_type(COUNT)
    
    def _get_columns_of_type(self, var_type):
        ''' returns a list of column indices with variables of the desired type '''
        
        return sorted([col for col,var in self.cols_2_vars.items() if var.get_type()==var_type])
    
    ################# END get columns of a particular type ###################
    
    
    def _make_arbitrary_mapping_of_rows_to_studies(self):
        studies = self.dataset.get_studies()
        return dict(enumerate(studies))

    def _make_arbitrary_mapping_of_cols_to_variables(self):
        variables = self.dataset.get_variables()
        labeled_studies_present = len(self.dataset.get_study_labels()) != 0

        cols2vars = {}
        # just set the first column as label if there are labeled studies
        if labeled_studies_present:
            label_column = 0
            cols2vars.update(enumerate(variables, start=1))
        else:
            label_column = None
            cols2vars.update(enumerate(variables, start=0))
        return (cols2vars, label_column)
    
    def get_label_column(self):
        return self.label_column
        
        
    def rowCount(self, index=QModelIndex()):
        return self.rowlimit

        
        
    def change_row_count_if_needed(self):
        old_rowlimit = self.rowlimit
        max_occupied_row = self._get_max_occupied_row()
        if max_occupied_row is None:
            new_row_limit = ADDITIONAL_ROWS
        else:
            nearest_row_increment = int(round(float(max_occupied_row)/ADDITIONAL_ROWS) * ADDITIONAL_ROWS)
            new_rowlimit = nearest_row_increment + ADDITIONAL_ROWS
        if new_rowlimit != old_rowlimit:
            self.rowlimit = new_rowlimit
            self.beginResetModel()
            self.endResetModel()
            
    def change_column_count_if_needed(self):
        old_collimit = self.collimit
        max_occupied_col = self._get_max_occupied_col()
        if max_occupied_col is None:
            new_col_limit = ADDITIONAL_COLS
        else:
            nearest_col_increment = int(round(float(max_occupied_col)/ADDITIONAL_COLS) * ADDITIONAL_COLS)
            new_collimit = nearest_col_increment + ADDITIONAL_COLS
        if new_collimit != old_collimit:
            self.collimit = new_collimit
            self.beginResetModel()
            self.endResetModel()
    
    def columnCount(self, index=QModelIndex()):
        return self.collimit
    
    def _get_max_occupied_row(self):
        ''' Returns the highest numbered row index of the occupied rows
            returns None if no rows are occupied '''
        
        occupied_rows = self.rows_2_studies.keys()
        if len(occupied_rows) == 0:
            return None
        else:
            return max(occupied_rows)
        
    def _get_max_occupied_col(self):
        occupied_cols = Set(self.cols_2_vars.keys())
        if self.label_column is not None:
            occupied_cols.add(self.label_column)
        max_occupied_col = max(occupied_cols) if len(occupied_cols) != 0 else None
        return max_occupied_col

    def change_variable_name(self, var, new_name):
        ''' Change the name of a variable '''
        
        self.beginResetModel()
        var.set_label(new_name)
        self.endResetModel()


    def _get_column_assigned_to_variable(self, var):
        ''' Returns the index of the column assigned to the variable with name
        var_name '''
        
        return self._get_key_for_value(self.cols_2_vars, var)
    
    def get_variable_assigned_to_column(self, col):
        return self.cols_2_vars[col]
    
    def get_study_assigned_to_row(self, row):
        return self.rows_2_studies[row]
    
    def get_row_assigned_to_study(self, study):
        return self._get_key_for_value(self.rows_2_studies, study)
    
        
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
        
    
    def shift_column_assignments(self, columns, shift_amount):
        ''' Shifts the variable column assignments of the columns given in
        'columns' to the right by 'shift_amount' columns if shift amount is
        +ve, to the left if -ve
        
        Raising exception if new column assignment is already assigned to a
        variable '''
        
        shift_col = lambda col: col if col not in columns else col+shift_amount
        self.cols_2_vars = dict([(shift_col(col),var) for col,var in self.cols_2_vars.items()])
        


    def shift_row_assignments(self, rows, shift_amount):
        ''' Shifts the study row assignments of the rows given in rows down
        by 'shift_amount' rows if shift_amount is +ve, up if -ve '''
        
        shift_row = lambda row: row if row not in rows else row+shift_amount
        self.rows_2_studies = dict([(shift_row(row),study) for row,study in self.rows_2_studies.items()])

    
    def change_label_column_name(self, new_name):
        ''' Changes the name of the label column '''
        
        self.beginResetModel()
        self.label_column_name_label = new_name
        self.endResetModel()
        
    def get_column_name(self, column_index):
        ''' Returns the column name if we store a reference to it,
            raises an error otherwise'''
        
        # handle case that this is the label column
        if column_index == self.label_column:
            return self.label_column_name_label
        
        return self.cols_2_vars[column_index].get_label()
    
    def can_convert_variable_to_type(self, var, new_type):
        return self.dataset.can_convert_variable_to_type(var, new_type)
    
    def change_variable_type(self, var, new_type, precision):
        self.beginResetModel()
        self.dataset.change_variable_type(var, new_type, precision)
        self.endResetModel()
        
        
    def mark_column_as_label(self, column_index):
        ''' Sets the contents of this column as the labels for the studies in the column '''
        
        # Only one column can be set as the label column at a time
        if self.label_column:
            raise Exception("Only one column can be set as the label column at a time")
        
        var = self.get_variable_assigned_to_column(column_index)
        
        # Set values from column to be the study labels
        studies = self.dataset.get_studies()
        for study in studies:
            label = study.get_var(var)
            if label is not None:
                study.set_label(str(label))
            else:
                study.set_label(None)
        
        # Set label column label to the name of the variable
        self.label_column_name_label = var.get_label()
            
        # Delete references to that column in the studies and remove it from the variable collection
        self.remove_variable(var)
        
        # Mark the column as the label column
        self.label_column = column_index
        
    
    def remove_variable(self, var):
        ''' Deletes a variable from the collection and removes it from the
        mapping of columns to variables '''
        
        col = self._get_column_assigned_to_variable(var)
        
        self.dataset.remove_variable(var)
        del self.cols_2_vars[col]
        
    def remove_study(self, study):
        row = self.get_row_assigned_to_study(study)
        
        self.dataset.remove_study(study)
        del self.rows_2_studies[row]
        
    def remove_study_by_row(self, row):
        study = self.rows_2_studies[row]
        self.dataset.remove_study(study)
        del self.rows_2_studies[row]
    
    
    def removeColumns(self, column, count=1, index=QModelIndex()):
        # Deletes variable at the column's location and shifts columns left

        self.undo_stack.push(RemoveColumnsCommand(model=self,
                                                  column=column,
                                                  count=count,
                                                  description="Remove columns %d to %d" % (column, column+count-1)))
        return True
    
    
    def removeRows(self, row, count=1, index=QModelIndex()):
        ''' Deletes study the column's location and shifts rows up '''
    
        self.undo_stack.push(RemoveRowsCommand(model=self,
                                               row=row,
                                               count=count,
                                               description="Remove studies at rows %d to %d" % (row, row+count-1)))
        return True
    
    
    def insertRows(self, row, count=1, index=QModelIndex()):
        ''' Insert rows above selected row (just shifts studies down)'''
        
        self.undo_stack.push(InsertRowsCommand(model=self, 
                                               row=row,
                                               count=count,
                                               description="Insert %d rows before row %d" % (count, row)))
        return True
    
    
    def insertColumns(self, column, count=1, index=QModelIndex()):
        ''' Inserts columns before selected column (just shifts variables right) '''
        
        self.undo_stack.push(InsertColumnsCommand(model=self,
                                                  column=column,
                                                  count=count,
                                                  description="Insert %d columns before column %d" % (count, column)))
        return True






         
    def unmark_column_as_label(self, column_index):
        '''
        Unmark the column as the label column.
        Turns the column into a categorical variable '''
        
        # verification
        if self.label_column != column_index:
            raise Exception("This is not the label column!")
        
        # Add new variable with 'categorical' type (the most general)
        variable_name = self.label_column_name_label
        new_var = self.dataset.make_new_variable(label=variable_name, var_type=CATEGORICAL)
        # Assign the variable to the column
        self.cols_2_vars[column_index] = new_var
        
        # Set values from label column to be the values of the variable
        # Set labels to None in studies
        studies = self.dataset.get_studies()
        for study in studies:
            value = study.get_label()
            # converts the value from a string to a string (overkill but whatever)
            value = self.dataset.convert_var_value_to_type(CATEGORICAL, CATEGORICAL, value)
            study.set_var(new_var, value)
            study.set_label(None)
        
        # Un-mark label column
        self.label_column = None
        self.label_column_name_label = None
        
        
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
        
        if role == Qt.DisplayRole or role == Qt.EditRole:         
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
                var = self.cols_2_vars[col]
                var_value = study.get_var(var)
                if var_value is None: # don't display Nones
                    return QVariant()
                return QVariant(QString(self._var_value_for_display(var_value, var.get_type())))
            
        return QVariant()
    
    def column_assigned_to_variable(self, column_index):
        ''' Is the column assigned to a variable? '''
        return column_index in self.cols_2_vars
    
    def row_assigned_to_study(self, row_index):
        ''' Is the row assigned to a study? '''
        return row_index in self.rows_2_studies

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        
        if orientation == Qt.Horizontal:
            #default case
            unassigned_column = section not in self.cols_2_vars and section != self.label_column
            if unassigned_column:
                return QVariant(self.get_default_header(int(section)))
            
            # there is a study label or variable assignment to the column
            is_label_col = section == self.label_column
            if is_label_col:
                col_name = self.label_column_name_label
                suffix = " (label)"
            else: # is a variable column
                col_name = self.cols_2_vars[section].get_label()
                var_type = self.cols_2_vars[section].get_type()
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

            var = self.cols_2_vars[col]
            var_name = var.get_label()
            var_type = var.get_type()
            
            value_as_string = str(value.toString())
            # Set value in study for variable
            can_convert_value_to_desired_type = self.dataset.can_convert_var_value_to_type(var_type, value_as_string)
            if not can_convert_value_to_desired_type:
                self.emit(SIGNAL("DataError"), QString("Impossible Data Conversion"), QString("Cannot convert '%s' to %s data type" % (value_as_string, VARIABLE_TYPE_STRING_REPS[var_type])))
                cancel_macro_creation_and_revert_state()
                return False
                
            formatted_value = self._convert_input_value_to_correct_type_for_assignment(value_as_string, var_type)
            self.undo_stack.push(SetVariableValueCommand(study=study, variable=var, value=formatted_value))
            
            # If variables and label for this study are all blank, remove the
            # study from the dataset
            if study.is_totally_blank():
                self.undo_stack.push(RemoveStudyCommand(model=self, row=row))
            
        
        # End of the macro for undo/redo
        self.undo_stack.push(EmitDataChangedCommand(model=self, index=index))
        self.undo_stack.endMacro()
        
        self.dirty = True
        self.change_row_count_if_needed()
        self.change_column_count_if_needed()
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
        
    def get_default_header(self, col):
        if col > len(self.default_headers) - 1:
            self._generate_header_string(col*2)
        return self.default_headers[col]
    
    def get_default_header_string(self):
        return self.default_headers
    
    def _generate_header_string(self, length):
        self.default_headers = []
        for i,label in zip(range(length), excel_column_headers()):
            self.default_headers.append(QString(label))
        return self.default_headers
    
    
    def add_effect_sizes_to_model(self, metric, effect_sizes):
    
        studies = self.get_studies_in_current_order()
        last_occupied_col = sorted(self.cols_2_vars.keys(), reverse=True)[0]
        yi_col = last_occupied_col+1
        vi_col = yi_col+1
        
    
        self.undo_stack.beginMacro(QString("Adding effect size to spreadsheet"))
        
        start_cmd = GenericUndoCommand(redo_fn=self.beginResetModel,
                                      undo_fn=self.endResetModel)
        self.undo_stack.push(start_cmd)
        ##################################################################
        # Make new variables to hold the effect size calculations
        add_vi_cmd = MakeNewVariableCommand(model=self,
                                            var_name=METRIC_TEXT_SHORT[metric],
                                            col=yi_col,
                                            var_type=CONTINUOUS)
        add_yi_cmd = MakeNewVariableCommand(model=self,
                                            var_name="Var(%s)" % METRIC_TEXT_SHORT[metric],
                                            col=vi_col,
                                            var_type=CONTINUOUS)
        self.undo_stack.push(add_vi_cmd)
        self.undo_stack.push(add_yi_cmd)
        
        variable_yi = self.get_variable_assigned_to_column(yi_col)
        variable_vi = self.get_variable_assigned_to_column(vi_col)
        
        for study, val_yi, val_vi in zip(studies, effect_sizes['yi'], effect_sizes['vi']):
            set_vi_cmd = SetVariableValueCommand(study, variable_yi, val_yi)
            set_yi_cmd = SetVariableValueCommand(study, variable_vi, val_vi)
            self.undo_stack.push(set_vi_cmd)
            self.undo_stack.push(set_yi_cmd)
            
        ##################################################################
        end_cmd = GenericUndoCommand(redo_fn=self.endResetModel,
                                     undo_fn=self.beginResetModel)
        self.undo_stack.push(end_cmd)
        
        
        self.undo_stack.endMacro()
    
    
        
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
        if DEBUG: print("redo: make new study_command")
        model = self.model
        if self.study is None: # this should only execute once
            self.study = model.dataset.make_new_study()
        else:            # we should always be here on subsequent runs of redo
            model.dataset.add_existing_study(self.study)
        model.rows_2_studies[self.row] = self.study
    
    
    def undo(self):
        ''' Remove study at the specified row in the model '''
        
        if DEBUG: print("undo: make new study_command")
        model = self.model
        model.dataset.remove_study(self.study)
        del model.rows_2_studies[self.row]
        

class RemoveStudyCommand(QUndoCommand):
    ''' Removes / unremoves study at the specified row in the model '''
    def __init__(self, model, row):
        super(RemoveStudyCommand, self).__init__()
        
        self.setText(QString("Remove study @ row %d" % row))
        
        self.model = model
        self.row = row
        self.study = self.model.rows_2_studies[self.row]
        
    def redo(self):
        if DEBUG: print("redo: remove study")
        self.model.dataset.remove_study(self.study)
        del self.model.rows_2_studies[self.row]
        
    def undo(self):
        if DEBUG: print("undo: remove study")
        self.model.dataset.add_existing_study(self.study)
        self.model.rows_2_studies[self.row]=self.study

        
class SetStudyLabelCommand(QUndoCommand):
    ''' Sets/unsets the label of the given study '''
    
    def __init__(self, study, new_label):
        super(SetStudyLabelCommand, self).__init__()
        self.study = study
        self.new_label = new_label
        self.old_label = study.get_label()
        
        self.setText(QString("set study label from '%s' to '%s" % (self.old_label, self.new_label)))
        
    def redo(self):
        if DEBUG: print("redo: set study label")
        self.study.set_label(self.new_label)
        
    def undo(self):
        if DEBUG: print("undo: set study label")
        self.study.set_label(self.old_label)
        

class MakeNewVariableCommand(QUndoCommand):
    ''' Creates/Deletes a new variable and assigns it to the given column '''
    
    def __init__(self, model, var_name, col, var_type=CATEGORICAL):
        super(MakeNewVariableCommand, self).__init__()
        
        self.model = model
        self.var_name = var_name
        self.col = col
        self.var_type = var_type
        
        self.var = None # this is where the new variable will be kept
        
        self.setText(QString("Created variable '%s'" % self.var_name))
        
        
    def redo(self):
        if DEBUG: print("redo: make new variable_command")
        if self.var is None:
            self.var = self.model.dataset.make_new_variable(label=self.var_name, var_type=self.var_type)
        else:
            self.model.dataset.add_existing_variable(self.var)
        self.model.cols_2_vars[self.col] = self.var
        
    def undo(self):
        if DEBUG: print("undo: make new variable_command")
        self.model.remove_variable(self.var)
        

class SetVariableValueCommand(QUndoCommand):
    ''' Sets/unsets the value of the variable for the given study'''
    
    def __init__(self, study, variable, value):
        super(SetVariableValueCommand, self).__init__()
        
        self.study = study
        self.variable = variable
        self.new_value = value
        self.old_value = self.study.get_var(variable)
        
        self.setText(QString("Set '%s' from '%s' to '%s' for a study" % (self.variable.get_label(), str(self.old_value), str(self.new_value))))
        
    def redo(self):
        if DEBUG: print("redo: set variable value command")
        self.study.set_var(self.variable, self.new_value)

    def undo(self):
        if DEBUG: print("undo: set variable value command")
        self.study.set_var(self.variable, self.old_value)

class EmitDataChangedCommand(QUndoCommand):
    ''' Not really a command, just the last thing called @ the end of the macro
    in setData in order to notify the view that the model has changed '''
    
    def __init__(self, model, index):
        super(EmitDataChangedCommand, self).__init__()
        
        self.model = model
        self.index = index
        
        self.setText(QString("Data changed emission"))
    
    def undo(self):
        if DEBUG: print("undo: emit data changed")
        self.model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
          self.index, self.index)
        
    def redo(self):
        if DEBUG: print("redo: emit data changed")
        self.model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
          self.index, self.index)
        
        
class RemoveColumnsCommand(QUndoCommand):
    ''' Removes columns from the model spreadsheet: used in reimplemented
    removeColumns function'''
    
    # column is the start column
    def __init__(self, model, column, count, description="Remove columns"):
        super(RemoveColumnsCommand, self).__init__()
        
        self.setText(QString(description))
        
        self.model = model
        self.column = column
        self.count = count
        
        self.label_column = None 
        self.label_column_label = None
        self.studies_2_labels = {} # mapping of studies to study labels
        self.removed_cols_2_vars = {}  # dictionary of variables and their mappings to columns that have been removed
        
        # 2-level dictionary storing the study values for the removed variables
        # vars-->dictionary(studies-->values)
        self.variables_2_studies_2_values = {} 
        
        # Save info from cols that will be removed
        for col in range(self.column, self.column+self.count):
            if col == self.model.label_column:
                self.save_label_column_info(col)
            # col is a variable column
            if self.model.column_assigned_to_variable(col):
                self._store_variable_column_data(col) # variable index, variable data in studies

        
    def redo(self):
        self.model.beginRemoveColumns(QModelIndex(), self.column, self.column + self.count - 1)
        
        # Delete variables in columns
        for col in range(self.column, self.column+self.count):
            # turn label column in to a variable before deletion
            if col == self.model.label_column: 
                self.model.unmark_column_as_label(col)
            # remove variable
            if self.model.column_assigned_to_variable(col):
                var = self.model.get_variable_assigned_to_column(col)
                self.model.remove_variable(var)
        
        # Shift columns beyond column+count-1 to the left by count columns
        self.cols_to_shift = []
        for col in self.model.cols_2_vars.keys():
            if col > self.column+self.count-1:
                self.cols_to_shift.append(col)
        self.model.shift_column_assignments(self.cols_to_shift, -self.count)
        
        self.model.endRemoveColumns()
        
        
    def undo(self):   
        self.model.beginInsertColumns(QModelIndex(), self.column, self.column + self.count - 1)
        
        # shift columns to the right (reclaiming the space for the deleted columns)
        cols_to_shift_right = [col-self.count for col in self.cols_to_shift]
        self.model.shift_column_assignments(cols_to_shift_right, self.count)
        
        # restore label column data if it was deleted
        if self.label_column:
            self.restore_label_column()
            
        # restore variable column data
        for col in self.removed_cols_2_vars.keys():
            self._restore_variable_column_data(col)
        
        self.model.endInsertColumns()
    
    def restore_label_column(self):
        self.model.label_column = self.label_column
        self.model.label_column_name_label = self.label_column_label
        
        for study in self.model.dataset.get_studies():
            label = self.studies_2_labels[study]
            study.set_label(label)
        
    def save_label_column_info(self, col):
        self.label_column = col
        self.label_column_label = self.model.label_column_name_label
        for study in self.model.dataset.get_studies():
            self.studies_2_labels[study] = study.get_label()
        
    def _store_variable_column_data(self, col):
        ''' Stores the data from the variable_column '''
        
        # store column index
        var = self.model.cols_2_vars[col]
        self.removed_cols_2_vars[col] = var
        
        self.variables_2_studies_2_values[var] = {}
        # store data from studies
        for study in self.model.dataset.get_studies():
            self.variables_2_studies_2_values[var][study] = study.get_var(var)
            
    def _restore_variable_column_data(self, col):
        var = self.removed_cols_2_vars[col]
        
        # reinsert variable into dataset
        self.model.dataset.add_existing_variable(var)
        
        # recreate mapping of variable to column
        self.model.cols_2_vars[col] = var
        
        # copy stored variable data for studies back into place
        for study in self.model.dataset.get_studies():
            value = self.variables_2_studies_2_values[var][study]
            study.set_var(var, value)
        
        
class RemoveRowsCommand(QUndoCommand):
    ''' Removes rows (studies) from the model: used in reimplemented
    removeRows function '''
    
    def __init__(self, model, row, count, description="Remove Rows"):
        super(RemoveRowsCommand, self).__init__()
        
        self.setText(QString(description))
        
        self.model = model
        self.row = row
        self.count = count
        
        self.removed_rows_2_studies = {}
        # Save studies that will be removed
        for row in range(self.row, self.row+self.count):
            # row is an assigned row
            if row in self.model.rows_2_studies:
                study = self.model.rows_2_studies[row]
                self.removed_rows_2_studies[row] = study
                
    def redo(self):
        self.model.beginRemoveRows(QModelIndex(), self.row, self.row+self.count-1)
        
        # remove studies on rows we are removing
        for row in self.removed_rows_2_studies.keys():
            self.model.remove_study_by_row(row)
            
        # shift rows beyond row + count-1 up by count rows
        self.rows_to_shift = []
        for row in self.model.rows_2_studies.keys():
            if row > self.row + self.count - 1:
                self.rows_to_shift.append(row)
        self.model.shift_row_assignments(self.rows_to_shift, -self.count)
            
        
        self.model.endRemoveRows()
        
    def undo(self):
        self.model.beginInsertRows(QModelIndex(), self.row, self.row+self.count-1)
        
        # shift rows down (reclaiming space for the deleted rows)
        rows_to_shift_down = [row-self.count for row in self.rows_to_shift]
        self.model.shift_row_assignments(rows_to_shift_down, self.count)
        
        
        # restore studies to rows and in dataset
        for row, study in self.removed_rows_2_studies.items():
            self.model.dataset.add_existing_study(study)
            self.model.rows_2_studies[row] = study
        
        self.model.endInsertRows()
        
        

class InsertRowsCommand(QUndoCommand):
    ''' Inserts rows at the requested location: used in reimplemented
    insertRows function '''
    
    def __init__(self, model, row, count, description="Insert Rows"):
        super(InsertRowsCommand, self).__init__()
        
        self.setText(QString(description))
        
        self.model = model
        self.row = row
        self.count = count
        
    def redo(self):
        self.model.beginInsertRows(QModelIndex(), self.row, self.row+self.count-1)
        
        # shift rows down making space for more studies
        self.rows_to_shift_down = [row for row in self.model.rows_2_studies.keys() if row >= self.row]
        self.model.shift_row_assignments(self.rows_to_shift_down, self.count)
        
        
        self.model.endInsertRows()
        
        
        
    def undo(self):
        self.model.beginRemoveRows(QModelIndex(), self.row, self.row+self.count-1)
        
        # shift rows back up
        rows_to_shift_up = [row+self.count for row in self.rows_to_shift_down]
        self.model.shift_row_assignments(rows_to_shift_up, -self.count)
        
        self.model.endRemoveRows()
        
        
class InsertColumnsCommand(QUndoCommand):
    ''' Inserts columns at the requested location: used in reimplemented
    insertColumns function '''
    
    def __init__(self, model, column, count, description="Insert Columns"):
        super(InsertColumnsCommand, self).__init__()
        
        self.setText(QString(description))
        
        self.model = model
        self.column = column
        self.count = count
        
        self.label_column_was_shifted = None
        
    def redo(self):
        self.model.beginInsertColumns(QModelIndex(), self.column, self.column + self.count - 1)
        
        self.variable_columns_to_shift_right = [col for col in self.model.cols_2_vars.keys() if col >= self.column]
        self.model.shift_column_assignments(self.variable_columns_to_shift_right, self.count)
        if self.model.label_column >= self.column:
            self.model.label_column = self.model.label_column + self.count
        
        
        self.model.endInsertColumns()
        
    def undo(self):
        self.model.beginRemoveColumns(QModelIndex(), self.column, self.column + self.count - 1)
        
        # shift columns back (left)
        cols_to_shift_left = [col+self.count for col in self.variable_columns_to_shift_right]
        self.model.shift_column_assignments(cols_to_shift_left, -self.count)
        
        # was label was shifted in redo/step?
        if self.model.label_column >= self.column + self.count:
            self.model.label_column -= self.count # if so, shift it back
        
        self.model.endRemoveColumns()