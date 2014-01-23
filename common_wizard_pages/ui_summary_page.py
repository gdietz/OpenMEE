# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'summary_page.ui'
#
# Created: Thu Jan 23 09:59:14 2014
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
        WizardPage.resize(381, 302)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(WizardPage)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.save_selections_checkBox = QtGui.QCheckBox(WizardPage)
        self.save_selections_checkBox.setChecked(True)
        self.save_selections_checkBox.setObjectName(_fromUtf8("save_selections_checkBox"))
        self.verticalLayout.addWidget(self.save_selections_checkBox)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        WizardPage.setTitle(_translate("WizardPage", "Summary", None))
        WizardPage.setSubTitle(_translate("WizardPage", "A summary of the parameters for this analysis", None))
        self.plainTextEdit.setPlainText(_translate("WizardPage", "\"Beware the Jabberwock, my son!\n"
"The jaws that bite, the claws that catch!\n"
"Beware the Jubjub bird, and shun\n"
"The frumious Bandersnatch!\"\n"
"\n"
"He took his vorpal sword in hand:\n"
"Long time the manxome foe he sought—\n"
"So rested he by the Tumtum tree,\n"
"And stood awhile in thought.\n"
"\n"
"And as in uffish thought he stood,\n"
"The Jabberwock, with eyes of flame,\n"
"Came whiffling through the tulgey wood,\n"
"And burbled as it came!\n"
"\n"
"One, two! One, two! and through and through\n"
"The vorpal blade went snicker-snack!\n"
"He left it dead, and with its head\n"
"He went galumphing back.\n"
"\n"
"\"And hast thou slain the Jabberwock?\n"
"Come to my arms, my beamish boy!\n"
"O frabjous day! Callooh! Callay!\"\n"
"He chortled in his joy.", None))
        self.save_selections_checkBox.setText(_translate("WizardPage", "Save selections for next analysis?", None))

