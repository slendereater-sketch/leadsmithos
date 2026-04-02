
# ==========================================================
# LEADSMITH Z2A: FAKE USB STAGE CREATOR
# ==========================================================
# This script creates a "Virtual USB" stage on your C: drive.
# The LeadSmith ISO will "Reach-Back" and find these files
# during the boot process, enabling a USB-less install.
# ==========================================================

$StageDir = "C:\LeadSmithOS_Final"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   FORGING FAKE USB STAGE ON C:\          " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if (!(Test-Path $StageDir)) {
    Write-Host "[+] Creating Stage Directory..."
    New-Item -ItemType Directory -Path $StageDir -Force | Out-Null
} else {
    Write-Host "[!] Stage Directory already exists. Refreshing files..."
}

# Copy all project files to the Stage Directory
Write-Host "[+] Injecting LeadSmith OS Source..."
Copy-Item -Path ".\*" -Destination $StageDir -Recurse -Force -Exclude ".git", ".gemini", "__pycache__", "archlinux-*.iso"

# Create a "FAKE_USB" marker for the Linux installer
New-Item -ItemType File -Path (Join-Path $StageDir "FORGE_LIVE_MEDIA.flag") -Force | Out-Null

Write-Host "==========================================" -ForegroundColor Green
Write-Host "   FAKE USB STAGE READY!                  " -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "1. Boot from your Arch Linux ISO."
Write-Host "2. The installer will automatically find C:\LeadSmithOS_Final."
Write-Host "3. It will ignite the installation onto Disk 1."
Write-Host "=========================================="
