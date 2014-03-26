'''
Created on Mar 24, 2014

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import ui_meta_analysis_parameters_page

class MetaAnalysisParametersPage(QWizardPage, ui_meta_analysis_parameters_page.Ui_WizardPage):
    def __init__(self,
                 method="REML", # random effects method
                 level=DEFAULT_CONFIDENCE_LEVEL,  # confidence level
                 digits=3,
                 knha=False, # knapp and hartung adjustment
                 parent=None): 
        super(MetaAnalysisParametersPage, self).__init__(parent)
        self.setupUi(self)

        # populate random effects combobox
        self.add_random_effect_methods_to_combo_box(default_method=method)
        
        # Set confidence level
        self.conf_level_spinbox.setValue(level)
        
        # Set digits of precision
        self.digits_spinBox.setValue(digits)
        
        # Set knapp and hartung adjustment
        self.knha_checkBox.setChecked(knha)

        # Setup connections
        self.setup_connections()
        
        # Disable knha for now since its not implemented on the R side
        self.knha_checkBox.setEnabled(False)
        self.knha_checkBox.setToolTip("disabled for now since its not implemented on the R side yet")
        
    
    def setup_connections(self):
        # radio buttons
        self.fixed_effects_radio_btn.clicked.connect(self.choose_fixed_effects)
        self.random_effects_radio_btn.clicked.connect(self.choose_random_effects)

    def choose_fixed_effects(self):
        self.random_effects_method_GroupBox.setEnabled(False)
        
    def choose_random_effects(self):
        self.random_effects_method_GroupBox.setEnabled(True)
    
    def add_random_effect_methods_to_combo_box(self, default_method):
        self.random_effects_method_ComboBox.clear()
        
        for short_name, pretty_name in RANDOM_EFFECTS_METHODS_TO_PRETTY_STRS.items():
            self.random_effects_method_ComboBox.addItem(
                        pretty_name,
                        userData=QVariant(short_name))
        if default_method:
            idx = self.random_effects_method_ComboBox.findData(QVariant(default_method))
            self.random_effects_method_ComboBox.setCurrentIndex(idx)

    ####### getter functions #################


    def get_confidence_level(self):
        return self.conf_level_spinbox.value()
        
    def get_using_fixed_effects(self):
        return self.get_method() == "FE"
    
    def get_method(self):
        current_index = self.random_effects_method_ComboBox.currentIndex()
        current_data = self.random_effects_method_ComboBox.itemData(current_index)
        method = str(current_data.toString())
        return method
    
    def get_digits(self):
        return self.digits_spinBox.value()
    
    def get_knha(self):
        return self.knha_checkBox.isChecked()
    
    def get_parameters(self):
        # Just call this instead of calling the bunches of functions above
        # returns a dictionary:
        #
        
        params = {'level':self.get_confidence_level(),
                  'method':self.get_method(),
                  'digits':self.get_digits(),
                  'knha':self.get_knha()}
        return params
    

    ###########################################################################
    
    def __str__(self):
        fixed_effects_str = "Using Fixed Effects" if self.get_using_fixed_effects() else "Using Random Effects"
        random_effects_method_str = "Random Effects Method: %s" % self.get_method()
        effects_str = fixed_effects_str if self.get_using_fixed_effects() else fixed_effects_str+"\n"+random_effects_method_str
        conf_level_str = "Confidence Level: %s" % (str(self.get_confidence_level()) + "%")
        summary = "Meta Regression Details:\n" + "\n".join([effects_str, conf_level_str])
        return summary
    
    




