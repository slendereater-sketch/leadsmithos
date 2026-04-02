
$drive = Get-Volume | Where-Object { $_.FileSystemLabel -eq "LEXAR" }
if ($null -eq $drive) {
    Write-Host "ERROR: LEXAR drive not found. Please insert the USB drive." -ForegroundColor Red
    exit
}

$driveLetter = $drive.DriveLetter + ":"
$targetDir = Join-Path $driveLetter "LeadSmithOS_Final"

Write-Host "Found LEXAR drive at $driveLetter" -ForegroundColor Cyan
Write-Host "Injecting LeadSmith OS Files into $targetDir..." -ForegroundColor Cyan

if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

Copy-Item -Path ".\*" -Destination $targetDir -Recurse -Force -Exclude ".git", ".gemini", "__pycache__"

Write-Host "Injection Complete! LeadSmith OS is now staged on the boot drive." -ForegroundColor Green
