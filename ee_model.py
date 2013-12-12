################
#              #
# George Dietz #
# CEBM@Brown   #
#              #
################

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *


import pdb
import string
from sets import Set
from functools import partial
#import copy


# handrolled
from dataset.ee_dataset import EEDataSet
from globals import *
import python_to_R
from dataset.variable import Variable
import copy

# Some constants
ADDITIONAL_ROWS = 20
ADDITIONAL_COLS = 20

# Forbidden variable names
LABEL_PREFIX_MARKER  = "*lbl*" # marker placed at start of a label(but is not displayed)
FORBIDDEN_VARIABLE_NAMES = [LABEL_PREFIX_MARKER,]

class ModelState:
    def __init__(self, dataset, dirty, rows_2_studies, cols_2_vars,
                 label_column, label_column_name_label, column_groups,
                 last_analysis_selections, conf_level):
        self.dataset   = dataset
        self.dirty     = dirty
        self.rows_2_studies = rows_2_studies
        self.cols_2_vars    = cols_2_vars
        self.label_column   = label_column
        self.label_column_name_label = label_column_name_label
        self.variable_groups = column_groups
        # analysis stuff
        self.last_analysis_selections = last_analysis_selections
        self.conf_level = conf_level
        
        
DEFAULT_LAST_ANALYSIS_SELECTIONS = {'data_locations': {MEANS_AND_STD_DEVS:{},
                                                       TWO_BY_TWO_CONTINGENCY_TABLE:{},
                                                       CORRELATION_COEFFICIENTS:{},},
                                    'included_studies'   : None,
                                    'included_covariates': None,           
                                    'data_type'          : None,
                                    'metric'             : None,
                                    'method'             : None,
                                    'ma_param_vals'      : None,
                                    'subgroup_variable'  : None,
                                    'fixed_effects'      : None,
                                    'conf_level'         : None,
                                    'cov_2_ref_values'   : None,
                                    'bootstrap_params'   : None,
                                    'selected_cov'       : None,
                                    'covs_to_values'     : None,
                                    'failsafe_parameters': None,
                                    }
        

