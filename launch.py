
import sys
import time

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import python_to_R
import main_form
import icons_rc

SPLASH_DISPLAY_TIME = 0

def load_R_libraries(app, splash=None):
    ''' Loads the R libraries while updating the splash screen'''
    
    rloader = python_to_R.RlibLoader()

    splash.showMessage("Loading metafor\n....")
    app.processEvents()
    rloader.load_metafor()
    
    splash.showMessage("Loading openmetar\n........")
    app.processEvents()
    rloader.load_openmetar()
    
    splash.showMessage("Loading igraph\n............")
    app.processEvents()
    rloader.load_igraph()
    
    splash.showMessage("Loading grid\n................")
    app.processEvents()
    rloader.load_grid()
    
def start():
    app = QtGui.QApplication(sys.argv)
    
    splash_pixmap = QPixmap(":/splash/splash.jpg")
    splash = QSplashScreen(splash_pixmap)
    splash.show()
    splash.raise_()
    splash_starttime = time.time()
    
    load_R_libraries(app, splash)
    
    # Show splash screen for at least SPLASH_DISPLAY_TIME seconds
    time_elapsed  = time.time() - splash_starttime
    print("It took %s seconds to load the R libraries" % str(time_elapsed))
    if time_elapsed < SPLASH_DISPLAY_TIME: # seconds
        print("Going to sleep for %f seconds" % float(SPLASH_DISPLAY_TIME-time_elapsed))
        QThread.sleep(int(SPLASH_DISPLAY_TIME-time_elapsed))
        print("woke up")

    form = main_form.MainForm()
    splash.finish(form)
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start()