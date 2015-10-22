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
#from common_wizard_pages.failsafe_page import FailsafeWizardPage
#from common_wizard_pages.funnel_page import FunnelPage

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MethodsAndParameters, Page_Summary, Page_Failsafe,
Page_FunnelParameters) = range(7)

# map page keys (from R) to wizard page ids
pageid = {
    'DATALOCATION': Page_DataLocation,
    'REFINESTUDIES': Page_RefineStudies,
    'SUMMARY': Page_Summary
}

class DynamicWizard(QtGui.QWizard):
    def __init__(self, model, wizard_parameters, parent=None):
        super(DynamicWizard, self).__init__(parent)

        self.model = model
        self.wizard_parameters = wizard_parameters

        self.setWindowTitle(self.wizard_parameters['WIZARD.WINDOW.TITLE'])
        self.setWizardStyle(QWizard.ClassicStyle)

        self._create_wizard_pages()
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()

    def _create_wizard_pages(self):
        '''
        Initialize wizard pages specified by wizard parameters
        '''

        print "wizard parameters: %s" % str(self.wizard_parameters)

        for page_key, page_parameters in self.wizard_parameters['WIZARD.PAGES'].items():
            page_arguments = {}
            print "page key: %s, page parameters: %s" % (page_key, str(page_parameters))
            if page_key == 'DATALOCATION':
                if 'SHOW.RAW.DATA' in page_parameters:
                    page_arguments['show_raw_data'] = page_parameters['SHOW.RAW.DATA']
                    print "Page arguments: %s" % str(page_arguments)
                self.data_location_page = DataLocationPage(model=self.model, **page_arguments)
                self.setPage(Page_DataLocation, self.data_location_page)
            elif page_key == 'REFINESTUDIES':
                self.refine_studies_page = RefineStudiesPage(model=self.model)
                self.setPage(Page_RefineStudies, self.refine_studies_page)
            elif page_key == 'SUMMARY':
                self.summary_page = SummaryPage()
                self.setPage(Page_Summary, self.summary_page)

    def nextId(self):
        page_id = self.currentId()
        
        return self.next_id_helper(page_id)
        
    def next_id_helper(self, page_id):
        pages = self.wizard_parameters['WIZARD.PAGES'].keys() # pages in order
        pageids = [pageid[pagekey] for pagekey in pages]

        currentpageindex = pageids.index(page_id)

        if currentpageindex == len(pageids) - 1:
            # End wizard if on last page
            return -1

        # go to next page
        return pageids[currentpageindex+1]

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
        return wizard_summary(wizard=self, next_id_helper=self.next_id_helper,
                              summary_page_id=Page_Summary,
                              analysis_label="Failsafe Analysis")

    def save_selections(self): # returns a bool
        # Should the selections be saved? 
        return self.summary_page.save_selections()
