# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_column_group_transform_effect_page.ui'
#
# Created: Fri Aug 30 10:56:09 2013
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

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName(_fromUtf8("WizardPage"))
        WizardPage.resize(449, 462)
        self.verticalLayout_4 = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.trans_layout = QtGui.QVBoxLayout()
        self.trans_layout.setObjectName(_fromUtf8("trans_layout"))
        self.trans_grp_box = QtGui.QGroupBox(WizardPage)
        self.trans_grp_box.setObjectName(_fromUtf8("trans_grp_box"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.trans_grp_box)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(self.trans_grp_box)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.trans_grp_box)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.trans_effect_cbo_box = QtGui.QComboBox(self.trans_grp_box)
        self.trans_effect_cbo_box.setEnabled(True)
        self.trans_effect_cbo_box.setObjectName(_fromUtf8("trans_effect_cbo_box"))
        self.gridLayout.addWidget(self.trans_effect_cbo_box, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.trans_grp_box)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.trans_var_cbo_box = QtGui.QComboBox(self.trans_grp_box)
        self.trans_var_cbo_box.setObjectName(_fromUtf8("trans_var_cbo_box"))
        self.gridLayout.addWidget(self.trans_var_cbo_box, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.trans_layout.addWidget(self.trans_grp_box)
        self.verticalLayout_4.addLayout(self.trans_layout)
        self.raw_layout = QtGui.QVBoxLayout()
        self.raw_layout.setObjectName(_fromUtf8("raw_layout"))
        self.raw_grp_box = QtGui.QGroupBox(WizardPage)
        self.raw_grp_box.setEnabled(True)
        self.raw_grp_box.setObjectName(_fromUtf8("raw_grp_box"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.raw_grp_box)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_4 = QtGui.QLabel(self.raw_grp_box)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.raw_effect_cbo_box = QtGui.QComboBox(self.raw_grp_box)
        self.raw_effect_cbo_box.setObjectName(_fromUtf8("raw_effect_cbo_box"))
        self.gridLayout_2.addWidget(self.raw_effect_cbo_box, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.raw_grp_box)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.raw_lower_cbo_box = QtGui.QComboBox(self.raw_grp_box)
        self.raw_lower_cbo_box.setObjectName(_fromUtf8("raw_lower_cbo_box"))
        self.gridLayout_2.addWidget(self.raw_lower_cbo_box, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.raw_grp_box)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.raw_upper_cbo_box = QtGui.QComboBox(self.raw_grp_box)
        self.raw_upper_cbo_box.setObjectName(_fromUtf8("raw_upper_cbo_box"))
        self.gridLayout_2.addWidget(self.raw_upper_cbo_box, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.raw_grp_box)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.raw_layout.addWidget(self.raw_grp_box)
        self.verticalLayout_4.addLayout(self.raw_layout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_8 = QtGui.QLabel(WizardPage)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout.addWidget(self.label_8)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_9 = QtGui.QLabel(WizardPage)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout.addWidget(self.label_9)
        self.metric_cbo_box = QtGui.QComboBox(WizardPage)
        self.metric_cbo_box.setObjectName(_fromUtf8("metric_cbo_box"))
        self.horizontalLayout.addWidget(self.metric_cbo_box)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.trans_grp_box.setTitle(_translate("WizardPage", "Transformed Scale", None))
        self.label.setText(_translate("WizardPage", "The Effect Column you chose has not yet been associated with a variance. Please select the variance column now.", None))
        self.label_2.setText(_translate("WizardPage", "Effect Size:", None))
        self.label_3.setText(_translate("WizardPage", "Variance:", None))
        self.raw_grp_box.setTitle(_translate("WizardPage", "Raw Scale", None))
        self.label_4.setText(_translate("WizardPage", "The Effect column you chose has not yet been associated with upper or lower bounds for the confidence interval. Please select these columns now.", None))
        self.label_6.setText(_translate("WizardPage", "CI Lower Bound:", None))
        self.label_5.setText(_translate("WizardPage", "Effect Size:", None))
        self.label_7.setText(_translate("WizardPage", "CI Upper Bound:", None))
        self.label_8.setText(_translate("WizardPage", "What is the metric corresponding to this effect size?", None))
        self.label_9.setText(_translate("WizardPage", "Metric:", None))

