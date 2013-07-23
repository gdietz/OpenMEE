# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_effect_size_page.ui'
#
# Created: Tue Jul 23 15:38:59 2013
#      by: PyQt4 UI code generator 4.10.1
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

class Ui_choose_effect_size_page(object):
    def setupUi(self, choose_effect_size_page):
        choose_effect_size_page.setObjectName(_fromUtf8("choose_effect_size_page"))
        choose_effect_size_page.resize(450, 184)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(choose_effect_size_page.sizePolicy().hasHeightForWidth())
        choose_effect_size_page.setSizePolicy(sizePolicy)
        choose_effect_size_page.setMinimumSize(QtCore.QSize(450, 0))
        self.verticalLayout = QtGui.QVBoxLayout(choose_effect_size_page)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.data_type_groupBox = QtGui.QGroupBox(choose_effect_size_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_type_groupBox.sizePolicy().hasHeightForWidth())
        self.data_type_groupBox.setSizePolicy(sizePolicy)
        self.data_type_groupBox.setMinimumSize(QtCore.QSize(0, 160))
        self.data_type_groupBox.setObjectName(_fromUtf8("data_type_groupBox"))
        self.horizontalLayout.addWidget(self.data_type_groupBox)
        self.effect_size_groupBox = QtGui.QGroupBox(choose_effect_size_page)
        self.effect_size_groupBox.setObjectName(_fromUtf8("effect_size_groupBox"))
        self.horizontalLayout.addWidget(self.effect_size_groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(choose_effect_size_page)
        QtCore.QMetaObject.connectSlotsByName(choose_effect_size_page)

    def retranslateUi(self, choose_effect_size_page):
        choose_effect_size_page.setWindowTitle(_translate("choose_effect_size_page", "WizardPage", None))
        choose_effect_size_page.setSubTitle(_translate("choose_effect_size_page", "Choose a data type and effect size", None))
        self.data_type_groupBox.setTitle(_translate("choose_effect_size_page", "Data Type", None))
        self.effect_size_groupBox.setTitle(_translate("choose_effect_size_page", "Effect Size", None))

