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
        
#    def load_user_prefs(self, filename=USER_PREFERENCES_FILENAME):
#        try:
#            with open(filename, 'rb') as f:
#                self.user_prefs = pickle.load(f)
#        except IOError: # file doesn't exist
#            # make default preferences
#            self.user_prefs = {'recent_files': RecentFilesManager(),}
#            
#        
#        self.populate_recent_datasets()
       
#    def save_user_prefs(self, filename=USER_PREFERENCES_FILENAME):
#        with open(filename, 'wb') as f:
#            pickle.dump(self.user_prefs, f)

    def setup_menus(self):
        # File Menu
        QObject.connect(self.actionNew    , SIGNAL("triggered()"), self.new_dataset)
        self.actionNew.setShortcut(QKeySequence.New)
        
        QObject.connect(self.actionOpen   , SIGNAL("triggered()"), self.open)
        self.actionOpen.setShortcut(QKeySequence.Open)
        
        QObject.connect(self.actionSave   , SIGNAL("triggered()"), self.save)
        self.actionSave.setShortcut(QKeySequence.Save)
        
        QObject.connect(self.actionSave_As, SIGNAL("triggered()"), lambda: self.save(save_as=True))
        self.actionSave_As.setShortcut(QKeySequence.SaveAs)
        
        # Edit Menu
        QObject.connect(self.actionUndo, SIGNAL("triggered()"), self.undo)
        self.actionUndo.setShortcut(QKeySequence(QKeySequence.Undo))  
        
        QObject.connect(self.actionRedo, SIGNAL("triggered()"), self.redo)
        self.actionRedo.setShortcut(QKeySequence.Redo)
        
        # TODO: implement these menu item actions
        self.actionCut.setShortcut(QKeySequence.Cut)
        self.actionCopy.setShortcut(QKeySequence.Copy)
        self.actionPaste.setShortcut(QKeySequence.Paste)
        
        # Analysis Menu
        QObject.connect(self.actionCalculate_Effect_Size, SIGNAL("triggered()"), self.calculate_effect_size)
        QObject.connect(self.actionStandard_Meta_Analysis, SIGNAL("triggered()"), self.meta_analysis)
        
        
        
        
        
    
    def setup_connections(self):
        self.make_model_connections()
        

        
        
        
        
        
        
    def populate_recent_datasets(self):
        self.menuRecent_Data.clear()
        
        for fpath in self.user_prefs['recent_files'].get_list():
            action = self.menuRecent_Data.addAction("Load %s" % fpath)
            QObject.connect(action, SIGNAL("triggered()"), partial(self.open, file_path=fpath))
            
        
    def disconnect_model_connections(self):
        QObject.disconnect(self.model, SIGNAL("DataError"), self.warning_msg)
        QObject.disconnect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.change_index_after_data_edited)
        QObject.disconnect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.tableView.resizeColumnsToContents)
        
    def make_model_connections(self):
        QObject.connect(self.model, SIGNAL("DataError"), self.warning_msg)
        QObject.connect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.change_index_after_data_edited)
        QObject.connect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.tableView.resizeColumnsToContents)
    
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
            
    def meta_analysis(self):
        
        
        wizard = ma_wizard.MetaAnalysisWizard(model=self.model, parent=self)
        
        if wizard.exec_():
            meta_f_str = wizard.meta_f_str
            data_type = wizard.selected_data_type
            metric = wizard.selected_metric
            data_location = wizard.data_location
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            
            self.run_ma(included_studies, data_type, metric, data_location,
                        current_param_vals, chosen_method, meta_f_str)
    

    def run_ma(self, included_studies, data_type, metric, data_location,
               current_param_vals, chosen_method, meta_f_str):
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
                                                      data_location=data_location)
            if meta_f_str is None:
                result = python_to_R.run_binary_ma(chosen_method, current_param_vals)
                #pass
            else:
                result = python_to_R.run_meta_method(meta_f_str, chosen_method, current_param_vals)
                
            #_writeout_test_data(meta_f_str, self.current_method, current_param_vals, result) # FOR MAKING TESTS
        elif OMA_CONVENTION[data_type] == "continuous":
            python_to_R.dataset_to_simple_continuous_robj(self.model)
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
    
        if not (column_clicked == label_column or is_variable_column):
            return False
        
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
        
        # We will proceed with the nenaming
        if is_label_column:
            redo = partial(self.model.change_label_column_name, proposed_name)
            undo = partial(self.model.change_label_column_name, initial_name)
            rename_column_command = GenericUndoCommand(redo_fn=redo, undo_fn=undo, description="Renamed label column '%s' to '%s'" % (initial_name, proposed_name))
        else:
            redo = partial(self.model.change_variable_name, var, new_name=proposed_name)
            undo = partial(self.model.change_variable_name, var, new_name=initial_name)
            rename_column_command = GenericUndoCommand(redo_fn=redo, undo_fn=undo, description="Renamed variable '%s' to '%s'" % (initial_name, proposed_name))
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
            self.save()
            return True
        
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
            with open(file_path, 'rb') as f:
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
        
        return True
    
    def new_dataset(self):
        self.prompt_user_about_unsaved_data()
        
        self.undo_stack.clear()
        self.model = ee_model.EETableModel(undo_stack=self.undo_stack)
        self.model.dirty = False
        self.outpath = None
        self.tableView.setModel(self.model)
        
        self.statusbar.showMessage("Created a new dataset")
        
    def save(self, save_as=False):
        if self.outpath is None or save_as:
            out_fpath = os.path.join('.', DEFAULT_FILENAME)
            out_fpath = unicode(QFileDialog.getSaveFileName(self, "OpenMEE - Save File",
                                                         out_fpath, "OpenMEE files: (.ome)"))
            if out_fpath in ["", None]:
                return False
            else:
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