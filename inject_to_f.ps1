
# Targeted injection for Linux SSD (Partition F)
$targetDrive = "F:"
if (!(Test-Path $targetDrive)) {
    Write-Host "ERROR: Drive F:\ not found. Please ensure the Linux SSD is mounted as F:" -ForegroundColor Red
    exit
}

$targetDir = Join-Path $targetDrive "LeadSmithOS_Final"

Write-Host "Injecting LeadSmith OS Files into $targetDir on Linux SSD..." -ForegroundColor Cyan

if (!(Test-Path $targetDir)) {
    try {
        New-Item -ItemType Directory -Path $targetDir -Force -ErrorAction Stop | Out-Null
    } catch {
        Write-Host "CRITICAL: Access denied to F:\. The drive may be write-protected." -ForegroundColor Red
        exit
    }
}

Copy-Item -Path ".\*" -Destination $targetDir -Recurse -Force -Exclude ".git", ".gemini", "__pycache__", "inject_*.ps1"

Write-Host "Injection Complete! LeadSmith OS is now staged on the Linux SSD ($targetDrive)." -ForegroundColor Green
