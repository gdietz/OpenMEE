
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *





class EffectSizeLocationsPage(QWizardPage):
    def __init__(self, model, parent=None):
        super(EffectSizeLocationsPage, self).__init__(parent)