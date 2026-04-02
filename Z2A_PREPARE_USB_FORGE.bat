@echo off
title LEADSMITH Z2A - USB FORGE PREP
color 0b

echo ==========================================
echo    LEADSMITH Z2A: USB FORGE PREP
echo ==========================================
echo [âš™] DETECTING USB DRIVES...

:: Search for USB drive (excluding C:)
for /f "tokens=2 delims==" %%d in ('wmic logicaldisk where "drivetype=2" get name /value') do (
    set USB_DRIVE=%%d
    goto :FOUND
)

echo [!] NO USB DRIVE DETECTED. PLEASE PLUG IN YOUR DRIVE.
pause
exit

:FOUND
echo [âœ“] FOUND USB DRIVE AT %USB_DRIVE%
echo [âš’] DEPLOYING ZERO-TOUCH TOOLS...

:: Copying the installation tools to the root of the detected USB
xcopy /E /Y "C:\Users\creat\Desktop\Leadsmith_Project\LeadSmithOS_Final\*" "%USB_DRIVE%\"

echo ==========================================
echo    FORGE PREP COMPLETE. 
echo    USB %USB_DRIVE% IS READY FOR IGNITION.
echo ==========================================
timeout /t 5
exit
