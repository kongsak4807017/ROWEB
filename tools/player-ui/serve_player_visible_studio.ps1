param(
    [string]$Assets = "C:\RO-WEB-V1\private-assets\data",
    [int]$Port = 4173
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$directory = Join-Path $repoRoot "apps\admin-studio\mockup"
$script = Join-Path $PSScriptRoot "serve_player_visible_studio.py"

if (-not (Test-Path $Assets)) { throw "Asset root not found: $Assets" }
if (-not (Test-Path $directory)) { throw "Studio directory not found: $directory" }

Write-Host "Starting Player-visible Content Studio" -ForegroundColor Cyan
Write-Host "Studio: $directory"
Write-Host "Assets: $Assets"
Write-Host "URL: http://127.0.0.1:$Port/player-visible-content-studio.html"

& py $script --directory $directory --assets $Assets --port $Port
