[CmdletBinding()]
param(
    [string]$Root = "C:\Ragnarok-Prontera\HermesWorkSpace\ROWEB",
    [switch]$SkipInstall,
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Assert-Command {
    param([Parameter(Mandatory)][string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found in PATH."
    }
}

function Invoke-Checked {
    param(
        [Parameter(Mandatory)][string]$Label,
        [Parameter(Mandatory)][scriptblock]$Action
    )
    Write-Host "==> $Label"
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE."
    }
}

Assert-Command git
Assert-Command node
Assert-Command npm

$lockPath = Join-Path $Root "compatibility.lock.json"
if (-not (Test-Path $lockPath)) {
    throw "Missing compatibility lock: $lockPath"
}

$lock = Get-Content $lockPath -Raw | ConvertFrom-Json
$vendorRoot = Join-Path $Root "vendor"
$runtimeRoot = $lock.workspace.runtimeRoot
New-Item -ItemType Directory -Force -Path $vendorRoot, $runtimeRoot, (Join-Path $runtimeRoot "logs"), (Join-Path $runtimeRoot "pids") | Out-Null

$repos = @(
    @{
        Name = "roBrowserLegacy"
        Url = $lock.client.repository
        Commit = $lock.client.commit
        Path = Join-Path $vendorRoot "roBrowserLegacy"
    },
    @{
        Name = "rathena"
        Url = $lock.server.repository
        Commit = $lock.server.commit
        Path = Join-Path $vendorRoot "rathena"
    }
)

foreach ($repo in $repos) {
    if (-not (Test-Path (Join-Path $repo.Path ".git"))) {
        Invoke-Checked "Clone $($repo.Name)" { git clone --no-tags $repo.Url $repo.Path }
    }

    Push-Location $repo.Path
    try {
        Invoke-Checked "Fetch pinned commit for $($repo.Name)" { git fetch origin $repo.Commit --depth 1 }
        Invoke-Checked "Checkout pinned commit for $($repo.Name)" { git checkout --detach $repo.Commit }
        $actual = (git rev-parse HEAD).Trim()
        if ($actual -ne $repo.Commit) {
            throw "$($repo.Name) resolved to $actual, expected $($repo.Commit)."
        }
    }
    finally {
        Pop-Location
    }
}

$clientRoot = Join-Path $vendorRoot "roBrowserLegacy"
Push-Location $clientRoot
try {
    if (-not $SkipInstall) {
        if (Test-Path "package-lock.json") {
            Invoke-Checked "Install roBrowserLegacy dependencies" { npm ci }
        }
        else {
            Invoke-Checked "Install roBrowserLegacy dependencies" { npm install }
        }
    }

    if (-not $SkipBuild) {
        Invoke-Checked "Build roBrowserLegacy" { npm run build:all }
    }
}
finally {
    Pop-Location
}

$report = [ordered]@{
    generatedAt = (Get-Date).ToString("o")
    root = $Root
    node = (node --version).Trim()
    npm = (npm --version).Trim()
    git = (git --version).Trim()
    clientCommit = $lock.client.commit
    serverCommit = $lock.server.commit
    assetRoot = $lock.workspace.assetRoot
    assetRootExists = Test-Path $lock.workspace.assetRoot
    buildSkipped = [bool]$SkipBuild
    status = if ($SkipBuild) { "BOOTSTRAPPED" } else { "BUILD_COMPLETED" }
}

$reportPath = Join-Path $runtimeRoot "wp0-environment-report.json"
$report | ConvertTo-Json -Depth 6 | Set-Content -Path $reportPath -Encoding UTF8
Write-Host "WP0 bootstrap complete. Report: $reportPath"
