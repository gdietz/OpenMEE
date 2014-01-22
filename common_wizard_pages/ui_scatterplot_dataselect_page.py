# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scatterplot_dataselect_page.ui'
#
# Created: Mon Jan  6 11:30:46 2014
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
        WizardPage.resize(219, 74)
        self.formLayout = QtGui.QFormLayout(WizardPage)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(WizardPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.x_cbo_box = QtGui.QComboBox(WizardPage)
        self.x_cbo_box.setObjectName(_fromUtf8("x_cbo_box"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.x_cbo_box)
        self.label_2 = QtGui.QLabel(WizardPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.y_cbo_box = QtGui.QComboBox(WizardPage)
        self.y_cbo_box.setObjectName(_fromUtf8("y_cbo_box"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.y_cbo_box)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.label.setText(_translate("WizardPage", "horizontal data:", None))
        self.label_2.setText(_translate("WizardPage", "vertical data:", None))

