# Enable logging

# TODO Change appName, logroot
$appName = "TODO"
$logroot = "C:\temp\logs\$($appName)"
$daysToKeep = -14
If (!(Test-Path $logroot)) {New-Item -ItemType Directory -Force -Path $logroot}

$ErrorActionPreference="SilentlyContinue"
Stop-Transcript | out-null
$ErrorActionPreference = "Continue"
Start-Transcript -path "$($logroot)\$(get-date -f yyyyMMddHHmmss)-$($appName).txt" -append

# Remove old log files
# TODO change filter
Get-ChildItem -Path $logroot -Filter "*-$($appName).txt" -Recurse -File | Where-Object LastWriteTime -le (Get-Date).AddDays($daysToKeep) | Remove-Item -Force

Write-Output "Do something..."

Stop-Transcript