'''
Created on Jan 10, 2014

@author: George
'''

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_tree_page
import python_to_R
import os.path
from ome_globals import *

FILE_VALID_MSG = "Selected file does matches selected tree format"
FILE_INVALID_MSG = "Selected file does match selected tree format"

class TreePage(QWizardPage, ui_tree_page.Ui_WizardPage):
    def __init__(self, parent=None):
        super(TreePage, self).__init__(parent)
        self.setupUi(self)
        
        self.selected_file_path = None
        self.phylo = None # the phylo object (if successfully obtained from ape)
        self.valid_format = False
        
        self.radioButtons_to_formats = {self.caic_radioButton:"caic",
                                        self.nexus_radioButton:"nexus",
                                        self.newick_radioButton:"newick",
                                        self.nh_radioButton:"nh"}
        
        # connect radiobuttons to completeChanged signal
        for radioButton in self.radioButtons_to_formats.keys():
            radioButton.clicked.connect(self.radioButton_clicked)
            
        self.select_file_PushButton.clicked.connect(self.select_file)
    
    def radioButton_clicked(self):
        print("radio button clicked")
        self.completeChanged.emit()
    
    def initializePage(self):
        self.isComplete()
        
    def select_file(self):
        self.selected_file_path = unicode(
            QFileDialog.getOpenFileName(
                parent=self, caption=QString("Select tree file")))
        
        self.filename_Label.setText(self.selected_file_path)
        self.completeChanged.emit()
        
    def isComplete(self):
        if self.selected_file_path:
            file_exists = os.path.exists(self.selected_file_path)
            if file_exists:
                selected_format = self.get_selected_format()
                if self.file_matches_format(self.selected_file_path, selected_format):
                    self.show_valid_message()
                    return True
                else:
                    self.show_invalid_message()
                    return False
            else:
                self.show_invalid_message()
                return False
        else:
            self.filename_Label.setText("none yet")
            self.hide_validity_message()
            return False
        
    def show_valid_message(self):
        self.format_valid_label.setText(FILE_VALID_MSG)
        self.format_valid_label.setStyleSheet("color: rgb(0, 170, 0);")
        
    def show_invalid_message(self):
        self.format_valid_label.setText(FILE_INVALID_MSG)
        self.format_valid_label.setStyleSheet("color: rgb(255, 0, 0);")

    def hide_validity_message(self):
        self.format_valid_label.setText("")
        
        
    def get_selected_format(self):
        for radioButton, tree_format in self.radioButtons_to_formats.items():
            if radioButton.isChecked():
                return tree_format
        raise Exception("No tree format selected")
        
    def file_matches_format(self, file_path, tree_format):
        ''' returns a phylo object if the file matches the format '''
        
        try:
            phylo = python_to_R.load_ape_file(file_path, tree_format)
        except CrazyRError:
            return None
        self.phylo = phylo # store created phylo object
        return phylo
    
    def get_phylo_object(self):
        return self.phylo
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = TreePage()
    form.show()
    form.raise_()
    sys.exit(app.exec_())