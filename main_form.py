from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import sys
import pdb
from functools import partial
from sets import Set

import ui_main_window
import calculate_effect_sizes_wizard
import ee_model
import useful_dialogs
import python_to_R

from globals import *

DEBUG = False

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
        horizontal_header.customContextMenuRequested.connect(self.make_horizontal_header_context_menu)
        
        vertical_header = self.tableView.verticalHeader()
        vertical_header.setContextMenuPolicy(Qt.CustomContextMenu)
        vertical_header.customContextMenuRequested.connect(self.make_vertical_header_context_menu)
        
        
        

    def setup_menus(self):
        QObject.connect(self.actionUndo, SIGNAL("triggered()"), self.undo)
        self.actionUndo.setShortcut(QKeySequence(QKeySequence.Undo))  
        
        QObject.connect(self.actionRedo, SIGNAL("triggered()"), self.redo)
        self.actionRedo.setShortcut(QKeySequence.Redo)
        
    
    def setup_connections(self):
        QObject.connect(self.model, SIGNAL("DataError"), self.warning_msg)
        QObject.connect(self.model, SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.change_index_after_data_edited)
        QObject.connect(self.actionCalculate_Effect_Size, SIGNAL("triggered()"), self.calculate_effect_size)
    
    def calculate_effect_size(self):
        ''' Opens the calculate effect size wizard form and then calculates the new
        effect size. Places the new calculated effect + variance in the 2
        columns beyond the most recently occupied one as new continuous
        variables '''
        
        wizard = calculate_effect_sizes_wizard.CalculateEffectSizeWizard(self.model)
        
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
            print("Computed these effect sizes: %s" % str(effect_sizes))
            
        
    
    

        
        
    
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
        
        if DEBUG:
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
            convert_to_target = ChangeVariableFormatCommand(
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
        # dictionary mapping studies to their original values for the given variable
        self.orignal_vals = {}
        
    def redo(self):
        self._store_original_data_values_for_variable()
        self.model.change_variable_type(self.variable, self.target_type, self.precision)
        
    def undo(self):
        self.model.change_variable_type(self.variable, self.original_var_type, self.precision)
        self._restore_orignal_data_values_for_variable()
        
    def _store_original_data_values_for_variable(self):
        for study in self.model.dataset.get_studies():
            self.orignal_vals[study] = study.get_var(self.variable)
    
    def _restore_orignal_data_values_for_variable(self):
        for study, value in self.orignal_vals.items():
            study.set_var(self.variable, value)


        
if __name__ == '__main__':
    #pass        
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    
    app.exec_()