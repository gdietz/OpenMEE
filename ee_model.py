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
import copy

# handrolled
from dataset.ee_dataset import EEDataSet
from globals import *

# Some constants
ADDITIONAL_ROWS = 100
ADDITIONAL_COLS = 40

# Forbidden variable names
LABEL_PREFIX_MARKER  = "*lbl*" # marker placed at start of a label(but is not displayed)
FORBIDDEN_VARIABLE_NAMES = [LABEL_PREFIX_MARKER,]

class ModelState:
    def __init__(self, dataset, dirty, rows_2_studies, cols_2_vars,
                 label_column, label_column_name_label, data_location_choices,
                 previous_study_inclusion_state, column_groups):
        self.dataset   = dataset
        self.dirty     = dirty
        self.rows_2_studies = rows_2_studies
        self.cols_2_vars    = cols_2_vars
        self.label_column   = label_column
        self.label_column_name_label = label_column_name_label
        self.data_location_choices = data_location_choices
        self.previous_study_inclusion_state = previous_study_inclusion_state
        self.variable_groups = column_groups
        

class EETableModel(QAbstractTableModel):
    
    column_formats_changed = pyqtSignal()
    studies_changed = pyqtSignal()
    label_column_changed = pyqtSignal()
    column_groups_changed = pyqtSignal()
    
    def __init__(self, undo_stack, user_prefs, model_state=None):
        super(EETableModel, self).__init__()
        
        # Give model access to undo_stack
        self.undo_stack = undo_stack
        
        self.user_prefs = user_prefs
        if "color_scheme" not in self.user_prefs:
            self.user_prefs["color_scheme"]=DEFAULT_COLOR_SCHEME
        
        
        if model_state is None:
            self.dataset = EEDataSet()
            self.dirty = False
            self.data_location_choices = {} # maps data_types to column choices
            self.previous_study_inclusion_state = {}
            
            # mapping rows to studies
            self.rows_2_studies = self._make_arbitrary_mapping_of_rows_to_studies()
            self.studies_changed.emit()
            # For each variable name, store its column location
            (self.cols_2_vars, self.label_column) = self._make_arbitrary_mapping_of_cols_to_variables()
            self.label_column_changed.emit()
            self.label_column_name_label = "Study Labels"
            
            # Store groups of related variables
            self.variable_groups = []
        else:
            self.load_model_state(model_state)
        
        
        self.default_headers = self._generate_header_string(ADDITIONAL_COLS)
        # for rowCount() and colCount()
        self.rowlimit = ADDITIONAL_ROWS
        self.collimit = ADDITIONAL_COLS
        self.change_column_count_if_needed()
        self.change_row_count_if_needed()
        
    def set_user_prefs(self, user_prefs):
        self.user_prefs = user_prefs
    
    def get_state(self):
        ''' returns a class representing the model's state '''
        
        return ModelState(dataset   = self.dataset,
                          dirty     = self.dirty,
                          rows_2_studies = self.rows_2_studies, 
                          cols_2_vars    = self.cols_2_vars,
                          label_column   = self.label_column,
                          label_column_name_label = self.label_column_name_label,
                          data_location_choices = self.data_location_choices,
                          previous_study_inclusion_state = self.previous_study_inclusion_state,
                          column_groups = self.variable_groups
                          )
        
        
    def load_model_state(self, state):
        self.dataset        = state.dataset
        self.dirty          = state.dirty
        self.rows_2_studies = state.rows_2_studies
        self.cols_2_vars    = state.cols_2_vars
        self.label_column   = state.label_column
        self.label_column_name_label = state.label_column_name_label
        try:
            self.data_location_choices = state.data_location_choices
        except AttributeError: # backwards compatibility with old version of dataset w/o data_location_choices
            self.data_location_choices = {}
            
        try:
            self.previous_study_inclusion_state = state.previous_study_inclusion_state
        except:
            self.previous_study_inclusion_state = {}
            
        try:
            self.variable_groups = state.variable_groups
        except:
            self.variable_groups = []
        
        # Emit signals
        self.label_column_changed.emit()
        self.studies_changed.emit()
        self.column_formats_changed.emit()


    def add_vars_to_col_group(self, col_group, keys_to_vars):
        for key,var in keys_to_vars.items():
            col_group.set_var_with_key(key, var)


    def remove_vars_from_col_group(self, col_group, keys):
        for key in keys:
            col_group.unset_column_group_with_key(key)


    def update_data_location_choices(self, data_type, data_locations):
        ''' data locations is a dictionary obtained from the
        calculate effect size wizard or meta-analysis wizard that maps
        combo box choices to column #s '''
        
        if data_type not in self.data_location_choices:
            self.data_location_choices[data_type] = {}
        self.data_location_choices[data_type].update(data_locations)
        
        print("Data location choices are now: %s" % str(self.data_location_choices))
        
    
    def update_previously_included_studies(self, studies_inclusion_state):
        ''' included studies is a set() of studies obtained from the meta-
        analysis wizard '''
        
        self.previous_study_inclusion_state = {}
        self.previous_study_inclusion_state.update(studies_inclusion_state)
        
    def get_previously_included_studies(self):
        return self.previous_study_inclusion_state
        
    def get_data_location_choice(self, data_type, field_name):
        try:
            return self.data_location_choices[data_type][field_name]
        except KeyError:
            return None
        
        
    def set_undo_stack(self, undo_stack):
        self.undo_stack = undo_stack
        
    def get_studies_in_current_order(self):
        studies = [self.rows_2_studies[row] for row in sorted(self.rows_2_studies.keys())]
        return studies
        
    def __str__(self):
        rows_2_study_ids = dict([(row, study.get_id()) for (row, study) in self.rows_2_studies.items()])
        
        
        summary_str = "Dataset Info: %s\n" % str(self.dataset)
        model_info = "  ".join(["Model Info:\n",
                                "Dirty: %s\n" % str(self.dirty),
                                "Label Column: %s\n" % self.label_column,
                                "Rows-to-study ids: %s\n" % str(rows_2_study_ids),
                                "Columns to variables: %s\n" % str(self.cols_2_vars),
                                "Data location choices: %s\n" % str(self.data_location_choices),
                                "Variable Groups: %s\n" % str(self.variable_groups),
                                ])
        return summary_str + model_info
    
    
    ################ Get columns of a particular type ########################
    def get_categorical_columns(self):
        return self._get_columns_of_type(CATEGORICAL)
    
    def get_continuous_columns(self):
        
        ''' returns a list of column indices with variables that have continuous data'''
        return self._get_columns_of_type(CONTINUOUS)
    
    def get_count_columns(self):
        return self._get_columns_of_type(COUNT)
    
    def _get_columns_of_type(self, var_type):
        ''' returns a list of column indices with variables of the desired type '''
        
        return sorted([col for col,var in self.cols_2_vars.items() if var.get_type()==var_type])
    
    def get_variables(self, var_type=None):
        ''' Gets all the variables in a list, or all the variables of a 
        particular type '''
        
        if var_type == None: # special case, return all variables
            return self.dataset.get_variables()
        elif var_type not in VARIABLE_TYPES:
            raise Exception("Not a defined variable type!")
        
        variables = self.dataset.get_variables()
        desired_variables = [var for var in variables if var.get_type()==var_type]
        return desired_variables
    
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
        old_row_limit = self.rowlimit
        max_occupied_row = self.get_max_occupied_row()
        if max_occupied_row is None:
            new_row_limit = ADDITIONAL_ROWS
        else:
            nearest_row_increment = int(round(float(max_occupied_row)/ADDITIONAL_ROWS) * ADDITIONAL_ROWS)
            new_row_limit = nearest_row_increment + ADDITIONAL_ROWS
        if new_row_limit != old_row_limit:
            self.rowlimit = new_row_limit
            self.beginResetModel()
            self.endResetModel()
            
    def change_column_count_if_needed(self):
        old_col_limit = self.collimit
        max_occupied_col = self.get_max_occupied_col()
        if max_occupied_col is None:
            new_col_limit = ADDITIONAL_COLS
        else:
            nearest_col_increment = int(round(float(max_occupied_col)/ADDITIONAL_COLS) * ADDITIONAL_COLS)
            new_col_limit = nearest_col_increment + ADDITIONAL_COLS
        if new_col_limit != old_col_limit:
            self.collimit = new_col_limit
            self.beginResetModel()
            self.endResetModel()
    
    def columnCount(self, index=QModelIndex()):
        return self.collimit
    
    def get_max_occupied_row(self):
        ''' Returns the highest numbered row index of the occupied rows
            returns None if no rows are occupied '''
        
        occupied_rows = self.rows_2_studies.keys()
        if len(occupied_rows) == 0:
            return None
        else:
            return max(occupied_rows)
        
    def get_max_occupied_col(self):
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


    def get_column_assigned_to_variable(self, var):
        ''' Returns the index of the column assigned to the variable with name
        var_name '''
        
        return self._get_key_for_value(self.cols_2_vars, var)
    
    def get_variable_assigned_to_column(self, col):
        if col is None:
            return None
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
        
        # Emit signal
        self.column_formats_changed.emit()
        
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
        
        
        # Emit signals
        self.column_formats_changed.emit()
        self.label_column_changed.emit()
        
    
    def remove_variable(self, var):
        ''' Deletes a variable from the collection and removes it from the
        mapping of columns to variables '''
        
        col = self.get_column_assigned_to_variable(var)
        
        self.dataset.remove_variable(var)
        del self.cols_2_vars[col]
        
        # Emit signal
        self.column_formats_changed.emit()
        
    def remove_study(self, study):
        row = self.get_row_assigned_to_study(study)
        
        self.dataset.remove_study(study)
        del self.rows_2_studies[row]
        
        # Emit signal
        self.studies_changed.emit()
        
    def remove_study_by_row(self, row):
        study = self.rows_2_studies[row]
        self.dataset.remove_study(study)
        del self.rows_2_studies[row]
        
        # Emit signal
        self.studies_changed.emit()
    
    
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




    def make_new_variable(self, label=None, var_type=CATEGORICAL):
        new_var = self.dataset.make_new_variable(label=label, var_type=var_type)
        
        # Emit signal
        self.column_formats_changed.emit()
        
        return new_var

         
    def unmark_column_as_label(self, column_index):
        '''
        Unmark the column as the label column.
        Turns the column into a categorical variable '''
        
        # verification
        if self.label_column != column_index:
            raise Exception("This is not the label column!")
        
        # Add new variable with 'categorical' type (the most general)
        variable_name = self.label_column_name_label
        new_var = self.make_new_variable(label=variable_name, var_type=CATEGORICAL)
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
        
        # Emit signal
        self.column_formats_changed.emit()
        self.label_column_changed.emit()
        
        
    def set_precision(self, new_precision):
        ''' Sets precision (# of decimals after the decimal point for continuous)
        variable values '''
        
        self.user_prefs['digits']
        
        
    def get_precision(self):
        return self.user_prefs['digits']
        
        
    def _var_value_for_display(self, value, var_type):
        ''' Converts the variable value to a suitable string representation
        according to its type '''
        
        old_type = var_type
        # This just properly formats the value with the right precision
        # We're not actually saving a converted value in the dataset
        # TODO: should probably make this function static in the dataset
        return self.dataset.convert_var_value_to_type(old_type, CATEGORICAL, value, precision=self.get_precision())
            
    def data(self, index, role=Qt.DisplayRole):
        PLACEHOLDER_FOR_DISPLAY = "    "
        
        #if not index.isValid():
        #    return QVariant()
        #max_occupied_row = self.get_max_occupied_row()
        #if role!=Qt.BackgroundRole and max_occupied_row and not (0 <= index.row() <= max_occupied_row):
        #    return QVariant()
        
        row, col = index.row(), index.column()
        is_study_row = row in self.rows_2_studies
        is_label_col = col == self.label_column
        is_variable_col = self.column_assigned_to_variable(col)
        
        if role == Qt.DisplayRole or role == Qt.EditRole:         
            if not is_study_row: # no study for this row, no info to display
                if role == Qt.DisplayRole:
                    return QVariant(PLACEHOLDER_FOR_DISPLAY)
                else:
                    return QVariant()
            
            # Get the study this to which this row refers
            study = self.rows_2_studies[row]
            
            if is_label_col:
                label = study.get_label()
                if label is None: # no label
                    if role == Qt.DisplayRole:
                        return QVariant(PLACEHOLDER_FOR_DISPLAY)
                    else:
                        return QVariant()
                return QVariant(QString(label))
            else: # is a variable column or unassigned
                if not is_variable_col:
                    if role == Qt.DisplayRole:
                        return QVariant(PLACEHOLDER_FOR_DISPLAY)
                    else:
                        return QVariant()
                
                # the column is assigned to a variable
                var = self.cols_2_vars[col]
                var_value = study.get_var(var)
                if var_value is None: # don't display Nones
                    if role==Qt.DisplayRole:
                        return QVariant(PLACEHOLDER_FOR_DISPLAY) # display placeholder
                    else:
                        return QVariant()
                return QVariant(QString(self._var_value_for_display(var_value, var.get_type())))
        elif role == Qt.BackgroundRole or role == Qt.ForegroundRole:
            if is_label_col:
                return QVariant(QBrush(self._get_label_color(role)))
            elif is_variable_col:
                var = self.cols_2_vars[col]
                color = self._get_variable_color(var, role)
                return QVariant(QBrush(color))        
                      
            return QVariant(QBrush(self.user_prefs["color_scheme"]['DEFAULT_BACKGROUND_COLOR']))
        elif role == Qt.FontRole:
            if 'font' not in self.user_prefs:
                return QVariant()
            else:
                font = QFont()
                font.fromString(self.user_prefs['font'])
                return QVariant(font) 
            
        return QVariant()
    
    def _get_label_color(self, role=Qt.ForegroundRole):
        if role == Qt.ForegroundRole:
            return self.user_prefs["color_scheme"]['label'][FOREGROUND]
        else:
            return self.user_prefs["color_scheme"]['label'][BACKGROUND]
    
    def _get_variable_color(self, variable, role=Qt.ForegroundRole):
        
        var_type, var_subtype = variable.get_type(), variable.get_subtype()
        
        color = QVariant()
        if role == Qt.ForegroundRole:
            color = self.user_prefs["color_scheme"]['variable'][var_type][FOREGROUND]
            if var_subtype is not None:
                try:
                    color =  self.user_prefs["color_scheme"]['variable_subtype'][var_subtype][FOREGROUND]
                except KeyError:
                    if var_subtype in EFFECT_TYPES:
                        color =  self.user_prefs["color_scheme"]['variable_subtype']['DEFAULT_EFFECT'][FOREGROUND]
        else: # background role
            color = self.user_prefs["color_scheme"]['variable'][var_type][BACKGROUND]
            if var_subtype is not None:
                try:
                    color =  self.user_prefs["color_scheme"]['variable_subtype'][var_subtype][BACKGROUND]
                except KeyError:
                    if var_subtype in EFFECT_TYPES:
                        color =  self.user_prefs["color_scheme"]['variable_subtype']['DEFAULT_EFFECT'][BACKGROUND]
        return color
    
    
        
        
    
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
                suffix = "\n(label)"
            else: # is a variable column
                col_name = self.cols_2_vars[section].get_label()
                var_type = self.cols_2_vars[section].get_type()
                suffix = "\n(%s)" % VARIABLE_TYPE_SHORT_STRING_REPS[var_type]
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
        
        value_blank = (value == QVariant()) or (value is None) or (str(value.toString()) == "") 
        
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
                return True
            self.undo_stack.push(MakeStudyCommand(model=self, row=row))
            
        study = self.rows_2_studies[row]
        
        if is_label_col:
            existing_label = study.get_label()
            proposed_label = str(value.toString()) if not value_blank else None
            if proposed_label != existing_label:
                self.undo_stack.push(SetStudyLabelCommand(study=study, new_label=proposed_label))
            else:
                cancel_macro_creation_and_revert_state()
                return True
        else: # we are in a variable column (initialized or not)
            make_new_variable = not self.column_assigned_to_variable(col)
            if make_new_variable: # make a new variable and give it the default column header name
                if value_blank:
                    cancel_macro_creation_and_revert_state()
                    return True
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
                                                      precision=self.get_precision())


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
    
    @staticmethod
    def get_default_header_string_of_length(length):
        header_string = []
        for _,label in zip(range(length),excel_column_headers()):
            header_string.append(QString(label))
        return header_string
    
    def _set_dirty_bit(self, state=True):
        self.dirty = state
    
    def add_transformed_effect_sizes_to_model(self, metric, effect_sizes, transform_direction, column_group):
        verify_transform_direction(transform_direction)
        
        studies = self.get_studies_in_current_order()
        last_occupied_col = max(self.cols_2_vars.keys())
        
        self.undo_stack.beginMacro("Adding transformed effect to spreadsheet")
        
        if transform_direction == TRANS_TO_RAW:
            raw_yi_col = last_occupied_col+1
            raw_lb_col = raw_yi_col + 1
            raw_ub_col = raw_lb_col + 1
            start_cmd = GenericUndoCommand(redo_fn=partial(self.beginInsertColumns,QModelIndex(), raw_yi_col, raw_ub_col),
                                           undo_fn=self.endRemoveColumns)
            end_cmd = GenericUndoCommand(redo_fn=self.endInsertColumns,
                                         undo_fn=partial(self.beginRemoveColumns, QModelIndex(), raw_yi_col, raw_ub_col))
            # Make new variables to hold the results of the effect size calculations
            add_raw_yi_cmd = MakeNewVariableCommand(model=self,
                                                    var_name=METRIC_TEXT_SHORT_RAW_SCALE[metric],
                                                    col=raw_yi_col,
                                                    var_type=CONTINUOUS)
            add_raw_lb_cmd = MakeNewVariableCommand(model=self,
                                                    var_name="lb(%s)" % METRIC_TEXT_SHORT_RAW_SCALE[metric],
                                                    col=raw_lb_col,
                                                    var_type=CONTINUOUS)
            add_raw_ub_cmd = MakeNewVariableCommand(model=self,
                                                    var_name="ub(%s)" % METRIC_TEXT_SHORT_RAW_SCALE[metric],
                                                    col=raw_ub_col,
                                                    var_type=CONTINUOUS)
            variable_add_cmds = [add_raw_yi_cmd, add_raw_lb_cmd, add_raw_ub_cmd]
        elif transform_direction == RAW_TO_TRANS:
            trans_yi_col = last_occupied_col+1
            trans_vi_col = trans_yi_col + 1
            start_cmd = GenericUndoCommand(redo_fn=partial(self.beginInsertColumns,QModelIndex(), trans_yi_col, trans_vi_col),
                                           undo_fn=self.endInsertColumns)
            end_cmd = GenericUndoCommand(redo_fn=self.endInsertColumns,
                                         undo_fn=partial(self.beginRemoveColumns, QModelIndex(), trans_yi_col, trans_vi_col))
            
            add_trans_yi_cmd = MakeNewVariableCommand(model=self,
                                                      var_name=METRIC_TEXT_SHORT[metric],
                                                      col=trans_yi_col,
                                                      var_type=CONTINUOUS)
            add_trans_vi_cmd = MakeNewVariableCommand(model=self,
                                                      var_name="Var(%s)" % METRIC_TEXT_SHORT[metric],
                                                      col=trans_vi_col,
                                                      var_type=CONTINUOUS)
            variable_add_cmds = [add_trans_yi_cmd, add_trans_vi_cmd]
            
        # Execute commands
        self.undo_stack.push(start_cmd)
        for cmd in variable_add_cmds:
            self.undo_stack.push(cmd)
            
        # get the new variables
        # set their subtypes
        # add them to the column group
        if transform_direction == RAW_TO_TRANS:
            trans_yi = self.get_variable_assigned_to_column(trans_yi_col)
            trans_vi = self.get_variable_assigned_to_column(trans_vi_col)
            
            self.undo_stack.push(SetVariableSubTypeCommand(model=self, variable=trans_yi, new_subtype=TRANS_EFFECT))
            self.undo_stack.push(SetVariableSubTypeCommand(model=self, variable=trans_vi, new_subtype=TRANS_VAR))
            
            keys_to_vars = {TRANS_EFFECT:trans_yi,
                            TRANS_VAR: trans_vi}
        elif transform_direction == TRANS_TO_RAW:
            raw_yi = self.get_variable_assigned_to_column(raw_yi_col)
            raw_lb = self.get_variable_assigned_to_column(raw_lb_col)
            raw_ub = self.get_variable_assigned_to_column(raw_ub_col)
            
            self.undo_stack.push(SetVariableSubTypeCommand(model=self, variable=raw_yi, new_subtype=RAW_EFFECT))
            self.undo_stack.push(SetVariableSubTypeCommand(model=self, variable=raw_lb, new_subtype=RAW_LOWER))
            self.undo_stack.push(SetVariableSubTypeCommand(model=self, variable=raw_ub, new_subtype=RAW_UPPER))
            
            keys_to_vars = {RAW_EFFECT:raw_yi,
                            RAW_LOWER:raw_lb,
                            RAW_UPPER:raw_ub}
        # add vars to column group
        self.undo_stack.push(GenericUndoCommand(redo_fn=partial(self.add_vars_to_col_group,column_group, keys_to_vars),
                                                undo_fn=partial(self.remove_vars_from_col_group,column_group, keys=keys_to_vars.keys()),
                                                description="Add variables to column group"))
        
        if transform_direction == TRANS_TO_RAW:
            for study, yi_val, lb_val, ub_val in zip(studies, effect_sizes[RAW_EFFECT],effect_sizes[RAW_LOWER],effect_sizes[RAW_UPPER]):
                self.undo_stack.push(SetVariableValueCommand(study, raw_yi, yi_val))
                self.undo_stack.push(SetVariableValueCommand(study, raw_lb, lb_val))
                self.undo_stack.push(SetVariableValueCommand(study, raw_ub, ub_val))
        elif transform_direction == RAW_TO_TRANS:
            for study, yi_val, vi_val in zip(studies, effect_sizes[TRANS_EFFECT], effect_sizes[TRANS_VAR]):
                self.undo_stack.push(SetVariableValueCommand(study, trans_yi, yi_val))
                self.undo_stack.push(SetVariableValueCommand(study, trans_vi, vi_val))
        ##########
        self.undo_stack.push(end_cmd)
        
        self.undo_stack.endMacro()
            
        
    
    def add_effect_sizes_to_model(self, metric, effect_sizes):
    
        studies = self.get_studies_in_current_order()
        last_occupied_col = sorted(self.cols_2_vars.keys(), reverse=True)[0]
        yi_col = last_occupied_col+1
        vi_col = yi_col+1
        
    
        self.undo_stack.beginMacro(QString("Adding effect size to spreadsheet"))
        
        start_cmd = GenericUndoCommand(redo_fn=self.beginResetModel,
                                      undo_fn=self.endResetModel,)
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
        
        # Set subtype (for display purposes only for now)
        self.undo_stack.push(SetVariableSubTypeCommand(model=self, variable=variable_yi, new_subtype=TRANS_EFFECT))
        self.undo_stack.push(SetVariableSubTypeCommand(model=self, variable=variable_vi, new_subtype=TRANS_VAR))
        
        # add variables to new column_group
        col_group = self.make_new_variable_group(metric=metric, name=METRIC_TEXT_SIMPLE[metric] + " column group")
        keys_to_vars = {TRANS_EFFECT:variable_yi,
                        TRANS_VAR:variable_vi}
        self.undo_stack.push(GenericUndoCommand(redo_fn=partial(self.add_vars_to_col_group, col_group, keys_to_vars),
                                                undo_fn=partial(self.remove_vars_from_col_group, col_group, keys=keys_to_vars.keys()),
                                                description="Add variables to column group"))
        
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
        

    def make_new_variable_group(self, metric, name):
        col_group = VariableGroup(metric=metric, name=name)    
        
        redo_fn = partial(self.variable_groups.append,col_group)
        undo_fn = partial(self.variable_groups.remove,col_group)
        
        make_col_grp_cmd = GenericUndoCommand(redo_fn=redo_fn, undo_fn=undo_fn, 
                                              description="Make new column group")
        self.undo_stack.push(make_col_grp_cmd)
        
        return col_group
    
    

        
    def sort_by_column(self, col):
        ''' sorts studies by column data (ascending). If the studies are already
        sorted in ascending order, they sare sorted in descending order '''
        
        studies = self.rows_2_studies.values()
        old_rows_to_studies = self.rows_2_studies.copy()
        
        rows_in_order = sorted(old_rows_to_studies.keys())
        old_study_order = [old_rows_to_studies[row] for row in rows_in_order]
        
        is_label_column = col==self.label_column  
        
        if is_label_column:
            sorted_studies = sorted(studies, key=lambda study: study.get_label())
        else: # is a variable-ish column
            var = self.get_variable_assigned_to_column(col)
            sorted_studies = sorted(studies, key=lambda study: study.get_var(var))
        
        if sorted_studies == old_study_order:
            sorted_studies.reverse()
        
        new_rows_to_studies = dict(enumerate(sorted_studies))
        
        redo_f = lambda: self._set_rows_to_studies(new_rows_to_studies)
        undo_f = lambda: self._set_rows_to_studies(old_rows_to_studies)
        
        sort_cmd = GenericUndoCommand(redo_fn=redo_f, undo_fn=undo_f,
                                      on_undo_entry=self.beginResetModel,
                                      on_undo_exit=self.endResetModel,
                                      on_redo_entry=self.beginResetModel,
                                      on_redo_exit=self.endResetModel)
        self.undo_stack.push(sort_cmd)
        
        
    def _set_rows_to_studies(self, new_rows_to_studies):
        self.rows_2_studies = new_rows_to_studies
        
        
