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
        
        self.model = ee_model.EETableModel()
        self.tableView.setModel(self.model)
        
        self.statusBar().showMessage(QString("This is a test message"), 1000)

        self._setup_connections()
        
        horizontal_header = self.tableView.horizontalHeader()
        horizontal_header.setContextMenuPolicy(Qt.CustomContextMenu)
        horizontal_header.customContextMenuRequested.connect(self.make_header_context_menu)
        

    def _setup_connections(self):
        #self.connect(header, SIGNAL("sectionClicked(int)"),
        #                 self.sortTable)
        #self.connect(addShipButton, SIGNAL("clicked()"), self.addShip)
        #self.connect(removeShipButton, SIGNAL("clicked()"),
        #             self.removeShip)
        #self.connect(quitButton, SIGNAL("clicked()"), self.accept)
        pass
    
    def make_header_context_menu(self, pos):
        ''' Makes the context menu for column headers when user right-clicks '''
        
        column_clicked = self.tableView.columnAt(pos.x())
        
        if DEBUG:
            print("Right clicked column %d" % column_clicked)
        
        ''' Actions:
        change format of column
        rename column
        mark column as label
        unmark column as label (only for label columns)
        delete variable (label or variable)
        insert column '''
            
        
        
        label_column = self.model.get_label_column()
        is_variable_column = self.model.column_assigned_to_variable(column_clicked)
            
        context_menu = QMenu(self.tableView)
        
    
        if column_clicked != label_column:
            if is_variable_column:
                # Change format of column
                change_format_menu = context_menu.addMenu("Change format")
                self.add_choices_to_change_format_menu(change_format_menu, column_clicked)
                
                # Rename column
                rename_action = context_menu.addAction("Rename variable")
                QAction.connect(rename_action, SIGNAL("triggered()"), lambda: self.rename_variable(column_clicked))

        
        context_menu.popup(QCursor.pos())
    
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
        # construct set of disallowed names
        default_header_name = str(self.model.get_default_header(col))
        default_header_string = [str(x) for x in self.model.get_default_header_string()]
        disallowed_names = Set(default_header_string)
        used_variable_names = [str(x) for x in self.model.get_all_variable_names()]
        disallowed_names.update(used_variable_names)
        disallowed_names.discard(default_header_name)
        
        if proposed_name in disallowed_names:
            QMessageBox.information(self, "Cannot Rename Variable", "You cannot rename a variable to an existing column name.")
            return False
        
        if var_name == proposed_name:
            return False
        
        # We will proceed with the renaming
        self.model.change_variable_name(var_name, proposed_name)
        
    
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
            convert_to_target = partial(self.model.change_variable_type, var_name, target_conversion, self.model.get_precision())
            action = change_format_menu.addAction("--> %s" % variable_type_str)
            QObject.connect(action, SIGNAL("triggered()"), convert_to_target)
            QObject.connect(change_format_menu, SIGNAL("hovered(QAction*)"), self.status_from_action)

        return change_format_menu
    
    def status_from_action(self, action):
        self.statusBar().showMessage(action.text(), 2000)
        
        
if __name__ == '__main__':
    #pass        
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()