'''
Created on Mar 24, 2014

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import ui_meta_analysis_parameters_page

# TODO finish going through this and making the appropriate changes

class MetaAnalysisParamtersPage(QWizardPage, ui_meta_analysis_parameters_page.Ui_WizardPage):
    def __init__(self,
                 fixed_effects,
                 method, # random effects method
                 level, # confidence level
                 parent=None): 
        super(MetaAnalysisParamtersPage, self).__init__(parent)
        self.setupUi(self)

        # populate random effects combobox
        self.add_random_effect_methods_to_combo_box(default_method="REML")
        
        # Set confidence level
        self.conf_level_spinbox.setValue(level)

        # Setup connections
        self.setup_connections()
        
    
    def setup_connections(self):
        # radio buttons
        self.fixed_effects_radio_btn.clicked.connect(self.choose_fixed_effects)
        self.random_effects_radio_btn.clicked.connect(self.choose_random_effects)
        
    def initializePage(self):
        self.covariates = self.wizard().get_included_covariates()
        self.interactions = self.wizard().get_included_interactions()
        
        # list corresponding to the order of items in the combobox
        self.btt_comboBox_contents = [None,] + self.covariates + self.interactions
        
        self._populate_btt_combobox()
        
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
            
    def _populate_btt_combobox(self):
        get_combobox_item_str = lambda x: 'All' if x is None else str(x)
        combobox_stringlist = [get_combobox_item_str(x) for x in self.btt_comboBox_contents]
        
        self.btt_comboBox.clear()
        self.btt_comboBox.addItems(combobox_stringlist)
        self.btt_comboBox.setCurrentIndex(0)

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
    
    def get_btt(self):
        # returns a tuple that will be useful in building of the 'btt'
        # argument to rma.uni in metafor
        #      output: (choice, choice_type)
        # choice: a covariate or interaction object
        # choice_type: None, 'covariate', or 'interaction'
        
        index = self.btt_comboBox.currentIndex()
        choice = self.btt_comboBox_contents[index]
        
        # determine choice type: None, 'covariate', or 'interaction'
        n_cov = len(self.covariates)
        
        cov_idx_range = range(1,1+n_cov)
        interactions_idx_range = range(1+n_cov, len(self.btt_comboBox_contents))
        if index == 0:
            choice_type = None
        elif index in cov_idx_range:
            choice_type = 'covariate'
        elif index in interactions_idx_range:
            choice_type = 'interaction'
        else:
            raise Exception("Shouldn't be here, are the ranges correct?")
        
        return (choice, choice_type)
    
    ###########################################################################
    
    def __str__(self):
        fixed_effects_str = "Using Fixed Effects" if self.get_using_fixed_effects() else "Using Random Effects"
        random_effects_method_str = "Random Effects Method: %s" % self.get_random_effects_method()
        effects_str = fixed_effects_str if self.get_using_fixed_effects() else fixed_effects_str+"\n"+random_effects_method_str
        conf_level_str = "Confidence Level: %s" % (str(self.get_confidence_level()) + "%")
        analysis_str = "%s Analysis" % ("Parametric" if self.get_analysis_type() == PARAMETRIC else "Bootstrap")
        output_type_str = "Output type: %s" % ("Conditional Means" if self.get_output_type() == CONDITIONAL_MEANS else "Normal")
        # omnibus test of moderators
        btt_var = self.get_btt()[0]
        omnibus_str = "Omnibus test of moderators variable: %s" % str(btt_var)
        
        summary = "Meta Regression Details:\n" + "\n".join([analysis_str, effects_str, conf_level_str, output_type_str, omnibus_str])
        return summary
    
    




