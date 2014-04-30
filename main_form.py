################
#              #
# George Dietz #
# CEBM@Brown   #
#              #
################                

import sys
#import pdb
#import copy
from functools import partial
from collections import deque
import pickle
import cProfile

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_main_window
import about
import calculate_effect_sizes_wizard
import transform_effect_size_wizard
import ee_model
import useful_dialogs
import python_to_R
from python_to_R import exR
import csv_import_dlg
import csv_export_dlg
import preferences_dlg
from contingency_table_dlg import ContingencyTableDlg
import imputation.imputation_wizard

from variable_group_graphic import VariableGroupGraphic
from analyses import Analyzer
import r_log_dlg

from ome_globals import *

# TODO: Handle setting the dirty bit more correctly in undo/redo
# right now just set it all the time/(or not) (very haphazard) during redo but don't bother unsetting it


class RecentFilesManager:
    def __init__(self):
        self.recent_files = deque(maxlen=MAX_RECENT_FILES)
    
    def add_file(self, fpath):
        # add a new file to the front of the deque
        # move existing file to the front of the deque
        
        if fpath in [None, ""]:
            return False
        
        if fpath in self.recent_files: #file already in deque so move to front
            self.recent_files.remove(fpath)
        self.recent_files.appendleft(fpath)
        
    def get_list(self):
        return list(self.recent_files)
####################################################################################
import ui_conf_level_toolbar_widget

class ConfLevelToolbarWidget(QWidget, ui_conf_level_toolbar_widget.Ui_Form):
    def __init__(self, parent=None):
        super(ConfLevelToolbarWidget, self).__init__(parent)
        self.setupUi(self)
        
        #self.conf_level_spinbox
        
    def set_spinbox_value_no_signals(self, new_val):
        self.conf_level_spinbox.blockSignals(True)
        self.conf_level_spinbox.setValue(new_val)
        self.conf_level_spinbox.blockSignals(False)
####################################################################################

