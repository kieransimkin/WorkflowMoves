$ErrorActionPreference = 'Stop'
$frameRuntime = Join-Path $PSScriptRoot 'FrameRudiments/.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $frameRuntime)) { throw 'FrameRudiments runtime missing; see Tools/FrameRudiments/README.md.' }
$frameFFmpeg = Join-Path $PSScriptRoot 'ffmpeg/ffmpeg-9.0.1-full_build/bin/ffmpeg.exe'
if (-not $env:FRAMERUDIMENTS_FFMPEG -and (Test-Path -LiteralPath $frameFFmpeg)) {
    $env:FRAMERUDIMENTS_FFMPEG = $frameFFmpeg
}
& $frameRuntime -X utf8 -m framerudiments @args
exit $LASTEXITCODE
