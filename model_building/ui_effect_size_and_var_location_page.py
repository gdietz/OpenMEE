# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'effect_size_and_var_location_page.ui'
#
# Created: Sun Jan 12 17:58:49 2014
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
        WizardPage.resize(218, 126)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(WizardPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.effect_size_comboBox = QtGui.QComboBox(WizardPage)
        self.effect_size_comboBox.setObjectName(_fromUtf8("effect_size_comboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.effect_size_comboBox)
        self.label_2 = QtGui.QLabel(WizardPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.variance_comboBox = QtGui.QComboBox(WizardPage)
        self.variance_comboBox.setObjectName(_fromUtf8("variance_comboBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.variance_comboBox)
        self.horizontalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 49, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        WizardPage.setTitle(_translate("WizardPage", "Effect Size and Variance Location", None))
        WizardPage.setSubTitle(_translate("WizardPage", "Where are the effect sizes and variances?", None))
        self.label.setText(_translate("WizardPage", "Effect Size", None))
        self.label_2.setText(_translate("WizardPage", "Variance", None))

