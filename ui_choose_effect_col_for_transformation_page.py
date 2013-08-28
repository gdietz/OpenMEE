# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_effect_size_for_transformation_page.ui'
#
# Created: Wed Aug 28 14:04:30 2013
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
        WizardPage.resize(301, 126)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(WizardPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboBox = QtGui.QComboBox(WizardPage)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(WizardPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.current_scale_lbl = QtGui.QLabel(WizardPage)
        self.current_scale_lbl.setObjectName(_fromUtf8("current_scale_lbl"))
        self.gridLayout.addWidget(self.current_scale_lbl, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(WizardPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.new_scale_lbl = QtGui.QLabel(WizardPage)
        self.new_scale_lbl.setObjectName(_fromUtf8("new_scale_lbl"))
        self.gridLayout.addWidget(self.new_scale_lbl, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.label.setText(_translate("WizardPage", "Which Effect Size do you want to transform?", None))
        self.label_2.setText(_translate("WizardPage", "Current Scale:", None))
        self.current_scale_lbl.setText(_translate("WizardPage", "scale now", None))
        self.label_3.setText(_translate("WizardPage", "New scale: ", None))
        self.new_scale_lbl.setText(_translate("WizardPage", "new scale", None))

