'''
Created on Jan 6, 2014

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from histogram_page import HistogramPage
from scatterplot_page import ScatterPlotPage
from histogram_dataselect_page import HistogramDataSelectPage
from scatterplot_dataselect_page import ScatterplotDataSelectPage

# Histogram wizard ids
[Page_HistogramDataSelectPage, Page_HistogramParams,] = range(2)
# scatterplot wizard ids
[Page_ScatterplotDataSelectPage, Page_ScatterplotParams,] = range(2)


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
        
        
class ScatterPlotWizard(QtGui.QWizard):
    def __init__(self, model, old_scatterplot_params={}, prev_scatterplot_data=None, parent=None):
        super(ScatterPlotWizard, self).__init__(parent)
        
        self.model=model
        self.setWindowTitle("Scatterplot Wizard")

        self.data_select_page = ScatterplotDataSelectPage(model=model, prev_scatterplot_data=prev_scatterplot_data)
        self.scatterplot_page = ScatterPlotPage(old_scatterplot_params=old_scatterplot_params)
        self.setPage(Page_ScatterplotDataSelectPage, self.data_select_page)
        self.setPage(Page_ScatterplotParams, self.scatterplot_page)
        
    def nextId(self):
        if self.currentId()==Page_ScatterplotDataSelectPage:
            return Page_ScatterplotParams
        elif self.currentId() == Page_ScatterplotParams:
            return -1
        
    def get_selected_vars(self):
        return self.data_select_page.get_selected_vars()

    def get_scatterplot_params(self):
        return self.scatterplot_page.get_parameters()