$ErrorActionPreference = "Stop"
$ps = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"
$script = Join-Path $PSScriptRoot "open-buddy.ps1"
$night = "`"$ps`" -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$script`" -Checkin night"
$morning = "`"$ps`" -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$script`" -Checkin morning"

schtasks /Create /F /SC DAILY /ST 22:00 /TN "KaoyanBuddyNight" /TR $night
if ($LASTEXITCODE -ne 0) { throw "night task failed" }
schtasks /Create /F /SC DAILY /ST 08:30 /TN "KaoyanBuddyMorning" /TR $morning
if ($LASTEXITCODE -ne 0) { throw "morning task failed" }
Write-Host "tasks installed"
