'''
Created on Jan 11, 2014

@author: George
'''

class Interaction:
    def __init__(self, list_of_vars):
        self.combination = set(list_of_vars)
        
    def __str__(self):
        covs_in_order = sorted(self.combination, key=lambda cov: cov.get_label())
        return "*".join(covs_in_order)
        
    #def output # how should send this to R?