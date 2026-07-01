param(
    [switch]$SkipBuildDependencyInstall
)

$ErrorActionPreference = "Stop"

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [scriptblock]$Command
    )

    Write-Host ""
    Write-Host "==> $Name" -ForegroundColor Cyan
    Write-Host ""

    & $Command

    if ($LASTEXITCODE -ne $null -and $LASTEXITCODE -ne 0) {
        throw "Step failed: $Name"
    }

    Write-Host ""
    Write-Host "PASS: $Name" -ForegroundColor Green
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$distPath = Join-Path $repoRoot "dist"
$buildPath = Join-Path $repoRoot "build"
$tempRoot = Join-Path $repoRoot ".release-check"
$venvPath = Join-Path $tempRoot "venv"
$pythonPath = Join-Path $venvPath "Scripts\python.exe"
$consolePath = Join-Path $venvPath "Scripts\kyvoris-profiler.exe"

Set-Location $repoRoot

Write-Host "Kyvoris Profiler release check" -ForegroundColor Green
Write-Host "Repo: $repoRoot"

Invoke-Step "Clean build artifacts" {
    Remove-Item -LiteralPath $distPath -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $buildPath -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
}

if (-not $SkipBuildDependencyInstall) {
    Invoke-Step "Install build tools" {
        python -m pip install --upgrade build twine
    }
}

Invoke-Step "Build package artifacts" {
    python -m build
}

Invoke-Step "Validate package artifacts" {
    python -m twine check dist\*
}

Invoke-Step "Create clean install environment" {
    python -m venv $venvPath
}

Invoke-Step "Install built wheel" {
    $wheel = Get-ChildItem -LiteralPath $distPath -Filter "*.whl" | Select-Object -First 1
    if ($null -eq $wheel) {
        throw "No wheel was created in dist."
    }
    & $pythonPath -m pip install --upgrade pip
    & $pythonPath -m pip install $wheel.FullName
}

Invoke-Step "Validate installed package import" {
    & $pythonPath -c "import kyvoris_profiler; assert kyvoris_profiler.__version__ == '0.14.0', kyvoris_profiler.__version__; print(kyvoris_profiler.__version__)"
}

Invoke-Step "Validate installed console script" {
    & $consolePath --version
}

Write-Host ""
Write-Host "Release readiness checks completed." -ForegroundColor Green
