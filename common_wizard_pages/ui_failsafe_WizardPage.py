# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'failsafe_WizardPage.ui'
#
# Created: Fri Dec  6 11:12:21 2013
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
        WizardPage.resize(252, 165)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.method_layout = QtGui.QHBoxLayout()
        self.method_layout.setObjectName(_fromUtf8("method_layout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.method_layout.addItem(spacerItem)
        self.method_lbl = QtGui.QLabel(WizardPage)
        self.method_lbl.setObjectName(_fromUtf8("method_lbl"))
        self.method_layout.addWidget(self.method_lbl)
        self.method_comboBox = QtGui.QComboBox(WizardPage)
        self.method_comboBox.setObjectName(_fromUtf8("method_comboBox"))
        self.method_comboBox.addItem(_fromUtf8(""))
        self.method_comboBox.addItem(_fromUtf8(""))
        self.method_comboBox.addItem(_fromUtf8(""))
        self.method_layout.addWidget(self.method_comboBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.method_layout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.method_layout)
        self.alpha_layout = QtGui.QHBoxLayout()
        self.alpha_layout.setObjectName(_fromUtf8("alpha_layout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.alpha_layout.addItem(spacerItem2)
        self.alpha_lbl = QtGui.QLabel(WizardPage)
        self.alpha_lbl.setStatusTip(_fromUtf8(""))
        self.alpha_lbl.setObjectName(_fromUtf8("alpha_lbl"))
        self.alpha_layout.addWidget(self.alpha_lbl)
        self.alphaSpinBox = QtGui.QDoubleSpinBox(WizardPage)
        self.alphaSpinBox.setDecimals(3)
        self.alphaSpinBox.setMinimum(0.001)
        self.alphaSpinBox.setSingleStep(0.01)
        self.alphaSpinBox.setProperty("value", 0.05)
        self.alphaSpinBox.setObjectName(_fromUtf8("alphaSpinBox"))
        self.alpha_layout.addWidget(self.alphaSpinBox)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.alpha_layout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.alpha_layout)
        self.target_layout = QtGui.QHBoxLayout()
        self.target_layout.setObjectName(_fromUtf8("target_layout"))
        spacerItem4 = QtGui.QSpacerItem(38, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.target_layout.addItem(spacerItem4)
        self.target_lbl = QtGui.QLabel(WizardPage)
        self.target_lbl.setObjectName(_fromUtf8("target_lbl"))
        self.target_layout.addWidget(self.target_lbl)
        self.target_le = QtGui.QLineEdit(WizardPage)
        self.target_le.setMinimumSize(QtCore.QSize(41, 21))
        self.target_le.setMaximumSize(QtCore.QSize(41, 21))
        self.target_le.setObjectName(_fromUtf8("target_le"))
        self.target_layout.addWidget(self.target_le)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.target_layout.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.target_layout)
        self.digits_layout = QtGui.QHBoxLayout()
        self.digits_layout.setObjectName(_fromUtf8("digits_layout"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.digits_layout.addItem(spacerItem6)
        self.digits_lbl = QtGui.QLabel(WizardPage)
        self.digits_lbl.setObjectName(_fromUtf8("digits_lbl"))
        self.digits_layout.addWidget(self.digits_lbl)
        self.digits_SpinBox = QtGui.QSpinBox(WizardPage)
        self.digits_SpinBox.setMinimum(1)
        self.digits_SpinBox.setMaximum(10)
        self.digits_SpinBox.setProperty("value", 4)
        self.digits_SpinBox.setObjectName(_fromUtf8("digits_SpinBox"))
        self.digits_layout.addWidget(self.digits_SpinBox)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.digits_layout.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.digits_layout)
        spacerItem8 = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "Fail-Safe N", None))
        WizardPage.setTitle(_translate("WizardPage", "Fail-Safe N", None))
        WizardPage.setSubTitle(_translate("WizardPage", "Calculate the fail-safe N", None))
        self.method_lbl.setText(_translate("WizardPage", "Method to use:", None))
        self.method_comboBox.setToolTip(_translate("WizardPage", "The Rosenthal method calculates the number of studies averaging null results that would have to be\n"
"added to the given set of observed outcomes to reduce the combined significance level (p-value) to\n"
"a target alpha level (e.g., .05). The calculation is based on Stouffer’s method to combine p-values\n"
"and is described in Rosenthal (1979).\n"
"\n"
"The Orwin method calculates the number of studies averaging null results that would have to be\n"
"added to the given set of observed outcomes to reduce the (unweighted) average effect size to a\n"
"target (unweighted) average effect size. The method is described in Orwin (1983).\n"
"\n"
"The Rosenberg method calculates the number of studies averaging null results that would have to be\n"
"added to the given set of observed outcomes to reduce significance level (p-value) of the (weighted)\n"
"average effect size (based on a fixed-effects model) to a target alpha level (e.g., .05). The method is\n"
"described in Rosenberg (2005).", None))
        self.method_comboBox.setItemText(0, _translate("WizardPage", "Rosenthal", None))
        self.method_comboBox.setItemText(1, _translate("WizardPage", "Orwin", None))
        self.method_comboBox.setItemText(2, _translate("WizardPage", "Rosenberg", None))
        self.alpha_lbl.setText(_translate("WizardPage", "alpha:", None))
        self.alphaSpinBox.setToolTip(_translate("WizardPage", "target alpha level to use for the Rosenthal and Rosenberg methods.", None))
        self.target_lbl.setText(_translate("WizardPage", "target:", None))
        self.target_le.setToolTip(_translate("WizardPage", "target average effect size to use for the Orwin method. If blank, then the target\n"
"average effect size will be equal to the observed average effect size divided by\n"
"2.", None))
        self.digits_lbl.setText(_translate("WizardPage", "digits:", None))
        self.digits_SpinBox.setToolTip(_translate("WizardPage", "an integer specifying the number of decimal places to which the printed results\n"
"should be rounded.", None))

