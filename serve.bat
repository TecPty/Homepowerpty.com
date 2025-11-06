@echo off
setlocal ENABLEDELAYEDEXPANSION

set PORT=8080
rem Basic port check fallback
PowerShell -NoProfile -Command "if ((Test-NetConnection -ComputerName 127.0.0.1 -Port %PORT% -WarningAction SilentlyContinue).TcpTestSucceeded) { exit 0 } else { exit 1 }"
if %ERRORLEVEL%==0 (
  set PORT=8000
)

where php >nul 2>nul
if %ERRORLEVEL%==0 (
  echo Starting PHP server at http://localhost:%PORT% ...
  php -S localhost:%PORT% -t .
  goto :eof
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
  echo Starting Python server at http://localhost:%PORT% ...
  python -m http.server %PORT%
  goto :eof
)

echo No PHP or Python found in PATH. Please install one.
exit /b 1

