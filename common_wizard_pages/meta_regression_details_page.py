from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import ui_meta_regression_details_page

class MetaRegDetailsPage(QWizardPage, ui_meta_regression_details_page.Ui_WizardPage):
    def __init__(self, model,
                 previously_included_covs = [],
                 fixed_effects=True,
                 conf_level=95,
                 random_effects_method = "DL",
                 need_categorical = False, # need at least one categorical variable?
                 parent=None): # todo: set defaults of previous parameters to None
        super(MetaRegDetailsPage, self).__init__(parent)
        self.setupUi(self)