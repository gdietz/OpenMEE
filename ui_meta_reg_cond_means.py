# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meta_reg_cond_means.ui'
#
# Created: Thu Sep 19 13:12:40 2013
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
        WizardPage.resize(414, 393)
        self.verticalLayout_3 = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(WizardPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.choose_cov_comboBox = QtGui.QComboBox(WizardPage)
        self.choose_cov_comboBox.setObjectName(_fromUtf8("choose_cov_comboBox"))
        self.choose_cov_comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.choose_cov_comboBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(WizardPage)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_3.addWidget(self.line)
        self.label_4 = QtGui.QLabel(WizardPage)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(WizardPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.cont_listWidget = QtGui.QListWidget(WizardPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cont_listWidget.sizePolicy().hasHeightForWidth())
        self.cont_listWidget.setSizePolicy(sizePolicy)
        self.cont_listWidget.setMinimumSize(QtCore.QSize(160, 100))
        self.cont_listWidget.setMaximumSize(QtCore.QSize(160, 100))
        self.cont_listWidget.setObjectName(_fromUtf8("cont_listWidget"))
        self.verticalLayout.addWidget(self.cont_listWidget)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.cont_le = QtGui.QLineEdit(WizardPage)
        self.cont_le.setBaseSize(QtCore.QSize(90, 21))
        self.cont_le.setObjectName(_fromUtf8("cont_le"))
        self.horizontalLayout_3.addWidget(self.cont_le)
        spacerItem3 = QtGui.QSpacerItem(190, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(WizardPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.cat_listWidget = QtGui.QListWidget(WizardPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cat_listWidget.sizePolicy().hasHeightForWidth())
        self.cat_listWidget.setSizePolicy(sizePolicy)
        self.cat_listWidget.setMinimumSize(QtCore.QSize(160, 100))
        self.cat_listWidget.setMaximumSize(QtCore.QSize(160, 100))
        self.cat_listWidget.setObjectName(_fromUtf8("cat_listWidget"))
        self.verticalLayout_2.addWidget(self.cat_listWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.cat_cbo_box = QtGui.QComboBox(WizardPage)
        self.cat_cbo_box.setObjectName(_fromUtf8("cat_cbo_box"))
        self.horizontalLayout_2.addWidget(self.cat_cbo_box)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        WizardPage.setTitle(_translate("WizardPage", "Conditional Means", None))
        WizardPage.setSubTitle(_translate("WizardPage", "Meta-Regression-Based conditional means", None))
        self.label.setText(_translate("WizardPage", "For which covariate do you want the conditional means?", None))
        self.choose_cov_comboBox.setItemText(0, _translate("WizardPage", "Categorical Covariates", None))
        self.label_4.setText(_translate("WizardPage", "Specify the values to use for the other covariates:", None))
        self.label_2.setText(_translate("WizardPage", "Continuous Covariates", None))
        self.label_3.setText(_translate("WizardPage", "Categorical Covariates", None))

