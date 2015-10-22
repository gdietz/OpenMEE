REM reinstall openmeer script

rm openmeer_0.1.tar.gz
R CMD build openmeer 
R CMD INSTALL openmeer_0.1.tar.gz
