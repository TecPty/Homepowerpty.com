param([int]$Port = 8080)

Write-Host "Checking port..." -ForegroundColor Cyan
if ((Test-NetConnection -ComputerName 127.0.0.1 -Port $Port -WarningAction SilentlyContinue).TcpTestSucceeded) {
  $Port = 8000
}

if (Get-Command php -ErrorAction SilentlyContinue) {
  Write-Host ("Starting PHP server at http://localhost:{0}" -f $Port) -ForegroundColor Green
  php -S "localhost:$Port" -t .
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
  Write-Host ("Starting Python server at http://localhost:{0}" -f $Port) -ForegroundColor Green
  python -m http.server $Port
}
else {
  Write-Error "PHP or Python not found in PATH. Please install one."
}

