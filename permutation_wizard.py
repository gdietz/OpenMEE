from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
from common_wizard_pages.choose_effect_size_page import ChooseEffectSizePage
from common_wizard_pages.data_location_page import DataLocationPage
from common_wizard_pages.refine_studies_page import RefineStudiesPage
from common_wizard_pages.select_covariates_page import SelectCovariatesPage
from common_wizard_pages.reference_value_page import ReferenceValuePage
from common_wizard_pages.ma_details_page import MADetailsPage
from common_wizard_pages.meta_regression_details_page import MetaRegDetailsPage
from common_wizard_pages.permutation_page import PermuationPage
from common_wizard_pages.summary_page import SummaryPage

(
    Page_ChooseEffectSize,
    Page_DataLocation,
    Page_RefineStudies,
    Page_SelectCovariates,
    Page_ReferenceValues,
    Page_MADetails,
    Page_MetaRegDetails,
    Page_Permutation,
    Page_Summary,
) = range(9)

# This wizard works a little different than the others. Instead of having a lot
# of accessor methods to get info out of it, this one just has one that returns
# a dict
class PermutationWizard(QtGui.QWizard):
    # if meta_reg mode is True, the wizard will do a permutation
    # test for a meta-regression, otherwise it does a standard 
    # meta-analysis
    def __init__(self, model, meta_reg_mode=False, parent=None):
        super(PermutationWizard, self).__init__(parent)
        
        self.model = model
        last_analysis = model.get_last_analysis_selections()
        self.meta_reg_mode = meta_reg_mode

        # Set window title
        if meta_reg_mode:
            self.analysis_label = "Permuted Meta-Regression"
        else:
            self.analysis_label = "Permuted Meta-Analysis"
        self.setWindowTitle(self.analysis_label)

        self.setup_pages(model=model, last_analysis=last_analysis)
        
        self.setWizardStyle(QWizard.ClassicStyle)
        # Automatically resize wizard on each page flip
        self.currentIdChanged.connect(self.adjustSize)

    def setup_pages(self, model, last_analysis):
        self.choose_effect_size_page = ChooseEffectSizePage(
            add_generic_effect=True,
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
                random_effects_method=last_analysis['random_effects_method'],
                analysis_type=last_analysis['analysis_type'], # PARAMETRIC or BOOTSTRAP
                conf_level=last_analysis['conf_level'],
                phylogen=last_analysis['phylogen'],
                disable_analysis_type_groupbox=True,
                disable_output_type_groupbox=True)
        self.setPage(Page_MetaRegDetails, self.meta_reg_details_page)
        
        self.ma_details_page = MADetailsPage()
        self.setPage(Page_MADetails, self.ma_details_page)

        self.perm_pg = PermuationPage()
        self.setPage(Page_Permutation, self.perm_pg)

        self.select_covariates_page = SelectCovariatesPage(
                model=model,
                previously_included_covs=last_analysis['included_covariates'],
                disable_require_categorical=True)
        self.setPage(Page_SelectCovariates, self.select_covariates_page)
        
        self.reference_value_page = ReferenceValuePage(
                    model=model,
                    prev_cov_to_ref_level=last_analysis['cov_2_ref_values'])
        self.setPage(Page_ReferenceValues, self.reference_value_page)
        
        self.summary_page = SummaryPage()
        self.setPage(Page_Summary, self.summary_page)
        
    def nextId(self):
        current_id = self.currentId()
        return self.nextId_helper(current_id)
        
    def nextId_helper(self, page_id):

        if self.meta_reg_mode:
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
                    return Page_Permutation
            elif page_id == Page_ReferenceValues:
                return Page_Permutation
            elif page_id == Page_Permutation:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1
        else: # non-meta regression mode (no moderators)
            if page_id == Page_ChooseEffectSize:
                return Page_DataLocation
            elif page_id == Page_DataLocation:
                return Page_RefineStudies
            elif page_id == Page_RefineStudies:
                return Page_MADetails
            elif page_id == Page_MADetails:
                return Page_Permutation
            elif page_id == Page_ReferenceValues:
                return Page_Permutation
            elif page_id == Page_Permutation:
                return Page_Summary
            elif page_id == Page_Summary:
                return -1

    def _categorical_covariates_selected(self):
        '''are categorical variables selected?'''
        
        included_covariates = self.get_included_covariates()
        categorical_covariates = [cov for cov in included_covariates if cov.get_type()==CATEGORICAL]
        return len(categorical_covariates) > 0
        
    ################# getters #########################
    def get_parameters(self):
        data_type_and_metric = self.choose_effect_size_page.get_data_type_and_metric()
        data_location = self.data_location_page.get_data_locations()
        studies = self.refine_studies_page.get_included_studies_in_proper_order()

        parameters = {
            'data_type_and_metric': data_type_and_metric,
            'data_location': data_location,
            'studies': studies,
        }
        
        parameters.update(self.perm_pg.get_choices())

        # meta-regression specific
        if self.meta_reg_mode:
            covariates = self.select_covariates_page.get_included_covariates()
            interactions = self.select_covariates_page.get_interactions()
            _fixed_effects = self.meta_reg_details_page.get_using_fixed_effects()
            level = self.meta_reg_details_page.get_confidence_level()
            _random_effects_method = self.meta_reg_details_page.get_random_effects_method()
            method = _random_effects_method if not _fixed_effects else FIXED_EFFECTS_METHOD_STR
            phylogen = self.meta_reg_details_page.get_phylogen()
            btt = self.meta_reg_details_page.get_btt()
            reference_values = self.reference_value_page.get_covariate_reference_levels()

            parameters.update({
                'covariates': covariates,
                'interactions': interactions,
                'level': level,
                'method': method,
                'phylogen': phylogen,
                'btt': btt,
                'reference_values': reference_values,
            })
        else:
            # ma specific (no moderators)
            method = self.ma_details_page.get_method()
            intercept = self.ma_details_page.get_intercept()
            weighted = self.ma_details_page.get_weighted_least_squares()
            knha = self.ma_details_page.get_knha()
            level = self.ma_details_page.get_confidence_level()
            digits = self.ma_details_page.get_digits()

            parameters.update({
                'method':method,
                'intercept':intercept,
                'weighted':weighted,
                'knha':knha,
                'level':level,
                'digits':digits,
            })
        return parameters

    # Summary page
    def save_selections(self):
        return self.summary_page.save_selections()
    
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
    
    ######################### end of getters #################################

    # Summary Page
    def get_summary(self):
        ''' Make a summary string to show the user at the end of the wizard summarizing most of the user selections '''
        summary = wizard_summary(
            wizard=self,
            next_id_helper=self.nextId_helper,
            summary_page_id=Page_Summary,
            analysis_label=self.analysis_label
        )
        return summary