class EETableModel(QAbstractTableModel):
    
    column_formats_changed = pyqtSignal()
    studies_changed        = pyqtSignal()
    label_column_changed   = pyqtSignal()
    column_groups_changed  = pyqtSignal()
    duplicate_label        = pyqtSignal()
    should_resize_column   = pyqtSignal(int)
    conf_level_changed_during_undo = pyqtSignal(float)
    error_msg_signal       = pyqtSignal(str, str)
    
    def __init__(self, undo_stack, user_prefs, model_state=None):
        super(EETableModel, self).__init__()
        
        # Give model access to undo_stack
        self.undo_stack = undo_stack
        
        self.user_prefs = user_prefs
        if "color_scheme" not in self.user_prefs:
            self.user_prefs["color_scheme"]=DEFAULT_COLOR_SCHEME
        
        self.max_occupied_row = None
        self.max_occupied_col = None
        self.col_2_max_length = {} # the values in this dict will only be valid if not much messing around has happened
        
        if model_state is None:
            self.dataset = EEDataSet()
            self.dirty = False
            self.data_location_choices = {} # maps data_types to column choices
            self.conf_level = DEFAULT_CONFIDENCE_LEVEL
            # analysis info
            self.last_analysis_selections = DEFAULT_LAST_ANALYSIS_SELECTIONS
            
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
            self.calculate_max_occupied_row()
            self.calculate_max_occupied_col()
        
        # Set confidence level
        self.set_conf_level(self.conf_level, ignore_undo=True)
        
        self.default_headers = self._generate_header_string(ADDITIONAL_COLS)
        # for rowCount() and colCount()
        self.rowlimit = ADDITIONAL_ROWS
        self.collimit = ADDITIONAL_COLS
        self.change_column_count_if_needed()
        self.change_row_count_if_needed()
        
        self.big_paste_mode = False # state to set/reset while pasting/importing
        
    def set_user_prefs(self, user_prefs):
        self.user_prefs = user_prefs
        
    def set_conf_level(self, conf_level, ignore_undo=False):  # i.e. 95
        if ignore_undo:
            old_conf_level = self.conf_level
            self.conf_level = conf_level
            python_to_R.set_conf_level_in_R(conf_level)
            self.do_when_conf_level_changes(old_conf_level, conf_level, use_undo=False)
        else:
            old_conf_level = self.conf_level
            redo_fn = lambda: setattr(self, 'conf_level', conf_level)
            undo_fn = lambda: setattr(self, 'conf_level', old_conf_level)
            self.undo_stack.beginMacro("Setting confidence level and performing associated actions")
            self.undo_stack.push(GenericUndoCommand(redo_fn=redo_fn, undo_fn=undo_fn,
                                                    on_undo_exit=lambda: self.conf_level_changed_during_undo.emit(old_conf_level),
                                                    description="set confidence level"))
            self.do_when_conf_level_changes(old_conf_level, conf_level)
            self.undo_stack.endMacro()
        print("Confidence level is now %.1f" % self.conf_level)
    
    def do_when_conf_level_changes(self, old_conf_level, new_conf_level, use_undo=True):
        
        ################## Update raw effect columns ########################
        if use_undo:
            self.undo_stack.beginMacro("Updating raw effect columns")
        for var_grp in self.variable_groups:
            metric = var_grp.get_metric()
            
            if not var_grp.raw_effects_full(): # make sure a variable is assigned to each column of the raw effects
                continue
            
            #transform raw data columns to transform scale, then get them back again in no transform scale at the new conf level
            raw_data_location = {RAW_EFFECT: var_grp.get_var_with_key(RAW_EFFECT),
                                 RAW_LOWER:  var_grp.get_var_with_key(RAW_LOWER),
                                 RAW_UPPER:  var_grp.get_var_with_key(RAW_UPPER)}
            data = python_to_R.gather_data(self, raw_data_location, vars_given_directly=True)
            old_data = copy.deepcopy(data)
            try:
                trans_effects = python_to_R.transform_effect_size(
                                                      metric=metric,
                                                      source_data=data,
                                                      direction=RAW_TO_TRANS,
                                                      conf_level=old_conf_level)
                raw_effects_new_scale = python_to_R.transform_effect_size(
                                                    metric=metric,
                                                    source_data=trans_effects,
                                                    direction=TRANS_TO_RAW,
                                                    conf_level=new_conf_level)
            except CrazyRError as e:
                QMessageBox.critical(self, QString("R error"), QString(str(e)))
                return False
            
            studies = self.get_studies_in_current_order()
            
            for effect in [RAW_EFFECT, RAW_LOWER, RAW_UPPER]:
                var = var_grp.get_var_with_key(effect)
                col = self.get_column_assigned_to_variable(var)
                old_values = old_data[effect]
                new_values = raw_effects_new_scale[effect]
                if use_undo:
                    redo_fn = partial(self.set_variable_values, studies=studies, variable=var, values=new_values)
                    undo_fn = partial(self.set_variable_values, studies=studies, variable=var, values=old_values)
                    cmd = GenericUndoCommand(redo_fn=redo_fn, undo_fn=undo_fn,
                                             on_redo_exit=partial(self.emit_change_signals_for_col,col=col),
                                             on_undo_exit=partial(self.emit_change_signals_for_col,col=col))
                    self.undo_stack.push(cmd)
                else:
                    self.set_variable_values(studies=studies, variable=var, values=new_values)
        if use_undo:
            self.undo_stack.endMacro()
        ################## end update raw effect columns ########################
            
            
            
            
            
    
    def get_conf_level(self):
        return self.conf_level
        
    def get_sorted_continuous_covariates(self):
        return self.get_sorted_covariates(CONTINUOUS)
    
    def get_sorted_categorical_covariates(self):
        return self.get_sorted_covariates(CATEGORICAL)
    
    def get_sorted_count_covariates(self):
        return self.get_sorted_covariates(COUNT)
    
    def get_sorted_covariates(self, var_type):
        covs = self.get_variables(var_type)
        covs = [cov for cov in covs if cov.get_subtype() not in EFFECT_TYPES] # stuff in EFFECT_TYPES are not really covariates
        covs.sort(key=lambda cov_var: cov_var.get_label().lower())
        return covs
    
    def get_state(self):
        ''' returns a class representing the model's state '''
        
        return ModelState(dataset   = self.dataset,
                          dirty     = self.dirty,
                          rows_2_studies = self.rows_2_studies, 
                          cols_2_vars    = self.cols_2_vars,
                          label_column   = self.label_column,
                          label_column_name_label = self.label_column_name_label,
                          column_groups = self.variable_groups,
                          conf_level = self.conf_level,
                          # analysis info
                          last_analysis_selections = self.last_analysis_selections,
                          )
        
        
    def load_model_state(self, state):
        self.dataset        = state.dataset
        self.dirty          = state.dirty
        self.rows_2_studies = state.rows_2_studies
        self.cols_2_vars    = state.cols_2_vars
        self.label_column   = state.label_column
        self.label_column_name_label = state.label_column_name_label
        try:
            self.variable_groups = state.variable_groups
        except AttributeError:
            self.variable_groups = []
            
        try:
            self.last_analysis_selections = state.last_analysis_selections
        except AttributeError:
            self.last_analysis_selections = DEFAULT_LAST_ANALYSIS_SELECTIONS
            
        try:
            self.conf_level = state.conf_level
        except AttributeError:
            self.conf_level = DEFAULT_CONFIDENCE_LEVEL
        
        # Emit signals
        self.label_column_changed.emit()
        self.studies_changed.emit()
        self.column_formats_changed.emit()


    def add_vars_to_col_group(self, col_group, keys_to_vars):
        assert col_group is not None
        
        for key,var in keys_to_vars.items():
            col_group.set_var_with_key(key, var)


    def remove_vars_from_col_group(self, col_group, keys):
        for key in keys:
            col_group.unset_key(key)

