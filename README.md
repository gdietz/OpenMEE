OpenMEE
=======

OpenMEE

To run OpenMEE from source, you'll need to install the corresponding dependencies.

You'll need to install the necessary R packages. 
First install the dependencies:

From within a (possibly) sudo-ed R session type:

	> install.packages(c("metafor","lme4","MCMCpack","igraph", "ape", "mice", "Hmisc"))

Next, you'll need to build and install the openmetar packages and altered HSROC (NOT THE ONE FROM CRAN) package and install them. For now, these packages are located in the [OpenMetaAnalyst Repository](https://github.com/bwallace/OpenMeta-analyst-). These package are distributed with the source (NOT the OpenMEE source; the OpenMetaAnalyst source!) under the "src/R" directory of the OMA repository. 

    > R CMD build HSROC
    > R CMD build openmetar
    > sudo R CMD INSTALL HSROC_2.0.5.tar.gz
    > sudo R CMD INSTALL openmetar_1.0.tar.gz

Once R is setup for OpenMeta, you'll need to install Python (we use 2.7) and the necessary libraries. You'll need PyQT (and QT: see http://www.riverbankcomputing.co.uk/software/pyqt/intro) installed -- we use PyQt 4.9; your mileage may vary with other versions. 

Next, install rpy2 (rpy.sourceforge.net/rpy2.html) in Python. Verify that all is well by executing:

    > import rpy2
    > from rpy2 import robjects 

At the Python console.

That should be all you need. Once everything is setup, you can launch the program by typing:

    > python launch.py

At the console. This should fire up the GUI.

important dependency versions:
R      : 3.0.1 (2013-05-16) -- "Good Sport"
metafor: 1.6.0
pyqt4  : 4.10.1
