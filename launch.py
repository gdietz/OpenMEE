################
#              #
# George Dietz #
# CEBM@Brown   #
#              #
################

import os
import sys
import time

from PyQt4 import QtGui
from PyQt4.Qt import QPixmap, QSplashScreen, QThread

import python_to_R
import main_form
import ome_globals

def load_R_libraries(app, splash=None):
    ''' Loads the R libraries while updating the splash screen'''
    
    python_to_R.get_R_libpaths() # print the lib paths
    rloader = python_to_R.RlibLoader()

    splash.showMessage("Loading metafor\n....")
    app.processEvents()
    rloader.load_metafor()
    
    splash.showMessage("Loading openmetar\n........")
    app.processEvents()
    rloader.load_openmetar()

    splash.showMessage("Loading openmee\n............")
    app.processEvents()
    rloader.load_openmeer()
    
    splash.showMessage("Loading igraph\n............")
    app.processEvents()
    rloader.load_igraph()
    
    splash.showMessage("Loading grid\n................")
    app.processEvents()
    rloader.load_grid()

    splash.showMessage("Loading APE\n................")
    app.processEvents()
    rloader.load_ape()

    splash.showMessage("Loading mice\n................")
    app.processEvents()
    rloader.load_mice()


def start(open_file_path=None, reset_settings=False):
    ###### Setup directories ######
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName(ome_globals.PROGRAM_NAME)
    app.setOrganizationName(ome_globals.ORGANIZATION_NAME)
    
    # Make working directory for python and R and sets up r_tmp (where R does
    # its calculations. Also clears r_tmp
    ## N.B. This MUST come after setting the app name and stuff in order for the
    # paths and subsequent calls to get_base_path() to work correctly
    python_to_R.setup_directories()
    
    if reset_settings:
        ome_globals.reset_settings()
    
    splash_pixmap = QPixmap(":/splash/splash.png")
    splash = QSplashScreen(splash_pixmap)
    splash.show()
    
    splash_starttime = time.time()
    load_R_libraries(app, splash)
    
    # Show splash screen for at least ome_globals.SPLASH_DISPLAY_TIME seconds
    time_elapsed  = time.time() - splash_starttime
    print("It took %s seconds to load the R libraries" % str(time_elapsed))
    if time_elapsed < ome_globals.SPLASH_DISPLAY_TIME: # seconds
        print("Going to sleep for %f seconds" % float(ome_globals.SPLASH_DISPLAY_TIME-time_elapsed))
        QThread.sleep(int(ome_globals.SPLASH_DISPLAY_TIME-time_elapsed))
        print("woke up")

    # create and show the main window
    form = main_form.MainForm()
    form.show()
    #form.raise_()
    if open_file_path:
        form.open(open_file_path)
        
    # Close the splash screen
    splash.finish(form)
    
    sys.exit(app.exec_())
 
def clear_r_tmp():
    r_tmp_dir = os.path.join(ome_globals.get_base_path(), "r_tmp")
    print("Clearing %s" % r_tmp_dir)
    for file_p in os.listdir(r_tmp_dir):
        file_path = os.path.join(r_tmp_dir, file_p)
        try:
            if os.path.isfile(file_path):
                print("deleting %s" % file_path)
                os.unlink(file_path) # same as remove
        except Exception, e:
            print e    

if __name__ == "__main__":
    start()
