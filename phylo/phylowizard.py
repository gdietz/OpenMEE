'''
Created on Jan 10, 2014

@author: George
'''


from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from tree_page import TreePage
from phylo_model_design_page import PhyloModelDesignPage

# Histogram wizard ids
[Page_TreePage, Page_PhyloModelDesignPage] = range(1)

class PhyloWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(PhyloWizard, self).__init__(parent)
        
        self.tree_page = TreePage()
        self.setPage(Page_TreePage, self.tree_page)
        
        self.phylo_model_design_page = PhyloModelDesignPage()
        self.setPage(Page_PhyloModelDesignPage, self.phylo_model_design_page)

    def nextID(self):
        if self.currentId() == Page_TreePage:
            return Page_PhyloModelDesignPage
        elif self.currentId() == Page_PhyloModelDesignPage:
            return -1
        
    #def get_phylo_object(self):
    #    return self.tree_page.get_phylo_object()
    
    def get_tree_and_filename(self):
        return self.tree_page.get_tree_and_filename()