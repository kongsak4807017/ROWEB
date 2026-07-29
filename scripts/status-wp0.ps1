[CmdletBinding()]
param(
    [string]$Root = "C:\Ragnarok-Prontera\HermesWorkSpace\ROWEB"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$lockPath = Join-Path $Root "compatibility.lock.json"
if (-not (Test-Path $lockPath)) {
    throw "Missing compatibility lock: $lockPath"
}

$lock = Get-Content $lockPath -Raw | ConvertFrom-Json
$checks = [System.Collections.Generic.List[object]]::new()

function Add-Check {
    param([string]$Name, [bool]$Pass, [string]$Detail)
    $checks.Add([pscustomobject]@{ name = $Name; pass = $Pass; detail = $Detail })
}

function Read-Head {
    param([string]$Path)
    if (-not (Test-Path (Join-Path $Path ".git"))) { return $null }
    Push-Location $Path
    try { return (git rev-parse HEAD 2>$null).Trim() }
    finally { Pop-Location }
}

$clientPath = Join-Path $Root "vendor\roBrowserLegacy"
$serverPath = Join-Path $Root "vendor\rathena"
$clientHead = Read-Head $clientPath
$serverHead = Read-Head $serverPath

Add-Check "compatibility-lock" (Test-Path $lockPath) $lockPath
Add-Check "client-checkout" ($clientHead -eq $lock.client.commit) "actual=$clientHead expected=$($lock.client.commit)"
Add-Check "server-checkout" ($serverHead -eq $lock.server.commit) "actual=$serverHead expected=$($lock.server.commit)"
Add-Check "asset-root" (Test-Path $lock.workspace.assetRoot) $lock.workspace.assetRoot
Add-Check "client-package" (Test-Path (Join-Path $clientPath "package.json")) (Join-Path $clientPath "package.json")
Add-Check "client-build" (Test-Path (Join-Path $clientPath "dist\Web")) (Join-Path $clientPath "dist\Web")
Add-Check "packetver-resolved" ($null -ne $lock.server.packetver.value) "status=$($lock.server.packetver.status) value=$($lock.server.packetver.value)"

$failed = @($checks | Where-Object { -not $_.pass })
$status = if ($failed.Count -eq 0) { "PASS" } else { "BLOCKED" }

$result = [ordered]@{
    generatedAt = (Get-Date).ToString("o")
    status = $status
    checks = $checks
    failedCount = $failed.Count
    nextExecutableAction = if ($failed.Count -eq 0) {
        "Run roBrowserLegacy browser demo and Map Viewer; capture machine-readable and visual evidence."
    } else {
        "Resolve failed checks, then rerun scripts/status-wp0.ps1."
    }
}

$result | ConvertTo-Json -Depth 8
if ($failed.Count -gt 0) { exit 1 }