class VariableGroup:
    # Stores info on related groups of variables i.e. effect size and variance, etc
    def __init__(self, metric, name=""):
        self.name = name
        self.metric = metric
        
        self.group_data = {RAW_EFFECT:None,
                           RAW_LOWER:None,
                           RAW_UPPER:None,
                           TRANS_EFFECT:None,
                           TRANS_VAR:None,
                           }
        
    def isEmpty(self):
        return not any(self.group_data.values())
    
    def isFull(self):
        return all(self.group_data.values())
    
    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name
    
    def get_metric(self):
        return self.metric
    
    def set_var_with_key(self, key, var):
        self.group_data[key] = var
        var.set_column_group(self)

    def get_var_with_key(self, key):
        return self.group_data[key]
    
    def unset_column_group_with_key(self, key):
        ''' unsets it in the variable as well '''
        var = self.group_data[key]
        var.set_column_group(None)
        self.group_data[key]=None
        
    def get_var_key(self, var):
        for k,v in self.group_data.items():
            if v==var:
                return k
        raise KeyError("No such variable in the group")
    
        
    def __str__(self):
        raw_yi   = self.group_data[RAW_EFFECT]
        raw_lb   = self.group_data[RAW_LOWER]
        raw_ub   = self.group_data[RAW_UPPER]
        trans_yi = self.group_data[TRANS_EFFECT]
        trans_vi = self.group_data[TRANS_VAR]
        
        raw_yi_lbl   = None if raw_yi   is None else raw_yi.get_label()
        raw_lb_lbl   = None if raw_lb   is None else raw_lb.get_label()
        raw_ub_lbl   = None if raw_ub   is None else raw_ub.get_label()
        trans_yi_lbl = None if trans_yi is None else trans_yi.get_label()
        trans_vi_lbl = None if trans_vi is None else trans_vi.get_label()

        raw_scale_str = "Raw Scale: effect [lower, upper]: %s [%s,%s]" % (raw_yi_lbl,
                                                                          raw_lb_lbl,
                                                                          raw_ub_lbl)
        trans_scale_str = "Transformed Scale: effect, variance: %s, %s" % (trans_yi_lbl,
                                                                           trans_vi_lbl,)
        return trans_scale_str + '\n' + raw_scale_str
    
        
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
        self.model.dirty = True
        
        
    def redo(self):
        if DEBUG_MODE: print("redo: make new study_command")
        model = self.model
        if self.study is None: # this should only execute once
            self.study = model.dataset.make_new_study()
        else:            # we should always be here on subsequent runs of redo
            model.dataset.add_existing_study(self.study)
        model.rows_2_studies[self.row] = self.study
        
        # emit signal
        self.model.studies_changed.emit()
    
    def undo(self):
        ''' Remove study at the specified row in the model '''
        
        if DEBUG_MODE:
            print("undo: make new study_command")
        self.model.remove_study(self.study)
        

