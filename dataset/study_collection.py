#########################
#                       #
# Author: George Dietz  #
#                       #
#########################

from study import Study
from managed_collection import ManagedCollection

from globals import *


class StudyCollection(ManagedCollection):
    # Holds a collection of studies
    
    def __init__(self):
        super(StudyCollection, self).__init__(Study)
        
    def data_item_name(self, plural=False):
        if plural:
            return "studies"
        return "study"
    
    def get_studies_with_variable(self, var):
        studylist = []
        for study in self.get_items():
            if study.get_var(var) != None:
                studylist.append(study)
        return studylist