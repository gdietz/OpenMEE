################################################################################
#              
# George Dietz 
# CEBM@Brown   
#              
# My policy for the wizards is that they should know nothing about the various
# selections that are made on the pages (store nothing internally)
# rather the selections are stored in the pages themselves and are retrieved
# with accessor functions through the wizard 
#
################################################################################


from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import python_to_R
from common_wizard_pages.choose_effect_size_page import ChooseEffectSizePage
from common_wizard_pages.data_location_page import DataLocationPage
from common_wizard_pages.refine_studies_page import RefineStudiesPage
from common_wizard_pages.methods_and_parameters_page import MethodsAndParametersPage
from common_wizard_pages.summary_page import SummaryPage
from common_wizard_pages.failsafe_page import FailsafeWizardPage
from common_wizard_pages.funnel_page import FunnelPage

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MethodsAndParameters, Page_Summary, Page_Failsafe,
Page_FunnelParameters) = range(7)




class AbstractPublicationBiasWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(AbstractPublicationBiasWizard, self).__init__(parent)
    
        self.setOption(QWizard.HaveFinishButtonOnEarlyPages,True)
    
        self.model = model
        self.last_analysis = model.get_last_analysis_selections() # selections from last analysis of whatever type

        # Initialize pages that we will need to access later
        self.data_location_page = DataLocationPage(model=model)
        self.setPage(Page_DataLocation, self.data_location_page)
        
        self.refine_studies_page = RefineStudiesPage(model=model)
        self.setPage(Page_RefineStudies, self.refine_studies_page)
        
        self.summary_page = SummaryPage()
        self.setPage(Page_Summary, self.summary_page)

        self.setWizardStyle(QWizard.ClassicStyle)

        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
        
    def nextId(self):   
        raise NotImplementedError("Not implemented")
        
    #### Getters
    
    # Data location
    def get_data_location(self):
        return self.data_location_page.get_data_locations()
    
    # Refine Studies page
    def get_included_studies_in_proper_order(self):
        all_studies = self.model.get_studies_in_current_order()
        included_studies = self.refine_studies_page.get_included_studies()
        included_studies_in_order = [study for study in all_studies if study in included_studies]
        return included_studies_in_order
    
    # Summary Page
    def get_summary(self):
        ''' Make a summary string to show the user at the end of the wizard summarizing most of the user selections '''
        # This code is very similiar to that appearing in the meta_analysis() and meta_regression() functions of main_form
        # so be sure that the two are kept synchronized
        
        summary = ""
        if self.mode == FAILSAFE_MODE:
            summary_fields_in_order = ['Analysis Type','Data Location',
                                       'Included Studies',
                                       'Fail-Safe Parameters']
        else:
            summary_fields_in_order = ['Analysis Type',
                                       'Data Type', 'Metric', 'Data Location',
                                       'Included Studies','Chosen Method',
                                       'Subgroup Variable', 'Included Covariates',
                                       'Fixed Effects or Random Effects',
                                       'Random Effects Method',
                                       'Confidence Level', 'Covariate Reference Values',
                                       'Conditional Means Selections',
                                       '# Bootstrap Replicates']
        # initialize dict with values set to None
        fields_to_values = dict(zip(summary_fields_in_order,[None]*len(summary_fields_in_order)))
       
        
        data_type, metric = self.get_data_type_and_metric()
        data_location = self.get_data_location()
        included_studies = self.get_included_studies_in_proper_order()
        
        # Convert to strings:
        if self.mode == FAILSAFE_MODE:
            fields_to_values['Analysis Type'] = MODE_TITLES[self.mode]
            fields_to_values['Data Location'] = self._get_data_location_string(data_location)
            fields_to_values['Included Studies'] = self._get_labels_string(included_studies)
            fields_to_values['Fail-Safe Parameters'] =  self.failsafe_page.get_summary()
        else:  
            fields_to_values['Analysis Type'] = MODE_TITLES[self.mode]
            fields_to_values['Data Type']     = DATA_TYPE_TEXT[data_type]
            fields_to_values['Metric']        = METRIC_TEXT[metric]
            fields_to_values['Data Location'] = self._get_data_location_string(data_location)
            fields_to_values['Included Studies'] = self._get_labels_string(included_studies)
            fields_to_values['Random Effects Method']=self.get_random_effects_method()
        
        if self.mode in META_ANALYSIS_MODES:
            meta_f_str = self.get_modified_meta_f_str()
            current_param_vals = self.get_plot_params()
            chosen_method = self.get_current_method()
            if self.mode == SUBGROUP_MODE: 
                subgroup_variable = self.get_subgroup_variable()
            elif self.mode==BOOTSTRAP_MA:
                current_param_vals.update(self.get_bootstrap_params())
                bootstrap_params = self.get_bootstrap_params()
                
            # convert to strings
            fields_to_values['Chosen Method'] = self.get_current_method_pretty_name()
            fields_to_values['Subgroup Variable'] = subgroup_variable.get_label() if self.mode == SUBGROUP_MODE else None
            fields_to_values['# Bootstrap Replicates'] = str(bootstrap_params['num.bootstrap.replicates']) if self.mode == BOOTSTRAP_MA else None
            if 'rm.method' in current_param_vals:
                fields_to_values['Random Effects Method'] = python_to_R.get_random_effects_methods_descriptions(chosen_method)[current_param_vals['rm.method']]
            
        elif self.mode in META_REG_MODES:
            included_covariates = self.get_included_covariates()
            fixed_effects = self.using_fixed_effects()
            conf_level = self.get_covpage_conf_level()
            cov_2_ref_values = self.get_covariate_reference_levels() if len(self.get_covariate_reference_levels()) > 0 else None
            if self.mode in [META_REG_COND_MEANS, BOOTSTRAP_META_REG_COND_MEANS]:
                selected_cov, covs_to_values = self.get_meta_reg_cond_means_info()
            else:
                selected_cov, covs_to_values = None, None
            bootstrap_params = self.get_bootstrap_params() if self.mode in [BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS] else {}
            
    
            if not fixed_effects:
                fields_to_values['Random Effects Method'] = RANDOM_EFFECTS_METHODS_TO_PRETTY_STRS[self.get_random_effects_method()]
            fields_to_values['# Bootstrap Replicates'] = str(bootstrap_params['num.bootstrap.replicates']) if self.mode in [BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS] else None
            fields_to_values['Included Covariates'] = self._get_labels_string(included_covariates)
            fields_to_values['Fixed Effects or Random Effects'] = "Fixed Effects" if fixed_effects else "Random Effects"
            fields_to_values['Confidence Level'] = str(conf_level) + "%"
            fields_to_values['Covariate Reference Values'] = self._get_covariate_ref_values_string(cov_2_ref_values) if cov_2_ref_values else None
            fields_to_values['Conditional Means Selections'] = self._get_conditional_means_selections_str(selected_cov, covs_to_values)
        
        lines = []
        for field_name in summary_fields_in_order:
            if field_name not in fields_to_values:
                continue
            value = fields_to_values[field_name]
            if value:
                lines.append("".join([field_name,": ",str(value)]))
        summary = "\n\n".join(lines)
        return summary
            
            
    def _get_data_location_string(self, data_location):
        ''' helper for summary '''
        
        get_column_name_for_key = lambda key: self.model.get_variable_assigned_to_column(data_location[key]).get_label()
        get_substr_for_key = lambda key: "\n  " + key.replace('_',' ') + ": " + get_column_name_for_key(key)
        
        sorted_keys = sorted(data_location.keys())
        data_location_str = ""
        for key in sorted_keys:
            if key in ['effect_size','variance']:
                continue
            if data_location[key] == None: # skip if no column assigned
                continue
            data_location_str += get_substr_for_key(key)
        if 'effect_size' in sorted_keys:
            data_location_str += get_substr_for_key('effect_size')
        if 'variance' in sorted_keys:
            data_location_str += get_substr_for_key('variance')
        return data_location_str
    
    def _get_labels_string(self, included_studies):
        ''' helper for summary ''' # using it for covariates too, don't worry that things are called 'study', just using it for polymorphism with things that have a get_label() method
        
        included_studies_str = "\n"
        study_lines  = ["  " + study.get_label() for study in included_studies]
        included_studies_str += "\n".join(study_lines)
        return included_studies_str
    
    def _get_covariate_ref_values_string(self, covariate_ref_values):
        strings = ["".join(["  ",cov.get_label(),': ',str(covariate_ref_values[cov])]) for cov in sorted(covariate_ref_values.keys())]
        ref_val_string = "\n" + "\n".join(strings)
        return ref_val_string
    
    def _get_conditional_means_selections_str(self, selected_cov, covs_to_values):
        if (selected_cov, covs_to_values) == (None, None):
            return None
        
        cond_means_str = "\n  Selected Covariate: %s\n  Values for other covariates:" % selected_cov.get_label()
        
        for cov in sorted(covs_to_values.keys(), key=lambda cov: cov.get_label()):
            cond_means_str += "\n    " + cov.get_label() + ": " + str(covs_to_values[cov])
        return cond_means_str
    
    def save_selections(self): # returns a bool
        # Should the selections be saved? 
        return self.summary_page.save_selections()



