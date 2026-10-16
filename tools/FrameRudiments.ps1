$ErrorActionPreference = 'Stop'
$frameRuntime = Join-Path $PSScriptRoot 'FrameRudiments/.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $frameRuntime)) { throw 'FrameRudiments runtime missing; see Tools/FrameRudiments/README.md.' }
$frameFFmpeg = Join-Path $PSScriptRoot 'ffmpeg/ffmpeg-9.0.1-full_build/bin/ffmpeg.exe'
if (-not $env:FRAMERUDIMENTS_FFMPEG -and (Test-Path -LiteralPath $frameFFmpeg)) {
    $env:FRAMERUDIMENTS_FFMPEG = $frameFFmpeg
}
$frameEffectConfig = Join-Path $PSScriptRoot 'FrameRudiments/local/effects-runtime.json'
if (Test-Path -LiteralPath $frameEffectConfig) {
    $frameEffectEnvironment = (Get-Content -Raw -LiteralPath $frameEffectConfig | ConvertFrom-Json).environment
    $frameAllowedVariables = @('FRAMERUDIMENTS_BUTTERCHURN_RUNTIME', 'FRAMERUDIMENTS_BROWSER', 'FRAMERUDIMENTS_NODE', 'FRAMERUDIMENTS_PROJECTM_LIBRARY', 'FRAMERUDIMENTS_PROJECTM_DLL_DIRS')
    foreach ($frameVariable in $frameEffectEnvironment.PSObject.Properties) {
        if ($frameVariable.Name -notin $frameAllowedVariables -or $frameVariable.Value -isnot [string]) { throw 'Invalid FrameRudiments effects runtime configuration.' }
        if (-not [Environment]::GetEnvironmentVariable($frameVariable.Name, 'Process')) {
            [Environment]::SetEnvironmentVariable($frameVariable.Name, $frameVariable.Value, 'Process')
        }
    }
}
& $frameRuntime -X utf8 -m framerudiments @args
exit $LASTEXITCODE
