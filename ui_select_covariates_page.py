# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_covariates_page.ui'
#
# Created: Mon Aug 26 13:25:54 2013
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
        WizardPage.resize(317, 328)
        self.verticalLayout_4 = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_2 = QtGui.QLabel(WizardPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_4.addWidget(self.label_2)
        self.groupBox = QtGui.QGroupBox(WizardPage)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.covariate_listWidget = QtGui.QListWidget(self.groupBox)
        self.covariate_listWidget.setObjectName(_fromUtf8("covariate_listWidget"))
        self.verticalLayout_3.addWidget(self.covariate_listWidget)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.line = QtGui.QFrame(WizardPage)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_4.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
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
        self.horizontalLayout.addWidget(self.model_type_groupBox)
        self.groupBox_2 = QtGui.QGroupBox(WizardPage)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.conf_level_spinbox = QtGui.QDoubleSpinBox(self.groupBox_2)
        self.conf_level_spinbox.setDecimals(1)
        self.conf_level_spinbox.setMinimum(70.0)
        self.conf_level_spinbox.setMaximum(99.9)
        self.conf_level_spinbox.setSingleStep(0.1)
        self.conf_level_spinbox.setProperty("value", 95.0)
        self.conf_level_spinbox.setObjectName(_fromUtf8("conf_level_spinbox"))
        self.verticalLayout.addWidget(self.conf_level_spinbox)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.label_2.setText(_translate("WizardPage", "Select covariates for regression:", None))
        self.groupBox.setTitle(_translate("WizardPage", "available covariates", None))
        self.model_type_groupBox.setTitle(_translate("WizardPage", "Model Type", None))
        self.random_effects_radio_btn.setText(_translate("WizardPage", "random effects", None))
        self.fixed_effects_radio_btn.setText(_translate("WizardPage", "fixed effects", None))
        self.groupBox_2.setTitle(_translate("WizardPage", "Confidence Level", None))
        self.conf_level_spinbox.setSuffix(_translate("WizardPage", " %", None))

