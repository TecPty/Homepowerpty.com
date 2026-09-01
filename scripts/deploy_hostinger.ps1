param(
  [string]$ZipOut = $(Join-Path (Resolve-Path .) ("deploy/site_" + (Get-Date -Format yyyyMMdd_HHmm) + ".zip")),
  [switch]$SkipBuild
)

<#
Usage:
  - Run this script to build the site and produce a clean ZIP of dist/ you can
    upload to Hostinger hPanel/cPanel File Manager.
  - After it finishes, login to hPanel/cPanel, open File Manager, upload the ZIP
    directly into your document root (e.g. public_html) and use the Extract option.
  - IMPORTANT: extract into the document root itself, NOT into a subfolder. The
    build uses root-absolute asset paths (/assets/...), so it only works when
    deployed at the domain root.

History:
  - This script used to ZIP a raw mirror of the whole repo (relative paths,
    no build step). That approach shipped ~400MB of dev-only content (two
    Python venvs with compiled binaries, internal docs, a confidential .xlsx,
    test artifacts) and, in production on Hostinger, left the site completely
    unstyled. It was replaced 2026-07 after `npm run build` -> upload dist/
    was confirmed working in production and the mirror approach was not.

Notes:
  - Requires Node/npm installed (runs `npm run build`, i.e. `vite build`).
  - Pass -SkipBuild to zip an existing dist/ without rebuilding.
  - It does NOT perform FTP/FTPS upload (recommended: use File Manager or an
    FTP client like FileZilla/WinSCP).
#>

$ErrorActionPreference = 'Stop'

function New-DistZip {
  param(
    [Parameter(Mandatory)][string]$DestinationZip,
    [bool]$RunBuild
  )

  $distDir = (Join-Path (Resolve-Path .).Path 'dist')

  if ($RunBuild) {
    Write-Host "Building (npm run build)..." -ForegroundColor Cyan
    & npm run build
    if ($LASTEXITCODE -ne 0) { throw "npm run build failed with code $LASTEXITCODE" }
  }

  if (!(Test-Path $distDir)) {
    throw "dist/ not found at $distDir. Run without -SkipBuild, or run 'npm run build' first."
  }

  $destDir = Split-Path -Parent $DestinationZip
  if (!(Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }

  Write-Host "Creating zip: $DestinationZip" -ForegroundColor Green
  if (Test-Path $DestinationZip) { Remove-Item $DestinationZip -Force }
  # dist/* directo a la raiz del zip (no metemos la carpeta "dist" adentro):
  # al extraer en public_html, index.html debe quedar en la raiz del docroot.
  Compress-Archive -Path (Join-Path $distDir '*') -DestinationPath $DestinationZip -CompressionLevel Optimal

  $sizeMB = [Math]::Round((Get-Item $DestinationZip).Length/1MB,2)
  Write-Host ("ZIP ready: {0} ({1} MB)" -f $DestinationZip, $sizeMB) -ForegroundColor Green
}

New-DistZip -DestinationZip $ZipOut -RunBuild (-not $SkipBuild)

Write-Host "Next: Upload the ZIP via Hostinger hPanel > Files > File Manager > public_html > Upload > Extract (into public_html itself, not a subfolder)." -ForegroundColor Yellow
