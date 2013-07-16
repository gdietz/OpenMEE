from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import sys
import pdb
from functools import partial
from sets import Set

import ui_main_window
import ee_model
import useful_dialogs

from globals import *

DEBUG = False #True

class MainForm(QtGui.QMainWindow, ui_main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi(self)
        
        self.undo_stack = QUndoStack(self)
        

        
        self.model = ee_model.EETableModel(undo_stack=self.undo_stack)
        self.tableView.setModel(self.model)
        
        #### Display undo stack
        self.undo_view_form = useful_dialogs.UndoViewForm(undo_stack=self.undo_stack, model=self.model, parent=self)
        self.undo_view_form.show()
        self.undo_view_form.raise_()
        
        self.statusBar().showMessage(QString("This is a test message"), 1000)

        self.setup_menus()
        self.setup_connections()
        
        horizontal_header = self.tableView.horizontalHeader()
        horizontal_header.setContextMenuPolicy(Qt.CustomContextMenu)
        horizontal_header.customContextMenuRequested.connect(self.make_header_context_menu)
        
        
        

    def setup_menus(self):
        QObject.connect(self.actionUndo, SIGNAL("triggered()"), self.undo)
        self.actionUndo.setShortcut(QKeySequence(QKeySequence.Undo))  
        
        QObject.connect(self.actionRedo, SIGNAL("triggered()"), self.redo)
        self.actionRedo.setShortcut(QKeySequence.Redo)
        
    
    def setup_connections(self):
        QObject.connect(self.model, SIGNAL("DataError"), self.warning_msg)
        
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

#    TODO: write vertical row header context menu       
#    def make_vertical_header_context_menu(self, pos):
#        ''' makes the context menu for the row headers when user right-clicks '''
#        
#        '''Actions:
#        Insert study (row)
#        delete study (row)
#        '''
        
    
    def make_header_context_menu(self, pos):
        ''' Makes the context menu for column headers when user right-clicks '''
        
        column_clicked = self.tableView.columnAt(pos.x())
        
        if DEBUG:
            print("Right clicked column %d" % column_clicked)
        
        ''' Actions                                     |  base |  w/undoredo
        change format of column                         |  [X]  |  [X]
        rename column                                   |  [X]  |  [X]
        mark column as label (only for categorical cols)|  [X]  |  [X]
        unmark column as label (only for label columns) |  [X]  |  [X]
        delete variable (label or variable)             |  [ ]  |  [ ]
        insert column                                   |  [ ]  |  [ ]
        '''
            
        label_column = self.model.get_label_column()
        is_variable_column = self.model.column_assigned_to_variable(column_clicked)
        context_menu = QMenu(self.tableView)
    
        variable_name = self.model.get_column_name(column_clicked)
        if column_clicked != label_column:
            if is_variable_column:
                variable_type = self.model.dataset.get_variable_type(variable_name)
                
                # Change format of column
                change_format_menu = context_menu.addMenu("Change format")
                self.add_choices_to_change_format_menu(change_format_menu, column_clicked)
                
                # Rename column
                rename_action = context_menu.addAction("Rename variable")
                QAction.connect(rename_action, SIGNAL("triggered()"), lambda: self.rename_variable(column_clicked))
                
                # Mark column as label
                if variable_type == CATEGORICAL:
                    mark_as_label_action = context_menu.addAction("Mark as label column")
                    QAction.connect(mark_as_label_action, SIGNAL("triggered()"), partial(self.mark_column_as_label, variable_name, column_clicked))
        else:                                       #  column is label column
            # Unmark column as label
            unmark_as_label_action = context_menu.addAction("Unmark as label column")
            QAction.connect(unmark_as_label_action, SIGNAL("triggered()"), partial(self.unmark_column_as_label, variable_name, column_clicked))
            
        
        context_menu.popup(QCursor.pos())
    
    def mark_column_as_label(self, variable_name, col):
        ''' Should only occur for columns of CATEGORICAL type and only for a
        column which is not already the label column
        (the check happens elsewhere) '''
         
        # build up undo command 
        redo = lambda: self.model.mark_column_as_label(col)
        undo = lambda: self.model.unmark_column_as_label(col)
        on_entry = lambda: self.model.beginResetModel()
        on_exit = lambda: self.model.endResetModel()
        mark_column_as_label_cmd = GenericUndoCommand(redo_fn=redo, undo_fn=undo,
                                                  on_entry=on_entry, on_exit=on_exit,
                                                  description="Mark column '%s' as label" % variable_name)
        self.undo_stack.push(mark_column_as_label_cmd)
        
        
    def unmark_column_as_label(self, variable_name, col):
        ''' Unmarks column as label and makes it a CATEGORICAL variable '''
        
        # build up undo command
        redo = lambda: self.model.unmark_column_as_label(col)
        undo = lambda: self.model.mark_column_as_label(col)
        on_entry = lambda: self.model.beginResetModel()
        on_exit = lambda: self.model.endResetModel()
        unmark_column_as_label_cmd = GenericUndoCommand(redo_fn=redo, undo_fn=undo,
                                              on_entry=on_entry, on_exit=on_exit,
                                              description="Unmark column '%s' as label" % variable_name)
        self.undo_stack.push(unmark_column_as_label_cmd)
        
    
    def rename_variable(self, col):
        ''' Renames a variable_column. Should never be called on the label column '''
        
        var_name = self.model.get_column_name(col)
        rename_variable_dlg = useful_dialogs.InputForm(message="Please enter a new variable name",
                                                       initial_text=var_name,
                                                       parent=self)
        # Open dialog to rename variable
        if not rename_variable_dlg.exec_():
            return False # cancelled out
        
        # Dialog exited by hitting 'ok'
        proposed_name = str(rename_variable_dlg.get_text())
        
        # get set of disallowed variables names
        disallowed_names = self._get_set_of_disallowed_new_variable_names(col)
        
        if proposed_name in disallowed_names:
            QMessageBox.information(self, "Cannot Rename Variable", "You cannot rename a variable to an existing column name.")
            return False
        
        if var_name == proposed_name:
            return False
        
        # We will proceed with the renaming
        redo = partial(self.model.change_variable_name, old_name=var_name, new_name=proposed_name)
        undo = partial(self.model.change_variable_name, old_name=proposed_name, new_name=var_name)
        rename_variable_command = GenericUndoCommand(redo_fn=redo, undo_fn=undo, description="Renamed variable '%s' to '%s'" % (var_name, proposed_name))
        self.undo_stack.push(rename_variable_command)
        #self.model.change_variable_name(var_name, proposed_name)
    
    def _get_set_of_disallowed_new_variable_names(self, col):
        '''
        construct set of disallowed names:
          None of the already used header labels or default header labels
          allowed except for the default label for this particular column
        '''
        default_header_name = str(self.model.get_default_header(col))
        default_header_string = [str(x) for x in self.model.get_default_header_string()]
        disallowed_names = Set(default_header_string)
        used_variable_names = [str(x) for x in self.model.cols_2_vars.values()]
        disallowed_names.update(used_variable_names)
        disallowed_names.discard(default_header_name)
        return disallowed_names # this is a set
        
    
    def add_choices_to_change_format_menu(self, change_format_menu, col):
        '''
        * Makes a menu that list the formats that the clicked column can be
        converted to and provides the action to do so.
        * Should not be here if the clicked column was the label column
        '''
        
        var_name = self.model.get_column_name(col)
        var_type = self.model.get_variable_type(var_name)
        
        possible_target_conversions = []
        other_variable_types = list(VARIABLE_TYPES)
        other_variable_types.remove(var_type)
        
        # Make list of targets for conversion for example, shoudn't see integer
        # here if one of the elements in the table is real text
        for vtype in other_variable_types:
            if self.model.can_convert_variable_to_type(var_name, vtype):
                possible_target_conversions.append(vtype)
        
        # sort possible_target_conversions list alphabetically
        possible_target_conversions.sort(key=lambda x: VARIABLE_TYPE_STRING_REPS[x])
        
        for target_conversion in possible_target_conversions:
            variable_type_str = VARIABLE_TYPE_STRING_REPS[target_conversion]
            
            # Construct undo/redo command
            # TODO: warn user about permanent loss of precision upon converting a double to an int
            #convert_to_target = partial(self.model.change_variable_type, var_name, target_conversion, self.model.get_precision())
            convert_to_target = ChangeVariableFormatCommand(
                                    model=self.model,
                                    var_name=var_name,
                                    target_type=target_conversion,
                                    precision=self.model.get_precision(),
                                    description="Change format of '%s' from '%s' to '%s'" % (var_name,
                                                                                             VARIABLE_TYPE_STRING_REPS[var_type],
                                                                                             VARIABLE_TYPE_STRING_REPS[target_conversion]))
            
            action = change_format_menu.addAction("--> %s" % variable_type_str)
            QObject.connect(action, SIGNAL("triggered()"), partial(self.undo_stack.push, convert_to_target))
            QObject.connect(change_format_menu, SIGNAL("hovered(QAction*)"), self.status_from_action)

        return change_format_menu
    
    def status_from_action(self, action):
        self.statusBar().showMessage(action.text(), 2000)

def do_nothing():
    'A very useful function indeed'
    pass
    
    
class GenericUndoCommand(QUndoCommand):
    ''' Generic undo command if the undo/redo is REALLY simple i.e. running
        redo/undo doesn't change the state for future executions
        
        on_entry and on_exit are functions that happen before and after the undo/redo
        '''
    
    def __init__(self, redo_fn, undo_fn, on_entry=do_nothing, on_exit=do_nothing, description="GenericUndo"):
        super(GenericUndoCommand, self).__init__()
        
        self.redo_fn = redo_fn
        self.undo_fn = undo_fn
        
        self.on_entry = on_entry
        self.on_exit = on_exit
        self.setText(QString(description))
        
    def redo(self):
        self.on_entry()
        self.redo_fn()
        self.on_exit()
    
    def undo(self):
        self.on_entry()
        self.undo_fn()
        self.on_exit()


class ChangeVariableFormatCommand(QUndoCommand):
    ''' Changes the format of a variable '''
    
    def __init__(self, model, var_name, target_type, precision, description="Change variable format"):
        super(ChangeVariableFormatCommand, self).__init__()
        
        self.setText(QString(description))
        
        self.model = model
        self.var_name = var_name
        self.target_type = target_type
        self.precision = precision
        
        self.original_var_type = self.model.dataset.get_variable_type(self.var_name)
        # dictionary mapping studies to their original values for the given variable
        self.orignal_vals = {}
        
    def redo(self):
        self._store_original_data_values_for_variable()
        self.model.change_variable_type(self.var_name, self.target_type, self.precision)
        
    def undo(self):
        self.model.change_variable_type(self.var_name, self.original_var_type, self.precision)
        self._restore_orignal_data_values_for_variable()
        
    def _store_original_data_values_for_variable(self):
        for study in self.model.dataset.get_all_studies():
            self.orignal_vals[study] = study.get_var(self.var_name)
    
    def _restore_orignal_data_values_for_variable(self):
        for study, value in self.orignal_vals.items():
            study.set_var(self.var_name, value)


        
if __name__ == '__main__':
    #pass        
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()