$ErrorActionPreference = 'Stop'
$rasterPython = Join-Path $PSScriptRoot 'rastermoves/0.3.0/.venv/Scripts/python.exe'
$rasterModels = Join-Path $PSScriptRoot 'rastermoves/models'
if (-not (Test-Path -LiteralPath $rasterPython)) { throw 'RasterMoves runtime is missing.' }
$rasterSettings = @{ RASTERMOVES_CACHE = $rasterModels; HF_HOME = (Join-Path $rasterModels 'huggingface'); TORCH_HOME = (Join-Path $rasterModels 'torch') }
$rasterPrevious = @{}
foreach ($rasterName in $rasterSettings.Keys) { $rasterPrevious[$rasterName] = [Environment]::GetEnvironmentVariable($rasterName,'Process') }
try {
    foreach ($rasterName in $rasterSettings.Keys) { [Environment]::SetEnvironmentVariable($rasterName,$rasterSettings[$rasterName],'Process') }
    & $rasterPython -X utf8 -m rastermoves @args
    $rasterExit = $LASTEXITCODE
} finally {
    foreach ($rasterName in $rasterSettings.Keys) { [Environment]::SetEnvironmentVariable($rasterName,$rasterPrevious[$rasterName],'Process') }
}
exit $rasterExit
