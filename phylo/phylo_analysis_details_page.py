from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_phylo_analysis_details_page
#import python_to_R

from ome_globals import *

RMA_MV_RANDOM_EFFECTS_METHODS_TO_PRETTY_STRS = {
                                        "ML":"maximum-likelihood estimator",
                                        "REML":"restricted maximum likelihood estimator",}


class PhyloAnalysisDetailsPage(QWizardPage, ui_phylo_analysis_details_page.Ui_WizardPage):
    def __init__(self, model, default_method="REML",parent=None):
        super(PhyloAnalysisDetailsPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model=model
        
        continuous_columns = self.model.get_continuous_columns()
        # TODO: make a 'species' variable subtype that can be assigned to categorical columns
        categorical_columns = self.model.get_categorical_columns()
        effect_columns = [col for col in self.continuous_columns if self._col_assigned_to_effect_variable(col)]
        variance_columns = [col for col in self.continuous_columns if self._col_assigned_to_variance_variable(col)]

        # populate effect, variance, species combo boxes
        self._populate_data_location_combo_box(self.effect_comboBox, effect_columns)
        self._populate_data_location_combo_box(self.variance_comboBox, variance_columns)
        self._populate_data_location_combo_box(self.species_comboBox, categorical_columns)

        # populate random effects method combo box
        self.add_random_effect_methods_to_combo_box(default_method)
        
        self.species_comboBox.currentIndexChanged.connect(self.enable_species_checkbox)
        
        self.completeChanged().emit()
        
    def enable_species_checkbox(self):
        
        # Make sure that species are NOT all unique
        included_studies = self.wizard().get_included_studies_in_proper_order()
        species_column = self.get_data_location()['species']
        species_var = self.model.get_variable_assigned_to_column(species_column)
        
        species_vals = [study.get_var(species_var) for study in included_studies]
        enable = len(species_vals) > len(set(species_vals))
        
        if enable:
            self.include_species_checkBoxsetEnabled(True)
            self.setToolTip("")
        else:
            self.include_species_checkBox.setChecked(False)
            self.include_species_checkBox.setEnabled(False)
            self.setToolTip("All the species are unique, cannot include species as a random factor")
    
    def add_random_effect_methods_to_combo_box(self, default_method):
        self.random_effects_method_ComboBox.clear()
        
        for short_name, pretty_name in RMA_MV_RANDOM_EFFECTS_METHODS_TO_PRETTY_STRS.items():
            self.random_effects_method_ComboBox.addItem(
                        pretty_name,
                        userData=QVariant(short_name))
            
        if default_method:
            idx = self.random_effects_method_ComboBox.findData(QVariant(default_method))
            self.random_effects_method_ComboBox.setCurrentIndex(idx)
            
    def _populate_data_location_combo_box(self, box, columns):
        box.blockSignals(True)
        box.clear()
        key_fn = lambda col: self.model.get_variable_assigned_to_column(col).get_label() # sort by column label
        for col in sorted(columns, key=key_fn):
            var = self.model.get_variable_assigned_to_column(col)
            box.addItem(var.get_label(), col) # store the chosen col
        # if there is only one choice for in columns, select it
        if box.count() > 0:
            box.setCurrentIndex(0)
        box.blockSignals(False)
            
    
        
    def isComplete(self):
        # effect size, variance, and species chosen
        data_locations = self.get_data_location()
        locations_not_none = [x is not None for x in data_locations.values()]
        if all(locations_not_none):
            return True
        else:
            return False
    
    def _col_assigned_to_effect_variable(self, col):
        var = self.model.get_variable_assigned_to_column(col)
        if var.get_subtype() == TRANS_EFFECT:
            return True
        else:
            return False
    
    def _col_assigned_to_variance_variable(self, col):
        var = self.model.get_variable_assigned_to_column(col)
        if var.get_subtype() == TRANS_VAR:
            return True
        else:
            return False
    
    ############# getters #############
    
    def get_data_location(self):
        locations = {'effect_size':self._selected_column(self.effect_comboBox),
                     'variance':self._selected_column(self.variance_comboBox),
                     'species':self._selected_column(self.species_comboBox)}
        
        return locations
    
    def _selected_column(self,combo_box):
        current_index = combo_box.currentIndex()
        if current_index < 0:
            return None
        item_data = combo_box.itemData(current_index)
        selected_column = item_data.toInt()[0]
        return selected_column
    
    def get_random_effects_method(self):
        current_index = self.random_effects_method_ComboBox.currentIndex()
        current_data = self.random_effects_method_ComboBox.itemData(current_index)
        method = str(current_data.toString())
        return method
    
    def get_conf_level(self):
        return self.conf_level_spinbox.value()
    
    def get_include_species_as_random_factor(self):
        return self.include_species_checkBox.isChecked()
    
    #######################
    
    def _get_data_location_string(self, data_location):
        ''' helper for summary '''
        
        get_column_name_for_key = lambda key: self.model.get_variable_assigned_to_column(data_location[key]).get_label()
        get_substr_for_key = lambda key: "  " + key.replace('_',' ') + ": " + get_column_name_for_key(key)
        
        lines = []
            
        lines.append(get_substr_for_key('effect_size'))
        lines.append(get_substr_for_key('variance'))
        lines.append(get_substr_for_key('species'))
            
            
        data_location_str = "\n".join(lines)
        return data_location_str
    
    def __str__(self):
        # data locations
        data_locations_str = self._get_data_location_string(self.get_data_locations())
        data_locations_output = "Data Location:\n%s" % indent(data_locations_str)
        
        # random_effects_method
        random_method_str = "Random Effects Method: %s" % RMA_MV_RANDOM_EFFECTS_METHODS_TO_PRETTY_STRS[self.get_random_effects_method()]
        
        # confidence level
        conf_level_str = "Confidence Level: %s%" % self.get_conf_level()
        
        # Species as random factor
        species_as_random_factor_str = "Species " + ("will" if self.get_include_species_as_random_factor() else "will not") + " be included as a random factor"
        
        return "\n".join([data_locations_output, random_method_str, conf_level_str, species_as_random_factor_str])