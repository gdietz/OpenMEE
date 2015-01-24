# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'results_window.ui'
#
# Created: Mon Jan 19 23:06:12 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ResultsWindow(object):
    def setupUi(self, ResultsWindow):
        ResultsWindow.setObjectName(_fromUtf8("ResultsWindow"))
        ResultsWindow.resize(879, 508)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        ResultsWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(ResultsWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.export_btn = QtGui.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/function_icon_set/images/function_icon_set/paper_48.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.export_btn.setIcon(icon)
        self.export_btn.setIconSize(QtCore.QSize(24, 24))
        self.export_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.export_btn.setObjectName(_fromUtf8("export_btn"))
        self.horizontalLayout.addWidget(self.export_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.results_nav_splitter = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.results_nav_splitter.sizePolicy().hasHeightForWidth())
        self.results_nav_splitter.setSizePolicy(sizePolicy)
        self.results_nav_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.results_nav_splitter.setObjectName(_fromUtf8("results_nav_splitter"))
        self.nav_tree = QtGui.QTreeWidget(self.results_nav_splitter)
        self.nav_tree.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        self.nav_tree.setFont(font)
        self.nav_tree.setObjectName(_fromUtf8("nav_tree"))
        self.nav_tree.headerItem().setText(0, _fromUtf8("1"))
        self.graphics_view = QtGui.QGraphicsView(self.results_nav_splitter)
        self.graphics_view.setToolTip(_fromUtf8(""))
        self.graphics_view.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.graphics_view.setObjectName(_fromUtf8("graphics_view"))
        self.verticalLayout.addWidget(self.results_nav_splitter)
        ResultsWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(ResultsWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ResultsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ResultsWindow)
        QtCore.QMetaObject.connectSlotsByName(ResultsWindow)

    def retranslateUi(self, ResultsWindow):
        ResultsWindow.setWindowTitle(_translate("ResultsWindow", "results / analysis", None))
        self.export_btn.setText(_translate("ResultsWindow", "Export Results as Text", None))

import icons_rc