######## Analysis parameters section start ################


    #############################
    def update_data_location_choices(self, data_type, data_locations):
        ''' data locations is a dictionary obtained from the
        calculate effect size wizard or meta-analysis wizard that maps
        combo box choices to column #s '''
        
        self.last_analysis_selections['data_locations'][data_type].update(data_locations)
        print("Data location choices are now: %s" % str(self.last_analysis_selections['data_locations']))
    
    def get_data_location_choice(self, data_type, field_name):
        try:
            return self.last_analysis_selections['data_locations'][data_type][field_name]
        except KeyError:
            return None

    #############################
    def update_previously_included_covariates(self, covariates):
        # covariates is a set of included covariates
        if type(covariates) != set:
            raise TypeError("'covariates' must be a set")
        self.last_analysis_selections['included_covariates'] = covariates
    
    def get_previously_included_covariates(self):
        return self.last_analysis_selections['included_covariates']
    #############################
    
    def update_data_type_selection(self, data_type):                   # int
        self.last_analysis_selections['data_type'] = data_type
    def update_metric_selection(self, metric):                         # int
        self.last_analysis_selections['metric'] = metric
    def update_method_selection(self, chosen_method):                  # int??? str??
        self.last_analysis_selections['method'] = chosen_method
    def update_ma_param_vals(self, current_param_vals):                # dict
        self.last_analysis_selections['ma_param_vals'] = current_param_vals
    def update_subgroup_var_selection(self, subgroup_variable):        # variable
        self.last_analysis_selections['subgroup_variable'] = self.last_analysis_selections
    def update_fixed_vs_random_effects_selection(self, fixed_effects): # bool
        self.last_analysis_selections['fixed_effects'] = fixed_effects
    def update_conf_level_selection(self, conf_level):                 # double
        self.last_analysis_selections['conf_level'] = conf_level
    def update_cov_2_ref_values_selection(self, cov_2_ref_values):     # dict
        self.last_analysis_selections['cov_2_ref_values'] = cov_2_ref_values
    def update_bootstrap_params_selection(self, bootstrap_params):     # dict
        self.last_analysis_selections['bootstrap_params'] = bootstrap_params
    def update_previously_included_studies(self, included_studies):
        ''' included studies is a set() of studies obtained from the meta-
        analysis wizard or at least should be, not a dictionary study -> boolean '''
        self.last_analysis_selections['included_studies'] = included_studies
        
    def update_last_failsafe_parameters(self, failsafe_parameters):
        self.last_analysis_selections['failsafe_parameters'] = failsafe_parameters
    def get_last_failsafe_parameters(self):
        return self.try_to_get_last_selection('failsafe_parameters')
    
    def try_to_get_last_selection(self, key):
        '''tries to get the last selection from self.last_analysis_selections
        if it fails, reset the self.last_analysiss selections for the key to the
        default and return the result. This functions helps ensure backwards
        compatibility with old *.ome pickles '''
        
        try:
            return self.last_analysis_selections['failsafe_parameters']
        except KeyError:
            default_value = DEFAULT_LAST_ANALYSIS_SELECTIONS[key]
            self.last_analysis_selections[key] = default_value
            return default_value
    
        
    def update_selected_cov_and_covs_to_values(self, selected_cov, covs_to_values):
        self.last_analysis_selections['selected_cov'] = selected_cov
        self.last_analysis_selections['covs_to_values'] = covs_to_values

    def get_last_analysis_selections(self):
        ''' all the parameters previously selected in the course of choosing options
        on wizard screens '''
        return self.last_analysis_selections
    def get_data_type_selection(self):                   # int
        return self.last_analysis_selections['data_type']
    def get_metric_selection(self):                         # int
        return self.last_analysis_selections['metric']
    def get_method_selection(self):                  # int??? str??
        return self.last_analysis_selections['method']
    def get_ma_param_vals(self):                # dict 
        return self.last_analysis_selections['ma_param_vals']
    def get_subgroup_var_selection(self):        # variable
        return self.last_analysis_selections['subgroup_variable']
    def get_fixed_vs_random_effects_selection(self): # bool
        return self.last_analysis_selections['fixed_effects']
    def get_conf_level_selection(self):                 # double
        return self.last_analysis_selections['conf_level']
    def get_cov_2_ref_values_selection(self):     # dict
        return self.last_analysis_selections['cov_2_ref_values']
    def get_bootstrap_params_selection(self):     # dict
        return self.last_analysis_selections['bootstrap_params']
    def get_previously_included_studies(self):
        return self.last_analysis_selections['included_studies']
    def get_previous_selected_cov_and_covs_to_values(self):
        return self.last_analysis_selections['selected_cov'], self.last_analysis_selections['covs_to_values']
    
    def reset_last_analysis_selection(self):
        print("Resetting last_analysis selections to default")
        self.last_analysis_selections = DEFAULT_LAST_ANALYSIS_SELECTIONS.copy()
        for k,v in self.last_analysis_selections.items():
            print("%s: %s" % (str(k), str(v)))

####### Analysis Parameters Section End ############

    def get_data_type_from_data_location(self, data_location):
        # figure out the data type
        var = self.model.get_variable_assigned_to_column(data_location['effect_size'])
        var_grp = self.model.get_variable_group_of_var(var)
        metric = var_grp.get_metric()
        data_type = get_data_type_for_metric(metric)
        return data_type
        
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
    
    def get_trans_effect_columns(self): # of type TRANS_EFFECT
        continuous_columns = self._get_columns_of_type(CONTINUOUS)
        is_effect_col = lambda col: self.get_variable_assigned_to_column(col).get_subtype()==TRANS_EFFECT
        trans_eff_columns = [col for col in continuous_columns if is_effect_col(col)]
        return trans_eff_columns
    
    def get_trans_var_columns(self): # of type TRANS_VAR
        continuous_columns = self._get_columns_of_type(CONTINUOUS)
        is_trans_var_col = lambda col: self.get_variable_assigned_to_column(col).get_subtype()==TRANS_VAR
        trans_var_columns = [col for col in continuous_columns if is_trans_var_col(col)]
        return trans_var_columns
        
    ##########################################################################
    
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
        if self.max_occupied_row is None:
            new_row_limit = ADDITIONAL_ROWS
        else:
            nearest_row_increment = round(float(self.max_occupied_row)/ADDITIONAL_ROWS) * ADDITIONAL_ROWS
            new_row_limit = int(nearest_row_increment + ADDITIONAL_ROWS)
        if new_row_limit != old_row_limit:
            self.rowlimit = new_row_limit
            self.beginResetModel()
            self.endResetModel()
            
    def change_column_count_if_needed(self,debug=False):
        if debug:
            pass
        
        old_col_limit = self.collimit
        if self.max_occupied_col is None:
            new_col_limit = ADDITIONAL_COLS
        else:
            nearest_col_increment = round(float(self.max_occupied_col)/ADDITIONAL_COLS) * ADDITIONAL_COLS
            new_col_limit = int(nearest_col_increment + ADDITIONAL_COLS)
        if new_col_limit != old_col_limit:
            self.collimit = new_col_limit
            self.beginResetModel()
            self.endResetModel()
    
    def columnCount(self, index=QModelIndex()):
        return self.collimit
    
    def emit_change_signals_for_col(self, col, header_only=False, data_only=False):
        start_index = self.createIndex(0,col)
        end_index = self.createIndex(self.rowCount()-1,col)
        if not header_only:
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      start_index, end_index)
        if data_only:
            return
        self.headerDataChanged.emit(Qt.Horizontal, col, col)
        
        
    def emit_change_signals_from_start_to_end(self, srow, scol, erow, ecol, header_too=False):
        #srow,scol upper left row, column
        #erow,ecol lower right row, column
        
        start_index = self.createIndex(srow,scol)
        end_index = self.createIndex(erow,ecol)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                  start_index, end_index)
        self.headerDataChanged.emit(Qt.Horizontal, scol, ecol)
        print("emitting change signals from (%d,%d) to (%d,%d)" % (srow, scol, erow, ecol))
    
    def calculate_max_occupied_row(self):
        ''' Returns the highest numbered row index of the occupied rows
            returns None if no rows are occupied '''
        
        occupied_rows = self.rows_2_studies.keys()
        if len(occupied_rows) == 0:
            self.max_occupied_row = None
            return None
        else:
            self.max_occupied_row = max(occupied_rows)
            return self.max_occupied_row
        
    def calculate_max_occupied_col(self):
        occupied_cols = Set(self.cols_2_vars.keys())
        if self.label_column is not None:
            occupied_cols.add(self.label_column)
        self.max_occupied_col = max_occupied_col = max(occupied_cols) if len(occupied_cols) != 0 else None
        return max_occupied_col
    
