
# Targeted injection for Linux SSD (ARCH_202602)
$targetDrive = "H:"
if (!(Test-Path $targetDrive)) {
    Write-Host "ERROR: Drive H:\ not found. Please ensure the Linux SSD is mounted as H:" -ForegroundColor Red
    exit
}

$targetDir = Join-Path $targetDrive "LeadSmithOS_Final"

Write-Host "Injecting LeadSmith OS Files into $targetDir on Linux SSD..." -ForegroundColor Cyan

if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

Copy-Item -Path ".\*" -Destination $targetDir -Recurse -Force -Exclude ".git", ".gemini", "__pycache__", "inject_to_lexar.ps1"

Write-Host "Injection Complete! LeadSmith OS is now staged on the Linux SSD ($targetDrive)." -ForegroundColor Green
