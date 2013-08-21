from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import sys
import pdb
import os
from functools import partial
#from sets import Set
from collections import deque
import pickle

import ui_main_window
import calculate_effect_sizes_wizard
import ma_wizard
import ee_model
import useful_dialogs
import python_to_R
import results_window
import csv_import_dlg
import csv_export_dlg

from globals import *

# TODO: Handle setting the dirty bit more correctly in undo/redo
# right now just set it all the time during redo but don't bother unsetting it


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

class MainForm(QtGui.QMainWindow, ui_main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi(self)
        
        self.undo_stack = QUndoStack(self)
        
        self.model = ee_model.EETableModel(undo_stack=self.undo_stack)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        
        #### Display undo stack (if we want to...)
        self.undo_view_form = useful_dialogs.UndoViewForm(undo_stack=self.undo_stack, model=self.model, parent=self)
        if SHOW_UNDO_VIEW:
            self.undo_view_form.show()
            self.undo_view_form.raise_()
        
        self.statusBar().showMessage("Welcome to OpenMEE")

        self.setup_menus()
        self.setup_connections()
        self.load_user_prefs()
        self.outpath = None
        
        horizontal_header = self.tableView.horizontalHeader()
        horizontal_header.setContextMenuPolicy(Qt.CustomContextMenu)
        horizontal_header.customContextMenuRequested.connect(self.make_horizontal_header_context_menu)
        
        vertical_header = self.tableView.verticalHeader()
        vertical_header.setContextMenuPolicy(Qt.CustomContextMenu)
        vertical_header.customContextMenuRequested.connect(self.make_vertical_header_context_menu)
        
        self.set_window_title()
        python_to_R.set_conf_level_in_R(DEFAULT_CONFIDENCE_LEVEL)
        
        
    def set_window_title(self):
        if self.outpath is None:
            filename = DEFAULT_FILENAME
        else:
            filename = os.path.basename(self.outpath)
        self.setWindowTitle(' - '.join([PROGRAM_NAME, filename]))


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
        
        self.update_subgroup_ma_enable_status()
        
        

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
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.make_model_connections()

    def setup_menus(self):
        # File Menu
        QObject.connect(self.actionNew, SIGNAL("triggered()"), self.new_dataset)
        self.actionNew.setShortcut(QKeySequence.New)
        
        QObject.connect(self.actionOpen, SIGNAL("triggered()"), self.open)
        self.actionOpen.setShortcut(QKeySequence.Open)
        
        QObject.connect(self.actionSave, SIGNAL("triggered()"), self.save)
        self.actionSave.setShortcut(QKeySequence.Save)
        
        QObject.connect(self.actionSave_As, SIGNAL("triggered()"), lambda: self.save(save_as=True))
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
        
        # Analysis Menu
        QObject.connect(self.actionCalculate_Effect_Size, SIGNAL("triggered()"), self.calculate_effect_size)
        QObject.connect(self.actionStandard_Meta_Analysis, SIGNAL("triggered()"), self.meta_analysis)
        QObject.connect(self.actionCumulative, SIGNAL("triggered()"), self.cum_ma)
        QObject.connect(self.actionLeave_one_out, SIGNAL("triggered()"), self.loo_ma)
        QObject.connect(self.actionSubgroup, SIGNAL("triggered()"), self.subgroup_ma)
        
        
        
    
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
            
    def update_subgroup_ma_enable_status(self):
        print("intercepted column format changed")
        
        if self.model.get_categorical_variables() == []:
            self.actionSubgroup.setEnabled(False)
        else:
            self.actionSubgroup.setEnabled(True)
        
        
    def populate_recent_datasets(self):
        self.menuRecent_Data.clear()
        
        for fpath in self.user_prefs['recent_files'].get_list():
            action = self.menuRecent_Data.addAction("Load %s" % fpath)
            QObject.connect(action, SIGNAL("triggered()"), partial(self.open, file_path=fpath))
            
        
    def disconnect_model_connections(self):
        QObject.disconnect(self.model, SIGNAL("DataError"), self.warning_msg)
        QObject.disconnect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.change_index_after_data_edited)
        #QObject.disconnect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.tableView.resizeColumnsToContents)
        
        self.model.column_formats_changed.disconnect(self.update_subgroup_ma_enable_status)
        
    def make_model_connections(self):
        QObject.connect(self.model, SIGNAL("DataError"), self.warning_msg)
        QObject.connect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.change_index_after_data_edited)
        #QObject.connect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.tableView.resizeColumnsToContents) # was making responsiveness of tableView slow
    
        self.model.column_formats_changed.connect(self.update_subgroup_ma_enable_status)
        
    
    def calculate_effect_size(self):
        ''' Opens the calculate effect size wizard form and then calculates the new
        effect size. Places the new calculated effect + variance in the 2
        columns beyond the most recently occupied one as new continuous
        variables '''
        
        wizard = calculate_effect_sizes_wizard.CalculateEffectSizeWizard(model=self.model, parent=self)
        
        if wizard.exec_():
            data_type = wizard.selected_data_type
            metric = wizard.selected_metric
            data_location = wizard.data_location
            
            # save data locations choices for this data type in the model
            self.model.update_data_location_choices(data_type, data_location)
            
            
            data = python_to_R.gather_data(self.model, data_location)
            try:
                effect_sizes = python_to_R.effect_size(metric, data_type, data)
            except CrazyRError as e:
                QMessageBox.critical(self, QString("R error"), QString(str(e)))
                return False
            # effect sizes is just yi and vi
            self.model.add_effect_sizes_to_model(metric, effect_sizes)
            self.tableView.resizeColumnsToContents()
            
            print("Computed these effect sizes: %s" % str(effect_sizes))
            
    def meta_analysis(self, meta_f_str=None,
                            subgroup_ma = False):
        wizard = ma_wizard.MetaAnalysisWizard(model=self.model, meta_f_str=meta_f_str,
                                              enable_subgroup_options=subgroup_ma, parent=self)
        
        if wizard.exec_():
            meta_f_str = wizard.get_modified_meta_f_str()
            data_type = wizard.selected_data_type
            metric = wizard.selected_metric
            data_location = wizard.data_location
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            study_inclusion_state = wizard.studies_included_table
            subgroup_variable = wizard.get_subgroup_variable()
            
            # save data locations choices for this data type in the model
            self.model.update_data_location_choices(data_type, data_location)
            
            # save which studies were included on last meta-analysis
            self.model.update_previously_included_studies(study_inclusion_state)
            
            if subgroup_ma:
                covs_to_include = [subgroup_variable,]
            else:
                covs_to_include = []
                
                
            self.run_ma(included_studies, data_type, metric, data_location,
                        current_param_vals, chosen_method, meta_f_str, covs_to_include=covs_to_include)
            
    def cum_ma(self):
        self.meta_analysis(meta_f_str="cum.ma")
        
    def loo_ma(self):
        self.meta_analysis(meta_f_str="loo.ma")
        
    def subgroup_ma(self):
        self.meta_analysis(meta_f_str="subgroup.ma", subgroup_ma=True)
        
        
        
        
        

    def run_ma(self, included_studies, data_type, metric, data_location,
               current_param_vals, chosen_method, meta_f_str, covs_to_include=[]):
        ###
        # first, let's fire up a progress bar
        bar = MetaProgress(self)
        bar.show()
        result = None
        

        # also add the metric to the parameters
        # -- this is for scaling
        current_param_vals["measure"] = METRIC_TO_ESCALC_MEASURE[metric]
    
        
        # dispatch on type; build an R object, then run the analysis
        if OMA_CONVENTION[data_type] == "binary":
            # note that this call creates a tmp object in R called
            # tmp_obj (though you can pass in whatever var name
            # you'd like)
            python_to_R.dataset_to_simple_binary_robj(model=self.model,
                                                      included_studies=included_studies,
                                                      data_location=data_location,
                                                      covs_to_include=covs_to_include)
            if meta_f_str is None:
                result = python_to_R.run_binary_ma(chosen_method, current_param_vals)
                #pass
            else:
                result = python_to_R.run_meta_method(meta_f_str, chosen_method, current_param_vals)
                
            #_writeout_test_data(meta_f_str, self.current_method, current_param_vals, result) # FOR MAKING TESTS
        elif OMA_CONVENTION[data_type] == "continuous":
            python_to_R.dataset_to_simple_continuous_robj(model=self.model,
                                                          included_studies=included_studies,
                                                          data_location=data_location,
                                                          data_type=data_type, 
                                                          covs_to_include=covs_to_include)
            if meta_f_str is None:
                # run standard meta-analysis
                result = python_to_R.run_continuous_ma(chosen_method, current_param_vals)
            else:
                # get meta!
                result = python_to_R.run_meta_method(meta_f_str, chosen_method, current_param_vals)
            
            #_writeout_test_data(meta_f_str, self.current_method, current_param_vals, result) # FOR MAKING TESTS

        bar.hide()

        # update the user_preferences object for the selected method
        # with the values selected for this run
        current_dict = self.get_user_method_params_d()
        current_dict[chosen_method] = current_param_vals
        self.update_user_prefs("method_params", current_dict)
        self.analysis(result)
        
    def analysis(self, results):
        if results is None:
            return # analysis failed
        else: # analysis succeeded
            form = results_window.ResultsWindow(results, parent=self)
            form.show()
        
    
    def change_index_after_data_edited(self, index_top_left, index_bottom_right):
        row, col = index_top_left.row(), index_top_left.column()
        row += 1
        if row < self.model.rowCount():
            self.tableView.setFocus()
            new_index = self.model.createIndex(row,col)
            self.tableView.setCurrentIndex(new_index)
        
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
                        mark_as_label_action = context_menu.addAction("Mark as label column")
                        QAction.connect(mark_as_label_action, SIGNAL("triggered()"),
                                        partial(self.mark_column_as_label, column_clicked))
            
            else:     #  column is label column
                # Unmark column as label
                unmark_as_label_action = context_menu.addAction("Unmark as label column")
                QAction.connect(unmark_as_label_action, SIGNAL("triggered()"),
                                partial(self.unmark_column_as_label, column_clicked))
            
            # rename label column
            rename_column_action = context_menu.addAction("Rename %s" % ('variable' if is_variable_column else 'label column')) 
            QAction.connect(rename_column_action, SIGNAL("triggered()"), lambda: self.rename_column(column_clicked))
            
            # delete column
            delete_column_action = context_menu.addAction("Remove %s" % ('variable' if is_variable_column else 'label column'))
            QAction.connect(delete_column_action, SIGNAL("triggered()"), lambda: self.model.removeColumn(column_clicked))
            
            # insert column
            insert_column_action = context_menu.addAction("Insert column")
            QAction.connect(insert_column_action, SIGNAL("triggered()"), lambda: self.model.insertColumn(column_clicked))
            
            
        else: # column is not a label column or variable column
        
            # Make new variable
            make_new_categorical_variable_action = context_menu.addAction("Make new categorical variable")
            QObject.connect(make_new_categorical_variable_action, SIGNAL("triggered()"), partial(self.make_new_variable_at_col, col=column_clicked,var_type=CATEGORICAL))
        
        context_menu.popup(QCursor.pos())
        
    def mark_column_as_label(self, col):
        ''' Should only occur for columns of CATEGORICAL type and only for a
        column which is not already the label column
        (the check happens elsewhere) '''
        
        variable_name = self.model.get_variable_assigned_to_column(col).get_label()
         
        # build up undo command 
        redo = lambda: self.model.mark_column_as_label(col)
        undo = lambda: self.model.unmark_column_as_label(col)
        on_entry = lambda: self.model.beginResetModel()
        on_exit = lambda: self.model.endResetModel()
        mark_column_as_label_cmd = GenericUndoCommand(redo_fn=redo, undo_fn=undo,
                                                  on_redo_entry=on_entry, on_redo_exit=on_exit,
                                                  on_undo_entry=on_entry, on_undo_exit=on_exit,
                                                  description="Mark column '%s' as label" % variable_name)
        self.undo_stack.push(mark_column_as_label_cmd)
        self.model._set_dirty_bit()
        
    def unmark_column_as_label(self, col):
        ''' Unmarks column as label and makes it a CATEGORICAL variable '''
        
        label_column_name = self.model.label_column_name_label
        
        # build up undo command
        redo = lambda: self.model.unmark_column_as_label(col)
        undo = lambda: self.model.mark_column_as_label(col)
        on_entry = lambda: self.model.beginResetModel()
        on_exit = lambda: self.model.endResetModel()
        unmark_column_as_label_cmd = GenericUndoCommand(
                                            redo_fn=redo, undo_fn=undo,
                                            on_redo_entry=on_entry, on_redo_exit=on_exit,
                                            on_undo_entry=on_entry, on_undo_exit=on_exit,
                                            description="Unmark column '%s' as label" % label_column_name)
        self.undo_stack.push(unmark_column_as_label_cmd)
        self.model._set_dirty_bit()
        
    def make_new_variable_at_col(self, col, var_type=CATEGORICAL,var_name=None):
        if var_name is None:
            name = self.model.get_default_header(col)
        else:
            name = var_name
        
        self.undo_stack.beginMacro(QString("Make a new variable at col %d" % col))
        
        start_cmd = GenericUndoCommand(redo_fn=self.model.beginResetModel,
                                       undo_fn=self.model.endResetModel,
                                       on_undo_exit=self.tableView.resizeColumnsToContents)
        self.undo_stack.push(start_cmd)
        
        make_new_variable_cmd = ee_model.MakeNewVariableCommand(
                        model=self.model, var_name=name, col=col,
                        var_type=var_type)
        self.undo_stack.push(make_new_variable_cmd)
        
        end_cmd = GenericUndoCommand(undo_fn=self.model.beginResetModel,
                                     redo_fn=self.model.endResetModel,
                                     on_redo_exit=self.tableView.resizeColumnsToContents)
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
        
        if initial_name == proposed_name:
            return False
        
        # We will proceed with the renaming
        if is_label_column:
            redo = partial(self.model.change_label_column_name, proposed_name)
            undo = partial(self.model.change_label_column_name, initial_name)
            description = "Renamed label column '%s' to '%s'" % (initial_name, proposed_name)
            rename_column_command = GenericUndoCommand(redo_fn=redo, undo_fn=undo, description="Renamed label column '%s' to '%s'" % (initial_name, proposed_name))
        else:
            redo = partial(self.model.change_variable_name, var, new_name=proposed_name)
            undo = partial(self.model.change_variable_name, var, new_name=initial_name)
            description = "Renamed variable '%s' to '%s'" % (initial_name, proposed_name)
        
        
        rename_column_command = GenericUndoCommand(redo_fn=redo, undo_fn=undo,
                                                   on_redo_exit=self.tableView.resizeColumnsToContents,
                                                   description=description)
        self.undo_stack.push(rename_column_command)
        self.model._set_dirty_bit()
        
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
        

    def open(self, file_path=None):
        ''' Prompts user to open a file and then opens it (picked data model) '''
        
        # If user pressed cancel do nothing
        if not self.prompt_user_about_unsaved_data():
            return False
        
        # prompt the user if no file_name is provided
        if file_path is None:
            file_path = unicode(QFileDialog.getOpenFileName(parent=self, caption=QString("Open File"), filter="OpenMEE files (*.ome)"))
        
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
            return False

        # add to collection of recent files
        self.user_prefs['recent_files'].add_file(file_path)
        self._save_user_prefs()
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
        
        return True
    
    def new_dataset(self):
        self.prompt_user_about_unsaved_data()
        
        self.undo_stack.clear()
        self.model = ee_model.EETableModel(undo_stack=self.undo_stack)
        self.model.dirty = False
        self.outpath = None
        self.set_window_title()
        self.tableView.setModel(self.model)
        
        self.statusbar.showMessage("Created a new dataset")
        
    def save(self, save_as=False):
        if self.outpath is None or save_as:
            if self.outpath is None:
                out_fpath = os.path.join(BASE_PATH, DEFAULT_FILENAME)
            else:
                out_fpath = self.outpath # already have filename, maybe want to change it
            print("proposed file path: %s" % out_fpath)
            out_fpath = unicode(QFileDialog.getSaveFileName(self, "OpenMEE - Save File",
                                                         out_fpath, "OpenMEE files (.ome)"))
            if out_fpath in ["", None]:
                return False
            
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
        self.user_prefs['recent_files'].add_file(self.outpath)
        self._save_user_prefs()
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
            
            # Construct undo/redo command
            # TODO: warn user about permanent loss of precision upon converting a double to an int
            #convert_to_target = partial(self.model.change_variable_type, var_name, target_conversion, self.model.get_precision())
            convert_to_target = ee_model.ChangeVariableFormatCommand(
                                    model=self.model,
                                    variable=var,
                                    target_type=target_conversion,
                                    precision=self.model.get_precision(),
                                    description="Change format of '%s' from '%s' to '%s'" % (var.get_label(),
                                                                                             VARIABLE_TYPE_STRING_REPS[var.get_type()],
                                                                                             VARIABLE_TYPE_STRING_REPS[target_conversion]))
            
            action = change_format_menu.addAction("--> %s" % variable_type_str)
            QObject.connect(action, SIGNAL("triggered()"), partial(self.undo_stack.push, convert_to_target))
            QObject.connect(change_format_menu, SIGNAL("hovered(QAction*)"), self.status_from_action)

        return change_format_menu
    
    def status_from_action(self, action):
        self.statusBar().showMessage(action.text(), 2000)
        
    def closeEvent(self, event):
        ok_to_close = self.prompt_user_about_unsaved_data()
        if ok_to_close:
            print("*** Till we meet again, dear analyst ***")
            event.accept()
        else: # user cancelled
            event.ignore()
        
    def quit(self):
        ok_to_close = self.prompt_user_about_unsaved_data()
        if ok_to_close:
            print("*** Till we meet again, dear analyst ***")
            QApplication.quit()
        else:
            pass # do nothing, user cancelled
    
       

