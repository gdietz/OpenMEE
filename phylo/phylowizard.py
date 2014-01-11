'''
Created on Jan 10, 2014

@author: George
'''


from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from tree_page import TreePage

# Histogram wizard ids
[Page_TreePage,] = range(1)

class PhyloWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(PhyloWizard, self).__init__(parent)
        
        self.tree_page = TreePage()
        self.setPage(Page_TreePage, self.tree_page)

    def nextID(self):
        if self.currentId() == Page_TreePage:
            return -1
        
    def get_phylo_object(self):
        return self.tree_page.get_phylo_object()