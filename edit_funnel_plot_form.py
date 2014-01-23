'''
Created on Dec 12, 2013

@author: george
'''

import sys

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from common_wizard_pages.funnel_page import FunnelPage

class EditFunnelPlotForm(QDialog):
    def __init__(self, funnel_params, parent=None):
        super(EditFunnelPlotForm, self).__init__(parent)
        
        self.funnelpage = FunnelPage(old_funnel_params=funnel_params)
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        
        
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        
        self.ok_button= self.buttonbox.button(QDialogButtonBox.Ok)
        self.funnelpage.completeChanged.connect(self.setenable_OK)
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.funnelpage)
        vlayout.addWidget(self.buttonbox)
        self.setLayout(vlayout)
        self.adjustSize()
        
    def setenable_OK(self):
        if self.funnelpage.isComplete():
            self.ok_button.setEnabled(True)
        else:
            self.ok_button.setEnabled(False)
            
    def get_params(self):
        return self.funnelpage.get_parameters()
        
        
        
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = EditFunnelPlotForm()
    form.show()
    form.raise_()
    sys.exit(app.exec_())