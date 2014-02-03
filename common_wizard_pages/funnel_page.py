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
    def __init__(self, old_funnel_params, parent=None):
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
        
        # set up form based on last run
        if old_funnel_params:
            self.setup_form_from_last_run(old_funnel_params)
        
        
        
    def setup_form_from_last_run(self, old_params):
        ''' Sets the parameters based on the last run (if it is available) '''
        if 'xlim' in old_params:
            self.xlimCheckBox.setCheckState(Qt.Checked)
            self._change_target_enable_state(self.xlimCheckBox, Qt.Checked)
            self.xlimLowSpinBox.setValue(old_params['xlim'][0])
            self.xlimHighSpinBox.setValue(old_params['xlim'][0])
        if 'ylim' in old_params:
            self.ylimCheckBox.setCheckState(Qt.Checked)
            self._change_target_enable_state(self.ylimCheckBox, Qt.Checked)
            self.ylimLowSpinBox.setValue(old_params['ylim'][0])
            self.ylimHighSpinBox.setValue(old_params['ylim'][0])
        if 'xlab' in old_params:
            self.xlabCheckBox.setCheckState(Qt.Checked)
            self._change_target_enable_state(self.xlabCheckBox, Qt.Checked)
            self.xlab_le.setText(old_params['xlab'])
        if 'ylab' in old_params:
            self.ylabCheckBox.setCheckState(Qt.Checked)
            self._change_target_enable_state(self.ylabCheckBox, Qt.Checked)
            self.ylab_le.setText(old_params['ylab'])
        if 'steps' in old_params:
            self.stepsSpinBox.setValue(old_params['steps'])
        if 'digits' in old_params:
            self.digitsSpinBox.setValue(old_params['digits'])
        if 'addtau2' in old_params:
            no_index = self.addtau2ComboBox.findText("no")
            yes_index = self.addtau2ComboBox.findText("yes")
            if -1 in [no_index, yes_index]: raise ValueError("yes and no not found in combobox")
            if old_params['add_tau'] == True: # redundant but explicit
                self.addtau2ComboBox.setCurrentIndex(yes_index) 
            else:
                self.addtau2ComboBox.setCurrentIndex(no_index)
        if 'refline' in old_params:
            self.reflineCheckBox.setCheckState(Qt.Checked)
            self._change_target_enable_state(self.reflineCheckBox, Qt.Checked)
            self.reflineSpinBox.setValue(old_params['refline'])
            
        
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
                
        self.completeChanged.emit()
    
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
            #spinbox.valueChanged[float].connect(self._verify_choice_validity)
            spinbox.valueChanged[float].connect(self.spinbox_value_changed)
    
    def spinbox_value_changed(self):
        self.completeChanged.emit()
            
    def get_parameters(self):
        # the keys given here have the same name as the parameters in metafor
        # don't change them
        # parameter read_to_send_to_R tells function to give the results such
        # that they can be used in a call to R without any further formatting
        # like adding quotes around strings or whatnot
        
        p = {}
        
        p['xlim'] = [self.xlimLowSpinBox.value(), self.xlimHighSpinBox.value()]
        p['ylim'] = [self.ylimLowSpinBox.value(), self.ylimHighSpinBox.value()]
        p['xlab'] = str(self.xlab_le.text())
        p['ylab'] = str(self.ylab_le.text())
        p['steps'] = self.stepsSpinBox.value()
        p['digits'] = self.digitsSpinBox.value()
        p['addtau2'] = True if str(self.addtau2ComboBox.currentText())=="yes" else False
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
    
    ###########################################################################
    def __str__(self):
        return ""
        
            
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FunnelPage()
    form.show()
    form.raise_()
    sys.exit(app.exec_())