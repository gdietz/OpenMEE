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
# This is collection of meta analysis wizards: Regular meta analysis,
# cumulative, leave one out, subgroup, and bootstrap
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
from common_wizard_pages.subgroup_variable_page import SubgroupVariablePage
from common_wizard_pages.bootstrap_page import BootstrapPage
from common_wizard_pages.summary_page import SummaryPage


(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MethodsAndParameters, Page_SubgroupVariable, Page_Bootstrap,
Page_Summary) = range(7)

class AbstractMetaAnalysisWizard(QtGui.QWizard):
    def __init__(self, model, meta_f_str=None, parent=None):
        super(AbstractMetaAnalysisWizard, self).__init__(parent)
        
        self.model = model
        self.meta_f_str = meta_f_str
        last_analysis = model.get_last_analysis_selections() # selections from last analysis of whatever type
        
        # Initialize pages that we will need to access later
        self.methods_and_params_page_instance = MethodsAndParametersPage(model=model, meta_f_str=meta_f_str)
        self.setPage(Page_MethodsAndParameters, self.methods_and_params_page_instance)
        
        # choose effect size
        self.choose_effect_size_page = ChooseEffectSizePage(add_generic_effect=True,
                data_type=last_analysis['data_type'],
                metric=last_analysis['metric'],
                var_groups = model.get_variable_groups())
        self.setPage(Page_ChooseEffectSize, self.choose_effect_size_page)
        
        # data location page
        self.data_location_page = DataLocationPage(model=model)
        self.setPage(Page_DataLocation, self.data_location_page)
        
        # refine studies page
        self.refine_studies_page = RefineStudiesPage(model=model)
        self.setPage(Page_RefineStudies, self.refine_studies_page)
        
        # summary page
        self.summary_page = SummaryPage()
        self.setPage(Page_Summary, self.summary_page)
            
        self.setWizardStyle(QWizard.ClassicStyle)
        self.setStartId(Page_ChooseEffectSize)
        self.setOption(QWizard.HaveFinishButtonOnEarlyPages,True)
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()

    # Methods and parameters page
    def get_plot_params(self):
        return self.methods_and_params_page_instance.get_plot_params()
    def get_current_method(self):
        return self.methods_and_params_page_instance.get_current_method()
    def get_current_method_pretty_name(self):
        return self.methods_and_params_page_instance.get_current_method_pretty_name()
    def get_modified_meta_f_str(self):
        return self.methods_and_params_page_instance.get_modified_meta_f_str()
    
    # refine studies page
    def get_included_studies_in_proper_order(self):
        all_studies = self.model.get_studies_in_current_order()
        included_studies = self.refine_studies_page.get_included_studies()
        included_studies_in_order = [study for study in all_studies if study in included_studies]
        return included_studies_in_order

    # data location page
    def get_data_location(self):
        return self.data_location_page.get_data_locations()
    
    # choose effect size page
    def get_data_type_and_metric(self):
        ''' returns tuple (data_type, metric) '''
        return self.choose_effect_size_page.get_data_type_and_metric()

    def nextId(self):
        next_id = self.nextId_helper(self.currentId())
        return next_id
     
    def get_summary(self):
        ''' Make a summary string to show the user at the end of the wizard summarizing most of the user selections '''
        return wizard_summary(wizard=self, next_id_helper=self.nextId_helper,
                              summary_page_id=Page_Summary,
                              analysis_label="Meta-Analysis")
    
    def save_selections(self): # returns a bool
        # Should the selections be saved? 
        return self.summary_page.save_selections()

class RegularMetaAnalysisWizard(AbstractMetaAnalysisWizard):
    def __init__(self, model, parent=None):
        AbstractMetaAnalysisWizard.__init__(self, model=model, meta_f_str=None)
        
        self.setWindowTitle("Meta-Analysis")
    
    def nextId_helper(self, page_id):
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
        
class CumulativeMetaAnalysisWizard(AbstractMetaAnalysisWizard):
    def __init__(self, model, parent=None):
        AbstractMetaAnalysisWizard.__init__(self, model=model, meta_f_str="cum.ma")
        self.setWindowTitle("Cumulative Meta-Analysis")
        
    def nextId_helper(self, page_id):
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
        
class LeaveOneOutMetaAnalysisWizard(AbstractMetaAnalysisWizard):
    def __init__(self, model, parent=None):
        AbstractMetaAnalysisWizard.__init__(self, model=model, meta_f_str="loo.ma")
        self.setWindowTitle("Leave-one-out Meta-Analysis")
        
    def nextId_helper(self, page_id):
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
        
class SubgroupMetaAnalysisWizard(AbstractMetaAnalysisWizard):
    def __init__(self, model, parent=None):
        AbstractMetaAnalysisWizard.__init__(self, model=model, meta_f_str="subgroup.ma")
        
        # Subgroup variable page
        self.subgroup_var_page = SubgroupVariablePage(model=model)
        self.setPage(Page_SubgroupVariable, self.subgroup_var_page)
        
        self.setWindowTitle("Subgroup Meta-Analysis")
        
    def nextId_helper(self, page_id):
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
        
    def get_subgroup_variable(self):
        return self.subgroup_var_page.get_subgroup_variable()
    

class BootstrapMetaAnalysisWizard(RegularMetaAnalysisWizard):
    def __init__(self, model, parent=None):
        AbstractMetaAnalysisWizard.__init__(self, model=model, meta_f_str="bootstrap")
        
        # Bootstrap page
        self.bootstrap_page = BootstrapPage(model=model)
        self.setPage(Page_Bootstrap, self.bootstrap_page)
        
        self.setWindowTitle("Cumulative Meta-Analysis")
        
    def nextId_helper(self, page_id):
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
        
    def get_bootstrap_params(self):
        return self.bootstrap_page.get_bootstrap_params()




# if __name__ == '__main__':
#     import sys
# 
#     app = QtGui.QApplication(sys.argv)
#     wizard = MetaAnalysisWizard(parent=None)
#     wizard.show()
#     sys.exit(app.exec_())
