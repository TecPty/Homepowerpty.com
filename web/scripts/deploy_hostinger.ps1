param(
  [string]$ZipOut = $(Join-Path (Resolve-Path .) ("deploy/site_" + (Get-Date -Format yyyyMMdd_HHmm) + ".zip"))
)

<#
Usage:
  - Run this script to produce a clean ZIP you can upload to Hostinger hPanel/cPanel File Manager.
  - After it finishes, login to hPanel/cPanel, open File Manager, upload the ZIP to your document root (e.g. public_html) and use the Extract option.

Notes:
  - This script excludes common dev folders (.git, .vscode, node_modules, deploy) and temp files.
  - It does NOT perform FTP/FTPS upload (recommended: use File Manager or an FTP client like FileZilla/WinSCP).
#>

$ErrorActionPreference = 'Stop'

function New-CleanZip {
  param(
    [Parameter(Mandatory)][string]$DestinationZip
  )
  $src = (Resolve-Path .).Path
  $work = Join-Path $env:TEMP ("deploy_homepower_" + [System.Guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $work | Out-Null

  Write-Host "Staging files..." -ForegroundColor Cyan
  $excludeDirs = @('.git', '.vscode', '.idea', '.github', 'node_modules', 'deploy')
  $excludeFiles = @('*.pid', '*.tmp', '*.log')

  $args = @(
    '"{0}"' -f $src,
    '"{0}"' -f $work,
    '/MIR',
    '/NFL','/NDL','/NJH','/NJS','/NP','/R:1','/W:1'
  )
  foreach($d in $excludeDirs){ $args += @('/XD', $d) }
  foreach($f in $excludeFiles){ $args += @('/XF', $f) }

  $robocopy = Start-Process -FilePath robocopy -ArgumentList $args -NoNewWindow -PassThru -Wait
  # Robocopy exit codes 0-7 are success
  if ($robocopy.ExitCode -gt 7) { throw "Robocopy failed with code $($robocopy.ExitCode)" }

  $destDir = Split-Path -Parent $DestinationZip
  if (!(Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }

  Write-Host "Creating zip: $DestinationZip" -ForegroundColor Green
  if (Test-Path $DestinationZip) { Remove-Item $DestinationZip -Force }
  Compress-Archive -Path (Join-Path $work '*') -DestinationPath $DestinationZip -CompressionLevel Optimal

  $sizeMB = [Math]::Round((Get-Item $DestinationZip).Length/1MB,2)
  Write-Host ("ZIP ready: {0} ({1} MB)" -f $DestinationZip, $sizeMB) -ForegroundColor Green

  Remove-Item $work -Recurse -Force
}

New-CleanZip -DestinationZip $ZipOut

Write-Host "Next: Upload the ZIP via Hostinger hPanel > Files > File Manager > public_html > Upload > Extract." -ForegroundColor Yellow

