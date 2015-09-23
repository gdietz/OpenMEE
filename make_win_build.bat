call clean_build_win.bat

python write_version.py
python gsetup_win.py py2exe --includes sip

cd dist

REM Copy R in to executable
mkdir R_dist
cp -rv "C:\Program Files\R\R-3.2.2" R_dist

REM Copy sounds
cp -rv ../sounds .

REM copy over imageformats folder
cp -rv C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats .

REM copy over launch file
cp ../building/building_in_windows/LaunchOpenMEE.bat .

REM make batch file into exe and set icon, 64 bit version does'nt work on windows 8
"C:\Program Files\Bat To Exe Converter\Bat_To_Exe_Converter.exe" -bat LaunchOpenMEE.bat -save LaunchOpenMEE.exe -icon ../images/win_icon.ico

REM go back to original folder
cd ..

REM Repackage built program into nicer subdirectory
rename dist ome_files
mkdir dist
mv ome_files dist
cd dist

REM Copy over shortcut
cp ../building/building_in_windows/LaunchOpenMEE.lnk .

REM Copy over sample data
cp -rv ../sample_data .

REM go back to original folder
cd ..
