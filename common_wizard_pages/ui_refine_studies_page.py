# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'refine_studies_page.ui'
#
# Created: Tue Oct  8 11:30:54 2013
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
        WizardPage.resize(528, 391)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(WizardPage)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
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
        self.refine_studies_btn_layout = QtGui.QHBoxLayout()
        self.refine_studies_btn_layout.setObjectName(_fromUtf8("refine_studies_btn_layout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.refine_studies_btn_layout.addItem(spacerItem)
        self.select_all_btn = QtGui.QPushButton(self.refine_studies_tab)
        self.select_all_btn.setObjectName(_fromUtf8("select_all_btn"))
        self.refine_studies_btn_layout.addWidget(self.select_all_btn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.refine_studies_btn_layout.addItem(spacerItem1)
        self.deselect_all_btn = QtGui.QPushButton(self.refine_studies_tab)
        self.deselect_all_btn.setObjectName(_fromUtf8("deselect_all_btn"))
        self.refine_studies_btn_layout.addWidget(self.deselect_all_btn)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.refine_studies_btn_layout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.refine_studies_btn_layout)
        self.tabWidget.addTab(self.refine_studies_tab, _fromUtf8(""))
        self.refine_categories_tab = QtGui.QWidget()
        self.refine_categories_tab.setObjectName(_fromUtf8("refine_categories_tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.refine_categories_tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.cat_treeWidget = QtGui.QTreeWidget(self.refine_categories_tab)
        self.cat_treeWidget.setObjectName(_fromUtf8("cat_treeWidget"))
        self.cat_treeWidget.headerItem().setText(0, _fromUtf8("Choose Groups of Studies to Include in the Analysis"))
        self.verticalLayout_2.addWidget(self.cat_treeWidget)
        self.tabWidget.addTab(self.refine_categories_tab, _fromUtf8(""))
        self.exclude_studies_missing_data_tab = QtGui.QWidget()
        self.exclude_studies_missing_data_tab.setObjectName(_fromUtf8("exclude_studies_missing_data_tab"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.exclude_studies_missing_data_tab)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label = QtGui.QLabel(self.exclude_studies_missing_data_tab)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_5.addWidget(self.label)
        self.missing_data_listwidget = QtGui.QListWidget(self.exclude_studies_missing_data_tab)
        self.missing_data_listwidget.setObjectName(_fromUtf8("missing_data_listwidget"))
        self.verticalLayout_5.addWidget(self.missing_data_listwidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.missing_data_apply_btn = QtGui.QPushButton(self.exclude_studies_missing_data_tab)
        self.missing_data_apply_btn.setObjectName(_fromUtf8("missing_data_apply_btn"))
        self.horizontalLayout.addWidget(self.missing_data_apply_btn)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.exclude_studies_missing_data_tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(WizardPage)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.groupBox.setTitle(_translate("WizardPage", "Choose studies to include in the analysis", None))
        self.select_all_btn.setText(_translate("WizardPage", "Select All", None))
        self.deselect_all_btn.setText(_translate("WizardPage", "Deselect All", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.refine_studies_tab), _translate("WizardPage", "Refine Studies", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.refine_categories_tab), _translate("WizardPage", "Refine Categories", None))
        self.label.setText(_translate("WizardPage", "Select covariates for which you would like to exclude studies if no data is available. Then click Apply.", None))
        self.missing_data_apply_btn.setText(_translate("WizardPage", "Apply", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.exclude_studies_missing_data_tab), _translate("WizardPage", "Refine Missing Data", None))

