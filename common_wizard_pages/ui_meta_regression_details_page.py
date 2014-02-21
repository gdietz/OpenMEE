# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meta_regression_details_page.ui'
#
# Created: Fri Feb 21 13:23:15 2014
#      by: PyQt4 UI code generator 4.10.3
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
        WizardPage.resize(477, 217)
        self.verticalLayout_3 = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.model_type_groupBox = QtGui.QGroupBox(WizardPage)
        self.model_type_groupBox.setObjectName(_fromUtf8("model_type_groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.model_type_groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.random_effects_radio_btn = QtGui.QRadioButton(self.model_type_groupBox)
        self.random_effects_radio_btn.setChecked(True)
        self.random_effects_radio_btn.setObjectName(_fromUtf8("random_effects_radio_btn"))
        self.verticalLayout_2.addWidget(self.random_effects_radio_btn)
        self.fixed_effects_radio_btn = QtGui.QRadioButton(self.model_type_groupBox)
        self.fixed_effects_radio_btn.setObjectName(_fromUtf8("fixed_effects_radio_btn"))
        self.verticalLayout_2.addWidget(self.fixed_effects_radio_btn)
        self.horizontalLayout_2.addWidget(self.model_type_groupBox)
        self.random_effects_method_GroupBox = QtGui.QGroupBox(WizardPage)
        self.random_effects_method_GroupBox.setObjectName(_fromUtf8("random_effects_method_GroupBox"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.random_effects_method_GroupBox)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.random_effects_method_ComboBox = QtGui.QComboBox(self.random_effects_method_GroupBox)
        self.random_effects_method_ComboBox.setObjectName(_fromUtf8("random_effects_method_ComboBox"))
        self.random_effects_method_ComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.random_effects_method_ComboBox)
        self.horizontalLayout_2.addWidget(self.random_effects_method_GroupBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.analysis_type_groupBox = QtGui.QGroupBox(WizardPage)
        self.analysis_type_groupBox.setObjectName(_fromUtf8("analysis_type_groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.analysis_type_groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.parametric_radioButton = QtGui.QRadioButton(self.analysis_type_groupBox)
        self.parametric_radioButton.setChecked(True)
        self.parametric_radioButton.setObjectName(_fromUtf8("parametric_radioButton"))
        self.verticalLayout.addWidget(self.parametric_radioButton)
        self.bootstrapped_radioButton = QtGui.QRadioButton(self.analysis_type_groupBox)
        self.bootstrapped_radioButton.setObjectName(_fromUtf8("bootstrapped_radioButton"))
        self.verticalLayout.addWidget(self.bootstrapped_radioButton)
        self.horizontalLayout_4.addWidget(self.analysis_type_groupBox)
        self.output_type_groupBox = QtGui.QGroupBox(WizardPage)
        self.output_type_groupBox.setObjectName(_fromUtf8("output_type_groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.output_type_groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.conditional_means_checkBox = QtGui.QCheckBox(self.output_type_groupBox)
        self.conditional_means_checkBox.setObjectName(_fromUtf8("conditional_means_checkBox"))
        self.verticalLayout_4.addWidget(self.conditional_means_checkBox)
        self.horizontalLayout_4.addWidget(self.output_type_groupBox)
        self.conf_level_groupBox = QtGui.QGroupBox(WizardPage)
        self.conf_level_groupBox.setObjectName(_fromUtf8("conf_level_groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.conf_level_groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.conf_level_spinbox = QtGui.QDoubleSpinBox(self.conf_level_groupBox)
        self.conf_level_spinbox.setDecimals(1)
        self.conf_level_spinbox.setMinimum(70.0)
        self.conf_level_spinbox.setMaximum(99.9)
        self.conf_level_spinbox.setSingleStep(0.1)
        self.conf_level_spinbox.setProperty("value", 95.0)
        self.conf_level_spinbox.setObjectName(_fromUtf8("conf_level_spinbox"))
        self.horizontalLayout.addWidget(self.conf_level_spinbox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout_4.addWidget(self.conf_level_groupBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.phylogen_checkBox = QtGui.QCheckBox(WizardPage)
        self.phylogen_checkBox.setObjectName(_fromUtf8("phylogen_checkBox"))
        self.verticalLayout_3.addWidget(self.phylogen_checkBox)
        spacerItem3 = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.model_type_groupBox.setTitle(_translate("WizardPage", "Model Type", None))
        self.random_effects_radio_btn.setText(_translate("WizardPage", "random effects", None))
        self.fixed_effects_radio_btn.setText(_translate("WizardPage", "fixed effects", None))
        self.random_effects_method_GroupBox.setTitle(_translate("WizardPage", "Random Effects Method", None))
        self.random_effects_method_ComboBox.setItemText(0, _translate("WizardPage", "clear and then populate me", None))
        self.analysis_type_groupBox.setTitle(_translate("WizardPage", "Type of Analysis", None))
        self.parametric_radioButton.setText(_translate("WizardPage", "Parametric", None))
        self.bootstrapped_radioButton.setText(_translate("WizardPage", "Bootstrapped", None))
        self.output_type_groupBox.setTitle(_translate("WizardPage", "Output Type", None))
        self.conditional_means_checkBox.setText(_translate("WizardPage", "Conditional Means", None))
        self.conf_level_groupBox.setTitle(_translate("WizardPage", "Confidence Level", None))
        self.conf_level_spinbox.setSuffix(_translate("WizardPage", " %", None))
        self.phylogen_checkBox.setToolTip(_translate("WizardPage", "if checked, you will be asked to provide a phylogenetic tree", None))
        self.phylogen_checkBox.setText(_translate("WizardPage", "Use phylogenetic correlations?", None))