#    def calculate_max_col_lengths(self, cols_to_eval=[]):
#        study_rows = self.rows_2_studies.keys()
#        self.col_2_max_length = {}
#
#        if len(cols_to_eval)==0:
#            cols_to_eval = self.cols_2_vars.keys()
#        for col in cols_to_eval:
#            col_content_lengths = set()
#            col_content_lengths = [el_len(row,col) for row in study_rows]
#            if len(col_content_lengths) == 0:
#                self.col_2_max_length[col] = 0
#            else:
#                self.col_2_max_length[col] = max(col_content_lengths)
    
    def el_len(self, row, col): # element length
            index = self.createIndex(row, col)
            value = str(self.data(index, role=Qt.DisplayRole).toString())
            return len(value)
    
    def len_largest_element_of_col(self, col):
        study_rows = self.rows_2_studies.keys()
        lengths = set([self.el_len(row,col) for row in study_rows])
        return 0 if len(lengths) == 0 else max(lengths)
    
    def get_max_length_in_col(self, col):
        try:
            return self.col_2_max_length[col]
        except KeyError:
            return 0
    

    def change_variable_name(self, var, new_name):
        ''' Change the name of a variable '''
        
        var.set_label(new_name)
        col = self.get_column_assigned_to_variable(var)
        self.emit_change_signals_for_col(col, header_only=True)


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
        
        self.label_column_name_label = new_name
        col = self.label_column
        self.emit_change_signals_for_col(col, header_only=True)
        
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
        self.dataset.change_variable_type(var, new_type, precision)
        
        col = self.get_column_assigned_to_variable(var)
        self.emit_change_signals_for_col(col)
        
        # Emit signal
        self.column_formats_changed.emit()
        
    def mark_column_as_label(self, column_index, overridden_studies_2_labels={}):
        ''' Sets the contents of this column as the labels for the studies in the column '''
        
        # Only one column can be set as the label column at a time
        if self.label_column:
            raise Exception("Only one column can be set as the label column at a time")
        
        var = self.get_variable_assigned_to_column(column_index)
        
        # Set values from column to be the study labels
        studies = self.dataset.get_studies()
        for study in studies:
            label = study.get_var(var)
            #if label is not None:
            if study in overridden_studies_2_labels:
                study.set_label(overridden_studies_2_labels[study])
            else:
                if label is None:
                    label = ''
                study.set_label(str(label))
            #else:
            #    study.set_label(None)
        
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
        
        # remove variable from variable group if it exists
        var_group = self.get_variable_group_of_var(var)
        if var_group:
            key = var_group.get_var_key(var)
            var_group.unset_key(key)
        
        # Emit signal
        self.blockSignals(False)
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

    def make_study_at_row(self,row):
        study = self.dataset.make_new_study()
        self.rows_2_studies[row] = study
        if self.max_occupied_row is None or self.max_occupied_row < row:
            self.max_occupied_row = row
        # emit signal
        self.studies_changed.emit()
        
    def make_variable_at_column(self, col, var_name, var_type=CATEGORICAL):
        var = self.make_new_variable(label=var_name, var_type=var_type)
        self.cols_2_vars[col] = var
        if self.max_occupied_col is None or self.max_occupied_col < col:
            self.max_occupied_col = col
         
    def unmark_column_as_label(self, column_index, original_study_labels={}): # original study labels is a mapping of those studies whose labels were changed to their original values
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
            if study in original_study_labels:
                value = original_study_labels[study]
            else:
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
        #max_occupied_row = self.calculate_max_occupied_row()
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
            return QVariant(QString(manual_word_wrap(col_name) + suffix))
            
        elif orientation == Qt.Vertical:
            return QVariant(int(section + 1))
    


    #@profile_this
    def setData(self, index, value, role=Qt.EditRole, basic_value=False): # basic_value means a regular python type not a QVariant
        if not index.isValid() and not (0 <= index.row() < self.rowCount()):
            print("bad setData: Index not valid")
            return False
        if role != Qt.EditRole:
            print("bad setData: No implementation written when role != Qt.EditRole")
            return False
        # set dirty bit
        self.dirty = True
        
        row, col = index.row(), index.column()
        row_has_study = row in self.rows_2_studies
        is_label_col = col == self.label_column
        if basic_value:
            value_as_string = str(value)
        else: # value is a QVariant
            value_as_string = str(value.toString()) if value not in ["", None,QVariant(),QVariant(None)] else ""
            
        if '"' in value_as_string:
            self.error_msg_signal.emit("You have entered the land of forbidden characters, from which none have ever returned", "\" character not allowed, it breaks things")
            return False
        
        value_blank = (value == QVariant()) or (value is None) or (value_as_string == "")
        if value_blank:
            value = None
        
        # For doing/undoing all the sub_actions in one go
        # The emit data changed is so that it will be called LAST when the
        # macro is undone
        if not self.big_paste_mode:
            self.undo_stack.beginMacro(QString("SetDataMacro: (%d,%d), value: '%s'" % (row,col, value_as_string)))
            self.undo_stack.push(EmitDataChangedCommand(model=self, index=index))
        
        if not row_has_study: # no study on this row yet, we will make one
            if value_blank:
                if not self.big_paste_mode:
                    cancel_macro_creation_and_revert_state(self.undo_stack)
                return True
            if not self.big_paste_mode:
                self.undo_stack.push(MakeStudyCommand(model=self, row=row))
            else:
                self.make_study_at_row(row)
            
        study = self.rows_2_studies[row]
        
        if is_label_col:
            existing_label = study.get_label()
            proposed_label = value_as_string if not value_blank else None
            
            def label_valid():
                if proposed_label == existing_label:
                    return True
                # check for duplicate labels
                current_labels = set([study.get_label() for study in self.get_studies_in_current_order()])
                if proposed_label in current_labels:
                    self.duplicate_label.emit()
                    print("bad setData: proposed label %s already in current labels" % proposed_label)
                    return False
                return True
            
            if label_valid():
                if not self.big_paste_mode:
                    self.undo_stack.push(SetStudyLabelCommand(study=study, new_label=proposed_label))
                    self.adjust_max_length_for_col(col, existing_label, proposed_label)
                else:
                    self.study.set_label(self.new_label)
            else:
                if not self.big_paste_mode:
                    cancel_macro_creation_and_revert_state(self.undo_stack)
                return True

        else: # we are in a variable column (initialized or not)
            make_new_variable = not self.column_assigned_to_variable(col)
            if make_new_variable: # make a new variable and give it the default column header name
                if value_blank:
                    if not self.big_paste_mode:
                        cancel_macro_creation_and_revert_state(self.undo_stack)
                    return True
                new_var_name = str(self.get_default_header(col))
                if not self.big_paste_mode:
                    self.undo_stack.push(MakeNewVariableCommand(model=self, var_name=new_var_name, col=col))
                else:
                    self.make_variable_at_column(col=col, var_name=new_var_name)

            var = self.cols_2_vars[col]
            var_name = var.get_label()
            var_type = var.get_type()
            
            
            # Set value in study for variable
            can_convert_value_to_desired_type = self.dataset.can_convert_var_value_to_type(var_type, value_as_string)
            if not can_convert_value_to_desired_type:
                bad_conversion_msg = "Cannot convert '%s' to %s data type" % (value_as_string, VARIABLE_TYPE_STRING_REPS[var_type])
                self.emit(SIGNAL("DataError"), QString("Impossible Data Conversion"), QString(bad_conversion_msg))
                if not self.big_paste_mode:
                    cancel_macro_creation_and_revert_state(self.undo_stack)
                print("bad setData: %s" % bad_conversion_msg)
                return False
                
            formatted_value = self._convert_input_value_to_correct_type_for_assignment(value_as_string, var_type)
            
            
            if not self.big_paste_mode:
                old_value = study.get_var(var)
                self.undo_stack.push(SetVariableValueCommand(study=study, variable=var, value=formatted_value))
                self.adjust_max_length_for_col(col, old_value, formatted_value)
            else: # we are pasting something large
                study.set_var(var, formatted_value)
             
            # Check to see if variable belongs to a variable group (with effect sizes calculated)
            # If so, change effect size(s) as well (transformed and raw scale)   
            self.handle_grouped_variable_from_setData(study, var, value)
            
        # If variables and label for this study are all blank, remove the
        # study from the dataset
        if study.is_totally_blank():
            self.undo_stack.push(RemoveStudyCommand(model=self, row=row))
            
        
        
        if not self.big_paste_mode:
            # End of the macro for undo/redo
            self.undo_stack.push(EmitDataChangedCommand(model=self, index=index))
            self.undo_stack.endMacro()
            
            self.change_row_count_if_needed()
            self.change_column_count_if_needed()
        else: # don't check unnessarily (optimization)
            if row > self.rowlimit-10:
                self.change_row_count_if_needed()
            if col > self.collimit-10:
                self.change_column_count_if_needed()
                
                
        #self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
        #          index, index)
        return True
    
    
    def test_value_for_setData(self, index, value):
        # value assumed to be QVariant
        
        row, col = index.row(), index.column()
        row_has_study = row in self.rows_2_studies
        is_label_col = col == self.label_column
        value_as_string = str(value.toString()) if value not in ["", None,QVariant(),QVariant(None)] else ""
        
        value_blank = (value in [QVariant(), None, QVariant(None)]) or (value_as_string =="")
        if value_blank:
            value = None
            
        if row_has_study:
            study = self.rows_2_studies[row]
        
        if is_label_col:
            if row_has_study:
                existing_label = study.get_label()
            proposed_label = value_as_string if not value_blank else None
            
            def label_valid():
                if row_has_study:
                    if proposed_label == existing_label:
                        return True
                # check for duplicate labels
                current_labels = set([astudy.get_label() for astudy in self.get_studies_in_current_order()])
                if proposed_label in current_labels:
                    self.duplicate_label.emit()
                    return False
                return True
            
            if not label_valid():
                return False

        else: # we are in a variable column (initialized or not)
            make_new_variable = not self.column_assigned_to_variable(col)
            if make_new_variable:
                var_type = CATEGORICAL # most general
            else:
                var = self.cols_2_vars[col]
                var_name = var.get_label()
                var_type = var.get_type()
            
            can_convert_value_to_desired_type = self.dataset.can_convert_var_value_to_type(var_type, value_as_string)
            if not can_convert_value_to_desired_type:
                self.emit(SIGNAL("DataError"), QString("Impossible Data Conversion"), QString("Cannot convert '%s' to %s data type" % (value_as_string, VARIABLE_TYPE_STRING_REPS[var_type])))
                return False
        return True
    
    def handle_grouped_variable_from_setData(self, study, var, value):
        var_grps = self.get_variable_groups_of_var(var)
        if len(var_grps)==0: # we are done if the variable does not belong to a group
            return
        
        for var_grp in var_grps:
            var_key = var_grp.get_var_key(var)
            if not var_grp.key_in_data(var_key): # var is an effect so we don't care
                continue
            #data_keys = var_grp.get_data_keys()
            if not var_grp.data_full():
                continue
            
            data_location_as_vars = var_grp.get_data_keys_to_vars()
            # verify study contains values for each var
            if not are_valid_numbers([study.get_var(v) for v in data_location_as_vars.values()]):
                continue # quit if not all the required boxes are filled in properly
            data = python_to_R.gather_data_for_single_study(data_location_as_vars, study)
            data = dict([(k, [v,]) for k,v in data.items()]) # convert singletons to lists to be suitable for python_to_R.effect_size
            trans_scale_effect_sizes = python_to_R.effect_size(    # keys: 'yi', 'vi'
                                                    metric=var_grp.get_metric(),
                                                    data_type=var_grp.get_data_type(),
                                                    data=data)
            # transform data to raw scale in case we need to update that too
            trans_scale_data = {TRANS_EFFECT: trans_scale_effect_sizes['yi'],
                                TRANS_VAR: trans_scale_effect_sizes['vi']}
            raw_effect_sizes = python_to_R.transform_effect_size(
                                                    metric=var_grp.get_metric(),
                                                    source_data=trans_scale_data,
                                                    direction=TRANS_TO_RAW,
                                                    conf_level=self.conf_level)
    
            self.set_single_row_effect_data(var_grp, study, trans_scale_data, raw_effect_sizes)
            
    def set_single_row_effect_data(self, var_grp, study, trans_scale_data, raw_scale_data):
        # convert list values to scalars
        trans_scale_data = listvals_to_scalars(trans_scale_data)
        raw_scale_data = listvals_to_scalars(raw_scale_data)
        
        #
        row = self.get_row_assigned_to_study(study)
        
        def set_data_helper(data):
            for key, val in data.items():
                var = var_grp.get_var_with_key(key)
                if not var:
                    continue
                col = self.get_column_assigned_to_variable(var)
                model_index = self.createIndex(row, col)
                self.setData(model_index, value=val, basic_value=True)
        
        set_data_helper(trans_scale_data)
        set_data_helper(raw_scale_data)
    
    def adjust_max_length_for_col(self, col, old_value, new_value):
        # convert to strings
        old_value = str(old_value) if old_value is not None else ''
        new_value = str(new_value) if new_value is not None else ''
        old_value_length = len(old_value)
        new_value_length = len(new_value)
        
        if new_value_length > self.get_max_length_in_col(col):
            self.col_2_max_length[col] = new_value_length
            # emit signal to reset size of this column
            ##
            self.should_resize_column.emit(col)
            
    
    
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
            
        
    
    def add_effect_sizes_to_model(self, metric, effect_sizes, cols_to_overwrite=None):
    
        studies = self.get_studies_in_current_order()
        if not cols_to_overwrite:
            last_occupied_col = sorted(self.cols_2_vars.keys(), reverse=True)[0]
            yi_col = last_occupied_col+1
            vi_col = yi_col+1
        else:
            yi_col = cols_to_overwrite[TRANS_EFFECT]
            vi_col = cols_to_overwrite[TRANS_VAR]
        
        if not bool(cols_to_overwrite):
            self.undo_stack.beginMacro(QString("Adding effect size to spreadsheet"))
        else:
            self.undo_stack.beginMacro(QString("Adding effect size to spreadsheet (overwriting existing columns)"))
        
        
        def emit_change_signals():
            self.emit_change_signals_for_col(yi_col)
            self.emit_change_signals_for_col(vi_col)
        start_cmd = GenericUndoCommand(redo_fn=do_nothing,
                                      undo_fn=emit_change_signals)
        self.undo_stack.push(start_cmd)
        ##################################################################
        if not bool(cols_to_overwrite):
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
        #else: # variables already exist!
        

        variable_yi = self.get_variable_assigned_to_column(yi_col)
        variable_vi = self.get_variable_assigned_to_column(vi_col)
        
        # Set subtype (for display purposes only for now)
        self.undo_stack.push(SetVariableSubTypeCommand(model=self, variable=variable_yi, new_subtype=TRANS_EFFECT))
        self.undo_stack.push(SetVariableSubTypeCommand(model=self, variable=variable_vi, new_subtype=TRANS_VAR))
        
        # add variables to new column_group
        old_col_group = self.get_variable_group_of_var(variable_vi)
        if old_col_group: # this will exist in the case of overwriting existing columns probably (unless the columns were constucted by hand)
            col_group = old_col_group
        else:
            col_group = self.make_new_variable_group(metric=metric, name=METRIC_TEXT_SIMPLE[metric] + " column group")
        keys_to_vars = {TRANS_EFFECT:variable_yi,
                        TRANS_VAR:variable_vi}
        self.undo_stack.push(GenericUndoCommand(redo_fn=partial(self.add_vars_to_col_group, col_group, keys_to_vars),
                                                undo_fn=partial(self.remove_vars_from_col_group, col_group, keys=keys_to_vars.keys()),
                                                description="Add variables to column group"))
        
        self.set_values_of_variables(studies=studies,
                                     var_yi=variable_yi, var_vi=variable_vi,
                                     raw_yi=effect_sizes['yi'], raw_vi=effect_sizes['vi'])
            
        ##################################################################
        end_cmd = GenericUndoCommand(redo_fn=emit_change_signals,
                                     undo_fn=do_nothing)
        self.undo_stack.push(end_cmd)
        
        self.undo_stack.endMacro()
        
        return {TRANS_EFFECT: yi_col, # returns columns of new assignments
                TRANS_VAR: vi_col}
    
    def set_values_of_variables(self, studies, var_yi, var_vi, raw_yi, raw_vi, emit_change_signals=False):
        def emit_change_signals():
            yi_col = self.get_column_assigned_to_variable(var_yi)
            vi_col = self.get_column_assigned_to_variable(var_vi)
            self.emit_change_signals_for_col(yi_col)
            self.emit_change_signals_for_col(vi_col)
        
        self.undo_stack.beginMacro(QString("Setting variables values from yi,vi data and corresponding list of studies"))
        start_cmd = GenericUndoCommand(redo_fn=do_nothing,
                                      undo_fn=emit_change_signals)
        self.undo_stack.push(start_cmd)
        #######################################
        for study, val_yi, val_vi in zip(studies, raw_yi, raw_vi):
            set_vi_cmd = SetVariableValueCommand(study, var_yi, val_yi)
            set_yi_cmd = SetVariableValueCommand(study, var_vi, val_vi)
            self.undo_stack.push(set_vi_cmd)
            self.undo_stack.push(set_yi_cmd)
        #######################################
        end_cmd = GenericUndoCommand(redo_fn=emit_change_signals,
                                     undo_fn=do_nothing)
        self.undo_stack.push(end_cmd)
        self.undo_stack.endMacro()
        
        
    def set_variable_values(self, studies, variable, values):
        ''' studies is a list of studies in the same order as values '''
        
        for study, value in zip(studies, values):
            study.set_var(variable, value)
        
        

    def make_new_variable_group(self, metric, name):
        print("Making new column group")
        col_group = VariableGroup(metric=metric, name=name)    
        
        redo_fn = partial(self.variable_groups.append,col_group)
        undo_fn = partial(self.variable_groups.remove,col_group)
        
        make_col_grp_cmd = GenericUndoCommand(redo_fn=redo_fn, undo_fn=undo_fn, 
                                              description="Make new column group")
        self.undo_stack.push(make_col_grp_cmd)
        
        return col_group
    
    
    def remove_variable_group(self, var_group):
        if var_group is None:
            return None
        redo_fn = partial(self.variable_groups.remove,var_group)
        undo_fn = partial(self.variable_groups.append,var_group)
        
        remove_var_group_cmd = GenericUndoCommand(redo_fn=redo_fn,
                                                  undo_fn=undo_fn,
                                                  description="Remove variable group")
        self.undo_stack.push(remove_var_group_cmd)
        return var_group

        
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
                                      on_undo_entry=do_nothing,
                                      on_undo_exit=lambda: self.emit_change_signals_for_col(col),
                                      on_redo_entry=do_nothing,
                                      on_redo_exit=lambda: self.emit_change_signals_for_col(col))
        self.undo_stack.push(sort_cmd)
        
        
    def _set_rows_to_studies(self, new_rows_to_studies):
        self.rows_2_studies = new_rows_to_studies
    

    def get_variable_groups_of_var(self,var):
        ''' Returns a list containing the variable groups to which var belongs'''
        
        var_groups = []
        for var_group in self.variable_groups:
            if var_group.contains_var(var):
                var_groups.append(var_group)
        return var_groups
    
    def get_variable_group_of_var(self, var):
        ''' Assumes var belongs to just one group'''
        
        assert isinstance(var, Variable)
        
        var_groups = self.get_variable_groups_of_var(var)
        if var_groups == []:
            return None
        return var_groups[0]
        
        
