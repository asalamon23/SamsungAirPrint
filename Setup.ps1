$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
Write-Host 'Samsung AirPrint Bridge setup for Windows 11' -ForegroundColor Cyan
if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw 'Install Python 3.11+ from python.org (including the Python launcher), then rerun.' }
py -3 -m venv .venv
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $python -m pip install --upgrade pip
& $python -m pip install 'zeroconf>=0.130' 'PyMuPDF>=1.24' 'Pillow>=10' 'pywin32>=306'
if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed.' }
$source = 'https://raw.githubusercontent.com/salmanasmat/Windows-AirPrint-Bridge/main/airprint_bridge.py'
Invoke-WebRequest -Uri $source -OutFile (Join-Path $PSScriptRoot 'airprint_bridge.py')
Write-Host 'Downloaded GPL-3.0 AirPrint engine from its upstream repository.'
Write-Host 'You can inspect airprint_bridge.py before running.'
Write-Host 'Firewall rule: allow TCP 631 on Private networks only.'
$choice = Read-Host 'Add firewall rule now? (requires Administrator; Y/N)'
if ($choice -match '^[Yy]') {
  $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
  if (-not $isAdmin) { Write-Warning 'Re-run PowerShell as Administrator to add the rule, or allow the app through Windows Firewall manually.' }
  else {
    if (-not (Get-NetFirewallRule -DisplayName 'Samsung AirPrint Bridge TCP 631' -ErrorAction SilentlyContinue)) {
      New-NetFirewallRule -DisplayName 'Samsung AirPrint Bridge TCP 631' -Direction Inbound -Protocol TCP -LocalPort 631 -Action Allow -Profile Private | Out-Null
    }
  }
}
Write-Host 'Setup complete. Double-click Start Bridge.bat.' -ForegroundColor Green
Read-Host 'Press Enter to close'
