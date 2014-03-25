# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meta_analysis_parameters_page.ui'
#
# Created: Tue Mar 25 08:41:27 2014
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
        WizardPage.resize(411, 212)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(WizardPage)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.random_effects_radio_btn = QtGui.QRadioButton(self.groupBox_3)
        self.random_effects_radio_btn.setChecked(True)
        self.random_effects_radio_btn.setObjectName(_fromUtf8("random_effects_radio_btn"))
        self.verticalLayout_3.addWidget(self.random_effects_radio_btn)
        self.fixed_effects_radio_btn = QtGui.QRadioButton(self.groupBox_3)
        self.fixed_effects_radio_btn.setObjectName(_fromUtf8("fixed_effects_radio_btn"))
        self.verticalLayout_3.addWidget(self.fixed_effects_radio_btn)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.verticalLayout_3)
        self.random_effects_label = QtGui.QLabel(self.groupBox_3)
        self.random_effects_label.setObjectName(_fromUtf8("random_effects_label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.random_effects_label)
        self.random_effects_method_ComboBox = QtGui.QComboBox(self.groupBox_3)
        self.random_effects_method_ComboBox.setObjectName(_fromUtf8("random_effects_method_ComboBox"))
        self.random_effects_method_ComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.random_effects_method_ComboBox)
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.conf_level_spinbox = QtGui.QDoubleSpinBox(self.groupBox_3)
        self.conf_level_spinbox.setEnabled(False)
        self.conf_level_spinbox.setDecimals(1)
        self.conf_level_spinbox.setMinimum(70.0)
        self.conf_level_spinbox.setMaximum(99.9)
        self.conf_level_spinbox.setSingleStep(0.1)
        self.conf_level_spinbox.setProperty("value", 95.0)
        self.conf_level_spinbox.setObjectName(_fromUtf8("conf_level_spinbox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.conf_level_spinbox)
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.digits_spinBox = QtGui.QSpinBox(self.groupBox_3)
        self.digits_spinBox.setMinimum(1)
        self.digits_spinBox.setMaximum(10)
        self.digits_spinBox.setProperty("value", 3)
        self.digits_spinBox.setObjectName(_fromUtf8("digits_spinBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.digits_spinBox)
        self.knha_checkBox = QtGui.QCheckBox(self.groupBox_3)
        self.knha_checkBox.setObjectName(_fromUtf8("knha_checkBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.knha_checkBox)
        self.verticalLayout.addWidget(self.groupBox_3)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        WizardPage.setToolTip(_translate("WizardPage", "The confidence level is set on the main toolbar", None))
        self.groupBox_3.setTitle(_translate("WizardPage", "Analysis Details", None))
        self.label_2.setText(_translate("WizardPage", "Model Type:", None))
        self.random_effects_radio_btn.setText(_translate("WizardPage", "random effects", None))
        self.fixed_effects_radio_btn.setText(_translate("WizardPage", "fixed effects", None))
        self.random_effects_label.setText(_translate("WizardPage", "Random Effects Method:", None))
        self.random_effects_method_ComboBox.setItemText(0, _translate("WizardPage", "clear and then populate me", None))
        self.label_4.setText(_translate("WizardPage", "Confidence Level", None))
        self.conf_level_spinbox.setToolTip(_translate("WizardPage", "Global confidence level set on main toolbar", None))
        self.conf_level_spinbox.setSuffix(_translate("WizardPage", " %", None))
        self.label_5.setText(_translate("WizardPage", "digits:", None))
        self.knha_checkBox.setToolTip(_translate("WizardPage", "Should the method by Knapp and Hartung (2003) be used for adjusting test statistics and confidence intervals?", None))
        self.knha_checkBox.setText(_translate("WizardPage", "Knapp and Hartung adjustment", None))

