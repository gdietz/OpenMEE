# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mice_parameters_page.ui'
#
# Created: Fri Mar  7 09:30:08 2014
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
        WizardPage.resize(391, 288)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(WizardPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.m_spinBox = QtGui.QSpinBox(WizardPage)
        self.m_spinBox.setMinimum(1)
        self.m_spinBox.setMaximum(20)
        self.m_spinBox.setProperty("value", 5)
        self.m_spinBox.setObjectName(_fromUtf8("m_spinBox"))
        self.horizontalLayout.addWidget(self.m_spinBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtGui.QLabel(WizardPage)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.maxit_spinBox = QtGui.QSpinBox(WizardPage)
        self.maxit_spinBox.setMinimum(1)
        self.maxit_spinBox.setMaximum(20)
        self.maxit_spinBox.setProperty("value", 5)
        self.maxit_spinBox.setObjectName(_fromUtf8("maxit_spinBox"))
        self.horizontalLayout_2.addWidget(self.maxit_spinBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.defaultMethod_groupBox = QtGui.QGroupBox(WizardPage)
        self.defaultMethod_groupBox.setObjectName(_fromUtf8("defaultMethod_groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.defaultMethod_groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.defaultMethod_groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.numeric_comboBox = QtGui.QComboBox(self.defaultMethod_groupBox)
        self.numeric_comboBox.setObjectName(_fromUtf8("numeric_comboBox"))
        self.gridLayout.addWidget(self.numeric_comboBox, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.defaultMethod_groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.factor_2_levels_comboBox = QtGui.QComboBox(self.defaultMethod_groupBox)
        self.factor_2_levels_comboBox.setObjectName(_fromUtf8("factor_2_levels_comboBox"))
        self.gridLayout.addWidget(self.factor_2_levels_comboBox, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.defaultMethod_groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.factor_gt_2_levels_comboBox = QtGui.QComboBox(self.defaultMethod_groupBox)
        self.factor_gt_2_levels_comboBox.setObjectName(_fromUtf8("factor_gt_2_levels_comboBox"))
        self.gridLayout.addWidget(self.factor_gt_2_levels_comboBox, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.defaultMethod_groupBox)
        spacerItem2 = QtGui.QSpacerItem(20, 50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.label.setText(_translate("WizardPage", "# of multiple imputations:", None))
        self.label_5.setText(_translate("WizardPage", "# of iterations:", None))
        self.defaultMethod_groupBox.setTitle(_translate("WizardPage", "Imputation Methods", None))
        self.label_2.setText(_translate("WizardPage", "numeric covariates:", None))
        self.label_3.setText(_translate("WizardPage", "categorical with 2 levels:", None))
        self.label_4.setText(_translate("WizardPage", "categorical with \n"
"more than 2 levels:", None))

