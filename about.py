#import os

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from ome_globals import get_build_date

import ui_about

class About(QDialog, ui_about.Ui_Dialog):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
        
        # Set version
        self.versionLabel.setText("Build Date: %s" % get_build_date())

        self.contents.linkActivated.connect(self.open_link)
        
    def open_link(self, link_as_qstr):
        QDesktopServices.openUrl(QUrl(link_as_qstr))