class VariableGroup:
    # Stores info on related groups of variables i.e. effect size and variance, etc
    def __init__(self, metric, name=""):
        self.name = name
        self.metric = metric
        self.data_type = get_data_type_for_metric(self.metric)
        
        self.group_data = {RAW_EFFECT:None,
                           RAW_LOWER:None,
                           RAW_UPPER:None,
                           TRANS_EFFECT:None,
                           TRANS_VAR:None,
                           
                           # continuous
                           'control_mean'            : None,
                           'control_std_dev'         : None,
                           'control_sample_size'     : None,
                           'experimental_mean'       : None,
                           'experimental_std_dev'    : None,
                           'experimental_sample_size': None,
                           
                           # binary 
                           'control_response'       : None, 
                           'control_noresponse'     : None, 
                           'experimental_response'  : None, 
                           'experimental_noresponse': None, 
                           
                           # correlations
                           'correlation': None,
                           'sample_size': None,
                           
                           }
        self.effect_keys = [TRANS_VAR, TRANS_EFFECT, RAW_EFFECT, RAW_LOWER, RAW_UPPER]
        data_continuous_keys = ['control_mean', 'control_std_dev', 'control_sample_size',   
                                     'experimental_mean', 'experimental_std_dev', 'experimental_sample_size'] 
        data_binary_keys = ['control_response', 'control_noresponse',
                                 'experimental_response','experimental_noresponse']
        data_correlation_keys = ['correlation', 'sample_size']
        self.data_keys = {MEANS_AND_STD_DEVS: data_continuous_keys,
                          TWO_BY_TWO_CONTINGENCY_TABLE: data_binary_keys,
                          CORRELATION_COEFFICIENTS:data_correlation_keys}[self.data_type]
        
        
    def effects_empty(self):
        effects_subdict = dict([(key,val) for key,val in self.group_data.iteritems() if key in self.effect_keys])
        return not any(effects_subdict.values())
    
    def effects_full(self):
        effects_subdict = dict([(key,val) for key,val in self.group_data.iteritems() if key in self.effect_keys])
        return all(effects_subdict.values())
    
    def raw_effects_full(self):
        raw_effects_subdict = dict([(key,val) for key,val in self.group_data.iteritems() if key in [RAW_EFFECT, RAW_LOWER, RAW_UPPER]])
        return all(raw_effects_subdict.values())
    
    def data_full(self):
        data_subdict = dict([(key, val) for key,val in self.group_data.iteritems() if key in self.data_keys])
        return all(data_subdict)
    
    def get_data_keys_to_vars(self):
        data_subdict = dict([(key, val) for key,val in self.group_data.iteritems() if key in self.data_keys])
        return data_subdict
    
    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name
    
    def get_metric(self):
        return self.metric
    def get_data_type(self):
        return self.data_type
    
    def set_var_with_key(self, key, var):
        self.group_data[key] = var

    def get_var_with_key(self, key):
        return self.group_data[key]
    
    def unset_key(self, key):
        self.group_data[key]=None
        
    def get_var_key(self, var):
        for k,v in self.group_data.items():
            if v==var:
                return k
        raise KeyError("No such variable in the group")
    
    def key_in_data(self, key):
        return key in self.data_keys

    def get_data_keys(self):
        return self.data_keys
    
    def get_group_data_copy(self):
        return self.group_data.copy()
    def set_group_data(self, grp_data):
        ''' shouldn't be used except during undo/redo to reset the group data '''
        self.group_data=grp_data
    
    def contains_var(self, var):
        try:
            self.get_var_key(var)
            return True
        except KeyError:
            return False
        
    def get_assigned_vars(self):
        return [var for var in self.group_data.values() if var]
        
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
        
        self.old_max_occupied_row = self.model.max_occupied_row
        
        
    def redo(self):
        if DEBUG_MODE: print("redo: make new study_command")
        model = self.model
        if self.study is None: # this should only execute once
            self.study = model.dataset.make_new_study()
        else:            # we should always be here on subsequent runs of redo
            model.dataset.add_existing_study(self.study)
        model.rows_2_studies[self.row] = self.study
        if self.model.max_occupied_row is None or self.model.max_occupied_row < self.row:
            self.model.max_occupied_row = self.row
        
        # emit signal
        self.model.studies_changed.emit()
    
    def undo(self):
        ''' Remove study at the specified row in the model '''
        
        if DEBUG_MODE:
            print("undo: make new study_command")
        self.model.remove_study(self.study)
        self.model.max_occupied_row = self.old_max_occupied_row
        

