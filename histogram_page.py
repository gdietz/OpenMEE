'''
Created on Jan 2, 2014

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_histogram_page


class HistogramPage(QWizardPage, ui_histogram_page.Ui_WizardPage):
    def __init__(self, old_histogram_params, parent=None):
        super(HistogramPage, self).__init__(parent)
        self.setupUi(self)
        
        
        self.fill_color    = None  # white
        self.outline_color = None  # black
        self.low_color     = None  # red
        self.high_color    = None  # blue
        
        self.checkboxes = [self.xlabCheckBox, self.ylabCheckBox,
                           self.xlimCheckBox, self.ylimCheckBox,
                           self.binwidth_checkBox]
        
        self.checkboxes_to_targets = {self.xlimCheckBox: [self.xlimLowSpinBox, self.xlimHighSpinBox],
                                      self.ylimCheckBox: [self.ylimLowSpinBox, self.ylimHighSpinBox],
                                      self.xlabCheckBox: [self.xlab_le],
                                      self.ylabCheckBox: [self.ylab_le],
                                      self.binwidth_checkbox: [self.binwidth_spinBox]
                                      }
        
        self.radio_btns_to_targets = {self.no_gradient_radiobtn:self.fixed_color_layout,
                                      self.gradient_radiobtn:self.gradient_layout}
        
        # set up form based on last run
        if old_histogram_params:
            self.setup_form_from_last_run(old_histogram_params)
            
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
        if 'binwidth' in old_params:
            self.binwidth_checkBox.setCheckState(Qt.Checked)
            self._change_target_enable_state(self.binwidth_checkBox, Qt.Checked)
            self.binwidth_spinBox.setValue(old_params['binwidth'])
        #if old_params['gradient']:
        #    self.low_color_change_btn.setStyleSheet()