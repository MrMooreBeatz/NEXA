@echo off
setlocal
set "APP_PORT=8080"
set "API_DIR=C:\Users\Home\moore-awareness\NEXA\app\nexa-phone"
set "CFG=C:\Users\Home\.cloudflared\config.yml"
set "LOG=%API_DIR%\logs\watchdog.log"
set "PYDIR=C:\Users\Home\AppData\Local\hermes\hermes-agent\venv\Scripts"
if exist "%PYDIR%\python.exe" (set "PY=%PYDIR%\python.exe") else (set "PY=python")

:loop
  >nul 2>&1 netstat -ano | findstr ':8080.*LISTENING'
  if errorlevel 1 (
    echo %date% %time% [NEXA] starting...>>"%LOG%"
    start "" /B cmd /c ""%PY%" "%API_DIR%\api.py""
    timeout /t 3 /nobreak >nul
  )
  >nul 2>&1 nslookup nexa-dash.mooreawareness.com
  if errorlevel 1 (
    echo %date% %time% [CF] starting tunnel...>>"%LOG%"
    start "" /B cmd /c ""C:\Users\Home\moore-awareness\_bin\cloudflared.exe" tunnel --config "%CFG%" run nexa-dashboard"
    timeout /t 4 /nobreak >nul
  )
  timeout /t 30 /nobreak >nul
goto loop
