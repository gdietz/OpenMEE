# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_models_page.ui'
#
# Created: Sun Jan 12 11:36:06 2014
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
        WizardPage.resize(355, 209)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(WizardPage)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.frame = QtGui.QFrame(WizardPage)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.model_listWidget = QtGui.QListWidget(self.frame)
        self.model_listWidget.setObjectName(_fromUtf8("model_listWidget"))
        self.verticalLayout.addWidget(self.model_listWidget)
        self.verticalLayout_5.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(WizardPage)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.add_model_PushButton = QtGui.QPushButton(self.frame_2)
        self.add_model_PushButton.setObjectName(_fromUtf8("add_model_PushButton"))
        self.horizontalLayout.addWidget(self.add_model_PushButton)
        self.remove_last_model = QtGui.QPushButton(self.frame_2)
        self.remove_last_model.setObjectName(_fromUtf8("remove_last_model"))
        self.horizontalLayout.addWidget(self.remove_last_model)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.frame_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.groupBox = QtGui.QGroupBox(WizardPage)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.model_name_Label = QtGui.QLabel(self.groupBox)
        self.model_name_Label.setObjectName(_fromUtf8("model_name_Label"))
        self.horizontalLayout_3.addWidget(self.model_name_Label)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.label_5 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_3.addWidget(self.label_5)
        self.covariates_list_Label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.covariates_list_Label.sizePolicy().hasHeightForWidth())
        self.covariates_list_Label.setSizePolicy(sizePolicy)
        self.covariates_list_Label.setObjectName(_fromUtf8("covariates_list_Label"))
        self.verticalLayout_3.addWidget(self.covariates_list_Label)
        self.label_3 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.interactions_list_Label = QtGui.QLabel(self.groupBox)
        self.interactions_list_Label.setObjectName(_fromUtf8("interactions_list_Label"))
        self.verticalLayout_3.addWidget(self.interactions_list_Label)
        self.verticalLayout_4.addWidget(self.groupBox)
        spacerItem3 = QtGui.QSpacerItem(20, 14, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.label.setText(_translate("WizardPage", "Models:", None))
        self.add_model_PushButton.setText(_translate("WizardPage", "add model", None))
        self.remove_last_model.setText(_translate("WizardPage", "remove last model", None))
        self.groupBox.setTitle(_translate("WizardPage", "Model Info", None))
        self.label_2.setText(_translate("WizardPage", "Name:", None))
        self.model_name_Label.setText(_translate("WizardPage", "a name", None))
        self.label_5.setText(_translate("WizardPage", "Covariates:", None))
        self.covariates_list_Label.setText(_translate("WizardPage", "    list of covariates\n"
"    gfgd\n"
"    ggdf", None))
        self.label_3.setText(_translate("WizardPage", "Interactions:", None))
        self.interactions_list_Label.setText(_translate("WizardPage", "    list of interactions\n"
"    inter1\n"
"    inter2", None))

