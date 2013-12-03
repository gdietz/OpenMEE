'''
Created on Dec 2, 2013

@author: George Dietz
         CEBM@Brown
'''

import os

# Set R environment variables
oldpath = os.environ["PATH"]
cwd = os.getcwd()
rpath = os.path.join(cwd, "..","Resources", "Resources") # second 'Resources' is R directory
os.environ["PATH"] = os.path.join(rpath, "bin") + os.pathsep + oldpath
print("new path is: %s" % os.environ["PATH"])

os.environ["R"] = os.path.join(cwd, rpath, "bin")
os.environ["R_HOME"] = os.path.join(cwd, rpath)


#from rpy2 import robjects as ro

# we are ready to start the main program loop
import launch
if __name__ == "__main__":
    launch.start()