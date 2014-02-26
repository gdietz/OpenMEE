'''
Created on Feb 26, 2014

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_phylo_model_design_page
from ome_globals import *

class PhyloModelDesignPage(QWizardPage, ui_phylo_model_design_page.Ui_WizardPage):
    def __init__(self, parent=None):
        super(PhyloModelDesignPage, self).__init__(parent)
        self.setupUi(self)
        
    def initialize_page(self):
        tree_data = self.wizard().get_tree_and_filepath()
        tree = tree_data['tree']
        tree_filename = tree_data['filename']
        
        n_polytomies = self._count_polytomies_in_tree(tree)
        self.polytomies_info_label.setText("Your current tree, %s, has %d polytomies." % (tree_filename, n_polytomies))
        
    def _count_polytomies_in_tree(self, tree):
        # TODO
        raise Exception("Not implemented!")
    
    #### Interface out ######
    def get_phylo_model_type(self):
        if self.BM_radioButton.isChecked():
            return "BM"
        elif self.OU_radioButton.isChecked():
            return "OU"
        else:
            raise Exception("This is weird...")
        
    def get_lambda(self):
        return self.lambda_doubleSpinBox.value()
    def get_alpha(self):
        return self.alpha_doubleSpinBox.value()
    
    def get_randomly_resolve_polytomies(self):
        return self.randpoly_checkBox.isChecked()
    