class MainForm(QtGui.QMainWindow, ui_main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi(self)
        
        # Setup analyzer (which performs analyses)
        self.analyst = Analyzer(main_form=self)
        
        # R log dialog
        self.r_log_dlg = None
        
        layout = self.verticalLayout # 
        self.vargroup_graphic = VariableGroupGraphic()
        layout.addWidget(self.vargroup_graphic)
        
        # Confidence level spinbox
        self.conf_level_toolbar_widget = ConfLevelToolbarWidget(parent=self)
        self.toolBar.insertWidget(self.actionResetAnalysisChoices, 
                                    self.conf_level_toolbar_widget)
        
        self.undo_stack = QUndoStack(self)
        #### Handle user prefs / settings issue # 111
        load_settings()
        self.populate_recent_datasets()
        
        self.model = ee_model.EETableModel(undo_stack=self.undo_stack)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.conf_level_toolbar_widget.conf_level_spinbox.setValue(self.model.get_conf_level())
        python_to_R.set_conf_level_in_R(self.model.get_conf_level())
        
        #### Display undo stack (if we want to...)
        self.undo_view_form = useful_dialogs.UndoViewForm(undo_stack=self.undo_stack, model=self.model, parent=self)
        if SHOW_UNDO_VIEW:
            self.undo_view_form.show()
            self.undo_view_form.raise_()
        
        self.statusBar().showMessage("Welcome to OpenMEE")

        self.setup_menus()
        self.setup_connections()
        
        self.outpath = None
        
        horizontal_header = self.tableView.horizontalHeader()
        horizontal_header.setContextMenuPolicy(Qt.CustomContextMenu)
        horizontal_header.customContextMenuRequested.connect(self.make_horizontal_header_context_menu)
        
        vertical_header = self.tableView.verticalHeader()
        vertical_header.setContextMenuPolicy(Qt.CustomContextMenu)
        vertical_header.customContextMenuRequested.connect(self.make_vertical_header_context_menu)
        
        self.set_window_title()
        
        
        # issue #8: disable copy-pasta if nothing 
        # is selected (which is true at the outset)
        self.toggle_copy_pasta(False)

        
    def set_window_title(self):
        if self.outpath is None:
            filename = DEFAULT_FILENAME
        else:
            filename = os.path.basename(self.outpath)
        self.setWindowTitle(' - '.join([PROGRAM_NAME, filename]))
        self.setWindowIcon(QIcon(":/general/images/logo.png")) # don't know why this isn't set automatically (since I set it in Qt Designer for the main.ui)

    def toggle_copy_pasta(self, b):
        '''
        set all menu options pertaining to 
        copy/paste to (boolean) b.
        '''
        
        print("Toggling copy pasta %d" % b)
        
        self.actionCopy.setEnabled(b)
        self.actionPaste.setEnabled(b)
        self.actionCut.setEnabled(b)
        self.actionClear_Selected_Cells.setEnabled(b)

    def showEvent(self, show_event):
        ''' do custom stuff upon showing the window '''

        self.initialize_display()
        QMainWindow.showEvent(self, show_event)
    
    
    def initialize_display(self):
        ''' collection of function calls to perform when the main window is
        first displayed or a new model is loaded '''
        
        self._set_show_toolbar_txt() # change status of show toolbar action
        
        # undo/redo actions
        self.update_undo_enable_status()
        self.update_redo_enable_status()
        
        self.toggle_analyses_enable_status()
        
    
    def toggle_analyses_enable_status(self):
        ''' Toggle the enable status of the analysis actions according whether
        1) There are studies
        2) a label column has been set '''
        
        enable = True
        not_enabled_msg = ""
        try:
            old_enable_status = self.enable_analyses
        except AttributeError:
            old_enable_status = False
        
        studies = self.model.get_studies_in_current_order()
        if len(studies) == 0:
            enable = False
            not_enabled_msg = "No studies entered yet."
            
        if self.model.label_column is None:
            enable = False
            not_enabled_msg = "Can't enable analyses yet, did you set a study ID column?"
        

        if (old_enable_status != True) and (not enable) and (not_enabled_msg != ""):
            self.statusbar.showMessage("%s" % not_enabled_msg)
        else:
            self.statusbar.showMessage("")
            
        self.enable_analyses = enable
        print("Enable status for analyses: %s" % enable)
            
        self.actionCalculate_Effect_Size.setEnabled(enable)
        self.actionStandard_Meta_Analysis.setEnabled(enable)
        self.actionLeave_one_out.setEnabled(enable)
        self.actionCumulative.setEnabled(enable)
        self.actionMeta_Regression.setEnabled(enable)
        self.actionBootstrapped_Meta_Analysis.setEnabled(enable)
        
        if enable:
            if self.model.get_variables(var_type=CATEGORICAL) == []:
                self.actionSubgroup.setEnabled(False)
            else:
                self.actionSubgroup.setEnabled(True)
        else:
            self.actionSubgroup.setEnabled(False)   

    def set_model(self, state):
        '''
        Used when loading a picked model. Take note we clear the undo
        stack here
        '''
        self.disconnect_model_connections()
        
        self.undo_stack.clear()
        self.model = ee_model.EETableModel(undo_stack=self.undo_stack,
                                           model_state=state)
        self.model.dirty = False
        self.model.change_row_count_if_needed()
        self.model.change_column_count_if_needed(debug=True)
        
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.conf_level_toolbar_widget.conf_level_spinbox.setValue(self.model.get_conf_level())
        self.make_model_connections()

    def setup_menus(self):
        # File Menu
        QObject.connect(self.actionNew, SIGNAL("triggered()"), self.new_dataset)
        self.actionNew.setShortcut(QKeySequence.New)
        
        QObject.connect(self.actionOpen, SIGNAL("triggered()"), self.open)
        self.actionOpen.setShortcut(QKeySequence.Open)

        QObject.connect(self.actionSave, SIGNAL("triggered()"), self.save)
        self.actionSave.setShortcut(QKeySequence.Save)
        
        QObject.connect(self.actionSave_As, SIGNAL("triggered()"), 
                                        lambda: self.save(save_as=True))
        self.actionSave_As.setShortcut(QKeySequence.SaveAs)
        
        QObject.connect(self.actionQuit, SIGNAL("triggered()"), self.quit)
        self.actionQuit.setShortcut(QKeySequence.Quit)
        
        QObject.connect(self.actionImportCSV, SIGNAL("triggered()"), self.import_csv)
        QObject.connect(self.actionExportCSV, SIGNAL("triggered()"), self.export_csv)
        
        ### Edit Menu ###
        QObject.connect(self.actionUndo, SIGNAL("triggered()"), self.undo)
        self.actionUndo.setShortcut(QKeySequence(QKeySequence.Undo))  
        
        QObject.connect(self.actionRedo, SIGNAL("triggered()"), self.redo)
        self.actionRedo.setShortcut(QKeySequence.Redo)
        
        # Cut, Copy, Paste #
        QObject.connect(self.actionCut, SIGNAL("triggered()"), self.cut)
        self.actionCut.setShortcut(QKeySequence.Cut) 
        
        QObject.connect(self.actionCopy, SIGNAL("triggered()"), self.copy)
        self.actionCopy.setShortcut(QKeySequence.Copy)
        
        QObject.connect(self.actionPaste, SIGNAL("triggered()"), self.paste)
        self.actionPaste.setShortcut(QKeySequence.Paste)
        
        QObject.connect(self.actionClear_Selected_Cells, SIGNAL("triggered()"), self.clear_selected_cells)
        
        # Show/hide toolbar
        QObject.connect(self.actionShow_toolbar, SIGNAL("triggered()"), self.toggle_toolbar_visibility)
        
        ### Table Menu ###
        self.actionTable_Preferences.triggered.connect(self.adjust_preferences)
        
        ### Analysis Menu ###
        QObject.connect(self.actionCalculate_Effect_Size,  SIGNAL("triggered()"), self.calculate_effect_size)
        QObject.connect(self.actionStandard_Meta_Analysis, SIGNAL("triggered()"), self.analyst.meta_analysis)
        QObject.connect(self.actionCumulative,    SIGNAL("triggered()"), self.analyst.cum_ma)
        QObject.connect(self.actionLeave_one_out, SIGNAL("triggered()"), self.analyst.loo_ma)
        QObject.connect(self.actionSubgroup,      SIGNAL("triggered()"), self.analyst.subgroup_ma)
        
        self.actionTransform_Effect_Size.triggered.connect(self.transform_effect_size_bulk)
        self.actionModel_Building.triggered.connect(self.analyst.model_building)
        self.actionMultiple_Imputation_Meta_Analysis.triggered.connect(self.analyst.mi_meta_analysis)
        
        #self.actionMeta_Regression.triggered.connect(self.analyst.meta_regression)
        self.actionMeta_Regression.triggered.connect(self.analyst.gmeta_regression)
        self.actionBootstrapped_Meta_Analysis.triggered.connect(self.analyst.bootstrap_ma)

        QObject.connect(self.actionPhyloMA, SIGNAL("triggered()"), self.analyst.phylo_ma)
        
        #### Publication Bias Menu ###
        self.actionFail_Safe_N.triggered.connect(self.analyst.failsafe_analysis)
        self.actionFunnel_Plot.triggered.connect(self.analyst.funnel_plot_analysis)
        
        #### Data Exploration Menu ###
        self.actionHistogram.triggered.connect(self.analyst.histogram)
        self.actionScatterplot.triggered.connect(self.analyst.scatterplot)
        self.actionContingency_Table.triggered.connect(self.contingency_table)
        self.actionImpute_Missing_Data.triggered.connect(self.impute_missing_data)
        
        # Help Menu
        self.action_about.triggered.connect(self.show_about_dlg)
        self.actionGet_help_online.triggered.connect(self.open_help_online)
        
        # Through the looking glass .... Menu
        self.actionR_log.triggered.connect(self.show_R_log_dlg)
        
        # Toolbar
        self.actionResetAnalysisChoices.triggered.connect(self.reset_analysis_selection)
        
        
    def open_help_online(self):
        QDesktopServices.openUrl(QUrl(HELP_URL))
        
    def contingency_table(self):
        dlg = ContingencyTableDlg(model=self.model, parent=self)
        dlg.exec_()
    
    def show_about_dlg(self):
        dlg = about.About()
        dlg.exec_()
    
    def toggle_toolbar_visibility(self):
        status = self.toolBar.isVisible()
        self.toolBar.setVisible(not status)
        self._set_show_toolbar_txt()
            
    def _set_show_toolbar_txt(self):
        visible = self.toolBar.isVisible()
        
        if visible:
            print("hide toolbar")
            self.actionShow_toolbar.setText("Hide toolbar")
        else:
            self.actionShow_toolbar.setText("Show toolbar")

    def setup_connections(self):
        self.make_model_connections()

        # connect undo/redo signals to enable/disable menu items
        self.undo_stack.canUndoChanged.connect(self.update_undo_enable_status)
        self.undo_stack.canRedoChanged.connect(self.update_redo_enable_status)

        self.tableView.horizontalScrollBar().actionTriggered.connect(lambda: QTimer.singleShot(0, self.update_vargroup_graphic))


    def stupid(self):
        print("column formats changed")
        
    def reset_analysis_selection(self):
        self.model.reset_last_analysis_selection()

    def table_selection_changed(self):
        if self.model.big_paste_mode:
            return
        print("Table selection changed")
        anything_selected = False
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        upper_left_index = self._upper_left(selected_indexes)
        if upper_left_index is not None:
            anything_selected = True

        # issue #8
        self.toggle_copy_pasta(anything_selected)


    def update_undo_enable_status(self):
        if self.undo_stack.canUndo():
            self.actionUndo.setEnabled(True)
        else:
            self.actionUndo.setEnabled(False)

    def update_redo_enable_status(self):
        if self.undo_stack.canRedo():
            self.actionRedo.setEnabled(True)
        else:
            self.actionRedo.setEnabled(False)

    def populate_recent_datasets(self):
        self.menuRecent_Data.clear()
        
        for fpath in get_setting('recent_files'):
            action = self.menuRecent_Data.addAction("Load %s" % fpath)
            QObject.connect(action, SIGNAL("triggered()"), partial(self.open, file_path=fpath))
            
        
    def disconnect_model_connections(self):
        QObject.disconnect(self.model, SIGNAL("DataError"), self.warning_msg)
        QObject.disconnect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), 
                            self.change_index_after_data_edited)
        QObject.disconnect(self.tableView_selection_model, 
                    SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), 
                    self.table_selection_changed)
        
        self.model.column_formats_changed.disconnect(self.toggle_analyses_enable_status)
        self.model.studies_changed.disconnect(self.toggle_analyses_enable_status)
        self.model.label_column_changed.disconnect(self.toggle_analyses_enable_status)
        self.model.duplicate_label.disconnect(self.duplicate_label_attempt)
        self.model.error_msg_signal.disconnect(self.error_msg_signal_handler)
        self.model.should_resize_column.disconnect(self.resize_column)
        self.conf_level_toolbar_widget.conf_level_spinbox.valueChanged[float].disconnect(
            self.model.set_conf_level)
        self.model.conf_level_changed_during_undo.disconnect(self.conf_level_toolbar_widget.set_spinbox_value_no_signals)
        
        
    def make_model_connections(self):
        QObject.connect(self.model, SIGNAL("DataError"), self.warning_msg)
        QObject.connect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), 
                        self.change_index_after_data_edited)
        self.tableView_selection_model = self.tableView.selectionModel()
        QObject.connect(self.tableView_selection_model, 
                    SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), 
                    self.table_selection_changed)
    
        self.model.column_formats_changed.connect(self.toggle_analyses_enable_status)
        self.model.studies_changed.connect(self.toggle_analyses_enable_status)
        self.model.label_column_changed.connect(self.toggle_analyses_enable_status)
        self.model.duplicate_label.connect(self.duplicate_label_attempt)
        self.model.error_msg_signal.connect(self.error_msg_signal_handler)
        self.model.should_resize_column.connect(self.resize_column)
        
        self.model.column_formats_changed.connect(lambda: QTimer.singleShot(1, self.update_vargroup_graphic))
        
        self.conf_level_toolbar_widget.conf_level_spinbox.valueChanged[float].connect(self.model.set_conf_level)
        self.model.conf_level_changed_during_undo.connect(self.conf_level_toolbar_widget.set_spinbox_value_no_signals)
        
    def duplicate_label_attempt(self):
        QMessageBox.critical(self, "Attempted duplicate label", "Labels must be unique")

    def error_msg_signal_handler(self, title, err_msg):
        QMessageBox.critical(self, title, err_msg)
    
    def adjust_preferences(self):
        form = preferences_dlg.PreferencesDialog()
        
        if form.exec_():
            update_setting('digits',                 form.get_precision())
            update_setting('model_header_font_str',  form.get_model_header_font().toString())
            update_setting('model_data_font_str',    form.get_model_data_font().toString())
            update_setting('show_additional_values', form.get_show_additional_values())
            update_setting('show_analysis_selections', form.get_show_analysis_selections())
            
            # Copy color scheme into settings
            color_scheme = form.get_color_scheme()
            for key, color in color_scheme.items():
                settings_key = "colors/" + key # add colors prefix
                update_setting(settings_key, color)
            
            self.model.beginResetModel()
            self.model.endResetModel()
            self.tableView.resizeColumnsToContents()

    def calculate_effect_size(self):
        ''' Opens the calculate effect size wizard form and then calculates the new
        effect size. Places the new calculated effect + variance in the 2
        columns beyond the most recently occupied one as new continuous
        variables '''
        
        wizard = calculate_effect_sizes_wizard.CalculateEffectSizeWizard(model=self.model, parent=self)
        
        if wizard.exec_():
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            cols_to_overwrite = wizard.get_columns_to_overwrite()
            make_link = wizard.make_link()
            
            # save data locations choices for this data type in the model
            self.model.update_data_location_choices(data_type, data_location)
            
            
            data = python_to_R.gather_data(self.model, data_location)
            try:
                effect_sizes = python_to_R.effect_size(metric, data_type, data)
            except CrazyRError as e:
                QMessageBox.critical(self, QString("R error"), QString(str(e)))
                return False
            print("Computed these effect sizes: %s" % str(effect_sizes))
            
            self.undo_stack.beginMacro("Calculate Effect Size")
            ################################################################
            if cols_to_overwrite:
                effect_cols_dict = self.model.add_effect_sizes_to_model(metric, effect_sizes, cols_to_overwrite=cols_to_overwrite)
            else: # vanilla
                # effect sizes is just yi and vi
                effect_cols_dict = self.model.add_effect_sizes_to_model(metric, effect_sizes)
            
            #### Add raw data source variables to group ###
            tmp_var = self.model.get_variable_assigned_to_column(effect_cols_dict[TRANS_EFFECT]) 
            var_grp = self.model.get_variable_group_of_var(tmp_var)
            old_var_group_data = var_grp.get_group_data_copy()
            undo_fn = lambda: var_grp.set_group_data(old_var_group_data) 
            if make_link:
                redo_fn = lambda: self.add_data_vars_to_var_group(data_location, var_grp)
            else:
                redo_fn = lambda: self.clear_data_vars_from_var_group(data_location.keys(), var_grp)
            self.undo_stack.push(GenericUndoCommand(redo_fn=redo_fn, undo_fn=undo_fn))
            #####################################################################
            self.undo_stack.endMacro()
            
            self.tableView.resizeColumnsToContents()
            QTimer.singleShot(0, self.update_vargroup_graphic)
            
    
    def add_data_vars_to_var_group(self, data_location, var_group):
        data_location = self.column_data_location_to_var_data_location(data_location)
        for key, var in data_location.items():
            if key in ['effect_size','variance']:
                continue
            var_group.set_var_with_key(key, var)
    
    def clear_data_vars_from_var_group(self, keys, var_group):
        ''' clears out assignments from keys in the var_group '''
        for key in keys:
            var_group.unset_key(key)
    
    def column_data_location_to_var_data_location(self, col_data_location):
        ''' Convert data location given by columns to given by variables '''
        
        var_data_location = {}
        for key, col in col_data_location.items():
            var_data_location[key] = self.model.get_variable_assigned_to_column(col)
        return var_data_location
            
    def transform_effect_size_bulk(self):
        ''' transforms the effect size given in metric from either
            
            1) normal scale to transformed scale (usually log scale) or
            2) transformed scale to normal scale
            This is given in direction via the global enumerations
            TRANS_TO_NORM and NORM_TO_TRANS

            data_location is a dictionary mapping to columns 

            Output:
                Will make new columns at the end of existing columns and put
                the new info there.
            '''


        conf_level=self.model.conf_level

        wizard = transform_effect_size_wizard.TransformEffectSizeWizard(model=self.model)

        if not wizard.exec_():
            return False

        effect_var_to_transform = self.model.get_variable_assigned_to_column(wizard.get_chosen_column())
        transform_direction = wizard.get_transformation_direction()
        verify_transform_direction(transform_direction)

        self.undo_stack.beginMacro("Transforming/backtransforming effect size")

        # Need to make a new column group if the effect column we chose doesn't belong to one yet
        if wizard.make_new_column_group():
            print("Making new column group")
            new_grp_cols = wizard.get_new_column_group_column_selections()
            metric = wizard.get_new_column_group_metric()
            if transform_direction == TRANS_TO_RAW:
                trans_yi = self.model.get_variable_assigned_to_column(new_grp_cols[TRANS_EFFECT])
                trans_vi = self.model.get_variable_assigned_to_column(new_grp_cols[TRANS_VAR])
                keys_to_vars = {TRANS_EFFECT:trans_yi,
                                TRANS_VAR:trans_vi}
            elif transform_direction == RAW_TO_TRANS:
                raw_yi = self.model.get_variable_assigned_to_column(new_grp_cols[RAW_EFFECT])
                raw_lb = self.model.get_variable_assigned_to_column(new_grp_cols[RAW_LOWER])
                raw_ub = self.model.get_variable_assigned_to_column(new_grp_cols[RAW_UPPER])
                keys_to_vars = {RAW_EFFECT:raw_yi,
                                RAW_LOWER:raw_lb,
                                RAW_UPPER:raw_ub}
            
            # make new column group and add variables to it
            col_group = self.model.make_new_variable_group(metric=metric, name=METRIC_TEXT_SIMPLE[metric] + " column group")
            self.undo_stack.push(GenericUndoCommand(redo_fn=partial(self.model.add_vars_to_col_group, col_group, keys_to_vars),
                                                    undo_fn=partial(self.model.remove_vars_from_col_group, col_group, keys=keys_to_vars.keys()),
                                                    description="Add variables to column group"))
        else: # column group already exists
            col_group = self.model.get_variable_group_of_var(effect_var_to_transform)
        metric = col_group.get_metric()

        data_location = {}
        if transform_direction == TRANS_TO_RAW:
            trans_yi = col_group.get_var_with_key(TRANS_EFFECT)
            trans_vi = col_group.get_var_with_key(TRANS_VAR)
            data_location = {TRANS_EFFECT:trans_yi,
                             TRANS_VAR:trans_vi}
        elif transform_direction == RAW_TO_TRANS:
            raw_yi = col_group.get_var_with_key(RAW_EFFECT)
            raw_lb = col_group.get_var_with_key(RAW_LOWER)
            raw_ub = col_group.get_var_with_key(RAW_UPPER)
            data_location = {RAW_EFFECT: raw_yi,
                             RAW_LOWER: raw_lb,
                             RAW_UPPER: raw_ub}
        
        
        data = python_to_R.gather_data(self.model, data_location, vars_given_directly=True)
        
        try:
            effect_sizes = python_to_R.transform_effect_size(metric, data, transform_direction, conf_level)
        except CrazyRError as e:
            QMessageBox.critical(self, QString("R error"), QString(str(e)))
            return False
        # effect sizes is just yi and vi
        self.model.add_transformed_effect_sizes_to_model(metric, effect_sizes, transform_direction, col_group)
        self.tableView.resizeColumnsToContents()
        
        #print("Computed these effect sizes: %s" % str(results))
        
        self.undo_stack.endMacro()
        
    #@profile_this
    def change_index_after_data_edited(self, index_top_left, index_bottom_right):        
        row, col = index_top_left.row(), index_top_left.column()
        row += 1
        if row < self.model.rowCount():
            self.tableView.setFocus()
            new_index = self.model.createIndex(row,col)
            self.tableView.setCurrentIndex(new_index)
        if not self.model.big_paste_mode:
            #end_row, end_col = index_bottom_right.row(), index_bottom_right.column()
            end_col = index_bottom_right.column()
            ncols = end_col - col + 1
            if ncols >= 10:
                self.tableView.resizeColumnsToContents()
            #else: this is handled by resize_column when the appropriate signal comes out of the model

    def resize_column(self, col):
        print("resizing column %d" % col)
        self.tableView.resizeColumnToContents(col)


    def warning_msg(self, title="mystery warning", msg="a mysterious warning"):
        warning_box = QMessageBox(self)
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setText(msg)
        warning_box.setWindowTitle(title)
        warning_box.exec_()

    ##### Undo / redo
    def undo(self):
        #print("Undo action triggered")
        self.undo_stack.undo()

    def redo(self):
        #print("Redo action triggered")
        self.undo_stack.redo()

    def make_vertical_header_context_menu(self, pos):
        ''' makes the context menu for the row headers when user right-clicks '''

        '''Actions:
        Insert row 
        delete study (row)
        '''

        row_clicked = self.tableView.rowAt(pos.y())

        is_study_row = self.model.row_assigned_to_study(row_clicked)
        if not is_study_row:
            return False

        context_menu = QMenu(self.tableView)

        # Delete a row(study)
        delete_row_action = context_menu.addAction("Remove row")
        QAction.connect(delete_row_action, SIGNAL("triggered()"), lambda: self.model.removeRow(row_clicked))


        # Insert a row
        insert_row_action = context_menu.addAction("Insert row")
        QAction.connect(insert_row_action, SIGNAL("triggered()"), lambda: self.model.insertRow(row_clicked))

        context_menu.popup(QCursor.pos())





    def make_horizontal_header_context_menu(self, pos):
        '''
        Makes the context menu for column headers when user right-clicks:
        Possible actions:
            change format of column (only for variable columns)
            rename column
            mark column as label (only for categorical cols)
            unmark column as label (only for label column)
            delete column
            insert column
        '''

