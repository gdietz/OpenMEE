'''
Created on Jan 11, 2014

@author: George
'''

class Interaction:
    def __init__(self, list_of_vars):
        self.combination = set(list_of_vars)
        
    def __str__(self):
        covs_in_order = sorted(self.combination, key=lambda cov: cov.get_label())
        cov_labels = [cov.get_label() for cov in covs_in_order]
        
        return "*".join(cov_labels)
    
    def __eq__(self, otherInteraction):
        return self.combination == otherInteraction.combination
    
    def __contains__(self, var):
        return var in self.combination
    
    def get_vars(self):
        # sorted list of the interaction covariates (alphabetically)
        return sorted(list(self.combination), key=lambda x: x.get_label())
    
    def r_colon_name(self):
        # name of the interaction with colon separtion (for putting in to a model formula in R)
        # e.g. A:B
        return ":".join([cov.get_label() for cov in self.get_vars()])
    def r_vector_of_covs(self):
        # R code for string vector of covs
        # e.g. c("A","B")
        quoted_names = ["\"%s\"" % cov for cov in self.get_vars()]
        return "c(%s)" % ", ".join(quoted_names)