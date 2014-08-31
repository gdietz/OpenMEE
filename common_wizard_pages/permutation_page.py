from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import ui_permutation_details_page

class PermuationPage(QWizardPage, ui_permutation_details_page.Ui_WizardPage):
    def __init__(self, parent=None):
        super(PermuationPage, self).__init__(parent)
        self.setupUi(self)

    #### getters ####

    def get_choices(self):
        choices = {
            'exact':self.exact_checkBox.isChecked(),
            'iter':self.iter_spinBox.value(),
            'digits':self.digits_spinBox.value(),
            'retpermdist':self.retpermdist_checkBox.isChecked(),
            'make_histograms':self.perm_dist_hist_checkBox.isChecked()
        }
        return choices

    ########################################

    def __str__(self):
        choices = self.get_choices()

        if choices['exact']:
            iterations_str = "Peforming an exact permuation test."
        else:
            iterations_str = "Doing %d iterations." % choices['iter']
        digits_str = "%d digits in output" % choices['digits']
        permdist_str = "Displaying permuation distribution." if choices['retpermdist'] else ""
        hist_str = "Making histograms of permuation distributions for test statistics" if choices['make_histograms'] else ""

        # Collect all strings which are not empty
        detail_strs = [iterations_str, digits_str, permdist_str, hist_str]
        details = [x for x in detail_strs if x != ""]
        summary = "Permutation Test Details:\n" + "\n".join(details)
        return summary
    