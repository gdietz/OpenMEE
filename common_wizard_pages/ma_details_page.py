from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import ui_ma_details_page

class MADetailsPage(QWizardPage, ui_ma_details_page.Ui_WizardPage):
    def __init__(self, parent=None):
        super(MADetailsPage, self).__init__(parent)
        self.setupUi(self)

    def initializePage(self):
        self.populate_random_effects_method_choices()

    def populate_random_effects_method_choices(self):
        self.rand_effects_method_cbo_box.clear()
        
        for short_name, pretty_name in RANDOM_EFFECTS_METHODS_TO_PRETTY_STRS.items():
            self.rand_effects_method_cbo_box.addItem(
                        pretty_name,
                        userData=QVariant(short_name))
        # set current index to that of default method
        idx = self.rand_effects_method_cbo_box.findData(QVariant(DEFAULT_RANDOM_EFFECTS_METHOD))
        self.rand_effects_method_cbo_box.setCurrentIndex(idx)

    #### getters ####
    def get_method(self):
        if self.fixed_effects_radio_btn.isChecked():
            return FIXED_EFFECTS_METHOD_STR
        else:
            return self.get_random_effects_method()

    def get_using_fixed_effects(self):
        return self.get_method() == FIXED_EFFECTS_METHOD_STR

    def get_random_effects_method(self):
        current_index = self.rand_effects_method_cbo_box.currentIndex()
        current_data = self.rand_effects_method_cbo_box.itemData(current_index)
        method = str(current_data.toString())
        return method

    def get_intercept(self):
        return self.intercept_chkbox.isChecked()

    def get_weighted_least_squares(self):
        return self.weighted_chkbox.isChecked()

    def get_knha(self):
        return self.knha_chkbox.isChecked()

    def get_confidence_level(self):
        return self.level_spinbox.value()

    def get_digits(self):
        return self.digits_spinBox.value()
        self.dig

    ########################################

    def __str__(self):
        fixed_effects_str = "Using Fixed Effects" if self.get_using_fixed_effects() else "Using Random Effects"
        random_effects_method_str = "Random Effects Method: %s" % self.get_random_effects_method()
        effects_str = fixed_effects_str if self.get_using_fixed_effects() else fixed_effects_str+"\n"+random_effects_method_str
        conf_level_str = "Confidence Level: %s" % (str(self.get_confidence_level()) + "%")
        intercept_str = "Add intercept to model: " + "yes" if self.get_intercept() else "no"
        weighted_str = "Using " + ("weighted" if self.get_weighted_least_squares() else "unweighted") + "least squares"
        knha_str = "Using Knapp and Hartung method: " + "yes" if self.get_knha() else "no"
        digits_str = "%d digits in output" % self.get_digits()

        summary = "Meta Regression Details:\n" + "\n".join([
            effects_str,
            conf_level_str,
            intercept_str,
            weighted_str,
            knha_str,
            digits_str,
        ])
        return summary
    