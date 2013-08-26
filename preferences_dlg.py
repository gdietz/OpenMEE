import copy
from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *


import ui_preferences
from globals import *
#from ee_model import EETableModel

class PreferencesDialog(QDialog, ui_preferences.Ui_Dialog):
    def __init__(self, color_scheme, parent=None):
        super(PreferencesDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.color_scheme = copy.deepcopy(color_scheme)
        
        
        self.color_buttons()
        # Connect buttons to color pickers
        
        buttons = [self.label_bg, self.label_fg,
                   self.cont_bg, self.cont_fg,
                   self.cat_bg, self.cat_fg,
                   self.count_bg, self.count_fg,
                   self.calc_bg, self.calc_fg,
                   self.default_bg]
        for btn in buttons:
            btn.clicked.connect(partial(self.get_new_color,btn))
        
    def get_new_color(self, btn):
        ''' Pops up a dialog to get the new color for the btn, then sets
        the color in the color scheme '''
        
        old_color = self.get_btn_color(btn)
        color = QtGui.QColorDialog.getColor(old_color, self)
        if color.isValid():
            # set new color
            self.set_color_for_btn(btn, color)
            
    def get_btn_color(self, btn):
        if btn == self.label_bg:
            color = self.color_scheme['label'][BACKGROUND]
        elif btn == self.label_fg:
            color = self.color_scheme['label'][FOREGROUND]
        elif btn == self.cont_bg:
            color = self.color_scheme['variable'][CONTINUOUS][BACKGROUND]
        elif btn == self.cont_fg:
            color = self.color_scheme['variable'][CONTINUOUS][FOREGROUND]
        elif btn == self.cat_bg:
            color = self.color_scheme['variable'][CATEGORICAL][BACKGROUND]                                                      
        elif btn == self.cat_fg:
            color = self.color_scheme['variable'][CATEGORICAL][FOREGROUND]
        elif btn == self.count_bg:
            color = self.color_scheme['variable'][COUNT][BACKGROUND]
        elif btn == self.count_fg:
            color = self.color_scheme['variable'][COUNT][FOREGROUND]
        elif btn == self.calc_bg:
            color = self.color_scheme['variable_subtype'][CALCULATED_RESULT][BACKGROUND]
        elif btn == self.calc_fg:
            color = self.color_scheme['variable_subtype'][CALCULATED_RESULT][FOREGROUND]
        elif btn == self.default_bg:
            color = self.color_scheme['DEFAULT_BACKGROUND_COLOR']
        return color
    
    def set_color_for_btn(self, btn, color):
        if btn == self.label_bg:
            self.color_scheme['label'][BACKGROUND] = color
        elif btn == self.label_fg:
            self.color_scheme['label'][FOREGROUND] = color
        elif btn == self.cont_bg:
            self.color_scheme['variable'][CONTINUOUS][BACKGROUND] = color
        elif btn == self.cont_fg:
            self.color_scheme['variable'][CONTINUOUS][FOREGROUND] = color
        elif btn == self.cat_bg:
            self.color_scheme['variable'][CATEGORICAL][BACKGROUND] = color                                                   
        elif btn == self.cat_fg:
            self.color_scheme['variable'][CATEGORICAL][FOREGROUND] = color
        elif btn == self.count_bg:
            self.color_scheme['variable'][COUNT][BACKGROUND] = color
        elif btn == self.count_fg:
            self.color_scheme['variable'][COUNT][FOREGROUND] = color
        elif btn == self.calc_bg:
            self.color_scheme['variable_subtype'][CALCULATED_RESULT][BACKGROUND] = color
        elif btn == self.calc_fg:
            self.color_scheme['variable_subtype'][CALCULATED_RESULT][FOREGROUND] = color
        elif btn == self.default_bg:
            self.color_scheme['DEFAULT_BACKGROUND_COLOR'] = color
        
        # Actually apply the color change
        self.color_buttons()
        
    
    def color_buttons(self):
        ''' Colors the buttons with colors from the color scheme '''
        
        # Note: probably should replace all the self.color_scheme stuff with self.get_btn_color(btn). Too lazy now
        
        self.label_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['label'][BACKGROUND]))
        self.label_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['label'][FOREGROUND]))
        
        self.cont_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][CONTINUOUS][BACKGROUND]))
        self.cont_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][CONTINUOUS][FOREGROUND]))
        
        self.cat_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][CATEGORICAL][BACKGROUND]))
        self.cat_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][CATEGORICAL][FOREGROUND]))
        
        self.count_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][COUNT][BACKGROUND]))
        self.count_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][COUNT][FOREGROUND]))
        
        self.calc_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable_subtype'][CALCULATED_RESULT][BACKGROUND]))
        self.calc_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable_subtype'][CALCULATED_RESULT][FOREGROUND]))
        
        self.default_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['DEFAULT_BACKGROUND_COLOR']))
        
        if DEBUG_MODE:
            print("Set colors of buttons")
        
    def _get_rgb_for_stylesheet(self, color):
        r,g,b, alpha = color.getRgb()
        rgb_string = 'rgb(%d, %d, %d)' % (r,g,b) # stylesheet syntax
        return rgb_string
    
    def get_color_scheme(self):
        return self.color_scheme


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    form = PreferencesDialog(color_scheme=DEFAULT_COLOR_SCHEME)
    form.show()
    sys.exit(app.exec_())