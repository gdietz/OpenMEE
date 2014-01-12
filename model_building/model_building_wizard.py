'''
Created on Jan 11, 2014

@author: George
'''

# Pages:
# 1) Specify saturated model covariates and add interaction terms
# 2) Specify models by on a dialog. The models will show up in a list on the
#    left. There will be a button "new model" which will pop-up a dialog which
#    prompts the user for a name and which covariates and interaction terms
#    will be used. The combination of covariates and interaction terms must be
#    unique for each model. Also, each subsequent model must be a subset of the
#    previous model
# 3) The rest will be like the meta-regression wizard but:
#    a) The list of available studies to include will be filtered by those that
#       have data for all the covariates specified.
#    b) The "Select covariates for regression" page will not be present. (The
#       params previously specified there (conf. level and fixed vs. random
#       effects will be found on page #2 (the specify models dialog)
#
# 4) The rest will be like the normal meta-regression wizard
#
# 
#
# Results:
#   Option A: Show results in a table (see jessica email) with each successive
#     model i.e. the reverse of the order that they were entered.
#
#
#   Option B: For all possible combinations: (NO LONGER GOING TO IMPLEMENT, for now ....)
# A lower-triangular table labeled with model names on each axis. The main
# diagonal will be blank. Clicking a square will show the results output on the
# right hand side of the dialog. (exportable like the results_window)
#