# Run Guide

## Why the pages were conflicting

This workspace contains more than one Django project:

- `D:\workmulu\Learning_platform\Online_Learning`
- `D:\workmulu\Learning_platform\HelloWorld`
- `D:\workmulu\manage.py` also points to another older Django site outside this folder

If you run `python manage.py runserver` from the wrong directory, Django may start the old site instead of `Online_Learning`.

## Recommended fixed ports

- `Online_Learning`: `127.0.0.1:8012`
- `HelloWorld`: `127.0.0.1:8013`

## Start commands

From `D:\workmulu\Learning_platform` run:

```powershell
powershell -ExecutionPolicy Bypass -File .\start_online_learning.ps1
```

```powershell
powershell -ExecutionPolicy Bypass -File .\start_helloworld.ps1
```

You can also choose a custom port:

```powershell
powershell -ExecutionPolicy Bypass -File .\start_online_learning.ps1 8020
```

## Direct command format

If you do not want to use scripts, always use the absolute `manage.py` path:

```powershell
D:\workmulu\.venv\Scripts\python.exe D:\workmulu\Learning_platform\Online_Learning\manage.py runserver 127.0.0.1:8012
```

```powershell
D:\workmulu\.venv\Scripts\python.exe D:\workmulu\Learning_platform\HelloWorld\manage.py runserver 127.0.0.1:8013
```

Do not run `python manage.py runserver` from `D:\workmulu`, because that starts the older `kg_site` project.

## Quick checks

After startup, open:

- `http://127.0.0.1:8012/` for `Online_Learning`
- `http://127.0.0.1:8013/` for `HelloWorld`

If the page still looks wrong, check which process is listening:

```powershell
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 8012,8013,8000,8001 } | Select-Object LocalAddress,LocalPort,OwningProcess
```
