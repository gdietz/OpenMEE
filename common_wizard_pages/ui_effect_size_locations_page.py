# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'effect_size_locations_page.ui'
#
# Created: Tue Aug 27 16:49:55 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_wizardPage(object):
    def setupUi(self, wizardPage):
        wizardPage.setObjectName(_fromUtf8("wizardPage"))
        wizardPage.resize(498, 195)
        self.verticalLayout_3 = QtGui.QVBoxLayout(wizardPage)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_6 = QtGui.QLabel(wizardPage)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_3.addWidget(self.label_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.trans_grp_box = QtGui.QGroupBox(wizardPage)
        self.trans_grp_box.setObjectName(_fromUtf8("trans_grp_box"))
        self.gridLayout = QtGui.QGridLayout(self.trans_grp_box)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.trans_var_cbo_box = QtGui.QComboBox(self.trans_grp_box)
        self.trans_var_cbo_box.setObjectName(_fromUtf8("trans_var_cbo_box"))
        self.gridLayout.addWidget(self.trans_var_cbo_box, 1, 1, 1, 1)
        self.trans_effect_cbo_box = QtGui.QComboBox(self.trans_grp_box)
        self.trans_effect_cbo_box.setObjectName(_fromUtf8("trans_effect_cbo_box"))
        self.gridLayout.addWidget(self.trans_effect_cbo_box, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.trans_grp_box)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.trans_grp_box)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.trans_grp_box)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.raw_grp_box = QtGui.QGroupBox(wizardPage)
        self.raw_grp_box.setObjectName(_fromUtf8("raw_grp_box"))
        self.gridLayout_3 = QtGui.QGridLayout(self.raw_grp_box)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_3 = QtGui.QLabel(self.raw_grp_box)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.raw_effect_cbo_box = QtGui.QComboBox(self.raw_grp_box)
        self.raw_effect_cbo_box.setObjectName(_fromUtf8("raw_effect_cbo_box"))
        self.gridLayout_3.addWidget(self.raw_effect_cbo_box, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.raw_grp_box)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.raw_lower_cbo_box = QtGui.QComboBox(self.raw_grp_box)
        self.raw_lower_cbo_box.setObjectName(_fromUtf8("raw_lower_cbo_box"))
        self.gridLayout_3.addWidget(self.raw_lower_cbo_box, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.raw_grp_box)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)
        self.raw_upper_cbo_box = QtGui.QComboBox(self.raw_grp_box)
        self.raw_upper_cbo_box.setObjectName(_fromUtf8("raw_upper_cbo_box"))
        self.gridLayout_3.addWidget(self.raw_upper_cbo_box, 2, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.raw_grp_box)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(wizardPage)
        QtCore.QMetaObject.connectSlotsByName(wizardPage)

    def retranslateUi(self, wizardPage):
        wizardPage.setWindowTitle(_translate("wizardPage", "WizardPage", None))
        wizardPage.setTitle(_translate("wizardPage", "Effect Size Column Locations", None))
        self.label_6.setText(_translate("wizardPage", "Where is your data located?", None))
        self.trans_grp_box.setTitle(_translate("wizardPage", "Transformed Scale", None))
        self.label.setText(_translate("wizardPage", "Effect Size:", None))
        self.label_2.setText(_translate("wizardPage", "Variance:", None))
        self.raw_grp_box.setTitle(_translate("wizardPage", "Raw Scale", None))
        self.label_3.setText(_translate("wizardPage", "Effect Size:", None))
        self.label_4.setText(_translate("wizardPage", "CI Lower Bound:", None))
        self.label_5.setText(_translate("wizardPage", "CI Upper Bound:", None))