#         # profiling fun
#         pr=cProfile.Profile()
#         pr.enable()
#         ###############

 



        column_clicked = self.tableView.columnAt(pos.x())

        if DEBUG_MODE:
            print("Right clicked column %d" % column_clicked)

        label_column = self.model.get_label_column()
        is_variable_column = self.model.column_assigned_to_variable(column_clicked)
        context_menu = QMenu(self.tableView)

        if (column_clicked == label_column or is_variable_column):
            if column_clicked != label_column:
                if is_variable_column:
                    variable = self.model.get_variable_assigned_to_column(column_clicked)

                    # Change format of column
                    change_format_menu = QMenu("Change format", parent=context_menu)
                    self.add_choices_to_change_format_menu(change_format_menu, column_clicked)
                    if len(change_format_menu.actions()) > 0:
                        context_menu.addMenu(change_format_menu)

                    # Mark column as label
                    if label_column is None and variable.get_type() == CATEGORICAL:
                        mark_as_label_action = context_menu.addAction("Mark as Study ID column")
                        QAction.connect(mark_as_label_action, SIGNAL("triggered()"),
                                        partial(self.mark_column_as_label, column_clicked))

            else:     #  column is label column
                # Unmark column as label
                unmark_as_label_action = context_menu.addAction("Unmark as Study ID column")
                QAction.connect(unmark_as_label_action, SIGNAL("triggered()"),
                                partial(self.unmark_column_as_label, column_clicked))

            # rename label column
            rename_column_action = context_menu.addAction("Rename %s" % ('variable' if is_variable_column else 'Study ID column')) 
            QAction.connect(rename_column_action, SIGNAL("triggered()"), lambda: self.rename_column(column_clicked))

            # delete column
            delete_column_action = context_menu.addAction("Remove %s" % ('variable' if is_variable_column else 'Study ID column'))
            QAction.connect(delete_column_action, SIGNAL("triggered()"), partial(self.remove_column, column_clicked))

            # insert column
            insert_column_action = context_menu.addAction("Insert column")
            QAction.connect(insert_column_action, SIGNAL("triggered()"), lambda: self.model.insertColumn(column_clicked))

            # Sort by column data
            sort_action = context_menu.addAction("Sort by column data")
            QAction.connect(sort_action, SIGNAL("triggered()"), lambda: self.model.sort_by_column(column_clicked))
            
            
        else: # column is not a label column or variable column
        
            # Make new variable
            make_new_categorical_variable_action = context_menu.addAction("Make new categorical variable")
            QObject.connect(make_new_categorical_variable_action, SIGNAL("triggered()"), partial(self.make_new_variable_at_col, col=column_clicked,var_type=CATEGORICAL))
        
        context_menu.popup(QCursor.pos())
        

    def remove_column(self, column):
        is_variable_column = self.model.column_assigned_to_variable(column)
        
        # Remove other columns @ same scale in var_group
        if is_variable_column:
            var = self.model.get_variable_assigned_to_column(column)
            var_group = self.model.get_variable_group_of_var(var)
            if var_group is not None:
                var_is_trans = var_group.get_var_key(var) in [TRANS_EFFECT, TRANS_VAR]
                if var_is_trans:
                    keylist = [TRANS_EFFECT, TRANS_VAR]
                else:
                    keylist = [RAW_EFFECT, RAW_LOWER, RAW_UPPER]
                
                self.undo_stack.beginMacro("Deleting all columns at same scale as selected column to delete")
                for var_key in keylist:
                    othervar = var_group.get_var_with_key(var_key)
                    if othervar is not None:
                        other_var_col = self.model.get_column_assigned_to_variable(othervar)
                        self.model.removeColumn(other_var_col)
                
                # Delete var group if it is empty now
                if var_group.effects_empty():
                    self.model.remove_variable_group(var_group) # undoable
                        
                self.undo_stack.endMacro()
                return
            
        self.model.removeColumn(column)
        
        
        
        
    def mark_column_as_label(self, col):
        ''' Should only occur for columns of CATEGORICAL type and only for a
        column which is not already the label column
        (the check happens elsewhere) '''
        
        variable = self.model.get_variable_assigned_to_column(col)
        variable_name = variable.get_label()
        
        # Ensure that study labels are unique
        distinct_study_labels = {} # map labels to # of times used
        overridden_study_labels = {}
        original_study_labels = {}
        studies = self.model.get_studies_in_current_order()
        for study in studies:
            proposed_label = study.get_var(variable)
            if proposed_label is None:
                    proposed_label = ''
            if proposed_label not in distinct_study_labels:
                distinct_study_labels[proposed_label] = 1
            else:
                distinct_study_labels[proposed_label] += 1
                original_study_labels[study] = proposed_label
            num_times_used = distinct_study_labels[proposed_label]
            if num_times_used > 1:
                proposed_label = proposed_label + '-' + str(num_times_used)
                distinct_study_labels[proposed_label] = 1
                overridden_study_labels[study] = proposed_label
        if overridden_study_labels != {}:
            choice = QMessageBox.warning(self, "Warning",
                        "Variable names need to be unique. If you continue, labels will be slightly altered to ensure uniqueness (by appending #s to the end). Do you want to continue?",
                        QMessageBox.Ok | QMessageBox.Cancel)
            if choice == QMessageBox.Cancel:
                return # do nothing


        # build up undo command 
        redo = lambda: self.model.mark_column_as_label(col, overridden_study_labels)
        undo = lambda: self.model.unmark_column_as_label(col, original_study_labels)
        on_exit = lambda: self.model.emit_change_signals_for_col(col)
        mark_column_as_label_cmd = GenericUndoCommand(redo_fn=redo, undo_fn=undo,
                                                  on_redo_exit=on_exit,
                                                  on_undo_exit=on_exit,
                                                  description="Mark column '%s' as label" % variable_name)
        self.undo_stack.push(mark_column_as_label_cmd)
        self.model.set_dirty_bit()



    def unmark_column_as_label(self, col):
        ''' Unmarks column as label and makes it a CATEGORICAL variable '''

        label_column_name = self.model.label_column_name_label

        # build up undo command
        redo = lambda: self.model.unmark_column_as_label(col)
        undo = lambda: self.model.mark_column_as_label(col)
        on_exit = lambda: self.model.emit_change_signals_for_col(col)
        unmark_column_as_label_cmd = GenericUndoCommand(
                                            redo_fn=redo, undo_fn=undo,
                                            on_redo_exit=on_exit,
                                            on_undo_exit=on_exit,
                                            description="Unmark column '%s' as label" % label_column_name)
        self.undo_stack.push(unmark_column_as_label_cmd)
        self.model.set_dirty_bit()

    def make_new_variable_at_col(self, col, var_type=CATEGORICAL,var_name=None):
        if var_name is None:
            name = self.model.get_default_header(col)
        else:
            name = var_name

        self.undo_stack.beginMacro(QString("Make a new variable at col %d" % col))
        resize_columns = self.tableView.resizeColumnsToContents if not self.model.big_paste_mode else do_nothing
        start_cmd = GenericUndoCommand(redo_fn=do_nothing,
                                       undo_fn=lambda: self.model.emit_change_signals_for_col(col),
                                       on_undo_exit=resize_columns)
        self.undo_stack.push(start_cmd)

        make_new_variable_cmd = ee_model.MakeNewVariableCommand(
                        model=self.model, var_name=name, col=col,
                        var_type=var_type)
        self.undo_stack.push(make_new_variable_cmd)

        end_cmd = GenericUndoCommand(undo_fn=do_nothing,
                                     redo_fn=lambda: self.model.emit_change_signals_for_col(col),
                                     on_redo_exit=resize_columns)
        self.undo_stack.push(end_cmd)
        self.undo_stack.endMacro()


    def rename_column(self, col):
        is_label_column = col == self.model.label_column

        if is_label_column:
            initial_name = self.model.label_column_name_label
        else: #variable column
            var = self.model.get_variable_assigned_to_column(col)
            initial_name = var.get_label()

        rename_column_dlg = useful_dialogs.InputForm(message="Please enter a new %s name" % 'column' if is_label_column else 'variable',
                                                     initial_text=initial_name,
                                                     parent=self)

        # Open dialog to rename column
        if not rename_column_dlg.exec_():
            return False # cancelled out

        # Dialog exited by hitting 'ok'
        proposed_name = str(rename_column_dlg.get_text())

        # Verify name is ok
        if initial_name == proposed_name:
            return False
        current_var_names = [x.get_label() for x in self.model.get_variables()]
        if proposed_name in current_var_names:
            QMessageBox.warning(self,"Bad name", "That variable name is already present in the dataset, duplicates not allowed.")
            return False
       
        # check for disallowed chars that will cause problems on the R side
        disallowed_chars_with_quotes = ["'%s'" % char for char in VARIABLE_LABEL_DISALLOWED_CHARS]
        for char in VARIABLE_LABEL_DISALLOWED_CHARS:
            if char in proposed_name:
                msg = "The following characters are not allowed in column labels: %s" % ", ".join(disallowed_chars_with_quotes)
                QMessageBox.warning(self,"Forbidden characters", msg)
                return False
        
        # Warn about character issue #76 with variable names in R
        special_chars = [" ","-"]
        special_char_in_proposed_name = False
        for char in special_chars:
            if char in proposed_name:
                special_char_in_proposed_name = True
        if special_char_in_proposed_name:
            QMessageBox.warning(self,"Character Issue","Due to general R-craziness, the characters %s will be changed to '.' on the R side (and in ouput) -- just letting you know." % ", ".join(special_chars))


        # We will proceed with the renaming
        if is_label_column:
            redo = partial(self.model.change_label_column_name, proposed_name)
            undo = partial(self.model.change_label_column_name, initial_name)
            description = "Renamed label column '%s' to '%s'" % (initial_name, proposed_name)
        else:
            redo = partial(self.model.change_variable_name, var, new_name=proposed_name)
            undo = partial(self.model.change_variable_name, var, new_name=initial_name)
            description = "Renamed variable '%s' to '%s'" % (initial_name, proposed_name)

        resize_columns = self.tableView.resizeColumnsToContents if not self.model.big_paste_mode else do_nothing
        rename_column_command = GenericUndoCommand(redo_fn=redo, undo_fn=undo,
                                                   on_redo_exit=resize_columns,
                                                   description=description)
        self.undo_stack.push(rename_column_command)
        self.model.set_dirty_bit()

    def prompt_user_about_unsaved_data(self):
        ''' Prompts user to save if data as has changed. Returns true if user
        chose to save or discard their changes to the data, False if cancelled'''

        # If nothing has changed, just leave
        if not self.model.dirty:
            return True

        choice = QMessageBox.warning(self, "Warning",
                        "Changes have been made to the data. Do you want to save your changes, discard them, or cancel?",
                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if choice == QMessageBox.Save:
            return self.save() # true of save was successful, false if cancelled

        return choice != QMessageBox.Cancel

    def what_to_do_about_unsaved_data_prompt(self):
        choices = {QMessageBox.Save:'SAVE',
                   QMessageBox.Discard:'DISCARD',
                   QMessageBox.Cancel:'CANCEL',
                   QMessageBox.Close:'CANCEL'}
        
        choice = QMessageBox.warning(self, "Warning",
                        "Changes have been made to the data. Do you want to save your changes, discard them, or cancel?",
                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        
        return choices[choice]

    def model_has_unsaved_data(self):
        return self.model.dirty







    def open(self, file_path=None):
        ''' Prompts user to open a file and then opens it (picked data model) '''
        
        # What to do if current dataset is unsaved
        if self.model_has_unsaved_data():
            what_to_do_about_unsaved_data = self.what_to_do_about_unsaved_data_prompt()
            if what_to_do_about_unsaved_data == 'SAVE':
                save_successful = self.save()
                if not save_successful:
                    QMessageBox.information(self, "Saving failed", "Saving the dataset failed for some reason")
                    return True
            elif what_to_do_about_unsaved_data == 'CANCEL':
                return True;
            elif what_to_do_about_unsaved_data == 'DISCARD':
                pass # ok to disregard current data

        # prompt the user if no file_name is provided
        if file_path is None:
            file_path = unicode(QFileDialog.getOpenFileName(
                            parent=self,
                            caption=QString("Open File"),
                            directory=get_user_documents_path(),
                            filter="OpenMEE files (*.ome)"))

        # Leave if they didn't choose anything
        if file_path == "":
            return False


        print("Loading %s ..." % str(file_path))
        try:
            with open(file_path, 'r') as f:
                state = pickle.load(f)
        except Exception as e:
            msg = "Could not open %s, the error is: %s" % (str(file_path),str(e))
            QMessageBox.critical(self, "Oops", msg)
            raise e
            return False

        # add to collection of recent files
        add_file_to_recent_files(file_path)
        self.populate_recent_datasets()

        # Rebuilds model from state,
        #  sets model,
        #  clears undo stack,
        #  unsets dirty bit
        #  disconnects old model and establishes connections for new model
        self.set_model(state)

        # Store filename for when we want to save again
        self.outpath = file_path
        self.set_window_title()

        # display status
        print("Opened %s" % self.outpath)
        self.statusbar.showMessage("Opened %s" % self.outpath)

        # reset undo view form
        self.undo_view_form.set_stack_and_model(self.undo_stack, self.model)

        # reset menu/toolbar
        self.initialize_display()
        
        # check for forbidden chars in variable names
        self.check_for_forbidden_chars_in_variable_names()

        return True
    
    def check_for_forbidden_chars_in_variable_names(self):
        variables = self.vars_with_forbidden_chars()
        labels_with_forbidden_chars = [v.get_label() for v in variables]
        if len(labels_with_forbidden_chars) > 0:
            disallowed_chars_quoted = ["'%s'" % char for char in VARIABLE_LABEL_DISALLOWED_CHARS]
            charlist = ", ".join(disallowed_chars_quoted)
            msg = "The characters: %s are not allowed in variable names. The following variables names have these disallowed characters:\n%s\n\nIf it's ok to just remove the bad characters, click 'Ok' otherwise, click cancel and remove the characters manually. This action is not undoable." % (charlist, "\n".join(labels_with_forbidden_chars)) 
            choice = QMessageBox.warning(self, "Forbidden characters in variable names", msg, buttons=QMessageBox.Ok|QMessageBox.Cancel)
            if choice == QMessageBox.Ok:
                self.remove_disallowed_chars_from_var_labels(variables)
                occupied_cols = self.model.get_occupied_columns()
                self.model.headerDataChanged.emit(Qt.Horizontal,min(occupied_cols), max(occupied_cols))
    
                
    def remove_disallowed_chars_from_var_labels(self, variables):
        for v in variables:
            label = v.get_label()
            new_label = label
            for char in VARIABLE_LABEL_DISALLOWED_CHARS:
                new_label = new_label.replace(char, "")
            v.set_label(new_label)
    
    def vars_with_forbidden_chars(self):
        ''' returns list of variables with disallowed characters in label'''
        
        all_variables = self.model.get_variables()
        # exclude effects since these arn't covariates
        variables = filter(lambda v: v.get_subtype() not in EFFECT_TYPES, all_variables)
        vars_with_disallowed_chars = []
        
        for v in variables:
            label = v.get_label()
            bad_chars_present = any([char in label for char in VARIABLE_LABEL_DISALLOWED_CHARS])
            if bad_chars_present:
                vars_with_disallowed_chars.append(v)
        return vars_with_disallowed_chars
        

    def new_dataset(self):
        # What to do if current dataset is unsaved
        if self.model_has_unsaved_data():
            what_to_do_about_unsaved_data = self.what_to_do_about_unsaved_data_prompt()
            if what_to_do_about_unsaved_data == 'SAVE':
                save_successful = self.save()
                if not save_successful:
                    QMessageBox.information(self, "Saving failed", "Saving the dataset failed for some reason")
                    return False
                elif save_successful == "CANCEL":
                    print("cancelling save")
                    return True
            elif what_to_do_about_unsaved_data == 'CANCEL':
                return True;
            elif what_to_do_about_unsaved_data == 'DISCARD':
                pass # ok to disregard current data

        self.set_model(state=None) # disconnects old model, makes new model, etc
        self.outpath = None
        self.set_window_title()
        self.initialize_display()
        self.statusbar.showMessage("Created a new dataset")

    def save(self, save_as=False):
        if self.outpath is None or save_as:
            if self.outpath is None:
                # fix for issue #71
                DEFAULT_SAVE_PATH = os.path.expanduser("~")
                out_fpath = os.path.join(DEFAULT_SAVE_PATH, DEFAULT_FILENAME)
            else:
                out_fpath = QString(self.outpath) # already have filename, maybe want to change it
            print("proposed file path: %s" % out_fpath)
            out_fpath # In an extremely bizarre turn of events, the directory path below doesn't work unles out_fpath is evaluated beforehand just making it with QString doesn't seem to be enough!
            out_fpath = unicode(QFileDialog.getSaveFileName(parent=self, caption="OpenMEE - Save File",
                                                            directory=out_fpath, filter="OpenMEE files: (.ome)"))
            if out_fpath in ["", None]:
                print("save cancelled")
                return "CANCEL"

            if out_fpath[-4:] != u".ome": # add proper file extension
                out_fpath += u".ome"
            self.outpath = out_fpath

        # pickle the 'state' of the model which contains the dataset, etc
        try:
            with open(self.outpath, 'wb') as f:
                pickle.dump(self.model.get_state(), f)
        except Exception as e:
            QMessageBox.critical(self, "Oops", "Something bad happened when trying to save: %s" % str(e))
            return False

        # add to collection of recent files
        add_file_to_recent_files(self.outpath)
        self.populate_recent_datasets()

        print("Saved %s" % self.outpath)
        self.statusbar.showMessage("Saved %s" % self.outpath)
        self.set_window_title()

        return True


    def add_choices_to_change_format_menu(self, change_format_menu, col):
        '''
        * Makes a menu that list the formats that the clicked column can be
        converted to and provides the action to do so.
        * Should not be here if the clicked column was the label column
        '''
        var = self.model.get_variable_assigned_to_column(col)

        possible_target_conversions = []
        other_variable_types = list(VARIABLE_TYPES)
        other_variable_types.remove(var.get_type())

        # Make list of targets for conversion
        #   For example: shoudn't see integer here if one of the elements in
        #                the table is real text
        for vtype in other_variable_types:
            if self.model.can_convert_variable_to_type(var, vtype):
                possible_target_conversions.append(vtype)

        # sort possible_target_conversions list alphabetically
        possible_target_conversions.sort(key=lambda x: VARIABLE_TYPE_STRING_REPS[x])

        for target_conversion in possible_target_conversions:
            variable_type_str = VARIABLE_TYPE_STRING_REPS[target_conversion]
            
            action = change_format_menu.addAction("--> %s" % variable_type_str)
            action.triggered.connect(partial(self.change_var_format, var=var, target_type=target_conversion))                                   
                                                                   
            QObject.connect(change_format_menu, SIGNAL("hovered(QAction*)"), self.status_from_action)

        if var.get_type() == CONTINUOUS and var.get_subtype() is None:
            for target in EFFECT_TYPES:
                subtype_str = VARIABLE_SUBTYPE_STRING_REPS[target]
                set_subtype_cmd = ee_model.SetVariableSubTypeCommand(model=self.model,
                                                                     variable=var,
                                                                     new_subtype=target)
                action = change_format_menu.addAction("----> %s" % subtype_str)
                action.triggered.connect(partial(self.undo_stack.push,set_subtype_cmd))


#         # profiling fun
#         pr.disable()
#         pr.create_stats()
#         pr.print_stats(sort='cumulative')
        
        return change_format_menu
    
    def change_var_format(self, var, target_type):
        var_type = var.get_type()
        
        if var_type == CONTINUOUS and target_type == COUNT:
            choice = QMessageBox.warning(
                self,
                "Loss of precision",
                "This conversion will result in a loss of precision. Are you sure?",
                buttons=QMessageBox.Yes|QMessageBox.No,
                defaultButton=QMessageBox.Yes)
            if choice != QMessageBox.Yes:
                return
            
        
        convert_to_target = ee_model.ChangeVariableFormatCommand(
                model=self.model,
                variable=var,
                target_type=target_type,
                precision=self.model.get_precision(),
                description="Change format of '%s' from '%s' to '%s'" % (var.get_label(),
                                                                         VARIABLE_TYPE_STRING_REPS[var.get_type()],
                                                                         VARIABLE_TYPE_STRING_REPS[target_type]))
        self.undo_stack.push(convert_to_target)
        

    def status_from_action(self, action):
        self.statusBar().showMessage(action.text(), 2000)

    def closeEvent(self, event):
        self.quit(event)

    def quit(self, event=None):
        # What to do if current dataset is unsaved
        if self.model_has_unsaved_data():
            what_to_do_about_unsaved_data = self.what_to_do_about_unsaved_data_prompt()
            if what_to_do_about_unsaved_data == 'SAVE':
                save_successful = self.save()
                if save_successful == "CANCEL":
                    if event:
                        event.ignore()
                    return True
                if save_successful:
                    print("*** Till we meet again, dear analyst ***")
                    if event:
                        event.accept()
                else:
                    QMessageBox.information(self, "Saving failed", "Saving the dataset failed for some reason")
                    if event:
                        event.ignore()
                    return True
                
            elif what_to_do_about_unsaved_data == 'CANCEL':
                if event:
                    event.ignore()
                return True;
            elif what_to_do_about_unsaved_data == 'DISCARD':
                if event:
                    event.ignore()
                pass # ok to disregard current data

        # save settings
        save_settings()
        
        QApplication.quit()



    def get_variable_group_column_indices(self):
        vertical_sizehint = self.tableView.verticalHeader().sizeHint()
        offset = vertical_sizehint.width()
        
        column_indices = []
        for group in self.model.variable_groups:
            variables = group.get_assigned_vars()
            columns = [self.model.get_column_assigned_to_variable(var) for var in variables]
            get_pos = lambda col: (self.tableView.columnViewportPosition(col)+self.tableView.columnViewportPosition(col+1))/2+offset
            col_indices_of_cols_in_grp = [get_pos(col) for col in columns]
            column_indices.append(col_indices_of_cols_in_grp)
        return column_indices
    
#    def paintEvent(self, event):
#        QtGui.QMainWindow.paintEvent(self, event)
#        #self.update_vargroup_graphic()

    def resizeEvent(self, event):  
        QtGui.QMainWindow.resizeEvent(self, event)
        self.update_vargroup_graphic()
        

    def update_vargroup_graphic(self):
        self.vargroup_graphic.set_column_coordinates(self.get_variable_group_column_indices())

############### COPY & PASTE ###############################

    def clear_selected_cells(self):
        print("clearing selected cell")
        
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        self.undo_stack.beginMacro(QString("clearing selected cells"))
        
        for index in selected_indexes:
            self.model.setData(index, QVariant())
            
        self.undo_stack.endMacro()

    def cut(self):
        # copy the data onto the clipboard
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        upper_left_index  = self._upper_left(selected_indexes)
        lower_right_index = self._lower_right(selected_indexes)
        if upper_left_index is None: # leave if nothing is selected
            print("No selection")
            return False
        self.copy_contents_in_range(upper_left_index, lower_right_index,
                                    to_clipboard=True)  

        # create a matrix of Nones and then 'paste' that in to the space we
        # just copied from
        nrows = lower_right_index.row() - upper_left_index.row() + 1
        ncols = lower_right_index.column() - upper_left_index.column() + 1
        nonerow = [None] * ncols
        none_matrix = []
        for _ in xrange(nrows):
            none_matrix.append(nonerow[:])

        self.paste_contents(upper_left_index, none_matrix)

    def copy(self):
        # copy/paste: these only happen if at least one cell is selected
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        upper_left_index = self._upper_left(selected_indexes)
        lower_right_index = self._lower_right(selected_indexes)
        if upper_left_index is None: # leave if nothing is selected
            print("No selection")
            return False
        self.copy_contents_in_range(upper_left_index, lower_right_index,
                                    to_clipboard=True)

    def paste(self):
        # copy/paste: these only happen if at least one cell is selected
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        upper_left_index = self._upper_left(selected_indexes)
        if upper_left_index is None:
            print("No selection")
            return False

        self.paste_from_clipboard(upper_left_index)

    def _matrix_to_str(self, m, col_delimiter="\t", row_delimiter="\n", append_new_line =False):
        ''' takes a matrix of data (i.e., a nested list) and converts to a string representation '''
        m_str = []
        for row in m:
            m_str.append(col_delimiter.join(row))
        return_str = row_delimiter.join(m_str)
        if append_new_line:
            return_str += row_delimiter
        return return_str

    def _str_to_matrix(self, text, col_delimiter="\t", row_delimiter="\n"):
        ''' transforms raw text (e.g., from the clipboard) to a structured matrix '''
        m = []
        rows = text.split(row_delimiter)
        for row in rows:
            cur_row = row.split(col_delimiter)
            m.append(cur_row)
        return m

    def _upper_left(self, indexes):
        ''' returns the upper most index object in the indexes list.'''
        if len(indexes) > 0:
            upper_left = indexes[0]
            for index in indexes[1:]:
                if index.row() < upper_left.row() or index.column() < upper_left.column():
                    upper_left = index
            return upper_left
        return None

    def _lower_right(self, indexes):
        if len(indexes) > 0:
            lower_right = indexes[0]
            for index in indexes[1:]:
                if index.row() > lower_right.row() or index.column() > lower_right.column():
                    lower_right = index
            return lower_right
        return None
    
    def _print_index(self, index):
        print "(%s, %s)" % (index.row(), index.column())
    
    def copy_contents_in_range(self, upper_left_index, lower_right_index, to_clipboard):
        '''
        copy the (textual) content of the cells in provided cell_range -- the copied contents will be
        cast to python Unicode strings and returned. If the to_clipboard flag is true, the contents will
        also be copied to the system clipboard
        '''
        print "upper left index: %s, upper right index: %s" % \
                (self._print_index(upper_left_index), self._print_index(lower_right_index))
        text_matrix = []

        # +1s are because range() is right interval exclusive
        for row in range(upper_left_index.row(), lower_right_index.row()+1):
            current_row = []
            for col in range(upper_left_index.column(), lower_right_index.column()+1):
                cur_index = self.model.createIndex(row, col)
                cur_data = self.model.data(cur_index)
                if cur_data is not None:
                    # this looks redundant, but in fact the toString method
                    # converts the string into a QString
                    cur_str = str(cur_data.toString())
                    current_row.append(cur_str)
                else:
                    current_row.append("")
            text_matrix.append(current_row)

        copied_str = self._matrix_to_str(text_matrix)

        if to_clipboard:
            clipboard = QApplication.clipboard()
            clipboard.setText(copied_str)
        print "copied str: %s" % copied_str
        return copied_str

    def source_content_large(self, source_content):
        # disable certain undo commands to make pasting faster
        nrows = len(source_content)
        ncols = len(source_content[0])
        ncells = nrows*ncols
        if ncells > MAX_CELL_PASTE_UNDOABLE:
            return True
        else:
            return False
    
    def prompt_paste_even_though_not_undoable(self):
        msgBox = QMessageBox()
        msgBox.setText("You are pasting a lot of cells, this action is not undoable.")
        msgBox.setInformativeText("Do you want to continue?")
        msgBox.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Ok)
        if msgBox.exec_() == QMessageBox.Ok:
            return True
        else:
            return

    def paste_wrapper(self, upper_left_index, source_content):

        if not self.model.big_paste_mode:
            if self.source_content_large(source_content):
                if self.prompt_paste_even_though_not_undoable():
                    self.model.big_paste_mode=True
                else:
                    self.model.big_paste_mode=False
                    return
        
        #pr=cProfile.Profile()
        #pr.enable()
        print("Big paste mode: %s" % self.model.big_paste_mode)
        self.paste_contents(upper_left_index, source_content)
        self.model.big_paste_mode = False
        #pr.disable()
        #pr.create_stats()
        #pr.print_stats(sort='cumulative')
    

    def paste_contents(self, upper_left_index, source_content,
                       progress_bar_title="Pasting"):
        '''
        paste the content in source_content into the matrix starting at the upper_left_coord
        cell. new rows will be added as needed; existing data will be overwritten
        '''
        origin_row, origin_col = upper_left_index.row(), upper_left_index.column()

        if isinstance(source_content[-1], QtCore.QStringList) and \
                             len(str(source_content[-1].join(" ")))==0:
            # then there's a blank line; Excel has a habit
            # of appending blank lines (\ns) to copied
            # text -- we get rid of it here
            source_content = source_content[:-1]

        def cancel_macro_creation_and_revert_state():
            ''' Ends creation of macro (in progress) and reverts the state of
            the model to before the macro began to be created '''
            
            print("paste_contents: Cancelling macro creation and reverting")
            self.undo_stack.endMacro()
            self.undo_stack.undo()
            self.model.blockSignals(False)
            self.tableView.resizeColumnsToContents()
                
        nrows = len(source_content)
        ncols = len(source_content[0])
        end_row, end_col = origin_row+nrows-1, origin_col+ncols-1
        
        progress_dlg = QProgressDialog(QString(progress_bar_title),QString("cancel"),0,(nrows-1)*(ncols-1),parent=self)
        progress_dlg.setWindowModality(Qt.WindowModal)
        
        def paste_loop(test=False):
            if test:
                progress_dlg.setLabelText("Testing Paste")
            else:
                progress_dlg.setLabelText("Pasting...")
            
            for src_row in xrange(len(source_content)):
                for src_col in xrange(len(source_content[0])):
                    new_progress_val = src_row*ncols + src_col
                    if new_progress_val % 100 == 0:
                        progress_dlg.setValue(new_progress_val)
                        QApplication.processEvents()
                    
                    # note that we treat all of the data pasted as
                    # one event; i.e., when undo is called, it undos the
                    # whole paste
                    print "index: {0}, {1}".format(origin_row+src_row, origin_col+src_col)
                    index = self.model.createIndex(origin_row+src_row, origin_col+src_col)
                    raw_value = source_content[src_row][src_col]
                    if raw_value in [None, QVariant(None),QVariant()]:
                        value = None
                    else:
                        unicode_value = unicode(raw_value)
                        in_ascii = unicode_value.encode('ascii','replace')
                        value = str(in_ascii)
                        
                    if test:
                        setdata_ok = self.model.test_value_for_setData(index, QVariant(value))
                        if not setdata_ok:
                            return False
                    else:
                        setdata_ok = self.model.setData(index, QVariant(value))
                        if not self.model.big_paste_mode:
                            if not setdata_ok:
                                cancel_macro_creation_and_revert_state()
                                progress_dlg.close()
                                self.tableView_selection_model.blockSignals(False)
                                self.undo_stack.blockSignals(False)
                                self.model.blockSignals(False)
                                return False
            return True
        
        self.model.blockSignals(False)
        # note: doesn't test redundant labels properly 
        # since it just tests each row by itself, not all together
        loop_will_succeed = paste_loop(test=True)
        self.model.blockSignals(True)
        if loop_will_succeed:
            # temporarily disable sorting to prevent automatic sorting of pasted data.
            # (note: this is consistent with Excel's approach.)
            self.model.blockSignals(True)
            self.undo_stack.blockSignals(True)
            self.tableView_selection_model.blockSignals(True)
            
            if not self.model.big_paste_mode:
                self.undo_stack.beginMacro(QString("Pasting"))
                self.undo_stack.push(GenericUndoCommand(redo_fn=do_nothing,
                                     undo_fn=self.tableView.resizeColumnsToContents))
                self.undo_stack.push(GenericUndoCommand(redo_fn=do_nothing,
                                                        undo_fn=lambda: self.model.emit_change_signals_from_start_to_end(origin_row, origin_col, end_row, end_col)))
                print("beginning pasting macro")
            
            #####################
            paste_loop() # pasting actually happens here 
            progress_dlg.close()
            #####################
                    
            if self.model.big_paste_mode:
                self.undo_stack.clear()
                self.tableView.resizeColumnsToContents()
                #self.model.emit_change_signals_from_start_to_end(origin_row, origin_col, end_row, end_col)
            else:
                self.undo_stack.push(GenericUndoCommand(redo_fn=self.tableView.resizeColumnsToContents,
                                                    undo_fn=do_nothing))
                self.undo_stack.push(GenericUndoCommand(undo_fn=do_nothing,
                                                        redo_fn=lambda: self.model.emit_change_signals_from_start_to_end(origin_row, origin_col, end_row, end_col)))
                self.undo_stack.endMacro()
                print("ended paste macro")
            
            self.tableView_selection_model.blockSignals(False)
            self.undo_stack.blockSignals(False)
            self.undo_view_form.re_set_stack()
            self.model.blockSignals(False)
            self.update_undo_enable_status()
            
            print("resetting model")
            self.model.reset()
            return True
        else:
            self.tableView_selection_model.blockSignals(False)
            self.undo_stack.blockSignals(False)
            self.model.blockSignals(False)
            self.undo_view_form.re_set_stack()
            self.update_undo_enable_status()
            progress_dlg.close()
            print("Paste loop will fail, leaving before damage is done")
            return False


        
    def _is_blank_row(self, r):
        return len(r) == 1 and r[0] == ""
        
    def _normalize_newlines(self, qstr_text):
        return qstr_text.replace(newlines_re, "\n")
        
    def paste_from_clipboard(self, upper_left_index):
        ''' pastes the data in the clipboard starting at the currently selected cell.'''

        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()

        # fix for issue #169 (in OMA).
        # excel for mac, insanely, appends \r instead of
        # \n for new lines (rows).
        clipboard_text = self._normalize_newlines(clipboard_text)

        new_content = self._str_to_matrix(clipboard_text)

        # fix for issue #64 (in OMA). excel likes to append a blank row
        # to copied data -- we drop that here
        if self._is_blank_row(new_content[-1]):
            new_content = new_content[:-1]

        print("new content: %s" % new_content)
        print("upper left index:")
        print(self._print_index(upper_left_index))
    
        self.paste_wrapper(upper_left_index, new_content)
        
######################## END COPY & PASTE #####################

    def import_csv(self):
        # What to do if current dataset is unsaved
        if self.model_has_unsaved_data():
            what_to_do_about_unsaved_data = self.what_to_do_about_unsaved_data_prompt()
            if what_to_do_about_unsaved_data == 'SAVE':
                save_successful = self.save()
                if not save_successful:
                    QMessageBox.information(self, "Saving failed", "Saving the dataset failed for some reason")
                    return False
                elif save_successful == "CANCEL":
                    print("cancelling save")
                    return True
            elif what_to_do_about_unsaved_data == 'CANCEL':
                return True;
            elif what_to_do_about_unsaved_data == 'DISCARD':
                self.model.set_dirty_bit(False)
                pass # ok to disregard current data
        
        form = csv_import_dlg.CSVImportDialog(self)
        if form.exec_():
            data = form.get_csv_data()
            if data is None:
                QMessageBox.warning(self, "problem", "Couldn't import csv data for some reason")
                return
            matrix = data['data']
            headers = data['headers']
            
            big_paste_mode = False
            if self.source_content_large(matrix):
                if self.prompt_paste_even_though_not_undoable():
                    big_paste_mode=True
                else:
                    big_paste_mode=False
                    return
                
            self.new_dataset()
            self.model.big_paste_mode = big_paste_mode
            start_index = self.model.createIndex(0,0)
            
            progress_dlg = QProgressDialog(QString("Making column headers"),QString("cancel"),0,len(headers)-1,parent=self)
            progress_dlg.setWindowModality(Qt.WindowModal)
            progress_dlg.raise_()
            QApplication.processEvents()
            if headers != []:
                self.tableView_selection_model.blockSignals(True)
                for col,header in enumerate(headers):
                    self.make_new_variable_at_col(col, var_type=CATEGORICAL, var_name=str(header))
                    new_progress_val = col+1
                    if new_progress_val % 15 == 0:
                        progress_dlg.setValue(new_progress_val)
                        QApplication.processEvents()
                progress_dlg.close()
                self.tableView_selection_model.blockSignals(False)
            self.paste_wrapper(start_index, matrix)
            
            # check for forbidden characters in variable names
            self.check_for_forbidden_chars_in_variable_names()
            self.undo_stack.clear()

    def export_csv(self):
        form = csv_export_dlg.CSVExportDialog(model=self.model, filepath=self.outpath, parent=self)

        form.exec_()


    def _writeout_test_parameters(self, fnc_name, make_dataset_in_r_str="", results=None, **parameter_args):
        with open('test_data.txt', 'a') as f:
            f.write("Test Data:\n")
            f.write("{\n")
            f.write(" 'test_name': \"Insert Test Name here\"\n")
            f.write(",'fnc_to_evaluate'    : '%s'\n" % fnc_name)
            f.write(",'make_dataset_r_str' : '''%s'''\n" % make_dataset_in_r_str)
            f.write(",'results'            : %s\n" % str(results))
            for param_name, value in parameter_args.iteritems():
                if type(value)==str:
                    value = "'%s'" % value
                f.write(",'%s' : %s\n" % (param_name, value))
            f.write("},\n\n")
                

            # Write the data to the disk for sure
            f.flush()
            os.fsync(f)

    def _covs_to_values_to_cols_to_values(self, covs_to_values_or_cols_to_values, reverse=False):
        ''' Convert covs_to_values to cols_to_values in order to reproducibly store data for testing
        If reverse is true the conversion happens in the opposite direction '''

        get_col = self.model.get_column_assigned_to_variable
        get_var = self.model.get_variable_assigned_to_column
        
        if covs_to_values_or_cols_to_values is None:
            return None
        
        if not reverse:
            covs_to_values = covs_to_values_or_cols_to_values
            cols_to_values = dict([(get_col(cov), value) for cov, value in covs_to_values.items()])
            return cols_to_values
        else:
            cols_to_values = covs_to_values_or_cols_to_values
            covs_to_values = dict([(get_var(col),value) for col,value in cols_to_values.items()])
            return covs_to_values
    
    def _selected_cov_to_select_col(self, cov_or_col, reverse=False):
        ''' Converts selected covariate to a column if reverse is not True,
        else convert selected col to covariate '''
        
        if cov_or_col is None:
            return None
        
        if not reverse:
            return self.model.get_column_assigned_to_variable(cov_or_col)
        else:
            return self.model.get_variable_assigned_to_column(cov_or_col)
        
    def show_R_log_dlg(self):
        print("Opening R log dialog")
        self.r_log_dlg = r_log_dlg.RLogDialog(parent=self)
        self.r_log_dlg.show()
        self.r_log_dlg.raise_()
        self.actionR_log.setEnabled(False)
        
        exR.set_R_log_dialog(self.r_log_dlg)
        self.r_log_dlg.destroyed.connect(self.close_r_log_dlg)
        
    def close_r_log_dlg(self):
        print("R log dialog has been destroyed")
        self.r_log_dlg = None
        exR.unset_R_log_dialog()
        self.actionR_log.setEnabled(True)
        
    def impute_missing_data(self):
        '''
        This method handles (basic?) data imputation via MICE.
        I think the idea here will be to replace the current
        data set with the imputed values. 

        @TODO this needs to be made undoable
        '''
        
        wizard = imputation.imputation_wizard.ImputationWizard(model=self.model, parent=self)
        
        if wizard.exec_():
            # dict mapping covs --> {study --> values}
            imputed_values = wizard.get_imputed_values()
            
            ### Put imputed values into dataset undoably
            self.undo_stack.beginMacro("Impute Missing Data")
            ################################################################
            for cov, studies_to_values in imputed_values.iteritems():
                column = self.model.get_column_assigned_to_variable(cov)
                for study,value in studies_to_values.iteritems():
                    row = self.model.get_row_assigned_to_study(study)
                    index = self.model.createIndex(row, column)
                    self.model.setData(index, QVariant(value))
            #####################################################################
            self.undo_stack.endMacro()
            
#################### not part of main_form ##########


if __name__ == '__main__':
    #pass        
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    form.raise_()
    app.exec_()