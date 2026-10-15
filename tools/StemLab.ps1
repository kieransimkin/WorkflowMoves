$ErrorActionPreference = 'Stop'
$stemlabRuntime = Join-Path $PSScriptRoot 'stemlab-runtime-1.6.0/.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $stemlabRuntime)) {
    throw "Verified StemLab runtime missing: $stemlabRuntime. See Workflows/stemlab-rudiment-motion-selection.md."
}
& $stemlabRuntime -X utf8 -m stemlab @args
exit $LASTEXITCODE
