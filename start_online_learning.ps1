$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$appRoot = Join-Path $projectRoot "Online_Learning"
$managePy = Join-Path $appRoot "manage.py"
$pythonExe = "C:\Users\DELL\AppData\Local\Microsoft\WindowsApps\python.exe"
$hostAddress = "127.0.0.1"
$port = if ($args.Count -gt 0) { $args[0] } else { "8012" }

if (-not (Test-Path $managePy)) {
    Write-Error "Cannot find $managePy"
    exit 1
}

if (-not (Test-Path $pythonExe)) {
    Write-Error "Cannot find $pythonExe"
    exit 1
}

Write-Host "Starting Online_Learning at http://$hostAddress`:$port/"
Set-Location $appRoot
& $pythonExe $managePy runserver "$hostAddress`:$port"
