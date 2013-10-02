import os

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *
import ui_bootstrap_page


BOOTSTRAP_DEFAULT_FILENAME = "bootstrap.png"


class BootstrapPage(QWizardPage, ui_bootstrap_page.Ui_BootstrapPage):
    def __init__(self, mode = BOOTSTRAP_MA, parent=None):
        super(BootstrapPage, self).__init__(parent)
        self.setupUi(self)
        
        self.mode = mode
        self.base_path = os.getcwd()
        self.base_path = os.path.join(self.base_path, "r_tmp", BOOTSTRAP_DEFAULT_FILENAME)
    
    def initializePage(self):
        self.plot_path_le.setText(self.base_path)
    
    def get_bootstrap_params(self):
        params = {'bootstrap.plot.path': str(self.plot_path_le.text()),
                'num.bootstrap.replicates': self.replicates_spinBox.value(),
                'histogram.title': str(self.plot_title_le.text()),
                'histogram.xlab': str(self.xlab_le.text())}
        params['bootstrap.type'] = BOOTSTRAP_MODES_TO_STRING[self.mode]
        
        return params