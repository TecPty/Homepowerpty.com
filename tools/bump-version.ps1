param(
    [Parameter(Mandatory = $true)]
    [string]$Version
)

# Simple version bumper for asset URLs in index.html
$file = Join-Path $PSScriptRoot "..\index.html"
if (!(Test-Path $file)) {
    Write-Error "index.html no encontrado en el directorio esperado: $file"
    exit 1
}

$content = Get-Content $file -Raw

# Reemplaza query params existentes ?v=... en href/src locales
$content = $content -replace '(?<=\.(css|js))\?v=[0-9A-Za-z_.-]+', "?v=$Version"

# Agrega ?v si falta en archivos locales .css/.js (no afecta URLs absolutas http/https)
$content = $content -replace '(href|src)="((?!https?:)[^"]+\.(css|js))"', "$1=\"$2?v=$Version\""

Set-Content -Path $file -Value $content -Encoding UTF8
Write-Host "Versionado actualizado a v=$Version en index.html"

