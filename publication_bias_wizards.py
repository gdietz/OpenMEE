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

#import python_to_R
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
        
        return self.next_id_helper(page_id)
        
    def next_id_helper(self, page_id):
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
    
    # Summary Page
    def get_summary(self):
        ''' Make a summary string to show the user at the end of the wizard summarizing most of the user selections '''
        return wizard_summary(wizard=self, next_id_helper=self.next_id_helper,
                              summary_page_id=Page_Summary,
                              analysis_label="Failsafe Analysis")
        
        

class FunnelWizard(AbstractPublicationBiasWizard):
    def __init__(self, model, meta_f_str=None, parent=None):
        AbstractPublicationBiasWizard.__init__(self, model=model, parent=parent)
    
        ##### Add custom pages ####
        # Effect Size Page
        self.choose_effect_size_page = ChooseEffectSizePage(
                                    add_generic_effect=True,
                                    data_type=self.last_analysis['data_type'],
                                    metric=self.last_analysis['metric'],
                                    var_groups = model.get_variable_groups())
        self.setPage(Page_ChooseEffectSize, self.choose_effect_size_page)

        # Methods and parameters apge
        self.methods_and_params_page_instance = MethodsAndParametersPage(
                    model=model, meta_f_str=meta_f_str,
                    disable_forest_plot_tab=True, funnel_mode=True)
        self.setPage(Page_MethodsAndParameters, self.methods_and_params_page_instance)
        
        # Funnel page
        self.funnel_params_page = FunnelPage(old_funnel_params=self.model.get_funnel_params())
        self.setPage(Page_FunnelParameters, self.funnel_params_page)
        
        
        self.setStartId(Page_ChooseEffectSize)

    def nextId(self):
        page_id = self.currentId()
        
        return self.next_id_helper(page_id)
        
    def next_id_helper(self, page_id):

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
    
        # Summary Page
    def get_summary(self):
        ''' Make a summary string to show the user at the end of the wizard summarizing most of the user selections '''
        return wizard_summary(wizard=self, next_id_helper=self.next_id_helper,
                              summary_page_id=Page_Summary,
                              analysis_label="Funnelplot Analysis")


# if __name__ == '__main__':
#     import sys
# 
#     app = QtGui.QApplication(sys.argv)
#     wizard = MetaAnalysisWizard(parent=None)
#     wizard.show()
#     sys.exit(app.exec_())
