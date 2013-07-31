# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'refine_studies_page.ui'
#
# Created: Wed Jul 31 16:32:50 2013
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

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName(_fromUtf8("WizardPage"))
        WizardPage.resize(522, 389)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(WizardPage)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.refine_categories_tab = QtGui.QWidget()
        self.refine_categories_tab.setObjectName(_fromUtf8("refine_categories_tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.refine_categories_tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.cat_group_box = QtGui.QGroupBox(self.refine_categories_tab)
        self.cat_group_box.setObjectName(_fromUtf8("cat_group_box"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.cat_group_box)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.cat_treeWidget = QtGui.QTreeWidget(self.cat_group_box)
        self.cat_treeWidget.setObjectName(_fromUtf8("cat_treeWidget"))
        self.verticalLayout_5.addWidget(self.cat_treeWidget)
        self.verticalLayout_2.addWidget(self.cat_group_box)
        self.tabWidget.addTab(self.refine_categories_tab, _fromUtf8(""))
        self.refine_studies_tab = QtGui.QWidget()
        self.refine_studies_tab.setObjectName(_fromUtf8("refine_studies_tab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.refine_studies_tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox = QtGui.QGroupBox(self.refine_studies_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.refine_studies_list_widget = QtGui.QListWidget(self.groupBox)
        self.refine_studies_list_widget.setObjectName(_fromUtf8("refine_studies_list_widget"))
        self.verticalLayout_4.addWidget(self.refine_studies_list_widget)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.select_all_btn = QtGui.QPushButton(self.refine_studies_tab)
        self.select_all_btn.setObjectName(_fromUtf8("select_all_btn"))
        self.horizontalLayout.addWidget(self.select_all_btn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.deselect_all_btn = QtGui.QPushButton(self.refine_studies_tab)
        self.deselect_all_btn.setObjectName(_fromUtf8("deselect_all_btn"))
        self.horizontalLayout.addWidget(self.deselect_all_btn)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.refine_studies_tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(WizardPage)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.cat_group_box.setTitle(_translate("WizardPage", "Choose Groups of Studies to Include in the Analysis", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.refine_categories_tab), _translate("WizardPage", "Refine Categories", None))
        self.groupBox.setTitle(_translate("WizardPage", "Choose studies to include in the analysis", None))
        self.select_all_btn.setText(_translate("WizardPage", "Select All", None))
        self.deselect_all_btn.setText(_translate("WizardPage", "Deselect All", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.refine_studies_tab), _translate("WizardPage", "Refine Studies", None))

