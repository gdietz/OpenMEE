from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
from common_wizard_pages.choose_effect_size_page import ChooseEffectSizePage
from common_wizard_pages.data_location_page import DataLocationPage
from common_wizard_pages.refine_studies_page import RefineStudiesPage
from common_wizard_pages.select_covariates_page import SelectCovariatesPage
from common_wizard_pages.reference_value_page import ReferenceValuePage
from common_wizard_pages.meta_regression_details_page import MetaRegDetailsPage
from common_wizard_pages.summary_page import SummaryPage

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MetaRegDetails, Page_SelectCovariates, Page_ReferenceValues,
Page_Bootstrap, Page_Summary) = range(8)

class MetaRegressionWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(MetaRegressionWizard, self).__init__(parent)
        
        self.model = model
        last_analysis=model.get_last_analysis_selections()
        
        self.setWindowTitle("Meta Regression")
    
        self.setup_pages(last_analysis)
        
        self.setWizardStyle(QWizard.ClassicStyle)
        # Automatically resize wizard on each page flip
        self.currentIdChanged.connect(self._change_size)
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
        
    def setup_pages(self, model, last_analysis):
        self.choose_effect_size_page = ChooseEffectSizePage(add_generic_effect=True,
                                                            data_type=last_analysis['data_type'],
                                                            metric=last_analysis['metric'])
        self.setPage(Page_ChooseEffectSize, self.choose_effect_size_page)
        
        self.data_location_page = DataLocationPage(model=model, mode=MA_MODE)
        self.setPage(Page_DataLocation, self.data_location_page)
        
        self.refine_studies_page = RefineStudiesPage(model=model)
        self.setPage(Page_RefineStudies, self.refine_studies_page)
        
        self.meta_reg_details_page = MetaRegDetailsPage()
        self.setPage(Page_MetaRegDetails, self.meta_reg_details_page)
        
        self.select_covariates_page = SelectCovariatesPage(
                model=model,
                previously_included_covs = last_analysis['included_covariates'],
                fixed_effects=last_analysis['fixed_effects'],
                conf_level=last_analysis['conf_level'],
                random_effects_method = last_analysis['random_effects_method'],
                need_categorical = False)
        self.setPage(Page_SelectCovariates, self.select_covariates_page)
        
        self.reference_value_page = ReferenceValuePage(
                    model=model,
                    prev_cov_to_ref_level=last_analysis['cov_2_ref_values'])
        self.setPage(Page_ReferenceValues, self.reference_value_page)
        
        self.summary_page = SummaryPage()
        self.setPage(Page_Summary, self.summary_page)
        
    def nextId(self):
        current_id = self.currentId()
        
        if current_id == Page_ChooseEffectSize:
            return Page_DataLocation
        elif current_id == Page_DataLocation:
            return Page_RefineStudies
        elif current_id == Page_RefineStudies:
            return Page_MetaRegDetails
        elif current_id == Page_MetaRegDetails:
            return Page_SelectCovariates
        elif current_id == Page_SelectCovariates:
            if self._categorical_covariates_selected():
                return Page_ReferenceValues
            else:
                return Page_Summary
        elif current_id == Page_ReferenceValues:
            return Page_Summary
        elif current_id == Page_Summary:
            return -1

    def _categorical_covariates_selected(self):
        '''are categorical variables selected?'''
        
        included_covariates = self.get_included_covariates()
        categorical_covariates = [cov for cov in included_covariates if cov.get_type()==CATEGORICAL]
        return len(categorical_covariates) > 0
    
    ################ Getters to get data from wizard #########################
    
    # Effect Size Page
    def get_data_type_and_metric(self):
        ''' returns tuple (data_type, metric) '''
        return self.choose_effect_size_page.get_data_type_and_metric()
    
    # Data location page
    def get_data_location(self):
        return self.data_location_page.get_data_locations()
    
    # Refine studies page
    def get_included_studies_in_proper_order(self):
        all_studies = self.model.get_studies_in_current_order()
        included_studies = self.refine_studies_page.get_included_studies()
        included_studies_in_order = [study for study in all_studies if study in included_studies]
        return included_studies_in_order
    
    # Select covariates Page
    def get_included_covariates(self):
        return self.select_covariates_page.get_included_covariates()
    def get_included_interactions(self):
        return self.select_covariates_page.get_included_interactions()
    
    # Meta regression details page
    def using_fixed_effects(self):
        return self.meta_reg_details_page.get_using_fixed_effects()
    def get_conf_level(self):
        return self.meta_reg_details_page.get_confidence_level()
    def get_random_effects_method(self):
        return self.meta_reg_details_page.get_random_effects_method()
    def get_phylogen(self):
        return self.meta_reg_details_page.get_phylogen()
    def get_analysis_type(self):
        return self.meta_reg_details_page.get_analysis_type()
        
    # Reference Values page
    def get_covariate_reference_levels(self):
        return self.reference_value_page.get_covariate_reference_levels()

    # Summary page
    def save_selections(self):
        return self.summary_page.save_selections()
    
    ######################### end of getters #################################
    
    def get_summary(self):
        # TODO: refactor this into a much more light-weight function
        # instead, each wizard age should generate a summary of selections made
        # via the __str__ function and then this(get_summary) function will
        # just combine the various strings togehter
        
        
        ''' Make a summary string to show the user at the end of the wizard summarizing most of the user selections '''
        # This code is very similiar to that appearing in the meta_analysis() and meta_regression() functions of main_form
        # so be sure that the two are kept synchronized
        
        if self.get_analysis_type() == "parametric":
            if self.wizard().get_output_type == "conditional_means":
                mode = META_REG_COND_MEANS
            else:
                mode = META_REG_MODE
        elif self.get_analysis_type() == "bootstrapped":
            if self.wizard().get_output_type == "conditional_means":
                mode = BOOTSTRAP_META_REG_COND_MEANS
            else:
                mode = BOOTSTRAP_META_REG
        else:
            raise Exception("Analysis type not recognized")
        
        summary = ""
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
        fields_to_values['Analysis Type'] = MODE_TITLES[mode]
        fields_to_values['Data Type']     = DATA_TYPE_TEXT[data_type]
        fields_to_values['Metric']        = METRIC_TEXT[metric]
        fields_to_values['Data Location'] = self._get_data_location_string(data_location)
        fields_to_values['Included Studies'] = self._get_labels_string(included_studies)
        fields_to_values['Random Effects Method']=self.get_random_effects_method()

        included_covariates = self.get_included_covariates()
        fixed_effects = self.using_fixed_effects()
        conf_level = self.get_conf_level()
        cov_2_ref_values = self.get_covariate_reference_levels() if len(self.get_covariate_reference_levels()) > 0 else None
        if mode in [META_REG_COND_MEANS, BOOTSTRAP_META_REG_COND_MEANS]:
            selected_cov, covs_to_values = self.get_meta_reg_cond_means_info()
        else:
            selected_cov, covs_to_values = None, None
        bootstrap_params = self.get_bootstrap_params() if mode in [BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS] else {}
        

        if not fixed_effects:
            fields_to_values['Random Effects Method'] = RANDOM_EFFECTS_METHODS_TO_PRETTY_STRS[self.get_random_effects_method()]
        fields_to_values['# Bootstrap Replicates'] = str(bootstrap_params['num.bootstrap.replicates']) if mode in [BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS] else None
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
        ''' helper for summary ''' # using it for covariates too, don't worry that things are called 'study', just using it polymorphically with things that have a get_label() method
        
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

