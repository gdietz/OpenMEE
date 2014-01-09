# Author: George Dietz
#
# Notes: adapted from edit funnel_plot_form.py should probably combine this with that module to be
# economical

import sys

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from histogram_page import HistogramPage
from scatterplot_page import ScatterPlotPage

# TODO: add checkbox asking whether the values should be saved or not?

class EditDataExplorationPlotForm(QDialog):
    # form type is "histogram" or "scatterplot"
    def __init__(self, form_type, params, parent=None):
        super(EditDataExplorationPlotForm, self).__init__(parent)
        
        self.form_type = form_type
        
        if form_type == "histogram":
            self.page = HistogramPage(old_histogram_params=params)
        elif form_type == "scatterplot":
            self.page = ScatterPlotPage(old_scatterplot_params=params)
        else:
            raise Exception("Unrecognized page type")
        self.page.initializePage()
        ####self.funnelpage = FunnelPage(old_funnel_params=funnel_params)
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        
        
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        
        self.ok_button= self.buttonbox.button(QDialogButtonBox.Ok)
        self.page.completeChanged.connect(self.setenable_OK)
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.page)
        vlayout.addWidget(self.buttonbox)
        self.setLayout(vlayout)
        self.adjustSize()
        
    def setenable_OK(self):
        if self.page.isComplete():
            self.ok_button.setEnabled(True)
        else:
            self.ok_button.setEnabled(False)
            
    def get_params(self):
        if self.form_type in ["histogram", "scatterplot"]:
            return self.page.get_parameters()
    
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = EditDataExplorationPlotForm()
    form.show()
    form.raise_()
    sys.exit(app.exec_())