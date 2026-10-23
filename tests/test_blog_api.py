"""Run the real PowerShell entrypoint with synthetic HTTP/credential boundaries."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'tools/wordpress_blog_api.ps1'
PWSH = shutil.which('pwsh')


@unittest.skipUnless(PWSH, 'PowerShell is unavailable on this runner')
class BlogApiTests(unittest.TestCase):
    def run_case(self, case):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            harness = root / 'case.ps1'
            script = str(SCRIPT).replace("'", "''")
            path = str(root).replace("'", "''")
            harness.write_text("""$ErrorActionPreference='Stop'
$global:MockWrites=0
$global:MockReads=0
$global:LastFields=$null
$global:Case='CASE'
$root='ROOT'
$tool='TOOL'
$global:MockPost=[pscustomobject]@{id=4;status='draft';date_gmt='';slug='synthetic-article';title=[pscustomobject]@{raw='Synthetic title'};content=[pscustomobject]@{raw='<p>Original</p><figure>Test</figure>'};excerpt=[pscustomobject]@{raw='Synthetic excerpt'};author=1;categories=@(21);tags=@();featured_media=9;link='https://example.invalid/synthetic-article/'}
function Import-Clixml { param($LiteralPath) return [pscredential]::new('synthetic-user',(ConvertTo-SecureString 'synthetic-fixture-only' -AsPlainText -Force)) }
function Invoke-RestMethod { param($Method,$Uri,$Headers,$TimeoutSec,$Body,$ContentType,$InFile)
 if($Method -eq 'Post'){
  $global:MockWrites++
  $global:LastFields=[Text.Encoding]::UTF8.GetString($Body)|ConvertFrom-Json -DateKind String
  if($global:Case -like 'update-*' -and $global:LastFields.PSObject.Properties.Name -contains 'content'){
   if(@($global:LastFields.PSObject.Properties).Count -ne 1){throw 'Scheduled edit sent more than content'}
   $global:MockPost.content.raw=$global:LastFields.content
   if($global:Case -eq 'update-server-date'){$global:MockPost.date_gmt='2000-01-01T00:00:00'}
   return $global:MockPost
  }
  if($global:LastFields.status -eq 'draft'){$global:MockPost.tags=@(9,5);return $global:MockPost}
  if($global:LastFields.status -notin @('publish','future')){throw 'Unexpected synthetic mutation'}
  $global:MockPost.status=$global:LastFields.status
  if($global:LastFields.status -eq 'future'){$global:MockPost.date_gmt=$global:LastFields.date_gmt}
  return $global:MockPost
 }
 $global:MockReads++
 if($Uri -match '/posts/4\\?'){ return $global:MockPost }
 if($Uri -match '/posts\\?' -and $global:Case -eq 'duplicate'){ return $global:MockPost }
 if($Uri -match '/posts\\?' -and $global:Case -eq 'inventory'){
  $items=if($Uri -match 'page=2$'){@([pscustomobject]@{id=101})}else{@(1..100|ForEach-Object{[pscustomobject]@{id=$_}})}
  Write-Output -NoEnumerate $items
  return
 }
 Write-Output -NoEnumerate @()
}
function Manifest($value,$name){$p=Join-Path $root $name;[IO.File]::WriteAllText($p,($value|ConvertTo-Json -Depth 20),[Text.UTF8Encoding]::new($false));return $p}
if($global:Case -eq 'inventory'){
 $out=Join-Path $root 'inventory.json'
 & $tool -Mode Inventory -SiteUrl 'https://example.invalid' -ReceiptOut $out
 $saved=Get-Content -LiteralPath $out -Raw|ConvertFrom-Json
 if($saved.posts.Count -ne 101 -or $saved.posts[0].id -ne 1 -or $saved.posts[100].id -ne 101){throw 'Collection was truncated or nested'}
 if($saved.categories.Count -ne 0 -or $saved.tags.Count -ne 0){throw 'Empty arrays changed shape'}
}elseif($global:Case -eq 'draft'){
 $body=Join-Path $root 'body.html'
 [IO.File]::WriteAllText($body,$global:MockPost.content.raw,[Text.UTF8Encoding]::new($false))
 $manifest=Manifest @{slug='synthetic-article';title='Synthetic title';content_file=$body;content_sha256=(Get-FileHash $body).Hash.ToLowerInvariant();excerpt='Synthetic excerpt';categories=@(21);tags=@(5,9);featured_media=9;evidence_reviewed=$true} 'manifest.json'
 & $tool -Mode CreateDraft -SiteUrl 'https://example.invalid' -ManifestPath $manifest -ExpectedManifestSha256 (Get-FileHash $manifest).Hash -ReceiptOut (Join-Path $root 'draft.json') -Execute
 if($global:MockWrites -ne 1){throw 'Draft creation was repeated'}
}elseif($global:Case -like 'update-*'){
 $zoneId=if([Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT){'GMT Standard Time'}else{'Europe/London'}
 $when=[TimeZoneInfo]::ConvertTime([DateTimeOffset]::UtcNow.AddDays(30),[TimeZoneInfo]::FindSystemTimeZoneById($zoneId))
 $global:MockPost.status='future'
 $global:MockPost.date_gmt=$when.UtcDateTime.ToString('yyyy-MM-ddTHH:mm:ss')
 $read=Join-Path $root 'read.json'
 & $tool -Mode ReadPost -PostId 4 -SiteUrl 'https://example.invalid' -ReceiptOut $read
 $review=Get-Content -LiteralPath $read -Raw|ConvertFrom-Json
 $body=Join-Path $root 'body.html'
 [IO.File]::WriteAllText($body,'<p>New native findings</p><figure>Actual demo</figure>',[Text.UTF8Encoding]::new($false))
 $expected=if($global:Case -eq 'update-stale'){'0'*64}else{$review.review_sha256}
 $authority=if($global:Case -eq 'update-authority'){'false'}else{$true}
 $bodyHash=if($global:Case -eq 'update-hash'){'0'*64}else{(Get-FileHash $body).Hash.ToLowerInvariant()}
 $manifest=Manifest @{post_id=4;expected_review_sha256=$expected;content_update_authorized=$authority;prepublication_verified=$true;content_file=$body;content_sha256=$bodyHash;publication_time=$when.ToString('yyyy-MM-ddTHH:mm:sszzz');date_gmt=$global:MockPost.date_gmt;timezone='Europe/London'} 'manifest.json'
 if($global:Case -eq 'update-date'){$global:MockPost.date_gmt='2000-01-01T00:00:00'}
 if($global:Case -eq 'update-status'){$global:MockPost.status='draft'}
 $caught=$false
 $receipt=Join-Path $root 'update.json'
 try{ & $tool -Mode UpdateScheduledPost -SiteUrl 'https://example.invalid' -ManifestPath $manifest -ExpectedManifestSha256 (Get-FileHash $manifest).Hash -ReceiptOut $receipt -Execute }catch{$caught=$true;if($global:Case -eq 'update-success'){throw}}
 if($global:Case -eq 'update-success'){
  $saved=Get-Content -LiteralPath $receipt -Raw|ConvertFrom-Json -DateKind String
  if($caught -or $global:MockWrites -ne 1 -or $saved.state -ne 'verified_scheduled_content_update' -or $saved.post.status -ne 'future' -or $saved.post.date_gmt -ne $when.UtcDateTime.ToString('yyyy-MM-ddTHH:mm:ss')){throw 'Scheduled content/date verification failed'}
 }elseif($global:Case -eq 'update-server-date'){
  $saved=Get-Content -LiteralPath $receipt -Raw|ConvertFrom-Json
  if(-not $caught -or $global:MockWrites -ne 1 -or $saved.state -ne 'scheduled_update_request_started'){throw 'Uncertain server mutation was not retained as a hold'}
 }elseif(-not $caught -or $global:MockWrites -ne 0){throw 'Unsafe scheduled edit mutated the post'}
}elseif($global:Case -in @('schedule','offset','past','utc','string-authority')){
 $read=Join-Path $root 'read.json'
 & $tool -Mode ReadPost -PostId 4 -SiteUrl 'https://example.invalid' -ReceiptOut $read
 $review=Get-Content -LiteralPath $read -Raw|ConvertFrom-Json
 $zoneId=if([Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT){'GMT Standard Time'}else{'Europe/London'}
 $zone=[TimeZoneInfo]::FindSystemTimeZoneById($zoneId)
 $when=[TimeZoneInfo]::ConvertTime([DateTimeOffset]::UtcNow.AddDays(30),$zone)
 if($global:Case -eq 'past'){$when=$when.AddDays(-60)}
 $publication=$when.ToString('yyyy-MM-ddTHH:mm:sszzz')
 if($global:Case -eq 'offset'){$publication=$when.ToString('yyyy-MM-ddTHH:mm:ss')+'+08:00'}
 $utc=$when.UtcDateTime.ToString('yyyy-MM-ddTHH:mm:ss')
 if($global:Case -eq 'utc'){$utc=$when.UtcDateTime.AddHours(1).ToString('yyyy-MM-ddTHH:mm:ss')}
 $authority=if($global:Case -eq 'string-authority'){'false'}else{$true}
 $manifest=Manifest @{post_id=4;expected_review_sha256=$review.review_sha256;scheduling_authorized=$authority;prepublication_verified=$true;publication_time=$publication;date_gmt=$utc;timezone='Europe/London'} 'manifest.json'
 $caught=$false
 try{ & $tool -Mode SchedulePost -SiteUrl 'https://example.invalid' -ManifestPath $manifest -ExpectedManifestSha256 (Get-FileHash $manifest).Hash -ReceiptOut (Join-Path $root 'schedule.json') -Execute }catch{$caught=$true;if($global:Case -eq 'schedule'){throw}}
 if($global:Case -eq 'schedule'){
  $saved=Get-Content -LiteralPath (Join-Path $root 'schedule.json') -Raw|ConvertFrom-Json -DateKind String
  if($caught -or $global:MockWrites -ne 1 -or @($global:LastFields.PSObject.Properties).Count -ne 2 -or $saved.state -ne 'verified_persisted_schedule' -or $saved.post.date_gmt -ne $utc){throw 'Schedule was not one verified future/date mutation'}
 }elseif(-not $caught -or $global:MockWrites -ne 0){throw 'Invalid scheduling authority/time mutated the post'}
}elseif($global:Case -in @('publish','stale')){
 $read=Join-Path $root 'read.json'
 & $tool -Mode ReadPost -PostId 4 -SiteUrl 'https://example.invalid' -ReceiptOut $read
 $review=Get-Content -LiteralPath $read -Raw|ConvertFrom-Json
 $expected=if($global:Case -eq 'stale'){'0'*64}else{$review.review_sha256}
 $manifest=Manifest @{post_id=4;expected_review_sha256=$expected;immediate_publication_authorized=$true;prepublication_verified=$true} 'manifest.json'
 $caught=$false
 try{ & $tool -Mode PublishPost -SiteUrl 'https://example.invalid' -ManifestPath $manifest -ExpectedManifestSha256 (Get-FileHash $manifest).Hash -ReceiptOut (Join-Path $root 'publish.json') -Execute }catch{$caught=$true;if($global:Case -ne 'stale' -or $_.Exception.Message -notmatch 'snapshot changed'){throw}}
 if($global:Case -eq 'stale'){if(-not $caught -or $global:MockWrites -ne 0){throw 'Stale snapshot mutated'}}
 else{if($caught -or $global:MockWrites -ne 1 -or @($global:LastFields.PSObject.Properties).Count -ne 1){throw 'Publication was not a single status-only mutation'}}
}else{
 $value=@{slug='synthetic-article';file=(Join-Path $root 'unsupported.pdf');mime_type='application/pdf'}
 $manifest=Manifest $value 'manifest.json'
 $mode=if($global:Case -eq 'duplicate'){'CreateDraft'}else{'UploadMedia'}
 $hash=if($global:Case -eq 'hash'){'0'*64}else{(Get-FileHash $manifest).Hash}
 $arguments=@{Mode=$mode;SiteUrl='https://example.invalid';ManifestPath=$manifest;ExpectedManifestSha256=$hash;ReceiptOut=(Join-Path $root 'result.json')}
 if($global:Case -ne 'execute'){$arguments.Execute=$true}
 $caught=$false
 try{ & $tool @arguments }catch{$caught=$true}
 if(-not $caught -or $global:MockWrites -ne 0){throw 'Guard permitted a mutation'}
 if($global:Case -ne 'duplicate' -and $global:MockReads -ne 0){throw 'Local guard unexpectedly used HTTP'}
}
Write-Output ('PASS '+$global:Case)
""".replace('CASE', case).replace('ROOT', path).replace('TOOL', script), encoding='utf-8')
            completed = subprocess.run([PWSH, '-NoProfile', '-File', str(harness)], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertIn('PASS ' + case, completed.stdout)

    def test_inventory_flattens_native_rest_arrays_and_pages(self): self.run_case('inventory')
    def test_draft_accepts_server_taxonomy_order_with_exact_membership(self): self.run_case('draft')
    def test_publish_is_one_status_only_write_after_review(self): self.run_case('publish')
    def test_stale_review_never_publishes(self): self.run_case('stale')
    def test_changed_manifest_never_uses_http(self): self.run_case('hash')
    def test_explicit_execute_is_required(self): self.run_case('execute')
    def test_unsupported_media_never_uploads(self): self.run_case('mime')
    def test_duplicate_slug_never_creates_post(self): self.run_case('duplicate')
    def test_schedule_retains_content_and_commits_exact_utc_once(self): self.run_case('schedule')
    def test_wrong_named_zone_offset_never_schedules(self): self.run_case('offset')
    def test_past_time_never_schedules(self): self.run_case('past')
    def test_different_utc_time_never_schedules(self): self.run_case('utc')
    def test_string_false_is_not_scheduling_authority(self): self.run_case('string-authority')
    def test_scheduled_update_changes_content_only_and_keeps_date(self): self.run_case('update-success')
    def test_scheduled_update_rejects_stale_body(self): self.run_case('update-stale')
    def test_scheduled_update_rejects_changed_date(self): self.run_case('update-date')
    def test_scheduled_update_rejects_changed_status(self): self.run_case('update-status')
    def test_scheduled_update_requires_boolean_authority(self): self.run_case('update-authority')
    def test_scheduled_update_rejects_changed_disk_bytes(self): self.run_case('update-hash')
    def test_scheduled_update_retains_uncertain_mutation_without_retry(self): self.run_case('update-server-date')
