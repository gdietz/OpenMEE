'''
Created on Dec 6, 2013

@author: George Dietz
         CEBM@Brown
'''


import sys
from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_funnel_page


class FunnelPage(QWizardPage, ui_funnel_page.Ui_WizardPage):
    def __init__(self, parent=None):
        super(FunnelPage, self).__init__(parent)
        self.setupUi(self)
        
        self.checkboxes = [self.xlimCheckBox, self.ylimCheckBox,
                           self.xlabCheckBox, self.ylabCheckBox,
                           self.reflineCheckBox]
        # mapping checkboxes --> form elements that will be enabled depending
        # on the state of the checkbox
        self.checkboxes_to_en_targets = {self.xlimCheckBox: [self.xlimLowSpinBox, self.xlimHighSpinBox],
                                         self.ylimCheckBox: [self.ylimLowSpinBox, self.ylimHighSpinBox],
                                         self.xlabCheckBox: [self.xlab_le],
                                         self.ylabCheckBox: [self.ylab_le],
                                         self.reflineCheckBox: [self.reflineSpinBox],
                                         }
        self.setup_connections()
        
        # These have suitable default options as written in the metafor
        # documentation and should not be futzed around with willy-nilly
        self.set_checkboxes_state(Qt.Checked)
        self.set_checkboxes_state(Qt.Unchecked)
        
    def set_checkboxes_state(self, state):
        for checkbox in self.checkboxes:
            checkbox.setCheckState(state)

    def _change_target_enable_state(self, checkbox, check_state):
        if check_state == Qt.Checked:
            target_state = True
        else:
            target_state = False
        
        for target in self.checkboxes_to_en_targets[checkbox]:
                target.setEnabled(target_state)
                
        self._verify_choice_validity()
    
    def _verify_choice_validity(self):
        # xlims:
        if self.xlimLowSpinBox.isEnabled():
            if not (self.xlimLowSpinBox.value() <= self.xlimHighSpinBox.value()):
                self.status_lbl.setText("xlim lower limit must be less\nthan xlim upper limit")
                self.status_lbl.setStyleSheet("QLabel { color: red }")
                return False
        
        # ylims
        if self.ylimCheckBox.isEnabled():
            if not (self.ylimLowSpinBox.value() <= self.ylimHighSpinBox.value()):
                self.status_lbl.setText("ylim lower limit must be less\nthan ylim upper limit")
                self.status_lbl.setStyleSheet("QLabel { color: red }")
                return False
        
        self.status_lbl.setText("a-OK")
        self.status_lbl.setStyleSheet("QLabel { color: green }")
        return True
    
    def isComplete(self):
        return self._verify_choice_validity()
        

    def setup_connections(self):
        # enable/disable targets
        for checkbox in self.checkboxes:
            checkbox.stateChanged.connect(partial(self._change_target_enable_state, checkbox))
            
        # verify state when targets change
        for spinbox in [self.xlimLowSpinBox, self.xlimHighSpinBox,
                        self.ylimLowSpinBox, self.ylimHighSpinBox]:
            spinbox.valueChanged[float].connect(self._verify_choice_validity)
            
    def get_parameters(self, ready_to_send_to_R=True):
        # the keys given here have the same name as the parameters in metafor
        # don't change them
        # parameter read_to_send_to_R tells function to give the results such
        # that they can be used in a call to R without any further formatting
        # like adding quotes around strings or whatnot
        
        p = {}
        
        if ready_to_send_to_R:
            p['xlim'] = "c(%f,%f)" % (self.xlimLowSpinBox.value(), self.xlimHighSpinBox.value())
            p['ylim'] = "c(%f,%f)" % (self.ylimLowSpinBox.value(), self.ylimHighSpinBox.value())
            p['xlab'] = '"%s"' % str(self.xlab_le.text())
            p['ylab'] = '"%s"' % str(self.ylab_le.text())
            p['steps'] = '%d' % self.stepsSpinBox.value()
            p['digits'] = '%d' % self.digitsSpinBox.value()
            p['addtau2'] = "TRUE" if str(self.addtau2ComboBox.currentText())=="yes" else "FALSE"
            p['refline'] = '%f' % self.reflineSpinBox.value()
        else:
            p['xlim'] = [self.xlimLowSpinBox.value(), self.xlimHighSpinBox.value()]
            p['ylim'] = [self.ylimLowSpinBox.value(), self.ylimHighSpinBox.value()]
            p['xlab'] = str(self.xlab_le.text())
            p['ylab'] = str(self.ylab_le.text())
            p['steps'] = self.stepsSpinBox.value()
            p['digits'] = self.digitsSpinBox.value()
            p['addtau2'] = "TRUE" if str(self.addtau2ComboBox.currentText())=="yes" else "FALSE"
            p['refline'] = self.reflineSpinBox.value()
            
        
        # Remove unchecked parameters
        checkboxes_to_param = {self.xlimCheckBox: 'xlim',
                              self.ylimCheckBox: 'ylim',
                              self.xlabCheckBox: 'xlab',
                              self.ylabCheckBox: 'ylab',
                              self.reflineCheckBox: 'refline'}
        for checkbox,key in checkboxes_to_param.items():
            if not checkbox.isChecked():
                p.pop(key)
            
        print("Funnel params: %s" % p)
        return p
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FunnelPage()
    form.show()
    form.raise_()
    sys.exit(app.exec_())