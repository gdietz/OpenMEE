'''
Created on Jan 2, 2014

@author: george
'''

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
                              self.ylabCheckBox: [self.ylab_le],
                              self.binwidth_checkbox: [self.binwidth_spinBox]
                              }
        
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