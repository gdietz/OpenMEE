# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transform_effect_summary_page.ui'
#
# Created: Thu Aug 29 16:30:10 2013
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
        WizardPage.resize(375, 140)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(WizardPage)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(WizardPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(WizardPage)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(WizardPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.from_column_lbl = QtGui.QLabel(WizardPage)
        self.from_column_lbl.setObjectName(_fromUtf8("from_column_lbl"))
        self.gridLayout.addWidget(self.from_column_lbl, 0, 1, 1, 1)
        self.from_scale_lbl = QtGui.QLabel(WizardPage)
        self.from_scale_lbl.setObjectName(_fromUtf8("from_scale_lbl"))
        self.gridLayout.addWidget(self.from_scale_lbl, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(WizardPage)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.to_scale_lbl = QtGui.QLabel(WizardPage)
        self.to_scale_lbl.setObjectName(_fromUtf8("to_scale_lbl"))
        self.gridLayout.addWidget(self.to_scale_lbl, 2, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        WizardPage.setSubTitle(_translate("WizardPage", "Summary", None))
        self.label_2.setText(_translate("WizardPage", "You have chosen to make the following transformation:", None))
        self.label_4.setText(_translate("WizardPage", "   From:", None))
        self.label_3.setText(_translate("WizardPage", "column: ", None))
        self.from_column_lbl.setText(_translate("WizardPage", "name of column", None))
        self.from_scale_lbl.setText(_translate("WizardPage", "from_scale", None))
        self.label_5.setText(_translate("WizardPage", "   To:", None))
        self.to_scale_lbl.setText(_translate("WizardPage", "to_scale", None))