### HANDLE USER PREFERENCES
    def update_user_prefs(self, field, value):
        self.user_prefs[field] = value
        self._save_user_prefs()
            
    def get_user_method_params_d(self):
        return self.user_prefs["method_params"]

    def _save_user_prefs(self):
        try:
            fout = open(PREFS_PATH, 'wb')
            pickle.dump(self.user_prefs, fout)
            fout.close()
        except:
            print "failed to write preferences data!"
        
    def _default_user_prefs(self):       
        return {"splash":True,
                "digits":3,
                'recent_files': RecentFilesManager(),
                "method_params":{},
                }

    def load_user_prefs(self):
        '''
        Attempts to read a local dictionary of preferences
        ('user_prefs.dict'). If not such file exists, this file
        is created with defaults.
        '''
        
        self.user_prefs = {}
        if os.path.exists(PREFS_PATH):
            try:
                with open(PREFS_PATH, 'rb') as f:
                    self.user_prefs = pickle.load(f)
            except:
                print "preferences dictionary is corrupt! using defaults"
                self.user_prefs = self._default_user_prefs()
        else:
            self.user_prefs = self._default_user_prefs()

        # for backwards-compatibility
        if not "method_params" in self.user_prefs:
            self.user_prefs["method_params"] = {}

        self._save_user_prefs()
        print "loaded user preferences: %s" % self.user_prefs
        
        self.populate_recent_datasets()
        
