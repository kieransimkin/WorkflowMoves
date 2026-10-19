[CmdletBinding(PositionalBinding = $false)]
param([switch]$Server, [Parameter(ValueFromRemainingArguments = $true)][string[]]$ToolArguments)
$ErrorActionPreference = 'Stop'
# PixelCue and PrismMoves use one verified compatible Python environment.
# Their project-local model roots remain independent.
$pixelPython = Join-Path $PSScriptRoot 'PrismMoves/.venv/Scripts/python.exe'
$pixelModels = Join-Path $PSScriptRoot 'PixelCue/models'
if (-not (Test-Path -LiteralPath $pixelPython)) { throw 'The verified PixelCue/PrismMoves runtime is missing.' }
$pixelSettings = @{ PIXELCUE_MODELS_DIR = $pixelModels; HF_HOME = (Join-Path $pixelModels '.cache/huggingface'); TORCH_HOME = (Join-Path $pixelModels '.cache/torch') }
$pixelPrevious = @{}
foreach ($pixelName in $pixelSettings.Keys) { $pixelPrevious[$pixelName] = [Environment]::GetEnvironmentVariable($pixelName,'Process') }
try {
    foreach ($pixelName in $pixelSettings.Keys) { [Environment]::SetEnvironmentVariable($pixelName,$pixelSettings[$pixelName],'Process') }
    if ($Server) { & $pixelPython -X utf8 -m pixelcue.server @ToolArguments }
    else { & $pixelPython -X utf8 -m pixelcue.main @ToolArguments }
    $pixelExit = $LASTEXITCODE
} finally {
    foreach ($pixelName in $pixelSettings.Keys) { [Environment]::SetEnvironmentVariable($pixelName,$pixelPrevious[$pixelName],'Process') }
}
exit $pixelExit
