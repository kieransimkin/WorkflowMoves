[CmdletBinding(PositionalBinding = $false)]
param([switch]$Releases, [Parameter(ValueFromRemainingArguments = $true)][string[]]$ToolArguments)
$ErrorActionPreference = 'Stop'
$danceflowPython = Join-Path $PSScriptRoot 'DanceFlow/.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $danceflowPython)) { throw 'The released DanceFlow toolkit runtime is missing; use the official release preflight route.' }
if ($Releases) { & $danceflowPython -X utf8 -m danceflow_agents.releases @ToolArguments }
else { & $danceflowPython -X utf8 -m danceflow_agents.server @ToolArguments }
exit $LASTEXITCODE
