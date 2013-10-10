import os

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *
import ui_bootstrap_page


BOOTSTRAP_DEFAULT_FILENAME = "bootstrap.png"


class BootstrapPage(QWizardPage, ui_bootstrap_page.Ui_BootstrapPage):
    def __init__(self, model, mode = BOOTSTRAP_MA, parent=None):
        super(BootstrapPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.mode = mode
        self.base_path = os.getcwd()
        self.base_path = os.path.join(self.base_path, "r_tmp", BOOTSTRAP_DEFAULT_FILENAME)
        
        self.default_params = self.model.get_bootstrap_params_selection()
    
    def initializePage(self):
        if self.default_params is not None:
            if 'bootstrap.plot.path' in self.default_params:
                self.plot_path_le.setText(self.default_params['bootstrap.plot.path'])
            if 'num.bootstrap.replicates' in self.default_params:
                self.replicates_spinBox.setValue(self.default_params['num.bootstrap.replicates'])
            if 'histogram.title' in self.default_params:
                self.plot_title_le.setText(self.default_params['histogram.title'])
            if 'histogram.xlab' in self.default_params:
                self.xlab_le.setText(self.default_params['histogram.xlab'])
        else:
            self.plot_path_le.setText(self.base_path)
    
    def get_bootstrap_params(self):
        params = {'bootstrap.plot.path': str(self.plot_path_le.text()),
                'num.bootstrap.replicates': self.replicates_spinBox.value(),
                'histogram.title': str(self.plot_title_le.text()),
                'histogram.xlab': str(self.xlab_le.text())}
        params['bootstrap.type'] = BOOTSTRAP_MODES_TO_STRING[self.mode]
        
        return params