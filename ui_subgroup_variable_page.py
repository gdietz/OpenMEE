# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subgroup_variable_page.ui'
#
# Created: Wed Aug 14 14:00:12 2013
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

class Ui_subgroup_variable_page(object):
    def setupUi(self, subgroup_variable_page):
        subgroup_variable_page.setObjectName(_fromUtf8("subgroup_variable_page"))
        subgroup_variable_page.resize(404, 142)
        self.verticalLayout = QtGui.QVBoxLayout(subgroup_variable_page)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(subgroup_variable_page)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboBox = QtGui.QComboBox(subgroup_variable_page)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 23, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(subgroup_variable_page)
        QtCore.QMetaObject.connectSlotsByName(subgroup_variable_page)

    def retranslateUi(self, subgroup_variable_page):
        subgroup_variable_page.setWindowTitle(_translate("subgroup_variable_page", "WizardPage", None))
        self.label.setText(_translate("subgroup_variable_page", "Please choose a variable for the sub-group analysis. If you do not see the desired variable in the box, remember that the type needs to be categorical.", None))

