param(
    [string]$Source = "C:\RO-WEB-V1\roBrowserLegacy\src",
    [string]$Assets = "C:\RO-WEB-V1\private-assets\data",
    [string]$Output = ""
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if ([string]::IsNullOrWhiteSpace($Output)) {
    $Output = Join-Path $repoRoot "apps\admin-studio\mockup"
}

if (-not (Test-Path $Source)) {
    throw "roBrowserLegacy source path not found: $Source"
}
if (-not (Test-Path $Assets)) {
    Write-Warning "Asset root not found: $Assets. Catalog will be built but asset matches will be reported missing."
}

$script = Join-Path $PSScriptRoot "build_catalog.py"
$args = @($script, "--source", $Source, "--out", $Output)
if (Test-Path $Assets) {
    $args += @("--assets", $Assets)
}

Write-Host "Building Player UI catalog..." -ForegroundColor Cyan
Write-Host "Repository: $repoRoot"
Write-Host "Source: $Source"
Write-Host "Assets: $Assets"
Write-Host "Output: $Output"

& py @args
if ($LASTEXITCODE -ne 0) {
    throw "Catalog build failed with exit code $LASTEXITCODE"
}

Write-Host "Catalog build complete." -ForegroundColor Green
Write-Host "Open: http://127.0.0.1:4173/player-ui-catalog-studio.html"