class RemoveStudyCommand(QUndoCommand):
    ''' Removes / unremoves study at the specified row in the model '''
    def __init__(self, model, row):
        super(RemoveStudyCommand, self).__init__()
        
        self.setText(QString("Remove study @ row %d" % row))
        
        self.model = model
        self.row = row
        self.study = self.model.rows_2_studies[self.row]
        
        self.model.dirty = True
        
    def redo(self):
        if DEBUG_MODE:
            print("redo: remove study")
        self.model.remove_study(self.study)
        
    def undo(self):
        if DEBUG_MODE: print("undo: remove study")
        self.model.dataset.add_existing_study(self.study)
        self.model.rows_2_studies[self.row]=self.study
        
        #emit signal
        self.model.studies_changed.emit()

        
class SetStudyLabelCommand(QUndoCommand):
    ''' Sets/unsets the label of the given study '''
    
    def __init__(self, study, new_label):
        super(SetStudyLabelCommand, self).__init__()
        self.study = study
        self.new_label = new_label
        self.old_label = study.get_label()
        
        self.setText(QString("set study label from '%s' to '%s" % (self.old_label, self.new_label)))
        
    def redo(self):
        if DEBUG_MODE: print("redo: set study label")
        self.study.set_label(self.new_label)
        
    def undo(self):
        if DEBUG_MODE: print("undo: set study label")
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
        self.model.dirty = True
        
        
    def redo(self):
        if DEBUG_MODE: print("redo: make new variable_command")
        if self.var is None:
            self.var = self.model.make_new_variable(label=self.var_name, var_type=self.var_type)
        else:
            self.model.dataset.add_existing_variable(self.var)
        self.model.cols_2_vars[self.col] = self.var
        
    def undo(self):
        if DEBUG_MODE: print("undo: make new variable_command")
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
        if DEBUG_MODE: print("redo: set variable value command")
        self.study.set_var(self.variable, self.new_value)

    def undo(self):
        if DEBUG_MODE: print("undo: set variable value command")
        self.study.set_var(self.variable, self.old_value)
        
        