################ END HANDLE USER PREFS ######################

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
        nonerow = [None]*ncols
        none_matrix = []
        for _ in range(nrows):
            none_matrix.append(nonerow[:])

        self.paste_contents(upper_left_index, none_matrix)

    def copy(self):
        # copy/paste: these only happen if at least one cell is selected
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        upper_left_index  = self._upper_left(selected_indexes)
        lower_right_index = self._lower_right(selected_indexes)
        if upper_left_index is None: # leave if nothing is selected
            print("No selection")
            return False
        self.copy_contents_in_range(upper_left_index, lower_right_index,
                                    to_clipboard=True)   
                                                                                    
    def paste(self):
        # copy/paste: these only happen if at least one cell is selected
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        upper_left_index  = self._upper_left(selected_indexes)
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
        rows  = text.split(row_delimiter)
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



    def paste_contents(self, upper_left_index, source_content, progress_bar_title="Pasting", progress_bar_label=""):
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
            
            #print("Cancelling macro creation and reverting")
            self.undo_stack.endMacro()
            self.undo_stack.undo()
            self.model.blockSignals(False)
            
            self.tableView.resizeColumnsToContents()
            



        # temporarily disable sorting to prevent automatic sorting of pasted data.
        # (note: this is consistent with Excel's approach.)
        self.model.blockSignals(True)
        self.undo_stack.beginMacro(QString("Pasting"))
        self.undo_stack.push(GenericUndoCommand(redo_fn=do_nothing,
                                                undo_fn=self.tableView.resizeColumnsToContents))
        
        nrows = len(source_content)
        ncols = len(source_content[0])
        progress_dlg = QProgressDialog(QString(progress_bar_title),QString("cancel"),0,(nrows-1)*(ncols-1),parent=self)
        progress_dlg.setWindowModality(Qt.WindowModal)
        for src_row in range(len(source_content)):
            for src_col in range(len(source_content[0])):
                progress_dlg.setValue(src_row*ncols + src_col)
                QApplication.processEvents()
                try:
                    # note that we treat all of the data pasted as
                    # one event; i.e., when undo is called, it undos the
                    # whole paste
                    index = self.model.createIndex(origin_row+src_row, origin_col+src_col)
                    setdata_ok = self.model.setData(index, QVariant(source_content[src_row][src_col]))
                    if not setdata_ok:
                        cancel_macro_creation_and_revert_state()
                except Exception, e:
                    progress_dlg.setValue(progress_dlg.maximum())
                    print "whoops, exception while pasting: %s" % e
        progress_dlg.setValue(progress_dlg.maximum())               
                    
                    
        self.undo_stack.push(GenericUndoCommand(redo_fn=self.tableView.resizeColumnsToContents,
                                                undo_fn=do_nothing))
        self.undo_stack.endMacro()

        self.model.blockSignals(False)
        self.model.reset()
        
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
        
        self.paste_contents(upper_left_index, new_content)
        
######################## END COPY & PASTE #####################

    def import_csv(self):
        form = csv_import_dlg.CSVImportDialog(self)
        
        if form.exec_():
            data = form.get_csv_data()
            if data is None:
                QMessageBox.warning(self, "problem", "Coudln't import csv data for some reason")
                return
            matrix = data['data']
            headers = data['headers']
            
            self.new_dataset()
            
            start_index = self.model.createIndex(0,0)
            
            if headers != []:
                for col,header in enumerate(headers):
                    self.make_new_variable_at_col(col, var_type=CATEGORICAL, var_name=str(header))
            self.paste_contents(start_index, matrix)
            
            self.undo_stack.clear()
                
    def export_csv(self):
        form = csv_export_dlg.CSVExportDialog(model=self.model, filepath=self.outpath, parent=self)
        
        form.exec_()
    

# simple progress bar
import ui_running
class MetaProgress(QDialog, ui_running.Ui_running):
    
    def __init__(self, parent=None):
        super(MetaProgress, self).__init__(parent)
        self.setupUi(self)




        
if __name__ == '__main__':
    #pass        
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    
    app.exec_()