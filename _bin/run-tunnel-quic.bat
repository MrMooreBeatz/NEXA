@echo off
setlocal
cd /d "%~dp0"
echo [TUNNEL] starting cloudflared...
start "" /b cmd.exe /c ""%~dp0cloudflared.exe" tunnel --config "%APPDATA%\cloudflared\config.yml" run"
timeout /t 9999 >nul
endlocal
