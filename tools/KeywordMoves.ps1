$ErrorActionPreference = 'Stop'
$keywordPython = Join-Path $PSScriptRoot 'keywordmoves/.venv-313/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $keywordPython)) { throw 'KeywordMoves Python 3.13 runtime is missing.' }
& $keywordPython -X utf8 -m keywordmoves @args
exit $LASTEXITCODE
