# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Mon Jul  8 14:58:22 2013
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(721, 555)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 721, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuImport = QtGui.QMenu(self.menuFile)
        self.menuImport.setObjectName(_fromUtf8("menuImport"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuTable = QtGui.QMenu(self.menubar)
        self.menuTable.setObjectName(_fromUtf8("menuTable"))
        self.menuAnalysis = QtGui.QMenu(self.menubar)
        self.menuAnalysis.setObjectName(_fromUtf8("menuAnalysis"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionRecent_Data = QtGui.QAction(MainWindow)
        self.actionRecent_Data.setObjectName(_fromUtf8("actionRecent_Data"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.actionCSV = QtGui.QAction(MainWindow)
        self.actionCSV.setObjectName(_fromUtf8("actionCSV"))
        self.actionBanan = QtGui.QAction(MainWindow)
        self.actionBanan.setObjectName(_fromUtf8("actionBanan"))
        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionClear_Selected_Cells = QtGui.QAction(MainWindow)
        self.actionClear_Selected_Cells.setObjectName(_fromUtf8("actionClear_Selected_Cells"))
        self.actionSelect_All = QtGui.QAction(MainWindow)
        self.actionSelect_All.setObjectName(_fromUtf8("actionSelect_All"))
        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionInsert_Row = QtGui.QAction(MainWindow)
        self.actionInsert_Row.setObjectName(_fromUtf8("actionInsert_Row"))
        self.actionDelete_Row = QtGui.QAction(MainWindow)
        self.actionDelete_Row.setObjectName(_fromUtf8("actionDelete_Row"))
        self.actionInsert_Column = QtGui.QAction(MainWindow)
        self.actionInsert_Column.setObjectName(_fromUtf8("actionInsert_Column"))
        self.actionDelete_Column = QtGui.QAction(MainWindow)
        self.actionDelete_Column.setObjectName(_fromUtf8("actionDelete_Column"))
        self.actionChange_Column_Format = QtGui.QAction(MainWindow)
        self.actionChange_Column_Format.setObjectName(_fromUtf8("actionChange_Column_Format"))
        self.actionRename_Column = QtGui.QAction(MainWindow)
        self.actionRename_Column.setObjectName(_fromUtf8("actionRename_Column"))
        self.actionMark_Column_as_Label = QtGui.QAction(MainWindow)
        self.actionMark_Column_as_Label.setObjectName(_fromUtf8("actionMark_Column_as_Label"))
        self.actionUnmark_Column_as_Label = QtGui.QAction(MainWindow)
        self.actionUnmark_Column_as_Label.setObjectName(_fromUtf8("actionUnmark_Column_as_Label"))
        self.actionDecimal_Places = QtGui.QAction(MainWindow)
        self.actionDecimal_Places.setObjectName(_fromUtf8("actionDecimal_Places"))
        self.actionTable_Preferences = QtGui.QAction(MainWindow)
        self.actionTable_Preferences.setObjectName(_fromUtf8("actionTable_Preferences"))
        self.actionShow_toolbar = QtGui.QAction(MainWindow)
        self.actionShow_toolbar.setObjectName(_fromUtf8("actionShow_toolbar"))
        self.actionAs_CSV = QtGui.QAction(MainWindow)
        self.actionAs_CSV.setObjectName(_fromUtf8("actionAs_CSV"))
        self.actionUndo = QtGui.QAction(MainWindow)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionRedo = QtGui.QAction(MainWindow)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.menuImport.addAction(self.actionCSV)
        self.menuExport.addAction(self.actionAs_CSV)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionRecent_Data)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionClear_Selected_Cells)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionShow_toolbar)
        self.menuTable.addAction(self.actionInsert_Row)
        self.menuTable.addAction(self.actionDelete_Row)
        self.menuTable.addAction(self.actionInsert_Column)
        self.menuTable.addAction(self.actionDelete_Column)
        self.menuTable.addSeparator()
        self.menuTable.addAction(self.actionChange_Column_Format)
        self.menuTable.addAction(self.actionRename_Column)
        self.menuTable.addAction(self.actionMark_Column_as_Label)
        self.menuTable.addAction(self.actionUnmark_Column_as_Label)
        self.menuTable.addSeparator()
        self.menuTable.addAction(self.actionTable_Preferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTable.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuImport.setTitle(_translate("MainWindow", "Import", None))
        self.menuExport.setTitle(_translate("MainWindow", "Export", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuTable.setTitle(_translate("MainWindow", "Table", None))
        self.menuAnalysis.setTitle(_translate("MainWindow", "Analysis", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionRecent_Data.setText(_translate("MainWindow", "Recent Data...", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionSave_As.setText(_translate("MainWindow", "Save As...", None))
        self.actionCSV.setText(_translate("MainWindow", "CSV", None))
        self.actionBanan.setText(_translate("MainWindow", "banan", None))
        self.actionCopy.setText(_translate("MainWindow", "Copy", None))
        self.actionPaste.setText(_translate("MainWindow", "Paste", None))
        self.actionClear_Selected_Cells.setText(_translate("MainWindow", "Clear Selected Cells", None))
        self.actionSelect_All.setText(_translate("MainWindow", "Select All", None))
        self.actionCut.setText(_translate("MainWindow", "Cut", None))
        self.actionInsert_Row.setText(_translate("MainWindow", "Insert Row", None))
        self.actionDelete_Row.setText(_translate("MainWindow", "Delete Row", None))
        self.actionInsert_Column.setText(_translate("MainWindow", "Insert Column", None))
        self.actionDelete_Column.setText(_translate("MainWindow", "Delete Column", None))
        self.actionChange_Column_Format.setText(_translate("MainWindow", "Change Column Format", None))
        self.actionRename_Column.setText(_translate("MainWindow", "Rename Column", None))
        self.actionMark_Column_as_Label.setText(_translate("MainWindow", "Mark Column as Label", None))
        self.actionUnmark_Column_as_Label.setText(_translate("MainWindow", "Unmark Column as Label", None))
        self.actionDecimal_Places.setText(_translate("MainWindow", "Decimal Places", None))
        self.actionTable_Preferences.setText(_translate("MainWindow", "Table Preferences", None))
        self.actionShow_toolbar.setText(_translate("MainWindow", "Show toolbar", None))
        self.actionAs_CSV.setText(_translate("MainWindow", "As CSV", None))
        self.actionUndo.setText(_translate("MainWindow", "Undo", None))
        self.actionRedo.setText(_translate("MainWindow", "Redo", None))