class RemoveStudyCommand(QUndoCommand):
    ''' Removes / unremoves study at the specified row in the model '''
    def __init__(self, model, row):
        super(RemoveStudyCommand, self).__init__()
        
        self.setText(QString("Remove study @ row %d" % row))
        
        self.model = model
        self.row = row
        self.study = self.model.rows_2_studies[self.row]
        
        self.model.dirty = True
        self.old_max_occupied_row = self.model.max_occupied_row
        
    def redo(self):
        if DEBUG_MODE:
            print("redo: remove study")
        self.model.remove_study(self.study)
        if self.row == self.model.max_occupied_row:
            self.model.calculate_max_occupied_row()
        
    def undo(self):
        if DEBUG_MODE: print("undo: remove study")
        self.model.dataset.add_existing_study(self.study)
        self.model.rows_2_studies[self.row]=self.study
        
        self.model.max_occupied_row = self.old_max_occupied_row
        
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
        self.old_max_occupied_col = self.model.max_occupied_col
        
    def redo(self):
        if DEBUG_MODE: print("redo: make new variable_command")
        if self.var is None:
            self.var = self.model.make_new_variable(label=self.var_name, var_type=self.var_type)
        else:
            self.model.dataset.add_existing_variable(self.var)
        self.model.cols_2_vars[self.col] = self.var
        if self.model.max_occupied_col is None or self.model.max_occupied_col < self.col:
            self.model.max_occupied_col = self.col
        
    def undo(self):
        if DEBUG_MODE: print("undo: make new variable_command")
        self.model.remove_variable(self.var)
        self.model.max_occupied_col=self.old_max_occupied_col
        

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
        #if DEBUG_MODE: print("undo: emit data changed")
        self.model.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
          self.index, self.index)
        
    def redo(self):
        #if DEBUG_MODE: print("redo: emit data changed")
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
        
        # mapping of vars--> (variable_group, key_in_group)
        self.variable_group_info = {}
        
        
        # Save info from cols that will be removed
        for col in range(self.column, self.column+self.count):
            if col == self.model.label_column:
                self.save_label_column_info(col)
            # col is a variable column
            if self.model.column_assigned_to_variable(col):
                self._store_variable_column_data(col) # variable index, variable data in studies
                
        self.model.dirty = True
        self.old_max_occupied_col = self.model.max_occupied_col
        
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
        
        self.model.calculate_max_occupied_col()
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
        
        self.model.max_occupied_col=self.old_max_occupied_col
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
            
        # Store data about variable's variable_group
        var_group = self.model.get_variable_group_of_var(var)
        key = var_group.get_var_key(var) if var_group else None
        self.variable_group_info[var] = (var_group,key)
            
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
            
        # reassign variable to its variable group (if it exists)
        var_group,key = self.variable_group_info[var]
        if var_group:
            var_group.set_var_with_key(key=key, var=var)
        
        
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
        self.original_variable_group = self.model.get_variable_group_of_var(variable)
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
            self.original_variable_group.unset_key(self.key_var_group)

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
            