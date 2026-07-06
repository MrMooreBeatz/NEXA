# Start Moore Dashboard + Cloudflare tunnel as a scheduled-task launcher
Set-StrictMode -Version Latest
$ErrorActionPreference = 'SilentlyContinue'

$dashboard = 'C:\Users\Home\moore-awareness\04-app\steven-dashboard'
$pythonExe = 'C:\Users\Home\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe'
$streamlit = Join-Path $dashboard 'steven_dashboard.py'
$cloudflared = 'C:\Users\Home\moore-awareness\_bin\cloudflared.exe'
$cloudflaredConfig = 'C:\Users\Home\AppData\Roaming\cloudflared\config.yml'

if (-not (Test-Path $streamlit)) {
  Write-Error "Dashboard file missing: $streamlit"
  exit 1
}
if (-not (Test-Path $cloudflared)) {
  Write-Error "Cloudflared missing: $cloudflared"
  exit 1
}

# Launch streamlit detached
Start-Process -FilePath $pythonExe -ArgumentList "-u","$streamlit" -WorkingDirectory $dashboard

# Small delay to let streamlit bind
Start-Sleep -Seconds 3

# Launch cloudflared tunnel detached
Start-Process -FilePath $cloudflared -ArgumentList "tunnel","run","--config",$cloudflaredConfig
