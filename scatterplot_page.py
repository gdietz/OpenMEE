'''
Created on Jan 2, 2014

@author: george
'''

from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_scatterplot_page


class ScatterPlotPage(QWizardPage, ui_scatterplot_page.Ui_WizardPage):
    def __init__(self, old_scatterplot_params, parent=None):
        super(ScatterPlotPage, self).__init__(parent)
        self.setupUi(self)
        
        self.checkboxes = [self.xlabCheckBox, self.ylabCheckBox,
                           self.xlimCheckBox, self.ylimCheckBox]

        self.checkboxes_to_targets = {self.xlimCheckBox: [self.xlimLowSpinBox, self.xlimHighSpinBox],
                                      self.ylimCheckBox: [self.ylimLowSpinBox, self.ylimHighSpinBox],
                                      self.xlabCheckBox: [self.xlab_le],
                                      self.ylabCheckBox: [self.ylab_le]
                                      }
        
        self.setup_connections()
        self.set_checkboxes_state(Qt.Checked)
        self.set_checkboxes_state(Qt.Unchecked)
        
        # set up form based on last run
        if old_scatterplot_params:
            self.setup_form_from_last_run(old_scatterplot_params)
            
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
        
    def _change_target_enable_state(self, checkbox, check_state):
        if check_state == Qt.Checked:
            target_state = True
        else:
            target_state = False
        
        for target in self.checkboxes_to_targets[checkbox]:
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
            
        # TODO: disallow quote characters in labels
        
        self.status_lbl.setText("a-OK")
        self.status_lbl.setStyleSheet("QLabel { color: green }")
        return True
        
    def isComplete(self):
        return self._verify_choice_validity()
    
    def set_checkboxes_state(self, state):
        for checkbox in self.checkboxes:
            checkbox.setCheckState(state)
            
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
            
        
        # Remove unchecked parameters
        checkboxes_to_param = {self.xlimCheckBox: 'xlim',
                               self.ylimCheckBox: 'ylim',
                               self.xlabCheckBox: 'xlab',
                               self.ylabCheckBox: 'ylab',
                              }
        for checkbox,key in checkboxes_to_param.items():
            if not checkbox.isChecked():
                p.pop(key)
            
        print("scatterplot params: %s" % p)
        return p