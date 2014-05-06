##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

import copy
from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_preferences
from ome_globals import *

class PreferencesDialog(QDialog, ui_preferences.Ui_Dialog):
    def __init__(self,
                 parent=None):
        super(PreferencesDialog, self).__init__(parent)
        self.setupUi(self)

        self.initializeDialog()
        # Connect buttons to color pickers
        buttons = [self.label_bg, self.label_fg,
                   self.cont_bg, self.cont_fg,
                   self.cat_bg, self.cat_fg,
                   self.count_bg, self.count_fg,
                   self.calc_bg, self.calc_fg,
                   self.default_bg]

        for btn in buttons:
            btn.clicked.connect(partial(self.get_new_color,btn))
        self.header_font_btn.clicked.connect(partial(self.set_font, which="header"))
        self.data_font_btn.clicked.connect(partial(self.set_font, which="data"))
        self.reset_pushButton.clicked.connect(self._reset_everything)
        self.reg_coeff_checkBox.stateChanged.connect(self.enable_exclude_intercept_chkbox)
    
    def enable_exclude_intercept_chkbox(self):
        should_be_enabled = self.reg_coeff_checkBox.isChecked()
        self.exclude_intercept_checkBox.setEnabled(should_be_enabled)
        
    def initializeDialog(self):
        self.initialize_color_scheme_from_settings()
        self.color_buttons()
        self.digits_spinBox.setValue(get_setting('digits'))
        self.additional_values_checkBox.setChecked(get_setting('show_additional_values'))
        self.analysis_selections_checkBox.setChecked(get_setting('show_analysis_selections'))
        self.reg_coeff_checkBox.setChecked(get_setting('reg_coeff_forest_plot'))
        self.exclude_intercept_checkBox.setChecked(get_setting("exclude_intercept_coeff_fp"))
        
        self.header_font, self.data_font = None, None
        if get_setting('model_header_font_str'):
            font = QFont()
            font.fromString(get_setting('model_header_font_str'))
            self.set_font(which="header", font=font)
        else:
            font = QLabel().font()
            self.set_font(which="header", font=font)
        if get_setting('model_data_font_str'):
            font = QFont()
            font.fromString(get_setting('model_data_font_str'))
            self.set_font(which="data", font=font)
        else:
            font = QLabel().font()
            self.set_font(which="data", font=font)
        
    def showEvent(self, show_event):
        QDialog.showEvent(self, show_event)
        
    def _reset_everything(self):
        choice = QMessageBox.warning(self, "Reset Preferences", "Are you sure you want to reset all the user preferences?", buttons=QMessageBox.Yes|QMessageBox.Cancel)

        if choice == QMessageBox.Yes:
            print("reseting everything from the prefereces dlg")
            reset_settings()
            self.initializeDialog()
        
    def get_new_color(self, btn):
        ''' Pops up a dialog to get the new color for the btn, then sets
        the color in the color scheme '''
        
        old_color = self.get_btn_color(btn)
        color = QtGui.QColorDialog.getColor(old_color, self)
        if color.isValid():
            # set new color
            self.set_color_for_btn(btn, color)
            
    def set_font(self, which, font=None,):
        if font:
            ok=True
        else:
            print("No font given")
            
            if which == "data":
                font, ok = QFontDialog.getFont(self.data_font_preview_lbl)
            elif which == "header":
                font, ok = QFontDialog.getFont(self.header_font_preview_lbl)
            else:
                raise Exception("unrecognized font role")
            
        if ok:
            print("Font family: '%s'" % str(font.family()))
            
            if which == "data":
                self.data_font_preview_lbl.setText(font.family())
                self.data_font_preview_lbl.setFont(font)
                self.data_font = font
            elif which == "header":
                self.header_font_preview_lbl.setText(font.family())
                self.header_font_preview_lbl.setFont(font)
                self.header_font = font
            else:
                raise Exception("unrecognized font role")

            
    def get_btn_color(self, btn):
        if btn == self.label_bg:
            color = self.color_scheme["label/bg"]
        elif btn == self.label_fg:
            color = self.color_scheme["label/fg"]
        elif btn == self.cont_bg:
            color = self.color_scheme["variable/continuous/bg"]
        elif btn == self.cont_fg:
            color = self.color_scheme["variable/continuous/fg"]
        elif btn == self.cat_bg:
            color = self.color_scheme["variable/categorical/bg"]                                                      
        elif btn == self.cat_fg:
            color = self.color_scheme["variable/categorical/fg"]
        elif btn == self.count_bg:
            color = self.color_scheme["variable/count/bg"]
        elif btn == self.count_fg:
            color = self.color_scheme["variable/count/fg"]
        elif btn == self.calc_bg:
            color = self.color_scheme["var_with_subtype/default_effect/bg"]
        elif btn == self.calc_fg:
            color = self.color_scheme["var_with_subtype/default_effect/fg"]
        elif btn == self.default_bg:
            color = self.color_scheme["default_bg"]
        return color
    
    def initialize_color_scheme_from_settings(self):
        self.color_scheme = {}
        self.color_scheme["default_bg"] = get_setting("colors/default_bg")
        self.color_scheme["label/fg"] = get_setting("colors/label/fg")
        self.color_scheme["label/bg"] = get_setting("colors/label/bg")
        self.color_scheme["variable/categorical/fg"] = get_setting("colors/variable/categorical/fg")
        self.color_scheme["variable/categorical/bg"] = get_setting("colors/variable/categorical/bg")
        self.color_scheme["variable/count/fg"] = get_setting("colors/variable/count/fg")
        self.color_scheme["variable/count/bg"] = get_setting("colors/variable/count/bg")
        self.color_scheme["variable/continuous/fg"] = get_setting("colors/variable/continuous/fg")
        self.color_scheme["variable/continuous/bg"] = get_setting("colors/variable/continuous/bg")
        self.color_scheme["var_with_subtype/default_effect/fg"] = get_setting("colors/var_with_subtype/default_effect/fg")
        self.color_scheme["var_with_subtype/default_effect/bg"] = get_setting("colors/var_with_subtype/default_effect/bg")
    
    def set_color_for_btn(self, btn, color):
        if btn == self.label_bg:
            self.color_scheme["label/bg"] = color
        elif btn == self.label_fg:
            self.color_scheme["label/fg"] = color
        elif btn == self.cont_bg:
            self.color_scheme["variable/continuous/bg"] = color
        elif btn == self.cont_fg:
            self.color_scheme["variable/continuous/fg"] = color
        elif btn == self.cat_bg:
            self.color_scheme["variable/categorical/bg"] = color                                                   
        elif btn == self.cat_fg:
            self.color_scheme["variable/categorical/fg"] = color
        elif btn == self.count_bg:
            self.color_scheme["variable/count/bg"] = color
        elif btn == self.count_fg:
            self.color_scheme["variable/count/fg"] = color
        elif btn == self.calc_bg:
            self.color_scheme["var_with_subtype/default_effect/bg"] = color
        elif btn == self.calc_fg:
            self.color_scheme["var_with_subtype/default_effect/fg"] = color
        elif btn == self.default_bg:
            self.color_scheme["default_bg"] = color
        
        # Actually apply the color change
        self.color_buttons()
        
    
    def color_buttons(self):
        ''' Colors the buttons with colors from the color scheme '''
    
        # Note: probably should replace all the self.color_scheme stuff with self.get_btn_color(btn). Too lazy now
        
        self.label_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["label/bg"]))
        self.label_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["label/fg"]))
        
        self.cont_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["variable/continuous/bg"]))
        self.cont_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["variable/continuous/fg"]))
        
        self.cat_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["variable/categorical/bg"]))
        self.cat_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["variable/categorical/fg"]))
        
        self.count_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["variable/count/bg"]))
        self.count_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["variable/count/fg"]))
        
        self.calc_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["var_with_subtype/default_effect/bg"]))
        self.calc_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["var_with_subtype/default_effect/fg"]))
        
        self.default_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme["default_bg"]))
        
        print("Set colors of buttons")
        
    def _get_rgb_for_stylesheet(self, color):
        r,g,b, alpha = color.getRgb()
        rgb_string = 'rgb(%d, %d, %d)' % (r,g,b) # stylesheet syntax
        return rgb_string
    
    def get_color_scheme(self):
        return self.color_scheme
    
    def get_precision(self):
        return self.digits_spinBox.value()
    
    def get_model_header_font(self):
        return self.header_font
    
    def get_model_data_font(self):
        return self.data_font
    
    def get_show_additional_values(self):
        return self.additional_values_checkBox.isChecked()
    
    def get_show_analysis_selections(self):
        return self.analysis_selections_checkBox.isChecked()
    
    def get_make_reg_coeff_fp(self):
        return self.reg_coeff_checkBox.isChecked()
    
    def get_exclude_intercept(self):
        return self.exclude_intercept_checkBox.isChecked()

# if __name__ == '__main__':
# 
#     import sys
# 
#     app = QtGui.QApplication(sys.argv)
#     form = PreferencesDialog(color_scheme=DEFAULT_COLOR_SCHEME)
#     form.show()
#     sys.exit(app.exec_())