class SetVariableSubTypeCommand(QUndoCommand):
    def __init__(self, model, variable, new_subtype):
        super(SetVariableSubTypeCommand, self).__init__()
        
        self.model = model
        self.variable = variable
        self.new_subtype = new_subtype
        self.old_subtype = variable.get_subtype()
        
    def redo(self):
        if DEBUG_MODE: print("redo: set variable subtype command")
        self.variable.set_subtype(self.new_subtype)
        
        self.emit_change_signals_from_model()
    
    def undo(self):
        if DEBUG_MODE: print("undo: set variable subtype command")
        self.variable.set_subtype(self.old_subtype)
        
        self.emit_change_signals_from_model()
        
    def emit_change_signals_from_model(self):
        col = self.model.get_column_assigned_to_variable(self.variable)
        start_index = self.model.createIndex(0,col)
        end_index = self.model.createIndex(self.model.rowCount()-1,col)
        self.model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
          start_index, end_index)
        self.model.headerDataChanged.emit(Qt.Horizontal, col, col)
        
class EmitDataChangedCommand(QUndoCommand):
    ''' Not really a command, just the last thing called @ the end of the macro
    in setData in order to notify the view that the model has changed '''
    
    def __init__(self, model, index):
        super(EmitDataChangedCommand, self).__init__()
        
        self.model = model
        self.index = index
        
        self.setText(QString("Data changed emission"))
    
    def undo(self):
        if DEBUG_MODE: print("undo: emit data changed")
        self.model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
          self.index, self.index)
        
    def redo(self):
        if DEBUG_MODE: print("redo: emit data changed")
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
                
        self.model.dirty = True

        
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
        
        self.model.dirty = True
                
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
        #emit signal
        self.model.studies_changed.emit()
        
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
        self.model.dirty = True
        
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
        
        self.model.dirty = True
        
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
        

