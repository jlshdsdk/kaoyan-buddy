param(
  [ValidateSet("night", "morning")]
  [string]$Checkin = "morning"
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$log = Join-Path $root "buddy.log"
$port = 8766
$url = "http://127.0.0.1:$port/"
if ($Checkin -eq "night") { $url += "?checkin=night" }

function Write-Log([string]$message) {
  Add-Content -LiteralPath $log -Value ((Get-Date).ToString("yyyy-MM-dd HH:mm:ss") + " " + $message) -Encoding utf8
}

function Test-Port {
  $probe = New-Object System.Net.Sockets.TcpClient
  try {
    $probe.Connect("127.0.0.1", $port)
    return $true
  } catch {
    return $false
  } finally {
    $probe.Dispose()
  }
}

try {
  Write-Log ("open " + $Checkin)
  if (-not (Test-Port)) {
    $pythonw = Join-Path $env:LOCALAPPDATA "Programs\Python\Python314\pythonw.exe"
    $python = Join-Path $env:LOCALAPPDATA "Programs\Python\Python314\python.exe"
    if (Test-Path -LiteralPath $pythonw) {
      $exe = $pythonw
      $args = @("server.py")
    } elseif (Test-Path -LiteralPath $python) {
      $exe = $python
      $args = @("server.py")
    } else {
      $cmd = Get-Command python -ErrorAction SilentlyContinue
      if (-not $cmd) { throw "python not found" }
      $exe = $cmd.Source
      $args = @("server.py")
    }
    Write-Log ("start " + $exe)
    Start-Process -FilePath $exe -ArgumentList $args -WorkingDirectory $root -WindowStyle Hidden
    $ready = $false
    for ($i = 0; $i -lt 30; $i++) {
      Start-Sleep -Milliseconds 300
      if (Test-Port) { $ready = $true; break }
    }
    if (-not $ready) { throw "server did not start" }
  }
  Start-Process $url
  Write-Log "browser opened"
} catch {
  Write-Log ("ERROR " + $_.Exception.Message)
  throw
}
