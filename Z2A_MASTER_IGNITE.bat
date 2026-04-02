@echo off
title LEADSMITH Z2A MASTER IGNITION
color 0b

:: --- THE ZERO-TOUCH FORGE LAUNCHER ---
echo [âš’] IGNITING LEADSMITH Z2A MASTER CORE...
echo [âš™] OPTIMIZING FOR RDNA 3.5...

:: Ensure we are in the high-performance directory
cd /d "C:\Users\creat\Desktop\Leadsmith_Project\LeadSmithOS_Graphical"

:: Launch the Dashboard in TRUE FULLSCREEN
:: Using 'start /max' ensures it covers the taskbar immediately
start /max python leadsmith_os.py

:: Auto-exit the terminal to keep the workspace clean for touch
timeout /t 3 >nul
exit
