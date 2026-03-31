@echo off
title Kalyan Auto-Updater
cd /d "%~dp0"
echo ----------------------------------------------------
echo  Kalyan Matka Results Auto-Updater (Background Mode)
echo ----------------------------------------------------
echo  This window will monitor the internet for new numbers 
echo  every 15 minutes and update your Excel files.
echo  Keep it open for background updates.
echo ----------------------------------------------------
python auto_updater.py
pause
