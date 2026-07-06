@echo off
setlocal

set CLOUDFLARED=C:\Users\Home\moore-awareness\_bin\cloudflared.exe
set DASHBOARD=C:\Users\Home\moore-awareness\07-operations\nexa-dashboard.py
set TUNNEL_CONFIG=C:\Users\Home\.cloudflared\config.yml
set PROJECT_DIR=C:\Users\Home\moore-awareness
set LOG=C:\Users\Home\moore-awareness\_bin\nexa-startup.log

echo [%date% %time%] Nexa startup sequence initiated >> "%LOG%"

echo [%date% %time%] Starting Streamlit dashboard >> "%LOG%"
start "Nexa Dashboard" /B cmd /c "cd /d %PROJECT_DIR% && python -m streamlit run %DASHBOARD% --server.headless true >> C:\Users\Home\moore-awareness\_bin\nexa-dashboard.log 2>&1"

timeout /t 8 /nobreak >nul

echo [%date% %time%] Starting Cloudflare tunnel >> "%LOG%"
start "Nexa Tunnel" /B cmd /c ""%CLOUDFLARED%" tunnel --config "%TUNNEL_CONFIG%" run nexa-dashboard >> C:\Users\Home\moore-awareness\_bin\nexa-tunnel.log 2>&1"

timeout /t 5 /nobreak >nul

echo [%date% %time%] Startup sequence complete >> "%LOG%"

timeout /t 10 /nobreak >nul
curl -s -o nul -w "%%{http_code}" https://nexa-dash.mooreawareness.com/ > C:\Users\Home\moore-awareness\_bin\nexa-healthcheck.txt 2>nul
echo. >> C:\Users\Home\moore-awareness\_bin\nexa-healthcheck.txt

endlocal
