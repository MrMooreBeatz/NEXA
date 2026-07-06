$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\NEXA-Phone.lnk")
$Shortcut.TargetPath = "C:\Users\Home\moore-awareness\_bin\Start-Application.bat"
$Shortcut.WorkingDirectory = "C:\Users\Home\moore-awareness\_bin"
$Shortcut.WindowStyle = 7
$Shortcut.Save()
Write-Host 'Startup shortcut created'
