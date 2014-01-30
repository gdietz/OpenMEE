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
        
    #def output # how to send this to R?