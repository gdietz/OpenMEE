from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import ui_meta_regression_details_page

class MetaRegDetailsPage(QWizardPage, ui_meta_regression_details_page.Ui_WizardPage):
    def __init__(self,
                 fixed_effects,
                 random_effects_method,
                 analysis_type, # PARAMETRIC or BOOTSTRAP
                 conf_level,
				 phylogen,
                 parent=None): # todo: set defaults of previous parameters to None
        super(MetaRegDetailsPage, self).__init__(parent)
        self.setupUi(self)
        
        if analysis_type not in [PARAMETRIC, BOOTSTRAP]:
            raise Exception("Unrecognized analysis type")

        ### Set values from previous analysis ###
        self.setup_values_from_previous_analysis(
            conf_level=conf_level,
            random_effects_method=random_effects_method,
            fixed_effects=fixed_effects,
			analysis_type=analysis_type,
			phylogen=phylogen)

        # Setup connections
        self.setup_connections()
    
        # Disable phylogen checkbox until phylogenetic component included
        self.phylogen_checkBox.setEnabled(False)
        self.phylogen_checkBox.setToolTip("Disabled until phylogenetic component included")
        
    
    def setup_connections(self):
        # radio buttons
        self.fixed_effects_radio_btn.clicked.connect(self.choose_fixed_effects)
        self.random_effects_radio_btn.clicked.connect(self.choose_random_effects)
        
    def setup_values_from_previous_analysis(self, conf_level,
											random_effects_method,
											fixed_effects,
											analysis_type,
											phylogen):
        ### Set values from previous analysis ###
        if conf_level:
            self.conf_level_spinbox.setValue(conf_level)
        
        # populate random effects combobox
        self.add_random_effect_methods_to_combo_box(default_method=random_effects_method)
        
        # Using random effects or fixed effects?
        if fixed_effects:
            self.choose_fixed_effects()
            self.fixed_effects_radio_btn.setChecked(True)
        else:
            self.choose_random_effects()
            self.random_effects_radio_btn.setChecked(True)

        # analysis type: parametric or bootstrapped?
        if analysis_type == PARAMETRIC:
            self.parametric_radioButton.setChecked(True)
        elif analysis_type == BOOTSTRAP:
            self.bootstrapped_radioButton.setChecked(True)
            
        # Use phylogenetic correlations?
        self.phylogen_checkBox.setChecked(phylogen)
        
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
        return self.fixed_effects_radio_btn.isChecked()
    
    def get_random_effects_method(self):
        current_index = self.random_effects_method_ComboBox.currentIndex()
        current_data = self.random_effects_method_ComboBox.itemData(current_index)
        method = str(current_data.toString())
        return method
    
    def get_phylogen(self):
        return self.phylogen_checkBox.isChecked()
    
    def get_analysis_type(self):
        '''PARAMETRIC or BOOTSTRAP'''
        analysis_type = PARAMETRIC if self.parametric_radioButton.isChecked() else BOOTSTRAP
        return analysis_type
    
    def get_output_type(self):
        ''' NORMAL or CONDITIOAL_MEANS '''
        if self.conditional_means_checkBox.isChecked():
            return CONDITIONAL_MEANS
        return NORMAL