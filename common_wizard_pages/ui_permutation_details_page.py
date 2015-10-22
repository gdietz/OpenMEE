# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'permutation_details_page.ui'
#
# Created: Thu Aug 21 22:03:24 2014
#      by: PyQt4 UI code generator 4.10.4
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
        WizardPage.resize(304, 181)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.exact_checkBox = QtGui.QCheckBox(WizardPage)
        self.exact_checkBox.setObjectName(_fromUtf8("exact_checkBox"))
        self.verticalLayout.addWidget(self.exact_checkBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(WizardPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.iter_spinBox = QtGui.QSpinBox(WizardPage)
        self.iter_spinBox.setMinimum(1)
        self.iter_spinBox.setMaximum(10000000)
        self.iter_spinBox.setProperty("value", 1000)
        self.iter_spinBox.setObjectName(_fromUtf8("iter_spinBox"))
        self.horizontalLayout.addWidget(self.iter_spinBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(WizardPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.digits_spinBox = QtGui.QSpinBox(WizardPage)
        self.digits_spinBox.setMaximum(10)
        self.digits_spinBox.setProperty("value", 4)
        self.digits_spinBox.setObjectName(_fromUtf8("digits_spinBox"))
        self.horizontalLayout_2.addWidget(self.digits_spinBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.retpermdist_checkBox = QtGui.QCheckBox(WizardPage)
        self.retpermdist_checkBox.setObjectName(_fromUtf8("retpermdist_checkBox"))
        self.horizontalLayout_3.addWidget(self.retpermdist_checkBox)
        self.perm_dist_hist_checkBox = QtGui.QCheckBox(WizardPage)
        self.perm_dist_hist_checkBox.setEnabled(False)
        self.perm_dist_hist_checkBox.setObjectName(_fromUtf8("perm_dist_hist_checkBox"))
        self.horizontalLayout_3.addWidget(self.perm_dist_hist_checkBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(WizardPage)
        QtCore.QObject.connect(self.retpermdist_checkBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.perm_dist_hist_checkBox.setEnabled)
        QtCore.QObject.connect(self.exact_checkBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label.setDisabled)
        QtCore.QObject.connect(self.exact_checkBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.iter_spinBox.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        WizardPage.setTitle(_translate("WizardPage", "Permutation Details", None))
        self.exact_checkBox.setToolTip(_translate("WizardPage", "If selected, the model is fit to each possible permuation once.\n"
"Caution: The number of permuations can blow up quickly with the # of studies and # of moderators", None))
        self.exact_checkBox.setText(_translate("WizardPage", "exact permuation test (default: no)", None))
        self.label.setToolTip(_translate("WizardPage", "number of iterations for the permutation test when not\n"
"doing an exact test", None))
        self.label.setText(_translate("WizardPage", "Iterations:", None))
        self.iter_spinBox.setToolTip(_translate("WizardPage", "number of iterations for the permutation test when not\n"
"doing an exact test (default: 1000)", None))
        self.label_3.setToolTip(_translate("WizardPage", "# of decimal places to which to round the printed results", None))
        self.label_3.setText(_translate("WizardPage", "Digits:", None))
        self.digits_spinBox.setToolTip(_translate("WizardPage", "# of decimal places to which to round the printed results", None))
        self.retpermdist_checkBox.setText(_translate("WizardPage", "get permutation\n"
"distribution of test\n"
"statistics", None))
        self.perm_dist_hist_checkBox.setText(_translate("WizardPage", "make histograms\n"
"of test statistics", None))

