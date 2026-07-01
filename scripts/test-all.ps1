param(
    [switch]$IncludeHuggingFace,
    [switch]$InstallHuggingFace
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
Set-Location $repoRoot

$env:PYTHONPATH = "src"

Write-Host "Kyvoris Profiler test runner" -ForegroundColor Green
Write-Host "Repo: $repoRoot"
Write-Host "PYTHONPATH: $env:PYTHONPATH"

Invoke-Step "Pytest suite" {
    python -m pytest
}

Invoke-Step "Unittest suite" {
    python -m unittest discover -s tests
}

Invoke-Step "Simulated inference example" {
    python examples\run_demo.py
}

Invoke-Step "Async inference example" {
    python examples\run_async_demo.py
}

Invoke-Step "Inline profile_callable smoke test" {
    python -c "from kyvoris_profiler import profile_callable, format_text_report; r=profile_callable(lambda: [x for x in range(1000)], iterations=3, warmup=1, collect_cpu=True, collect_memory=True); print(format_text_report(r))"
}

Invoke-Step "CLI module smoke test" {
    python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --warmup 1 --collect-cpu --collect-memory
}

Invoke-Step "CLI JSON output smoke test" {
    python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --format json --output reports\cli-smoke.json
}

Invoke-Step "CLI async target smoke test" {
    python -m kyvoris_profiler examples.run_async_demo:simulated_async_inference --iterations 3 --warmup 1
}

if ($InstallHuggingFace) {
    Invoke-Step "Install Hugging Face model dependencies" {
        python -m pip install "transformers[torch]"
    }
}

if ($IncludeHuggingFace) {
    Invoke-Step "Hugging Face model example" {
        python examples\run_model_demo.py
    }
}
else {
    Write-Host ""
    Write-Host "SKIP: Hugging Face model example" -ForegroundColor Yellow
    Write-Host "Run with -IncludeHuggingFace to execute it."
    Write-Host "Run with -InstallHuggingFace -IncludeHuggingFace to install dependencies first."
}

Write-Host ""
Write-Host "All requested checks completed." -ForegroundColor Green
