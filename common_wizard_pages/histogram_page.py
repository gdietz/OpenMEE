'''
Created on Jan 2, 2014

@author: george
'''

import sys
from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_histogram_page


class HistogramPage(QWizardPage, ui_histogram_page.Ui_WizardPage):
    def __init__(self, old_histogram_params, parent=None):
        super(HistogramPage, self).__init__(parent)
        self.setupUi(self)
        
        self.old_histogram_params = old_histogram_params
        
        self.fill_color    = "#FFFFFF"  # white
        self.outline_color = "#000000"  # black
        self.low_color     = "#FF0000"  # red
        self.high_color    = "#0000FF"  # blue
        
        self.checkboxes = [self.xlabCheckBox, self.ylabCheckBox,
                           self.xlimCheckBox, self.ylimCheckBox,
                           self.binwidth_checkBox]
        
        self.checkboxes_to_targets = {self.xlimCheckBox: [self.xlimLowSpinBox, self.xlimHighSpinBox],
                                      self.ylimCheckBox: [self.ylimLowSpinBox, self.ylimHighSpinBox],
                                      self.xlabCheckBox: [self.xlab_le],
                                      self.ylabCheckBox: [self.ylab_le],
                                      self.binwidth_checkBox: [self.binwidth_spinBox]
                                      }
        
        self.radio_btns_to_targets = {self.no_gradient_radiobtn:self.fixed_color_layout,
                                      self.gradient_radiobtn:self.gradient_layout}
        self.color_btns = [self.low_color_change_btn, self.high_color_change_btn,
                           self.fill_color_btn, self.outline_color_btn]
        
        self.setup_connections()
        self.set_checkboxes_state(Qt.Checked)
        self.set_checkboxes_state(Qt.Unchecked)
        
    def initializePage(self):
        # set up form based on last run
        #if self.old_histogram_params:
        self.setup_form_from_last_run(self.old_histogram_params)
            
    def _get_btn_color(self, button):
            color_btns_to_color_vars = {self.fill_color_btn:self.fill_color,
                                        self.outline_color_btn:self.outline_color,
                                        self.low_color_change_btn:self.low_color,
                                        self.high_color_change_btn:self.high_color,
                                        }
            return color_btns_to_color_vars[button]
            
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
            
        self.xlabCheckBox.setCheckState(Qt.Checked)
        self._change_target_enable_state(self.xlabCheckBox, Qt.Checked)
        if 'xlab' in old_params:
            self.xlab_le.setText(old_params['xlab'])
            print("old xlabel found: %s" % old_params['xlab'])
        else:
            default_xlabel = self.wizard().get_selected_var().get_label()
            self.xlab_le.setText(default_xlabel)
            print("using default xlabel: %s" % default_xlabel)
        if 'ylab' in old_params:
            self.ylabCheckBox.setCheckState(Qt.Checked)
            self._change_target_enable_state(self.ylabCheckBox, Qt.Checked)
            self.ylab_le.setText(old_params['ylab'])
        if 'binwidth' in old_params:
            self.binwidth_checkBox.setCheckState(Qt.Checked)
            self._change_target_enable_state(self.binwidth_checkBox, Qt.Checked)
            self.binwidth_spinBox.setValue(old_params['binwidth'])
        if 'GRADIENT' in old_params:
            if old_params['GRADIENT']:
                self.low_color_change_btn.setStyleSheet("background-color: "+old_params['low']+";color: rgb(255, 255, 255);")
                self.high_color_change_btn.setStyleSheet("background-color: "+old_params['high']+";color: rgb(255, 255, 255);")
                self.low_color  = old_params['low']
                self.high_color = old_params['high']
                self.count_le.setText(old_params['name'])
                
                self.gradient_radiobtn.click()
            else:
                self.fill_color_btn.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: "+old_params['fill']+";")
                self.outline_color_btn.setStyleSheet("color: rgb(200, 200, 200);\nbackground-color: "+old_params['color']+";")
                self.fill_color = old_params['fill']
                self.outline_color = old_params['color']
                self.no_gradient_radiobtn.click()
        else:
            self.no_gradient_radiobtn.click()
    
    
    def _choose_color(self, button):
        initial_color = QColor(self._get_btn_color(button))
        color = QColorDialog.getColor(initial_color)
        color_str = color.name()
        
        if button == self.low_color_change_btn:
            self.low_color = color_str
            self.low_color_change_btn.setStyleSheet("background-color: "+self.low_color+";color: rgb(255, 255, 255);")
        elif button == self.high_color_change_btn:
            self.high_color = color_str
            self.high_color_change_btn.setStyleSheet("background-color: "+self.high_color+";color: rgb(255, 255, 255);")
        elif button == self.fill_color_btn:
            self.fill_color = color_str
            self.fill_color_btn.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: "+self.fill_color+";")
        elif button == self.outline_color_btn:
            self.outline_color = color_str
            self.outline_color_btn.setStyleSheet("color: rgb(200, 200, 200);\nbackground-color: "+self.outline_color+";")
        
    def setup_connections(self):
        # enable/disable targets
        for checkbox in self.checkboxes:
            checkbox.stateChanged.connect(partial(self._change_target_enable_state, checkbox))
            
        # verify state when targets change
        for spinbox in [self.xlimLowSpinBox, self.xlimHighSpinBox,
                        self.ylimLowSpinBox, self.ylimHighSpinBox]:
            #spinbox.valueChanged[float].connect(self._verify_choice_validity)
            spinbox.valueChanged[float].connect(self.spinbox_value_changed)
            
        for color_button in self.color_btns:
            color_button.clicked.connect(partial(self._choose_color, color_button))
            
        self.no_gradient_radiobtn.clicked.connect(self._fixed_clicked)
        self.gradient_radiobtn.clicked.connect(self._gradient_clicked)
        
        self.xlab_le.textEdited.connect(self.completeChanged.emit)
        self.ylab_le.textEdited.connect(self.completeChanged.emit)
    
    def _fixed_clicked(self):
        # hide gradient and show fixed
        self.fixed_color_widget.show()
        self.gradient_widget.hide()
        self.hist_colors_groupbox.adjustSize()
        self.adjustSize()
        self.wizard().adjustSize()
        
    def _gradient_clicked(self):
        # show gradient and hidefixed
        self.fixed_color_widget.hide()
        self.gradient_widget.show()
        self.hist_colors_groupbox.adjustSize()
        self.adjustSize()
        self.wizard().adjustSize()
            
    
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
        
    def isComplete(self):
        return self._verify_choice_validity()
    
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
    
        # make sure '"' character not in the labels
        quote_char_in_xlab = '"' in str(self.xlab_le.text())
        quote_char_in_ylab = '"' in str(self.ylab_le.text())
        if quote_char_in_xlab or quote_char_in_ylab:
            self.status_lbl.setText("'\"' character not allowed in labels")
            self.status_lbl.setStyleSheet("QLabel { color: red }")
            return False
            
        
        self.status_lbl.setText("a-OK")
        self.status_lbl.setStyleSheet("QLabel { color: green }")
        return True
    
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
        p['binwidth'] = self.binwidth_spinBox.value()
        p['GRADIENT'] = self.gradient_radiobtn.isChecked()
        if p['GRADIENT']:
            #c("name","low","high")
            p['name'] = self.count_le.text() # count legend title
            p['low']  = self.low_color # in #RRGGBBAA format
            p['high'] = self.high_color
        else: #no gradient, fixed color
            p['fill'] = self.fill_color
            p['color'] = self.outline_color  # outline color
            
        
        # Remove unchecked parameters
        checkboxes_to_param = {self.xlimCheckBox: 'xlim',
                              self.ylimCheckBox: 'ylim',
                              self.xlabCheckBox: 'xlab',
                              self.ylabCheckBox: 'ylab',
                              self.binwidth_checkBox: 'binwidth'}
        for checkbox,key in checkboxes_to_param.items():
            if not checkbox.isChecked():
                p.pop(key)
            
        print("histogram params: %s" % p)
        return p
    
    def set_checkboxes_state(self, state):
        for checkbox in self.checkboxes:
            checkbox.setCheckState(state)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = HistogramPage(old_histogram_params={})
    form.show()
    form.raise_()
    sys.exit(app.exec_())