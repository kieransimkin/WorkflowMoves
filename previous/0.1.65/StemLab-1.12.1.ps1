$ErrorActionPreference = 'Stop'
$stemlabProject = Join-Path $PSScriptRoot 'stemlab'
$stemlabRuntime = Join-Path $stemlabProject '.venv-beats-311/Scripts/python.exe'
$stemlabSource = Join-Path $stemlabProject 'models/runtimes/stemlab-1.12.1'
if (-not (Test-Path -LiteralPath (Join-Path $stemlabSource 'stemlab/__init__.py'))) { throw 'Verified StemLab 1.12.1 package is missing; complete release preflight/provisioning rather than falling back to historical source.' }
$stemlabModels = Join-Path $stemlabProject 'models'
$env:PYTHONPATH = $stemlabSource
$env:STEMLAB_CACHE = Join-Path $stemlabModels 'stemlab-cache'
$env:STEMLAB_BS_ROFORMER_MODELS = Join-Path $stemlabModels 'bs-roformer'
$env:HF_HOME = Join-Path $stemlabModels 'huggingface'
$env:TORCH_HOME = Join-Path $stemlabModels 'torch'
$env:XDG_CACHE_HOME = Join-Path $stemlabModels 'cache'
if (-not (Test-Path -LiteralPath $stemlabRuntime)) {
    throw "StemLab main-tracking CUDA runtime missing: $stemlabRuntime. See Workflows/stemlab-rudiment-motion-selection.md."
}
& $stemlabRuntime -X utf8 -m stemlab @args
exit $LASTEXITCODE
