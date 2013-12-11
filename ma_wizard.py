################
#              #
# George Dietz #
# CEBM@Brown   #
#              #
################


from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *

import python_to_R
from choose_effect_size_page import ChooseEffectSizePage
from data_location_page import DataLocationPage
from refine_studies_page import RefineStudiesPage
from methods_and_parameters_page import MethodsAndParametersPage
from subgroup_variable_page import SubgroupVariablePage
from select_covariates_page import SelectCovariatesPage
from reference_value_page import ReferenceValuePage
from meta_reg_cond_means import CondMeansPage
from bootstrap_page import BootstrapPage
from summary_page import SummaryPage
from failsafe_page import FailsafeWizardPage
from funnel_page import FunnelPage

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MethodsAndParameters, Page_SubgroupVariable, Page_SelectCovariates,
Page_ReferenceValues, Page_CondMeans, Page_Bootstrap, Page_Summary,
Page_Failsafe,Page_FunnelParameters) = range(12)
class MetaAnalysisWizard(QtGui.QWizard):
    def __init__(self, model, meta_f_str=None, mode = MA_MODE, parent=None):
        super(MetaAnalysisWizard, self).__init__(parent)
        
        self.model = model
        self.meta_f_str = meta_f_str
        self.mode = mode
        
        self.selected_data_type = None
        self.selected_metric = None
        self.data_location = None
        self.studies_included_table = None # dict mapping studies to if their inclusion state
        self.subgroup_variable_column = None
        self.covariates_included_table = None
        self.using_fixed_effects = None # will be a callable returning a boolean
        self.get_confidence_level = None # will be a callable returning a double
        self.cov_2_ref_values = {}
        
        self.setWindowTitle(MODE_TITLES[mode])
        self.setOption(QWizard.HaveFinishButtonOnEarlyPages,True)
        
        # Initialize pages that we will need to access later
        self.methods_and_params_page_instance = MethodsAndParametersPage(model=model, meta_f_str=meta_f_str, mode=mode)
        if mode in [BOOTSTRAP_MA, BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS]:
            self.bootstrap_page = BootstrapPage(model=model, mode=mode)
        self.cond_means_pg = CondMeansPage(model=model)
        
        self.setPage(Page_ChooseEffectSize, ChooseEffectSizePage(model=model, add_generic_effect=True))
        self.data_location_page = DataLocationPage(model=model, mode=MA_MODE)
        
        
        self.setPage(Page_MethodsAndParameters, self.methods_and_params_page_instance)
        self.setPage(Page_RefineStudies, RefineStudiesPage(model=model, mode=mode))
        self.setPage(Page_Summary, SummaryPage())
        if mode==SUBGROUP_MODE:
            self.setPage(Page_DataLocation, self.data_location_page)
            self.setPage(Page_SubgroupVariable, SubgroupVariablePage(model=model))
        elif mode==META_REG_MODE:
            self.setPage(Page_DataLocation, self.data_location_page)
            self.setPage(Page_SelectCovariates, SelectCovariatesPage(model=model, mode=mode))
            self.setPage(Page_ReferenceValues, ReferenceValuePage(model=model))
        elif mode==META_REG_COND_MEANS:
            self.setPage(Page_DataLocation, self.data_location_page)
            self.setPage(Page_SelectCovariates, SelectCovariatesPage(model=model, mode=mode))
            self.setPage(Page_CondMeans, self.cond_means_pg)
        elif mode==BOOTSTRAP_MA:
            self.setPage(Page_DataLocation, self.data_location_page)
            self.setPage(Page_Bootstrap, self.bootstrap_page)
        elif mode==BOOTSTRAP_META_REG:
            self.setPage(Page_DataLocation, self.data_location_page)
            self.setPage(Page_SelectCovariates, SelectCovariatesPage(model=model, mode=mode))
            self.setPage(Page_ReferenceValues, ReferenceValuePage(model=model))
            self.setPage(Page_Bootstrap, self.bootstrap_page)
        elif mode==BOOTSTRAP_META_REG_COND_MEANS:
            self.setPage(Page_DataLocation, self.data_location_page)
            self.setPage(Page_SelectCovariates, SelectCovariatesPage(model=model, mode=mode))
            self.setPage(Page_CondMeans, self.cond_means_pg)
            self.setPage(Page_Bootstrap, self.bootstrap_page)
        elif mode==FAILSAFE_MODE:
            self.data_location_page = DataLocationPage(model=model, mode=FAILSAFE_MODE)
            self.setPage(Page_DataLocation, self.data_location_page)
            
            self.failsafe_page = FailsafeWizardPage(previous_parameters=self.model.get_last_failsafe_parameters())
            self.setPage(Page_Failsafe, self.failsafe_page)
        elif mode == FUNNEL_MODE:
            self.data_location_page = DataLocationPage(model=model, mode=FUNNEL_MODE)
            self.setPage(Page_DataLocation, self.data_location_page)
            self.funnel_params_page = FunnelPage()
            self.setPage(Page_FunnelParameters, self.funnel_params_page)
        else:
            self.setPage(Page_DataLocation, self.data_location_page)
        
        if mode == FAILSAFE_MODE:
            self.setStartId(Page_DataLocation)
        else:
            self.setStartId(Page_ChooseEffectSize)
        self.setWizardStyle(QWizard.ClassicStyle)
        

        
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
        
    def get_bootstrap_params(self):
        return self.bootstrap_page.get_bootstrap_params()
        
    def get_included_covariates(self):
        included_covariates = [cov for cov,should_include in self.covariates_included_table.iteritems() if should_include]
        return included_covariates
        
    def get_subgroup_variable_column(self):
        return self.subgroup_variable_column

    
    def get_subgroup_variable(self):
        if self.subgroup_variable_column is None:
            return None
        return self.model.get_variable_assigned_to_column(self.subgroup_variable_column)
        
    def get_plot_params(self):
        return self.methods_and_params_page_instance.get_plot_params()
    
    def get_current_method(self):
        return self.methods_and_params_page_instance.get_current_method()
    def get_current_method_pretty_name(self):
        return self.methods_and_params_page_instance.get_current_method_pretty_name()
    
    
    def get_modified_meta_f_str(self):
        return self.methods_and_params_page_instance.get_modified_meta_f_str()
        
    def get_included_studies_in_proper_order(self):
        all_studies = self.model.get_studies_in_current_order()
        included_studies = [study for study in all_studies if self.studies_included_table[study]==True]
        return included_studies

    def categorical_covariates_selected(self):
        included_covariates = self.get_included_covariates()
        categorical_covariates = [cov for cov in included_covariates if cov.get_type()==CATEGORICAL]
        return len(categorical_covariates) > 0
    
    def get_meta_reg_cond_means_info(self):
        # returns a tuple (cat. cov to stratify over, the values for the other covariates)
        return self.cond_means_pg.get_meta_reg_cond_means_data()

    def get_failsafe_parameters(self):
        # parameters for failsafe calculation
        return self.failsafe_page.get_parameters()
    
    def get_funnel_parameters(self):
        return self.funnel_params_page.get_parameters(ready_to_send_to_R=True)
    
    def nextId(self):
        next_id = self.next_page(self.currentId())
        return next_id
            
    def next_page(self, page_id):
        ''' helper method for nextId '''
        if self.mode==SUBGROUP_MODE:
            # this is redundant but it makes the path easier to understand
            if page_id == Page_ChooseEffectSize:
                return Page_DataLocation
            elif page_id == Page_DataLocation:
                return Page_RefineStudies
            elif page_id == Page_RefineStudies:
                return Page_SubgroupVariable
            elif page_id == Page_SubgroupVariable:  #
                return Page_MethodsAndParameters             #
            elif page_id == Page_MethodsAndParameters:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1
        elif self.mode == META_REG_MODE:
            if page_id == Page_ChooseEffectSize:
                return Page_DataLocation
            elif page_id == Page_DataLocation:
                return Page_RefineStudies
            elif page_id == Page_RefineStudies:
                return Page_SelectCovariates
            elif page_id == Page_SelectCovariates:
                if self.categorical_covariates_selected():
                    return Page_ReferenceValues
                else:
                    return Page_Summary
            elif page_id == Page_ReferenceValues:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1
        elif self.mode == META_REG_COND_MEANS:
            if page_id == Page_ChooseEffectSize:
                return Page_DataLocation
            elif page_id == Page_DataLocation:
                return Page_RefineStudies
            elif page_id == Page_RefineStudies:
                return Page_SelectCovariates
            elif page_id == Page_SelectCovariates:
                return Page_CondMeans
            elif page_id == Page_CondMeans:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1
        elif self.mode == BOOTSTRAP_MA:
            if page_id == Page_ChooseEffectSize:
                return Page_DataLocation
            elif page_id == Page_DataLocation:
                return Page_RefineStudies
            elif page_id == Page_RefineStudies:
                return Page_MethodsAndParameters
            elif page_id == Page_MethodsAndParameters:
                return Page_Bootstrap
            elif page_id == Page_Bootstrap:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1
        elif self.mode == BOOTSTRAP_META_REG:
            if page_id == Page_ChooseEffectSize:
                return Page_DataLocation
            elif page_id == Page_DataLocation:
                return Page_RefineStudies
            elif page_id == Page_RefineStudies:
                return Page_SelectCovariates
            elif page_id == Page_SelectCovariates:
                if self.categorical_covariates_selected():
                    return Page_ReferenceValues
                else:
                    return Page_Bootstrap
            elif page_id == Page_ReferenceValues:
                return Page_Bootstrap
            elif page_id == Page_Bootstrap:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1
        elif self.mode == BOOTSTRAP_META_REG_COND_MEANS:
            if page_id == Page_ChooseEffectSize:
                return Page_DataLocation
            elif page_id == Page_DataLocation:
                return Page_RefineStudies
            elif page_id == Page_RefineStudies:
                return Page_SelectCovariates
            elif page_id == Page_SelectCovariates:
                return Page_CondMeans
            elif page_id == Page_CondMeans:
                return Page_Bootstrap
            elif page_id == Page_Bootstrap:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1
        elif self.mode == FAILSAFE_MODE:
            if page_id == Page_DataLocation:
                return Page_RefineStudies
            if page_id == Page_RefineStudies:
                return Page_Failsafe
            elif page_id == Page_Failsafe:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1
        elif self.mode == FUNNEL_MODE:
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
        else: # default vanilla meta-analysis case
            if page_id == Page_ChooseEffectSize:
                return Page_DataLocation
            elif page_id == Page_DataLocation:
                return Page_RefineStudies
            elif page_id == Page_RefineStudies:
                return Page_MethodsAndParameters
            elif page_id == Page_MethodsAndParameters:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1
            
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
       
        
        data_type = self.selected_data_type
        metric = self.selected_metric
        data_location = self.data_location
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
        
        
        
        
        if self.mode in META_ANALYSIS_MODES:
            meta_f_str = self.get_modified_meta_f_str()
            current_param_vals = self.get_plot_params()
            chosen_method = self.get_current_method()
            subgroup_variable = self.get_subgroup_variable()
            if self.mode==BOOTSTRAP_MA:
                current_param_vals.update(self.get_bootstrap_params())
                bootstrap_params = self.get_bootstrap_params()
                
            # convert to strings
            fields_to_values['Chosen Method'] = self.get_current_method_pretty_name()
            fields_to_values['Subgroup Variable'] = subgroup_variable.get_label() if subgroup_variable else None
            fields_to_values['# Bootstrap Replicates'] = str(bootstrap_params['num.bootstrap.replicates']) if self.mode == BOOTSTRAP_MA else None
            if 'rm.method' in current_param_vals:
                fields_to_values['Random Effects Method'] = python_to_R.get_random_effects_methods_descriptions(chosen_method)[current_param_vals['rm.method']]
            
        elif self.mode in META_REG_MODES:
            included_covariates = self.get_included_covariates()
            fixed_effects = self.using_fixed_effects()
            conf_level = self.get_confidence_level()
            cov_2_ref_values = self.cov_2_ref_values if len(self.cov_2_ref_values) > 0 else None
            if self.mode in [META_REG_COND_MEANS, BOOTSTRAP_META_REG_COND_MEANS]:
                selected_cov, covs_to_values = self.get_meta_reg_cond_means_info()
            else:
                selected_cov, covs_to_values = None, None
            bootstrap_params = self.get_bootstrap_params() if self.mode in [BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS] else {}
    
            if not fixed_effects:
                fields_to_values['Random Effects Method'] = DEFAULT_METAREG_RANDOM_EFFECTS_METHOD
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



if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = MetaAnalysisWizard(parent=None)
    wizard.show()
    sys.exit(app.exec_())