class ChangeVariableFormatCommand(QUndoCommand):
    ''' Changes the format of a variable '''
    
    def __init__(self, model, variable, target_type, precision, description="Change variable format"):
        super(ChangeVariableFormatCommand, self).__init__()
        
        self.setText(QString(description))
        
        self.model = model
        self.variable=variable
        self.target_type = target_type
        self.precision = precision
        
        self.original_var_type = variable.get_type()
        self.original_subtype = variable.get_subtype()
        self.original_variable_group = variable.get_column_group()
        self.key_var_group = None
        if self.original_variable_group is not None:
            self.key_var_group = self.original_variable_group.get_var_key(self.variable)

        # dictionary mapping studies to their original values for the given variable
        self.orignal_vals = {}
        
    def redo(self):
        self._store_original_data_values_for_variable()
        self.model.change_variable_type(self.variable, self.target_type, self.precision)
        
        self.variable.set_subtype(None)
        if self.key_var_group:
            self.original_variable_group.unset_column_group_with_key(self.key_var_group)

        self.model.dirty = True
        
    def undo(self):
        self.model.change_variable_type(self.variable, self.original_var_type, self.precision)
        self._restore_orignal_data_values_for_variable()
        
        self.variable.set_subtype(self.original_subtype)
        if self.key_var_group:
            self.original_variable_group.set_var_with_key(key=self.key_var_group, var=self.variable)
        
    def _store_original_data_values_for_variable(self):
        for study in self.model.dataset.get_studies():
            self.orignal_vals[study] = study.get_var(self.variable)
    
    def _restore_orignal_data_values_for_variable(self):
        for study, value in self.orignal_vals.items():
            study.set_var(self.variable, value)
            