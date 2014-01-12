# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sat_model_add_interactions_page.ui'
#
# Created: Sun Jan 12 10:04:50 2014
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
        WizardPage.resize(470, 301)
        self.verticalLayout_3 = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.frame = QtGui.QFrame(WizardPage)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.covariate_frame = QtGui.QFrame(self.frame)
        self.covariate_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.covariate_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.covariate_frame.setObjectName(_fromUtf8("covariate_frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.covariate_frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.covariate_frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.cov_listWidget = QtGui.QListWidget(self.covariate_frame)
        self.cov_listWidget.setObjectName(_fromUtf8("cov_listWidget"))
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.cov_listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.cov_listWidget.addItem(item)
        self.verticalLayout.addWidget(self.cov_listWidget)
        self.horizontalLayout_3.addWidget(self.covariate_frame)
        self.covariate_frame_2 = QtGui.QFrame(self.frame)
        self.covariate_frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.covariate_frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.covariate_frame_2.setObjectName(_fromUtf8("covariate_frame_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.covariate_frame_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.covariate_frame_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.cov_listWidget_2 = QtGui.QListWidget(self.covariate_frame_2)
        self.cov_listWidget_2.setObjectName(_fromUtf8("cov_listWidget_2"))
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.cov_listWidget_2.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.cov_listWidget_2.addItem(item)
        self.verticalLayout_2.addWidget(self.cov_listWidget_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.add_interaction_PushButton = QtGui.QPushButton(self.covariate_frame_2)
        self.add_interaction_PushButton.setObjectName(_fromUtf8("add_interaction_PushButton"))
        self.horizontalLayout_4.addWidget(self.add_interaction_PushButton)
        self.remove_interactio_PushButton = QtGui.QPushButton(self.covariate_frame_2)
        self.remove_interactio_PushButton.setObjectName(_fromUtf8("remove_interactio_PushButton"))
        self.horizontalLayout_4.addWidget(self.remove_interactio_PushButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addWidget(self.covariate_frame_2)
        self.verticalLayout_3.addWidget(self.frame)
        self.label_4 = QtGui.QLabel(WizardPage)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_3 = QtGui.QLabel(WizardPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.saturated_model_name_lineEdit = QtGui.QLineEdit(WizardPage)
        self.saturated_model_name_lineEdit.setObjectName(_fromUtf8("saturated_model_name_lineEdit"))
        self.horizontalLayout_5.addWidget(self.saturated_model_name_lineEdit)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        WizardPage.setTitle(_translate("WizardPage", "Specify Saturated Model", None))
        WizardPage.setSubTitle(_translate("WizardPage", "Specify all the covariates of interest and add interaction terms. All subsequent models will include increasingly narrow subsets of these terms.", None))
        self.label.setText(_translate("WizardPage", "Covariates:", None))
        __sortingEnabled = self.cov_listWidget.isSortingEnabled()
        self.cov_listWidget.setSortingEnabled(False)
        item = self.cov_listWidget.item(0)
        item.setText(_translate("WizardPage", "cov1", None))
        item = self.cov_listWidget.item(1)
        item.setText(_translate("WizardPage", "cov2", None))
        self.cov_listWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("WizardPage", "Interactions:", None))
        __sortingEnabled = self.cov_listWidget_2.isSortingEnabled()
        self.cov_listWidget_2.setSortingEnabled(False)
        item = self.cov_listWidget_2.item(0)
        item.setText(_translate("WizardPage", "interaction1", None))
        item = self.cov_listWidget_2.item(1)
        item.setText(_translate("WizardPage", "interaction2", None))
        self.cov_listWidget_2.setSortingEnabled(__sortingEnabled)
        self.add_interaction_PushButton.setText(_translate("WizardPage", "Add interaction", None))
        self.remove_interactio_PushButton.setText(_translate("WizardPage", "Remove Interaction", None))
        self.label_4.setText(_translate("WizardPage", " \n"
" ", None))
        self.label_3.setText(_translate("WizardPage", "Name of saturated model:", None))

