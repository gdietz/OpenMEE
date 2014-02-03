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
    def __init__(self, parent=None, previous_parameters=None):
        super(FailsafeWizardPage, self).__init__(parent)
        self.setupUi(self)
        
        self.setup_connections()
        self.target_text = str(self.target_le.text())
        self.methodbox_changed(self.method_comboBox.currentText())
        
        self.default_parameters = previous_parameters
    
    def initializePage(self):
        ''' Set previous parameters if they exist '''
        
        if not self.default_parameters:
            return
        
        #self.set_widgets_blockstate(True)
        if 'method' in self.default_parameters:
            index = self.method_comboBox.findText(QString(self.default_parameters['method']))
            if index == -1:
                raise ValueError("'%s' not found as a method choice" % self.default_parameters['method'])
            self.method_comboBox.setCurrentIndex(index)
        if 'digits' in self.default_parameters:
            self.digits_SpinBox.setValue(self.default_parameters['digits'])
        if 'alpha' in self.default_parameters:
            self.alphaSpinBox.setValue(self.default_parameters['alpha'])
        if 'target' in self.default_parameters:
            self.target_le.setText(self.default_parameters['target'])
                        
            
        #self.set_widgets_blockstate(False)
        
    def set_widgets_blockstate(self, state):
        self.method_comboBox.blockSignals(state)
        self.alphaSpinBox.blockSignals(state)
        self.target_le.blockSignals(state)
        self.digits_SpinBox.blockSignals(state)
    
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
        # parameters:
        #   'method': 'Rosenthal', 'Rosenberg', or 'Orwin'
        #   'digits': an integer > 0
        #   'alpha' : float value
        #   'target': float value or ""
        
        method = str(self.method_comboBox.currentText())
        parameters = dict(method=method,
                          digits=self.digits_SpinBox.value())
        if method in ['Rosenthal', 'Rosenberg']:
            parameters['alpha']=self.alphaSpinBox.value()
        if method == "Orwin":
            target_text = str(self.target_le.text())
            parameters['target']= target_text if target_text != "" else "NULL"
        
        return parameters
    
#     def get_summary(self):
#         params = self.get_parameters()
#         order = ['method', 'alpha', 'target', 'digits']
#         
#         summary = "\n"
#         for key in order:
#             if key in params:
#                 summary += "  %s: %s\n" % (key, params[key])
#         return summary
        
    def isComplete(self):
        return self.verify_target()

    def __str__(self):
        summary = "Failsafe Parameters:\n"
        params = self.get_parameters()
        order = ['method', 'alpha', 'target', 'digits']
        
        lines = []
        for key in order:
            if key in params:
                lines.append("  %s: %s" % (key, params[key]))
        summary += "\n".join(lines)
        return summary
                
                
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FailsafeWizardPage()
    form.show()
    form.raise_()
    sys.exit(app.exec_())