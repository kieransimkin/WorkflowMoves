function Assert-EpkYouTubeFlow {
    param(
        [string]$EditorHtml,
        [int]$PageId,
        [string]$SourceSha,
        [string]$CandidateSha,
        [string]$EvidencePath
    )

    $marker = '(?is)<[a-z][\w:-]*\b[^<>]*\bdata-epk-cover-player\s*=\s*["'']([A-Za-z0-9_-]{11})["'']'
    $videoIds = @([regex]::Matches($EditorHtml, $marker) | ForEach-Object { $_.Groups[1].Value })
    if (-not $EvidencePath) {
        if ($videoIds.Count) {
            throw 'Public EPKs with YouTube covers require YouTubeFlowEvidencePath for the exact candidate.'
        }
        return
    }

    $validator = Join-Path $PSScriptRoot 'audit_epk_youtube_flow.py'
    $arguments = @((Resolve-Path -LiteralPath $EvidencePath).Path,
        '--page-id', $PageId, '--source-sha256', $SourceSha, '--candidate-sha256', $CandidateSha)
    foreach ($videoId in $videoIds) {
        $arguments += "--expected-video-id=$videoId"
    }
    $report = & python -B $validator @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "YouTube reveal and return evidence failed. $($report -join ' ')"
    }
}
