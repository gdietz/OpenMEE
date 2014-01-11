# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tree_page.ui'
#
# Created: Fri Jan 10 18:15:59 2014
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
        WizardPage.resize(335, 168)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(WizardPage)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.select_file_PushButton = QtGui.QPushButton(WizardPage)
        self.select_file_PushButton.setObjectName(_fromUtf8("select_file_PushButton"))
        self.verticalLayout_2.addWidget(self.select_file_PushButton)
        self.tree_fmt_groupBox = QtGui.QGroupBox(WizardPage)
        self.tree_fmt_groupBox.setObjectName(_fromUtf8("tree_fmt_groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tree_fmt_groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.nexus_radioButton = QtGui.QRadioButton(self.tree_fmt_groupBox)
        self.nexus_radioButton.setChecked(True)
        self.nexus_radioButton.setObjectName(_fromUtf8("nexus_radioButton"))
        self.verticalLayout.addWidget(self.nexus_radioButton)
        self.newick_radioButton = QtGui.QRadioButton(self.tree_fmt_groupBox)
        self.newick_radioButton.setObjectName(_fromUtf8("newick_radioButton"))
        self.verticalLayout.addWidget(self.newick_radioButton)
        self.nh_radioButton = QtGui.QRadioButton(self.tree_fmt_groupBox)
        self.nh_radioButton.setObjectName(_fromUtf8("nh_radioButton"))
        self.verticalLayout.addWidget(self.nh_radioButton)
        self.caic_radioButton = QtGui.QRadioButton(self.tree_fmt_groupBox)
        self.caic_radioButton.setObjectName(_fromUtf8("caic_radioButton"))
        self.verticalLayout.addWidget(self.caic_radioButton)
        self.verticalLayout_2.addWidget(self.tree_fmt_groupBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.line = QtGui.QFrame(WizardPage)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_3.addWidget(self.line)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.label = QtGui.QLabel(WizardPage)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(WizardPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.filename_Label = QtGui.QLabel(WizardPage)
        self.filename_Label.setWordWrap(True)
        self.filename_Label.setObjectName(_fromUtf8("filename_Label"))
        self.horizontalLayout.addWidget(self.filename_Label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_4 = QtGui.QLabel(WizardPage)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.format_valid_label = QtGui.QLabel(WizardPage)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.format_valid_label.setFont(font)
        self.format_valid_label.setObjectName(_fromUtf8("format_valid_label"))
        self.horizontalLayout_2.addWidget(self.format_valid_label)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        WizardPage.setTitle(_translate("WizardPage", "Phylogenetic Tree", None))
        WizardPage.setSubTitle(_translate("WizardPage", "Select file describing phylogenetic tree", None))
        self.select_file_PushButton.setText(_translate("WizardPage", "Select File", None))
        self.tree_fmt_groupBox.setTitle(_translate("WizardPage", "Tree format", None))
        self.nexus_radioButton.setText(_translate("WizardPage", "Nexus", None))
        self.newick_radioButton.setText(_translate("WizardPage", "Newick", None))
        self.nh_radioButton.setText(_translate("WizardPage", "New Hampshire", None))
        self.caic_radioButton.setText(_translate("WizardPage", "CAIC", None))
        self.label.setText(_translate("WizardPage", "Selected File:", None))
        self.label_3.setText(_translate("WizardPage", "    ", None))
        self.filename_Label.setText(_translate("WizardPage", "Some filename", None))
        self.label_4.setText(_translate("WizardPage", "   ", None))
        self.format_valid_label.setText(_translate("WizardPage", "File Format Valid!", None))

