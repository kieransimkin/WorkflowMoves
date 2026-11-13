$ErrorActionPreference = 'Stop'
$stemlabProject = Join-Path $PSScriptRoot 'stemlab'
$stemlabRuntime = Join-Path $stemlabProject '.venv-beats-311/Scripts/python.exe'
$stemlabModels = Join-Path $stemlabProject 'models'
$stemlabVersion = '1.14.1'
$stemlabSource = Join-Path $stemlabModels "runtimes/stemlab-$stemlabVersion"
if (-not (Test-Path -LiteralPath $stemlabRuntime -PathType Leaf) -or
    -not (Test-Path -LiteralPath (Join-Path $stemlabSource 'stemlab/__init__.py') -PathType Leaf)) {
    throw "Verified StemLab $stemlabVersion runtime missing. See Workflows/lyric-timing-review.md."
}
$env:PYTHONPATH = $stemlabSource
$env:STEMLAB_CACHE = Join-Path $stemlabModels 'stemlab-cache'
$env:STEMLAB_BS_ROFORMER_MODELS = Join-Path $stemlabModels 'bs-roformer'
$env:HF_HOME = Join-Path $stemlabModels 'huggingface'
$env:TORCH_HOME = Join-Path $stemlabModels 'torch'
$env:XDG_CACHE_HOME = Join-Path $stemlabModels 'cache'
& $stemlabRuntime -X utf8 -m stemlab @args
exit $LASTEXITCODE
