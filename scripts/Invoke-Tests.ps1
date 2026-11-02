[CmdletBinding()]
param(
    [string] $Python = "python",
    [string] $Pattern = "test*.py"
)

$ErrorActionPreference = "Stop"
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$parent = if ([Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT -and $env:LOCALAPPDATA) {
    Join-Path $env:LOCALAPPDATA "WorkflowMoves\test-tmp"
} else {
    Join-Path $repoRoot ".test-tmp"
}
$parent = [IO.Path]::GetFullPath($parent)
$runRoot = [IO.Path]::GetFullPath((Join-Path $parent ("python-{0}-{1}" -f (Get-Date -Format "yyyyMMdd-HHmmss"), [guid]::NewGuid().ToString("N"))))
if (-not $runRoot.StartsWith($parent + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe test temp path: $runRoot"
}

New-Item -ItemType Directory -Force -Path $parent | Out-Null
$probe = Join-Path $parent ("probe-" + [guid]::NewGuid().ToString("N"))
$renamed = "$probe-renamed"
try {
    New-Item -ItemType Directory -Path $probe | Out-Null
    $marker = Join-Path $probe "probe.txt"
    [IO.File]::WriteAllText($marker, "workflowmoves-temp-probe")
    if ([IO.File]::ReadAllText($marker) -ne "workflowmoves-temp-probe") {
        throw "Test temp readback failed: $parent"
    }
    Move-Item -LiteralPath $probe -Destination $renamed
} finally {
    Remove-Item -LiteralPath $renamed -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $probe -Recurse -Force -ErrorAction SilentlyContinue
}

$saved = @{ TEMP = $env:TEMP; TMP = $env:TMP; TMPDIR = $env:TMPDIR }
try {
    New-Item -ItemType Directory -Path $runRoot | Out-Null
    $env:TEMP = $runRoot
    $env:TMP = $runRoot
    $env:TMPDIR = $runRoot
    & $Python -m unittest discover -s tests -p $Pattern -v
    if ($LASTEXITCODE -ne 0) {
        throw "WorkflowMoves tests failed with exit code $LASTEXITCODE"
    }
} finally {
    $env:TEMP = $saved.TEMP
    $env:TMP = $saved.TMP
    $env:TMPDIR = $saved.TMPDIR
    Remove-Item -LiteralPath $runRoot -Recurse -Force -ErrorAction SilentlyContinue
}
