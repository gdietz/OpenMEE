'''
Created on Jan 10, 2014

@author: George
'''


from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from tree_page import TreePage

# Histogram wizard ids
[Page_TreePage,] = range(1)


class HistogramWizard(QtGui.QWizard):
    def __init__(self, model, old_histogram_params={}, prev_hist_var=None, parent=None):
        super(HistogramWizard, self).__init__(parent)
        
        self.model=model
        self.setWindowTitle("Histogram Wizard")
        
        self.data_select_page = HistogramDataSelectPage(model=model, prev_hist_var=prev_hist_var)
        self.histogram_page = HistogramPage(old_histogram_params=old_histogram_params)
        
        self.setPage(Page_HistogramDataSelectPage, self.data_select_page)
        self.setPage(Page_HistogramParams, self.histogram_page)
        
    def nextId(self):
        if self.currentId()==Page_HistogramDataSelectPage:
            return Page_HistogramParams
        elif self.currentId() == Page_HistogramParams:
            return -1
        
    def get_selected_var(self):
        return self.data_select_page.get_selected_var()
    def get_histogram_params(self):
        return self.histogram_page.get_parameters()