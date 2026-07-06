@echo off
setlocal
set STARTUP_LOG=C:\Users\Home\moore-awareness\_bin\nexa-startup.log

:: Batch-mode watchdog until Windows Task Scheduler is configured to run alone.
call C:\Users\Home\moore-awareness\_bin\nexa-startup.bat

goto main

:wait_for_exit
set P=%1
set INTERVAL=5
:check_again
timeout /t %INTERVAL% /nobreak >nul
tasklist /FI "PID eq %P%" 2>NUL | find /I /N "%P%" >NUL
if %ERRORLEVEL% EQU 0 goto check_again
echo [%date% %time%] Process %P% exited >> "%STARTUP_LOG%"
goto :eof

:main
for /f "tokens=2 delims=," %%I in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul ^| find /I /C "python.exe"') do set PY_COUNT=%%I
for /f "tokens=2 delims=," %%I in ('tasklist /FI "IMAGENAME eq cloudflared.exe" /FO CSV /NH 2>nul ^| find /I /C "cloudflared.exe"') do set CF_COUNT=%%I

echo [%date% %time%] Watchdog check: python=%PY_COUNT% cloudflared=%CF_COUNT% >> "%STARTUP_LOG%"

if %PY_COUNT%==0 call C:\Users\Home\moore-awareness\_bin\nexa-startup.bat
if %CF_COUNT%==0 call C:\Users\Home\moore-awareness\_bin\nexa-startup.bat

timeout /t 60 /nobreak >nul
goto main
