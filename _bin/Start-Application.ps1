$ErrorActionPreference = 'Stop'
$ApiDir = 'C:\Users\Home\moore-awareness\NEXA\app\nexa-phone'
$ApiPy = Join-Path $ApiDir 'api.py'
$LogDir = Join-Path $ApiDir 'logs'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Logger = Join-Path $LogDir 'flask.log'
$Py = 'C:\Users\Home\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe'
if (-not (Test-Path $Py)) { $Py = 'python' }

Set-Content -Path $Logger -Value "[$(Get-Date -Format o)] START`r`n" -Encoding UTF8
$env:NEXA_API_DIR = $ApiDir
$proc = Start-Process -FilePath $Py -ArgumentList "$ApiPy" -WorkingDirectory $ApiDir -PassThru -NoNewWindow -Wait -RedirectStandardOutput $Logger -RedirectStandardError $Logger
if ($LASTEXITCODE -ne $null) { Write-Error "Exit: $LASTEXITCODE" }
if ((Test-Path $Logger) -and (Get-Content $Logger -Tail 20)) {
  Write-Host (Get-Content $Logger -Tail 20 | Out-String)
}
