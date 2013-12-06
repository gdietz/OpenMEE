'''
Created on Dec 6, 2013

@author: George Dietz
         CEBM@Brown
'''


import sys

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_failsafe_WizardPage


class FailsafeWizardPage(QWizardPage, ui_failsafe_WizardPage.Ui_WizardPage):
    def __init__(self, parent=None):
        super(FailsafeWizardPage, self).__init__(parent)
        self.setupUi(self)
        
        self.setup_connections()
        self.target_text = str(self.target_le.text())
        self.methodbox_changed(self.method_comboBox.currentText())
    
    def setup_connections(self): 
        self.method_comboBox.currentIndexChanged[QString].connect(self.methodbox_changed)
        self.target_le.editingFinished.connect(self.verify_target)
          
    def methodbox_changed(self, method):
        #### Notes #####
        # alpha only for Rosenthal and Rosenberg methods
        # target only for Orwin method. Should be NULL otherwise (in R)
        
        if method in ['Rosenthal', 'Rosenberg']:
            self.alpha_visibility = True
        else:
            self.alpha_visibility = False
        self.alpha_lbl.setVisible(self.alpha_visibility)
        self.alphaSpinBox.setVisible(self.alpha_visibility)
            
        if method == "Orwin":
            self.target_visibility = True
        else:
            self.target_visibility = False
        self.target_lbl.setVisible(self.target_visibility)
        self.target_le.setVisible(self.target_visibility)
        
    def verify_target(self):
        # can be blank or a number
        target = str(self.target_le.text())
        
        try:
            if target != "":
                float(target)
        except ValueError: # no it isn't
            QMessageBox.warning(self, "Not a number!", '%s is not a number, at least none that I can understand' % target)
            self.target_le.blockSignals(True)
            self.target_le.setText(self.target_text) # reset old text
            self.target_le.blockSignals(False)
            return False
        
        self.target_text = str(self.target_le.text())
        return True
        
    def get_parameters(self):
        method = self.method_comboBox.currentText()
        parameters = dict(method=method,
                          digits=self.digits_SpinBox.value())
        if method in ['Rosenthal', 'Rosenberg']:
            parameters['alpha']=self.alphaSpinBox.value()
        if method == "Orwin":
            target_text = str(self.target_le.text())
            parameters['target']= target_text if target_text != "" else "NULL"
        
        return parameters
        
    def isComplete(self):
        return self.verify_target()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FailsafeWizardPage()
    form.show()
    form.raise_()
    sys.exit(app.exec_())