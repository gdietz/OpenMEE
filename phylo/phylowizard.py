'''
Created on Jan 10, 2014

@author: George
'''


from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from tree_page import TreePage
from phylo_model_design_page import PhyloModelDesignPage
from ma_wizards import AbstractMetaAnalysisWizard

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MethodsAndParameters, Page_SubgroupVariable, Page_Bootstrap,
Page_Summary, Page_TreePage, Page_PhyloModelDesignPage, Page_Parameters) = range(10)

class PhyloWizard(AbstractMetaAnalysisWizard):
    def __init__(self, model, parent=None):
        AbstractMetaAnalysisWizard.__init__(self, model=model, meta_f_str=None, parent=parent)
        
        self.setWindowTitle("Phylogenetic Meta Analysis")
        
        # Tree selection page
        self.tree_page = TreePage()
        self.setPage(Page_TreePage, self.tree_page)
        
        # phylogenetic model design page
        self.phylo_model_design_page = PhyloModelDesignPage()
        self.setPage(Page_PhyloModelDesignPage, self.phylo_model_design_page)
        
        # data location page
        # TODO: make user choose a column for species (categorical)
        
        # Parameters page
        # TODO: (make page similiar to meta-reg details page (with limited selections for method just FE, ML, and REML)

    def nextID(self):
        if self.currentId() == Page_TreePage:
            return Page_PhyloModelDesignPage
        elif self.currentId() == Page_PhyloModelDesignPage:
            return -1
        
    def nextId_helper(self, page_id):
        if page_id == Page_ChooseEffectSize:
            return Page_DataLocation
        elif page_id == Page_DataLocation:
            return Page_RefineStudies
        elif page_id == Page_RefineStudies:
            return Page
        #    return Page_MethodsAndParameters
        #elif page_id == Page_MethodsAndParameters:
        #    return Page_Summary
        elif page_id == Page_Summary:
            return -1
        
    #def get_phylo_object(self):
    #    return self.tree_page.get_phylo_object()
    
    def get_tree_and_filename(self):
        return self.tree_page.get_tree_and_filename()