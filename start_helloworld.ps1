$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$appRoot = Join-Path $projectRoot "HelloWorld"
$managePy = Join-Path $appRoot "manage.py"
$pythonExe = "C:\Users\DELL\AppData\Local\Microsoft\WindowsApps\python.exe"
$hostAddress = "127.0.0.1"
$port = if ($args.Count -gt 0) { $args[0] } else { "8013" }
if (-not (Test-Path $managePy)) {
    Write-Error "Cannot find $managePy"
    exit 1
}
if (-not (Test-Path $pythonExe)) {
    Write-Error "Cannot find $pythonExe"
    exit 1
}
Write-Host "Starting HelloWorld at http://$hostAddress`:$port/"
Set-Location $appRoot
& $pythonExe $managePy runserver "$hostAddress`:$port"

# 新增：执行完毕暂停，按回车关闭
Read-Host "`n执行完成，按回车键关闭窗口"