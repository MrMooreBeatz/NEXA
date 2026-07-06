$action = New-ScheduledTaskAction -Execute 'C:\Users\Home\moore-awareness\_bin\cloudflared.exe' -Argument 'tunnel --config C:\Users\Home\.cloudflared\config.yml run nexa-dashboard' -WorkingDirectory 'C:\Users\Home\moore-awareness\_bin'
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId 'Home' -RunLevel Highest -LogonType S4U
Register-ScheduledTask -TaskName 'Nexa Tunnel' -Action $action -Trigger $trigger -Principal $principal -Description 'Cloudflare tunnel for Nexa dashboard' -Force
Write-Host '---'
Get-ScheduledTask 'Nexa Tunnel' | Select-Object TaskName, State, @{N='LastResult';E={(Get-ScheduledTaskInfo -TaskName 'Nexa Tunnel').LastTaskResult}}
Write-Host '---'
Get-Process -Name cloudflared -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, StartTime | Format-Table -AutoSize
Write-Host '---'
$env:PATH = 'C:\Users\Home\moore-awareness\_bin;' + $env:PATH
$t = Start-Process -FilePath 'powershell' -ArgumentList '-NoProfile -Command "cd C:\Users\Home\moore-awareness ; python -m streamlit run C:\Users\Home\moore-awareness\07-operations\nexa-dashboard.py --server.headless true"' -PassThru -WindowStyle Hidden
Write-Host 'Streamlit PID:' $t.Id
