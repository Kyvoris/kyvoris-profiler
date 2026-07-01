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

function Assert-PathExists {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Expected path was not created: $Path"
    }
}

function Assert-FileContains {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Text
    )

    Assert-PathExists $Path
    $content = Get-Content -LiteralPath $Path -Raw
    if (-not $content.Contains($Text)) {
        throw "Expected '$Path' to contain '$Text'"
    }
}

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$env:PYTHONPATH = "src"

Write-Host "Kyvoris Profiler test runner" -ForegroundColor Green
Write-Host "Repo: $repoRoot"
Write-Host "PYTHONPATH: $env:PYTHONPATH"

Invoke-Step "Package version check" {
    python -c "import kyvoris_profiler; assert kyvoris_profiler.__version__ == '0.12.0', kyvoris_profiler.__version__; print(kyvoris_profiler.__version__)"
}

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

Invoke-Step "CLI JSON output validation" {
    Assert-PathExists "reports\cli-smoke.json"
    python -c "import json; data=json.load(open('reports/cli-smoke.json', encoding='utf-8')); assert data['schema_version'] == '1.0'; assert data['metrics']['iterations'] == 3; assert 'average_ms' in data['metrics']; print('JSON report valid')"
}

Invoke-Step "CLI HTML output smoke test" {
    python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --format html --output reports\cli-smoke.html
}

Invoke-Step "CLI HTML output validation" {
    Assert-FileContains "reports\cli-smoke.html" "<!doctype html>"
    Assert-FileContains "reports\cli-smoke.html" "Benchmark Results"
}

Invoke-Step "CLI CSV output smoke test" {
    python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --format csv --output reports\cli-smoke.csv
}

Invoke-Step "CLI CSV output validation" {
    Assert-FileContains "reports\cli-smoke.csv" "metric,value"
    Assert-FileContains "reports\cli-smoke.csv" "Average"
}

Invoke-Step "Comparison demo" {
    python examples\run_comparison_demo.py
}

Invoke-Step "CLI comparison smoke test" {
    python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --format json --output reports\baseline-smoke.json
    python -m kyvoris_profiler examples.run_demo:simulated_inference --iterations 3 --format json --output reports\candidate-smoke.json
    python -m kyvoris_profiler compare reports\baseline-smoke.json reports\candidate-smoke.json --format markdown --output reports\comparison-smoke.md
}

Invoke-Step "CLI comparison output validation" {
    Assert-PathExists "reports\comparison-smoke.md"
    Assert-FileContains "reports\comparison-smoke.md" "Benchmark Comparison"
    Assert-FileContains "reports\comparison-smoke.md" "average_ms"
}

Invoke-Step "CLI comparison HTML output smoke test" {
    python -m kyvoris_profiler compare reports\baseline-smoke.json reports\candidate-smoke.json --format html --output reports\comparison-smoke.html
}

Invoke-Step "CLI comparison HTML output validation" {
    Assert-FileContains "reports\comparison-smoke.html" "<!doctype html>"
    Assert-FileContains "reports\comparison-smoke.html" "Benchmark Comparison"
}

Invoke-Step "CLI comparison CSV output smoke test" {
    python -m kyvoris_profiler compare reports\baseline-smoke.json reports\candidate-smoke.json --format csv --output reports\comparison-smoke.csv
}

Invoke-Step "CLI comparison CSV output validation" {
    Assert-FileContains "reports\comparison-smoke.csv" "metric,baseline,candidate,delta,percent_change,result"
    Assert-FileContains "reports\comparison-smoke.csv" "average_ms"
}

Invoke-Step "CLI history append smoke test" {
    Remove-Item -LiteralPath reports\history-smoke.jsonl -ErrorAction SilentlyContinue
    python -m kyvoris_profiler history append reports\baseline-smoke.json --history reports\history-smoke.jsonl --label baseline --metadata model=baseline-demo
    python -m kyvoris_profiler history append reports\candidate-smoke.json --history reports\history-smoke.jsonl --label candidate --metadata model=candidate-demo
}

Invoke-Step "CLI history list smoke test" {
    python -m kyvoris_profiler history list --history reports\history-smoke.jsonl | Tee-Object -FilePath reports\history-list-smoke.txt
}

Invoke-Step "CLI history list output validation" {
    Assert-FileContains "reports\history-list-smoke.txt" "Index | Timestamp | Label | Average | P95 | Metadata"
    Assert-FileContains "reports\history-list-smoke.txt" "model=baseline-demo"
}

Invoke-Step "CLI filtered history list smoke test" {
    python -m kyvoris_profiler history list --history reports\history-smoke.jsonl --metadata model=candidate-demo --limit 1 | Tee-Object -FilePath reports\history-filtered-list-smoke.txt
}

Invoke-Step "CLI filtered history list output validation" {
    Assert-FileContains "reports\history-filtered-list-smoke.txt" "model=candidate-demo"
    Assert-FileContains "reports\history-filtered-list-smoke.txt" "candidate"
}

