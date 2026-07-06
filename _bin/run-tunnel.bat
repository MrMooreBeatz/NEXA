@echo off
setlocal
set "CLOUDFLARED=C:\Users\Home\moore-awareness\_bin\cloudflared.exe"
set "CONFIG=C:\Users\Home\AppData\Roaming\cloudflared\config.yml"
echo starting tunnel...
"%CLOUDFLARED%" tunnel --config "%CONFIG%" run sobrr-tunnel
endlocal
