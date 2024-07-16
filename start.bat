@echo off
echo Starting AUTOHAP cursor and keyboard input WILL BE DISABLED
echo in case of failure use CTRL + ALT + DEL
timeout /t 5
python %cd%\\data_to_JSON.py
echo Executing scripts... Standby
timeout /t 5