Invoke-Step "CLI selected history comparison smoke test" {
    python -m kyvoris_profiler history compare --history reports\history-smoke.jsonl --baseline 1 --candidate 2 --format markdown --output reports\history-selected-comparison-smoke.md
}

Invoke-Step "CLI latest label history comparison smoke test" {
    python -m kyvoris_profiler history compare --history reports\history-smoke.jsonl --baseline latest:baseline --candidate latest:candidate --format markdown --output reports\history-latest-label-comparison-smoke.md
}

Invoke-Step "CLI selected history comparison validation" {
    Assert-FileContains "reports\history-selected-comparison-smoke.md" "Benchmark History Comparison"
    Assert-FileContains "reports\history-selected-comparison-smoke.md" 'Baseline: `baseline`'
    Assert-FileContains "reports\history-selected-comparison-smoke.md" 'Candidate: `candidate`'
    Assert-FileContains "reports\history-latest-label-comparison-smoke.md" "Benchmark History Comparison"
}

Invoke-Step "CLI history comparison smoke test" {
    python -m kyvoris_profiler history compare-latest --history reports\history-smoke.jsonl --format markdown --output reports\history-comparison-smoke.md
}

Invoke-Step "CLI history output validation" {
    Assert-PathExists "reports\history-smoke.jsonl"
    Assert-FileContains "reports\history-comparison-smoke.md" "Benchmark History Comparison"
    Assert-FileContains "reports\history-comparison-smoke.md" "average_ms"
}

Invoke-Step "CLI history threshold pass smoke test" {
    python -m kyvoris_profiler history compare-latest --history reports\history-smoke.jsonl --max-regression-percent 100 --threshold-metric average_ms --fail-on-regression
}

Invoke-Step "CLI threshold pass smoke test" {
    python -m kyvoris_profiler compare reports\baseline-smoke.json reports\candidate-smoke.json --max-regression-percent 100 --threshold-metric average_ms --fail-on-regression
}

Invoke-Step "CLI threshold failure smoke test" {
    $baseline = @{
        schema_version = "1.0"
        metrics = @{
            average_ms = 10.0
            min_ms = 10.0
            max_ms = 10.0
            p50_ms = 10.0
            p95_ms = 10.0
            iterations = 1
            warmup_iterations = 0
            failed_iterations = 0
            average_cpu_ms = $null
            min_cpu_ms = $null
            max_cpu_ms = $null
            peak_memory_kb = $null
        }
    }
    $candidate = @{
        schema_version = "1.0"
        metrics = @{
            average_ms = 12.0
            min_ms = 12.0
            max_ms = 12.0
            p50_ms = 12.0
            p95_ms = 12.0
            iterations = 1
            warmup_iterations = 0
            failed_iterations = 0
            average_cpu_ms = $null
            min_cpu_ms = $null
            max_cpu_ms = $null
            peak_memory_kb = $null
        }
    }
    $baseline | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath reports\threshold-baseline.json -Encoding ASCII
    $candidate | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath reports\threshold-candidate.json -Encoding ASCII
    python -m kyvoris_profiler compare reports\threshold-baseline.json reports\threshold-candidate.json --max-regression-percent 5 --threshold-metric average_ms --fail-on-regression
    if ($LASTEXITCODE -ne 1) {
        throw "Expected threshold comparison to exit with code 1, got $LASTEXITCODE"
    }
    $global:LASTEXITCODE = 0
}

Invoke-Step "CLI TOML config smoke test" {
    Copy-Item -LiteralPath reports\baseline-smoke.json -Destination reports\baseline.json -Force
    Copy-Item -LiteralPath reports\candidate-smoke.json -Destination reports\candidate.json -Force
    python -m kyvoris_profiler compare --config kyvoris-profiler.toml --format markdown --output reports\config-comparison-smoke.md --max-regression-percent 100 --threshold-metric average_ms
}

Invoke-Step "CLI TOML config output validation" {
    Assert-PathExists "reports\config-comparison-smoke.md"
    Assert-FileContains "reports\config-comparison-smoke.md" "Benchmark Comparison"
    Assert-FileContains "reports\config-comparison-smoke.md" "average_ms"
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
        python examples\run_model_demo.py --iterations 3 --warmup 1 | Tee-Object -FilePath reports\huggingface-smoke.txt
    }

    Invoke-Step "Hugging Face output validation" {
        Assert-FileContains "reports\huggingface-smoke.txt" "Model: distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        Assert-FileContains "reports\huggingface-smoke.txt" "Model: cardiffnlp/twitter-roberta-base-sentiment-latest"
        Assert-FileContains "reports\huggingface-smoke.txt" "Model: lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        Assert-FileContains "reports\huggingface-smoke.txt" "Sample output:"
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
