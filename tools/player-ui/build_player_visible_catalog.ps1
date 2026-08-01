param(
    [ValidateSet("player-visible", "ui", "items", "text")]
    [string]$Profile = "player-visible",
    [string]$Source = "C:\RO-WEB-V1\roBrowserLegacy\src",
    [string]$Assets = "C:\RO-WEB-V1\private-assets\data",
    [string]$Output = ""
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Source)) {
    throw "roBrowserLegacy source path not found: $Source"
}
if (-not (Test-Path $Assets)) {
    throw "private asset root not found: $Assets"
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if ([string]::IsNullOrWhiteSpace($Output)) {
    $Output = Join-Path $repoRoot "apps\admin-studio\mockup"
}

$script = Join-Path $PSScriptRoot "build_player_visible_catalog.py"
Write-Host "Building player-visible content catalog" -ForegroundColor Cyan
Write-Host "Profile: $Profile"
Write-Host "Source:  $Source"
Write-Host "Assets:  $Assets"
Write-Host "Output:  $Output"

& py $script --source $Source --assets $Assets --out $Output --profile $Profile
if ($LASTEXITCODE -ne 0) {
    throw "Player-visible catalog build failed with exit code $LASTEXITCODE"
}

Write-Host "Catalog written to:" -ForegroundColor Green
Write-Host (Join-Path $Output "player-visible-content-catalog.json")