class FailsafeWizard(AbstractPublicationBiasWizard):
    def __init__(self, model, parent=None):
        AbstractPublicationBiasWizard.__init__(self, model=model, parent=parent)
           
        self.setWindowTitle("Failsafe Analysis")
        
        # Add custom pages
        self.data_location_page.set_show_raw_data(False)
        
        self.failsafe_page = FailsafeWizardPage(previous_parameters=self.model.get_last_failsafe_parameters())
        self.setPage(Page_Failsafe, self.failsafe_page)
        
        self.setStartId(Page_DataLocation)
        
    def nextId(self):
        page_id = self.currentId()
        
        if page_id == Page_DataLocation:
            return Page_RefineStudies
        if page_id == Page_RefineStudies:
            return Page_Failsafe
        elif page_id == Page_Failsafe:
            return Page_Summary
        elif page_id == Page_Summary:
            return -1
        
    ### Getters ###
    # Failsafe page
    def get_failsafe_parameters(self):
        # parameters for failsafe calculation
        return self.failsafe_page.get_parameters()
        
        

class FunnelWizard(AbstractPublicationBiasWizard):
    def __init__(self, model, meta_f_str=None, parent=None):
        AbstractPublicationBiasWizard.__init__(self, model=model, parent=parent)
    
        ##### Add custom pages ####
        # Effect Size Page
        self.choose_effect_size_page = ChooseEffectSizePage(
                                    add_generic_effect=True,
                                    data_type=self.last_analysis['data_type'],
                                    metric=self.last_analysis['metric'])
        self.setPage(Page_ChooseEffectSize, self.choose_effect_size_page)

        # Methods and parameters apge
        self.methods_and_params_page_instance = MethodsAndParametersPage(
                    model=model, meta_f_str=meta_f_str,
                    disable_forest_plot_tab=True)
        self.setPage(Page_MethodsAndParameters, self.methods_and_params_page_instance)
        
        # Funnel page
        self.funnel_params_page = FunnelPage(old_funnel_params=self.model.get_funnel_params())
        self.setPage(Page_FunnelParameters, self.funnel_params_page)
        
        
        self.setStartId(Page_ChooseEffectSize)

    def nextId(self):
        page_id = self.currentId()

        if page_id == Page_ChooseEffectSize:
            return Page_DataLocation
        elif page_id == Page_DataLocation:
            return Page_RefineStudies
        elif page_id == Page_RefineStudies:
            return Page_MethodsAndParameters
        elif page_id == Page_MethodsAndParameters:
            return Page_FunnelParameters
        elif page_id == Page_FunnelParameters:
            return Page_Summary
        elif page_id == Page_Summary:
            return -1
    
    ### Getters ####
    
    # Effect Size Page
    def get_data_type_and_metric(self):
        ''' returns tuple (data_type, metric) '''
        return self.choose_effect_size_page.get_data_type_and_metric()
    
    # Methods and parameters page
    def get_plot_params(self):
        return self.methods_and_params_page_instance.get_plot_params()
    def get_current_method(self):
        return self.methods_and_params_page_instance.get_current_method()
    def get_current_method_pretty_name(self):
        return self.methods_and_params_page_instance.get_current_method_pretty_name()
    def get_modified_meta_f_str(self):
        return self.methods_and_params_page_instance.get_modified_meta_f_str()
    
    # Funnel page
    def get_funnel_parameters(self):
        return self.funnel_params_page.get_parameters()


# if __name__ == '__main__':
#     import sys
# 
#     app = QtGui.QApplication(sys.argv)
#     wizard = MetaAnalysisWizard(parent=None)
#     wizard.show()
#     sys.exit(app.exec_())
