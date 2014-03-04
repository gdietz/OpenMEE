'''
Created on Feb 26, 2014

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_phylo_model_design_page
from ome_globals import *

model_type_short_to_long_names = {"BM": "Brownian Motion Model",
                                  "OU": "Ornstein-Uhlenbeck"
                                  }

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
    
    ##########
    
    def __str__(self):
        model_type = self.get_phylo_model_type()
        phylo_model_type_str = "Phylogenetic Model Type: %s" % model_type_short_to_long_names[model_type]
        param_val = self.get_lambda() if model_type == "BM" else self.get_alpha()
        parameter_str = "Pagel's lambda" if model_type == "BM" else "Martins and Hansen's alpha" + "%s" % param_val
        polytomies_resolution_str = " ".join(["Polytomies","will" if self.get_randomly_resolve_polytomies() else "will not","be resolved randomly."])
        
        return "\n".join([phylo_model_type_str, parameter_str, polytomies_resolution_str])