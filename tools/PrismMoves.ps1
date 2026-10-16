$ErrorActionPreference = 'Stop'
$prismPython = Join-Path $PSScriptRoot 'PrismMoves/.venv/Scripts/python.exe'
$prismModels = Join-Path (Split-Path $PSScriptRoot -Parent) 'Repositories/PrismMoves/models'
if (-not (Test-Path -LiteralPath $prismPython)) { throw 'PrismMoves runtime missing; see Workflows/prismmoves-visual-analysis.md.' }
$prismNames = @('PIXELCUE_MODELS_DIR','HF_HOME','TORCH_HOME','OMP_NUM_THREADS','MKL_NUM_THREADS')
$prismPrevious = @{}
foreach ($prismName in $prismNames) { $prismPrevious[$prismName] = [Environment]::GetEnvironmentVariable($prismName,'Process') }
try {
    $env:PIXELCUE_MODELS_DIR = $prismModels
    $env:HF_HOME = Join-Path $prismModels '.cache/huggingface'
    $env:TORCH_HOME = Join-Path $prismModels '.cache/torch'
    if (-not $env:OMP_NUM_THREADS) { $env:OMP_NUM_THREADS = '4' }
    if (-not $env:MKL_NUM_THREADS) { $env:MKL_NUM_THREADS = '4' }
    & $prismPython -X utf8 -m prismmoves --models-dir $prismModels @args
    $prismExit = $LASTEXITCODE
} finally {
    foreach ($prismName in $prismNames) { [Environment]::SetEnvironmentVariable($prismName,$prismPrevious[$prismName],'Process') }
}
exit $prismExit
