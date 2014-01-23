# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_covariates_page.ui'
#
# Created: Thu Jan 23 16:21:25 2014
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
        WizardPage.resize(458, 369)
        self.verticalLayout_8 = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.frame = QtGui.QFrame(WizardPage)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.available_covs_listWidget = QtGui.QListWidget(self.groupBox)
        self.available_covs_listWidget.setObjectName(_fromUtf8("available_covs_listWidget"))
        self.verticalLayout_7.addWidget(self.available_covs_listWidget)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.add_all_pushbutton = QtGui.QPushButton(self.frame_2)
        self.add_all_pushbutton.setObjectName(_fromUtf8("add_all_pushbutton"))
        self.verticalLayout_5.addWidget(self.add_all_pushbutton)
        self.add_pushbutton = QtGui.QPushButton(self.frame_2)
        self.add_pushbutton.setObjectName(_fromUtf8("add_pushbutton"))
        self.verticalLayout_5.addWidget(self.add_pushbutton)
        self.remove_pushButton = QtGui.QPushButton(self.frame_2)
        self.remove_pushButton.setObjectName(_fromUtf8("remove_pushButton"))
        self.verticalLayout_5.addWidget(self.remove_pushButton)
        self.remove_all_pushButton = QtGui.QPushButton(self.frame_2)
        self.remove_all_pushButton.setObjectName(_fromUtf8("remove_all_pushButton"))
        self.verticalLayout_5.addWidget(self.remove_all_pushButton)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBox_3 = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.selected_covs_listWidget = QtGui.QListWidget(self.groupBox_3)
        self.selected_covs_listWidget.setMinimumSize(QtCore.QSize(0, 100))
        self.selected_covs_listWidget.setObjectName(_fromUtf8("selected_covs_listWidget"))
        self.verticalLayout_4.addWidget(self.selected_covs_listWidget)
        self.verticalLayout_6.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_4.setBaseSize(QtCore.QSize(0, 0))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.unavailable_covs_listWidget = QtGui.QListWidget(self.groupBox_4)
        self.unavailable_covs_listWidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unavailable_covs_listWidget.sizePolicy().hasHeightForWidth())
        self.unavailable_covs_listWidget.setSizePolicy(sizePolicy)
        self.unavailable_covs_listWidget.setMaximumSize(QtCore.QSize(16777215, 150))
        self.unavailable_covs_listWidget.setObjectName(_fromUtf8("unavailable_covs_listWidget"))
        self.verticalLayout.addWidget(self.unavailable_covs_listWidget)
        self.label = QtGui.QLabel(self.groupBox_4)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_6.addWidget(self.groupBox_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_8.addWidget(self.frame)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.groupBox.setTitle(_translate("WizardPage", "Available Covariates", None))
        self.add_all_pushbutton.setText(_translate("WizardPage", ">>", None))
        self.add_pushbutton.setText(_translate("WizardPage", ">", None))
        self.remove_pushButton.setText(_translate("WizardPage", "<", None))
        self.remove_all_pushButton.setText(_translate("WizardPage", "<<", None))
        self.groupBox_3.setTitle(_translate("WizardPage", "Selected Covariates", None))
        self.groupBox_4.setTitle(_translate("WizardPage", "Unavailable Covariates", None))
        self.label.setText(_translate("WizardPage", "(selected studies have missing data for these covariates)", None))

