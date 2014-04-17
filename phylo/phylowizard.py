'''
Created on Jan 10, 2014

@author: George
'''


from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from tree_page import TreePage
from phylo_model_design_page import PhyloModelDesignPage
from phylo_analysis_details_page import PhyloAnalysisDetailsPage
from ma_wizards import AbstractMetaAnalysisWizard
from common_wizard_pages.refine_studies_page import RefineStudiesPage

from ome_globals import wizard_summary

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MethodsAndParameters, Page_SubgroupVariable, Page_Bootstrap,
Page_Summary, Page_TreePage, Page_PhyloModelDesignPage, Page_Parameters) = range(10)

class PhyloMAWizard(AbstractMetaAnalysisWizard):
    def __init__(self, model, parent=None):
        AbstractMetaAnalysisWizard.__init__(self, model=model, meta_f_str=None, parent=parent)
        
        self.analysis_label = "Phylogenetic Meta Analysis"
        self.setWindowTitle(self.analysis_label)
        
        
        # Refine studies page
        self.removePage(Page_RefineStudies)
        self.refine_studies_page = RefineStudiesPage(model=model, need_species=True)
        self.setPage(Page_RefineStudies, self.refine_studies_page)
        
        # Tree selection page
        self.tree_page = TreePage()
        self.setPage(Page_TreePage, self.tree_page)
        
        # phylogenetic model design page
        self.phylo_model_design_page = PhyloModelDesignPage()
        self.setPage(Page_PhyloModelDesignPage, self.phylo_model_design_page)
        
        # data location page and parameters page
        self.parameters_page = PhyloAnalysisDetailsPage(model=model, default_method="REML")
        self.setPage(Page_Parameters, self.parameters_page)
        
    def nextId_helper(self, page_id):

        if page_id == Page_ChooseEffectSize:
            return Page_Parameters
        elif page_id == Page_Parameters:
            return Page_RefineStudies
        elif page_id == Page_RefineStudies:
            return Page_TreePage
        elif page_id == Page_TreePage:
            return Page_PhyloModelDesignPage
        elif page_id == Page_PhyloModelDesignPage:
            return Page_Summary
        elif page_id == Page_Summary:
            return -1
        
    # Summary Page
    def get_summary(self):
        ''' Make a summary string to show the user at the end of the wizard summarizing most of the user selections '''
        return wizard_summary(wizard=self, next_id_helper=self.nextId_helper,
                              summary_page_id=Page_Summary,
                              analysis_label=self.analysis_label)
    
    ##### getters #####
        
    def get_tree_and_filename(self):
        return self.tree_page.get_tree_and_filename()
    
    def get_tree(self):
        tree = self.get_tree_and_filename()['tree']
        return tree
    
    ### Phylo Model Design Page ####
    def get_phylo_model_type(self): # BM or OU
        return self.phylo_model_design_page.get_phylo_model_type()
        
    def get_lambda(self):
        return self.phylo_model_design_page.get_lambda()
    def get_alpha(self):
        return self.phylo_model_design_page.get_alpha()
    
    def get_randomly_resolve_polytomies(self):
        return self.phylo_model_design_page.get_randomly_resolve_polytomies()
    
    ### phylo meta-analysis details page ####
    def get_data_location(self):
        return self.parameters_page.get_data_location()
    
    def get_random_effects_method(self):
        return self.parameters_page.get_random_effects_method()
    
    def get_conf_level(self):
        return self.parameters_page.get_conf_level()
    
    def get_include_species_as_random_factor(self):
        return self.parameters_page.get_include_species_as_random_factor()
    
    def get_plot_params(self):
        return self.parameters_page.get_plot_params()
    