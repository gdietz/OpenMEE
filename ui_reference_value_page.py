# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reference_value_page.ui'
#
# Created: Tue Sep 10 16:01:10 2013
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
        WizardPage.resize(473, 251)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(WizardPage)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.splitter = QtGui.QSplitter(WizardPage)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.cov_listWidget = QtGui.QListWidget(self.splitter)
        self.cov_listWidget.setObjectName(_fromUtf8("cov_listWidget"))
        item = QtGui.QListWidgetItem()
        self.cov_listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.cov_listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.cov_listWidget.addItem(item)
        self.val_listWidget = QtGui.QListWidget(self.splitter)
        self.val_listWidget.setObjectName(_fromUtf8("val_listWidget"))
        item = QtGui.QListWidgetItem()
        self.val_listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.val_listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.val_listWidget.addItem(item)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "Reference Values", None))
        WizardPage.setTitle(_translate("WizardPage", "Reference Value", None))
        WizardPage.setSubTitle(_translate("WizardPage", "Choose reference value(s):", None))
        self.label.setText(_translate("WizardPage", "You have selected some categorical covariates. If you would like to set their reference values, please do so now.", None))
        __sortingEnabled = self.cov_listWidget.isSortingEnabled()
        self.cov_listWidget.setSortingEnabled(False)
        item = self.cov_listWidget.item(0)
        item.setText(_translate("WizardPage", "cov 1", None))
        item = self.cov_listWidget.item(1)
        item.setText(_translate("WizardPage", "cov 2", None))
        item = self.cov_listWidget.item(2)
        item.setText(_translate("WizardPage", "cov 3", None))
        self.cov_listWidget.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.val_listWidget.isSortingEnabled()
        self.val_listWidget.setSortingEnabled(False)
        item = self.val_listWidget.item(0)
        item.setText(_translate("WizardPage", "value1", None))
        item = self.val_listWidget.item(1)
        item.setText(_translate("WizardPage", "value2", None))
        item = self.val_listWidget.item(2)
        item.setText(_translate("WizardPage", "value3", None))
        self.val_listWidget.setSortingEnabled(__sortingEnabled)

