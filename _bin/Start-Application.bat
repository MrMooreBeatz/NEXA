@echo off
setlocal
set "PYDIR=C:\Users\Home\AppData\Local\hermes\hermes-agent\venv\Scripts"
if exist "%PYDIR%\python.exe" (
  set "PY=%PYDIR%\python.exe"
) else (
  set "PY=python"
)
cd /d C:\Users\Home\moore-awareness\NEXA\app\nexa-phone
start "" /B cmd /c ""%PY%" api.py""
start "" /B cmd /c ""C:\Users\Home\moore-awareness\_bin\cloudflared.exe" tunnel --config "C:\Users\Home\.cloudflared\config.yml" run nexa-dashboard"
endlocal
