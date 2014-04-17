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
from common_wizard_pages.meta_reg_cond_means_page import CondMeansPage
from common_wizard_pages.bootstrap_page import BootstrapPage

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MetaRegDetails, Page_SelectCovariates, Page_ReferenceValues,
Page_Bootstrap, Page_Summary, Page_CondMeans) = range(9)

class MetaRegressionWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(MetaRegressionWizard, self).__init__(parent)
        
        self.model = model
        last_analysis=model.get_last_analysis_selections()
        
        self.analysis_label = "Meta-Regression"
        self.setWindowTitle(self.analysis_label)
    
        self.setup_pages(model=model, last_analysis=last_analysis)
        
        self.setWizardStyle(QWizard.ClassicStyle)
        # Automatically resize wizard on each page flip
        self.currentIdChanged.connect(self._change_size)
        
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
        
    def setup_pages(self, model, last_analysis):
        self.choose_effect_size_page = ChooseEffectSizePage(add_generic_effect=True,
                                                            data_type=last_analysis['data_type'],
                                                            metric=last_analysis['metric'],
                                                            var_groups = model.get_variable_groups())
        self.setPage(Page_ChooseEffectSize, self.choose_effect_size_page)
        
        self.data_location_page = DataLocationPage(model=model)
        self.setPage(Page_DataLocation, self.data_location_page)
        
        self.refine_studies_page = RefineStudiesPage(model=model)
        self.setPage(Page_RefineStudies, self.refine_studies_page)
        
        self.meta_reg_details_page = MetaRegDetailsPage(
                fixed_effects=last_analysis['fixed_effects'], 
                random_effects_method = last_analysis['random_effects_method'],
                analysis_type=last_analysis['analysis_type'], # PARAMETRIC or BOOTSTRAP
                conf_level=last_analysis['conf_level'],
                phylogen=last_analysis['phylogen'])
        self.setPage(Page_MetaRegDetails, self.meta_reg_details_page)
        
        self.select_covariates_page = SelectCovariatesPage(
                model=model,
                previously_included_covs=last_analysis['included_covariates'])
        self.setPage(Page_SelectCovariates, self.select_covariates_page)
        
        self.reference_value_page = ReferenceValuePage(
                    model=model,
                    prev_cov_to_ref_level=last_analysis['cov_2_ref_values'])
        self.setPage(Page_ReferenceValues, self.reference_value_page)
        
        self.summary_page = SummaryPage()
        self.setPage(Page_Summary, self.summary_page)
        
        # weird stuff
        self.cond_means_pg = CondMeansPage(model=model)
        self.setPage(Page_CondMeans, self.cond_means_pg)
        
        self.bootstrap_page = BootstrapPage(model=model)
        self.setPage(Page_Bootstrap, self.bootstrap_page)
        
    def _require_categorical(self):
        return self.meta_reg_details_page.get_output_type() == CONDITIONAL_MEANS
        
    def nextId(self):
        current_id = self.currentId()
        
        return self.nextId_helper(current_id)
        
    def nextId_helper(self, page_id):
        
        if page_id in [Page_MetaRegDetails, Page_Bootstrap, Page_ReferenceValues]:
            analysis_type = self.get_analysis_type() # PARAMETRIC or BOOTSTRAP
            output_type = self.get_output_type()     # NORMAL or CONDITIONAL_MEANS
        
        if page_id == Page_ChooseEffectSize:
            return Page_DataLocation
        elif page_id == Page_DataLocation:
            return Page_RefineStudies
        elif page_id == Page_RefineStudies:
            return Page_SelectCovariates
        elif page_id == Page_SelectCovariates:
            return Page_MetaRegDetails
        elif page_id == Page_MetaRegDetails:
            if self._categorical_covariates_selected():
                return Page_ReferenceValues
            else:
                if analysis_type == BOOTSTRAP:
                    return Page_Bootstrap
                elif output_type == CONDITIONAL_MEANS:
                    return Page_CondMeans
                else:
                    return Page_Summary
        elif page_id == Page_Bootstrap:
            if output_type == CONDITIONAL_MEANS:
                return Page_CondMeans
            else:
                return Page_Summary 
        elif page_id == Page_CondMeans:
            return Page_Summary
        elif page_id == Page_ReferenceValues:
            if analysis_type == BOOTSTRAP:
                return Page_Bootstrap
            elif output_type == CONDITIONAL_MEANS:
                return Page_CondMeans
            else:
                return Page_Summary
        elif page_id == Page_Summary:
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
        return self.select_covariates_page.get_interactions()
    
    # Meta regression details page
    def using_fixed_effects(self):
        return self.meta_reg_details_page.get_using_fixed_effects()
    def get_conf_level(self):
        return self.meta_reg_details_page.get_confidence_level()
    def get_random_effects_method(self):
        return self.meta_reg_details_page.get_random_effects_method()
    def get_phylogen(self):
        return self.meta_reg_details_page.get_phylogen()
    def get_analysis_type(self): # NORMAL or BOOTSTRAP
        return self.meta_reg_details_page.get_analysis_type()
    def get_output_type(self): # PARAMETRIC or CONDITIONAL_MEANS
        return self.meta_reg_details_page.get_output_type()
    def get_btt(self): # (a var or interaction, None, 'covariate', 'interaction' i.e. the type)
        return self.meta_reg_details_page.get_btt()
        
    # Reference Values page
    def get_covariate_reference_levels(self):
        return self.reference_value_page.get_covariate_reference_levels()
    
    # Conditional Means page
    def get_meta_reg_cond_means_info(self):
        # returns a tuple (cat. cov to stratify over, the values for the other covariates)
        return self.cond_means_pg.get_meta_reg_cond_means_data()
    
    # Bootstrap page
    def get_bootstrap_params(self):
        return self.bootstrap_page.get_bootstrap_params()

    # Summary page
    def save_selections(self):
        return self.summary_page.save_selections()
    
    ######################### end of getters #################################

    # Summary Page
    def get_summary(self):
        ''' Make a summary string to show the user at the end of the wizard summarizing most of the user selections '''
        return wizard_summary(wizard=self, next_id_helper=self.nextId_helper,
                              summary_page_id=Page_Summary,
                              analysis_label=self.analysis_label)
