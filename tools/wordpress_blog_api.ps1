#Requires -Version 7.5
[CmdletBinding()]
param(
    [ValidateSet('Inventory','ReadPost','UploadMedia','CreateDraft','PublishPost','SchedulePost','UpdateScheduledPost')][string]$Mode='Inventory',
    [string]$SiteUrl='https://kieransimkin.co.uk',
    [string]$CredentialPath='Z:\My Songs\.secrets\wordpress-api\kieransimkin-epk.credential.xml',
    [string]$ManifestPath,
    [string]$ExpectedManifestSha256,
    [int]$PostId,
    [Parameter(Mandatory=$true)][string]$ReceiptOut,
    [switch]$Execute
)
Set-StrictMode -Version 2
$ErrorActionPreference='Stop'
$utf8=[Text.UTF8Encoding]::new($false,$true)
$site=$SiteUrl.TrimEnd('/')
if(([uri]$site).Scheme -ne 'https'){throw 'HTTPS is required'}
$headers=$null
$credential=$null
$plain=$null

function Hash-Bytes([byte[]]$Bytes){
    $sha=[Security.Cryptography.SHA256]::Create()
    try{return ([BitConverter]::ToString($sha.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant()}
    finally{$sha.Dispose()}
}
function Same-Ids($Left,$Right){
    return ((@($Left|Sort-Object -Unique) -join ',') -ceq (@($Right|Sort-Object -Unique) -join ','))
}
function Save-Json($Value){
    $parent=Split-Path -Parent $ReceiptOut
    if($parent){New-Item -ItemType Directory -Path $parent -Force|Out-Null}
    [IO.File]::WriteAllText($ReceiptOut,($Value|ConvertTo-Json -Depth 30),$utf8)
}
function Request([string]$Method,[string]$Route,$Value=$null,[string]$File=$null,[string]$Mime=$null){
    try{
        $args=@{Method=$Method;Uri=($site+'/wp-json/wp/v2/'+$Route);Headers=$headers;TimeoutSec=90}
        if($File){$args.InFile=$File;$args.ContentType=$Mime}
        elseif($null -ne $Value){$args.Body=$utf8.GetBytes(($Value|ConvertTo-Json -Depth 25 -Compress));$args.ContentType='application/json; charset=utf-8'}
        $reply=Invoke-RestMethod @args
        return $reply
    }catch{
        $code='unavailable'
        if($_.Exception.Response){try{$code=[int]$_.Exception.Response.StatusCode}catch{}}
        throw ('WordPress '+$Method+' request failed; HTTP '+$code+'. Outcome may be uncertain. Re-read; do not blindly repeat.')
    }
}
function Review($Post){
    $snapshot=[ordered]@{id=$Post.id;status=$Post.status;slug=$Post.slug;title=$Post.title.raw;content=$Post.content.raw;excerpt=$Post.excerpt.raw;author=$Post.author;categories=@($Post.categories);tags=@($Post.tags);featured_media=$Post.featured_media}
    return [ordered]@{post=$Post;review_sha256=(Hash-Bytes $utf8.GetBytes(($snapshot|ConvertTo-Json -Depth 20 -Compress)));content_sha256=(Hash-Bytes $utf8.GetBytes($Post.content.raw))}
}
function Preserved-Post($Post){
    $snapshot=[ordered]@{}
    foreach($key in @('id','status','date','date_gmt','slug','link','title','excerpt','author','categories','tags','featured_media','meta','template','comment_status','ping_status','sticky','format','password')){
        if($Post.PSObject.Properties.Name -contains $key){$snapshot[$key]=$Post.$key}
    }
    return ($snapshot|ConvertTo-Json -Depth 25 -Compress)
}
function Assert-ReviewedSchedule($Manifest){
    $zoneId=[string]$Manifest.timezone
    if([Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT -and $zoneId -eq 'Europe/London'){$zoneId='GMT Standard Time'}
    $zone=[TimeZoneInfo]::FindSystemTimeZoneById($zoneId)
    if([string]$Manifest.publication_time -notmatch '(Z|[+-]\d{2}:\d{2})$'){throw 'An offset-bearing publication time is required'}
    $when=[DateTimeOffset]::Parse($Manifest.publication_time,[Globalization.CultureInfo]::InvariantCulture)
    $inZone=[TimeZoneInfo]::ConvertTime($when,$zone)
    if($when.Offset -ne $inZone.Offset -or $when.ToString('yyyy-MM-ddTHH:mm:ss') -ne $inZone.ToString('yyyy-MM-ddTHH:mm:ss')){throw 'Publication timezone offset does not match its named zone'}
    if($when.UtcDateTime.ToString('yyyy-MM-ddTHH:mm:ss') -ne $Manifest.date_gmt){throw 'UTC schedule differs from the reviewed local time'}
    if($when.UtcDateTime -le [DateTime]::UtcNow.AddMinutes(5)){throw 'Publication time must remain safely in the future'}
}
function Collection([string]$Route){
    $all=@();$page=1
    do{
        $join=if($Route.Contains('?')){'&'}else{'?'}
        $batch=@(Request 'Get' ($Route+$join+'per_page=100&page='+$page))
        $all+=$batch;$page++
    }while($batch.Count -eq 100)
    return $all
}
try{
    $credential=Import-Clixml -LiteralPath $CredentialPath
    $plain=$credential.UserName+':'+$credential.GetNetworkCredential().Password
    $headers=@{Authorization=('Basic '+[Convert]::ToBase64String($utf8.GetBytes($plain)))}
    if($Mode -eq 'Inventory'){
        Save-Json ([ordered]@{posts=@(Collection 'posts?context=edit&status=publish,future,draft,pending,private');categories=@(Collection 'categories');tags=@(Collection 'tags')})
        Write-Output 'Saved authenticated blog inventory; no mutation'
        return
    }
    if($Mode -eq 'ReadPost'){
        if($PostId -lt 1){throw 'A positive PostId is required'}
        Save-Json (Review (Request 'Get' ('posts/'+$PostId+'?context=edit')))
        Write-Output ('Saved independent post readback '+$PostId)
        return
    }
    if(-not $Execute){throw 'Mutation requires the explicit Execute switch'}
    if($ExpectedManifestSha256 -notmatch '^[a-fA-F0-9]{64}$'){throw 'Exact manifest SHA-256 is required'}
    $manifestBytes=[IO.File]::ReadAllBytes($ManifestPath)
    if((Hash-Bytes $manifestBytes) -ne $ExpectedManifestSha256.ToLowerInvariant()){throw 'Manifest hash mismatch'}
    $manifest=$utf8.GetString($manifestBytes)|ConvertFrom-Json -DateKind String
    if(Test-Path -LiteralPath $ReceiptOut){throw 'A receipt already exists; re-read its identity before any retry'}
    if($Mode -eq 'UploadMedia'){
        $mimeMap=@{'.png'='image/png';'.jpg'='image/jpeg';'.jpeg'='image/jpeg';'.webp'='image/webp';'.mp4'='video/mp4';'.webm'='video/webm'}
        $extension=[IO.Path]::GetExtension($manifest.file).ToLowerInvariant()
        if(-not $mimeMap.ContainsKey($extension) -or $mimeMap[$extension] -ne $manifest.mime_type){throw 'Unsupported or mismatched media MIME type'}
        $bytes=[IO.File]::ReadAllBytes($manifest.file)
        if((Hash-Bytes $bytes) -ne $manifest.sha256){throw 'Media file hash mismatch'}
        if(-not $manifest.public_use_basis -or -not $manifest.title){throw 'Public-use basis and title are required'}
        if($manifest.mime_type.StartsWith('image/') -and -not $manifest.alt_text){throw 'Image alt text is required'}
        $slug=[string]$manifest.slug
        if($slug -notmatch '^[a-z0-9-]+$'){throw 'Explicit safe attachment slug is required'}
        if(@(Request 'Get' ('media?context=edit&slug='+$slug)).Count){throw 'Attachment slug already exists; inspect before reusing or retrying'}
        $filename=[IO.Path]::GetFileName($manifest.file)
        if($filename -notmatch '^[a-zA-Z0-9_.-]+$'){throw 'Use a safe attachment basename'}
        $headers['Content-Disposition']='attachment; filename="'+$filename+'"'
        $query='media?context=edit&slug='+$slug+'&title='+[uri]::EscapeDataString($manifest.title)+'&alt_text='+[uri]::EscapeDataString([string]$manifest.alt_text)+'&caption='+[uri]::EscapeDataString([string]$manifest.caption)
        $uploaded=Request 'Post' $query $null $manifest.file $manifest.mime_type
        $headers.Remove('Content-Disposition')
        Save-Json ([ordered]@{state='uploaded';attachment=$uploaded;local_sha256=$manifest.sha256})
        $saved=Request 'Get' ('media/'+$uploaded.id+'?context=edit')
        if($saved.slug -ne $slug -or $saved.mime_type -ne $manifest.mime_type -or $saved.alt_text -ne $manifest.alt_text -or $saved.title.raw -ne $manifest.title -or $saved.caption.raw -ne $manifest.caption){throw 'Attachment metadata mismatch; initial receipt retained; do not repeat upload'}
        $response=Invoke-WebRequest -Uri $saved.source_url -TimeoutSec 90
        $publicBytes=if($response.Content -is [byte[]]){$response.Content}else{$response.RawContentStream.ToArray()}
        if((Hash-Bytes $publicBytes) -ne $manifest.sha256){throw 'Hosted original media hash mismatch; initial receipt retained'}
        Save-Json ([ordered]@{state='verified_hosted_bytes';attachment=$saved;local_sha256=$manifest.sha256;hosted_sha256=(Hash-Bytes $publicBytes);public_use_basis=$manifest.public_use_basis})
        Write-Output ('Verified attachment '+$saved.id)
        return
    }
    if($Mode -eq 'CreateDraft'){
        if(@(Request 'Get' ('posts?context=edit&status=publish,future,draft,pending,private&slug='+[uri]::EscapeDataString($manifest.slug))).Count){throw 'Post slug already exists; inspect current posts/drafts'}
        $body=$utf8.GetString([IO.File]::ReadAllBytes($manifest.content_file))
        if((Hash-Bytes $utf8.GetBytes($body)) -ne $manifest.content_sha256){throw 'Article content hash mismatch'}
        if(-not $manifest.featured_media -or -not $body.Contains('<figure') -or -not $manifest.evidence_reviewed){throw 'Reviewed evidence, featured artwork and in-body media are required'}
        $fields=[ordered]@{status='draft';slug=$manifest.slug;title=$manifest.title;content=$body;excerpt=$manifest.excerpt;categories=@($manifest.categories);tags=@($manifest.tags);featured_media=$manifest.featured_media}
        $created=Request 'Post' 'posts' $fields
        Save-Json ([ordered]@{state='draft_request_returned';post_id=$created.id})
        $read=Review (Request 'Get' ('posts/'+$created.id+'?context=edit'))
        foreach($key in @('slug','featured_media','status')){if($read.post.$key -ne $fields.$key){throw ('Persisted '+$key+' differs')}}
        if($read.post.title.raw -ne $fields.title -or $read.post.excerpt.raw -ne $fields.excerpt -or $read.post.content.raw -cne $body -or -not (Same-Ids $read.post.categories $fields.categories) -or -not (Same-Ids $read.post.tags $fields.tags)){throw 'Draft fields differ; initial receipt retained'}
        $read['state']='verified_draft';Save-Json $read
        Write-Output ('Verified draft '+$created.id)
        return
    }
    if($Mode -eq 'UpdateScheduledPost'){
        if($manifest.content_update_authorized -isnot [bool] -or -not $manifest.content_update_authorized){throw 'Content-update authority is required'}
        if($manifest.prepublication_verified -isnot [bool] -or -not $manifest.prepublication_verified){throw 'Completed prepublication checks are required'}
        Assert-ReviewedSchedule $manifest
        $body=$utf8.GetString([IO.File]::ReadAllBytes($manifest.content_file))
        if((Hash-Bytes $utf8.GetBytes($body)) -ne $manifest.content_sha256){throw 'Article content hash mismatch'}
        $before=Review (Request 'Get' ('posts/'+$manifest.post_id+'?context=edit'))
        if($before.review_sha256 -ne $manifest.expected_review_sha256){throw 'Fresh reviewed-post snapshot changed'}
        if($before.post.status -ne 'future' -or $before.post.date_gmt -ne $manifest.date_gmt){throw 'Scheduled post status or date changed'}
        $preserved=Preserved-Post $before.post
        Save-Json ([ordered]@{state='scheduled_update_request_started';post_id=$manifest.post_id;source_sha256=$before.content_sha256;candidate_sha256=$manifest.content_sha256;preserved_date_gmt=$manifest.date_gmt})
        $updated=Request 'Post' ('posts/'+$manifest.post_id) @{content=$body}
        $read=Review (Request 'Get' ('posts/'+$manifest.post_id+'?context=edit'))
        if($updated.id -ne $manifest.post_id -or $read.content_sha256 -ne $manifest.content_sha256 -or (Preserved-Post $read.post) -cne $preserved){throw 'Scheduled content or preserved fields mismatch; initial receipt retained; do not retry'}
        $read['state']='verified_scheduled_content_update'
        $read['request_fields']=@('content')
        $read['reviewed_publication_time']=$manifest.publication_time
        $read['reviewed_timezone']=$manifest.timezone
        Save-Json $read
        Write-Output ('Verified scheduled content update '+$manifest.post_id+'; original date and all retained fields unchanged')
        return
    }
    if($Mode -in @('PublishPost','SchedulePost')){
        if($manifest.prepublication_verified -isnot [bool] -or -not $manifest.prepublication_verified){throw 'Completed prepublication checks are required'}
        $commitFields=@{status='publish'}
        if($Mode -eq 'PublishPost'){
            if($manifest.immediate_publication_authorized -isnot [bool] -or -not $manifest.immediate_publication_authorized){throw 'Exact immediate-publication authority is required'}
        }else{
            if($manifest.scheduling_authorized -isnot [bool] -or -not $manifest.scheduling_authorized){throw 'Scheduling authority is required'}
            Assert-ReviewedSchedule $manifest
            $commitFields=@{status='future';date_gmt=[string]$manifest.date_gmt}
        }
        $before=Review (Request 'Get' ('posts/'+$manifest.post_id+'?context=edit'))
        if($before.review_sha256 -ne $manifest.expected_review_sha256){throw 'Fresh reviewed-post snapshot changed'}
        if($before.post.status -ne 'draft'){throw 'Only a reviewed draft may be committed by this route'}
        $published=Request 'Post' ('posts/'+$manifest.post_id) $commitFields
        Save-Json ([ordered]@{state='commit_request_returned';post_id=$published.id})
        $read=Review (Request 'Get' ('posts/'+$published.id+'?context=edit'))
        if($read.post.status -ne $commitFields.status -or $read.content_sha256 -ne $before.content_sha256){throw 'Commit persistence mismatch; initial receipt retained'}
        if($Mode -eq 'SchedulePost' -and $read.post.date_gmt -ne $manifest.date_gmt){throw 'Persisted UTC schedule mismatch; initial receipt retained'}
        foreach($key in @('slug','featured_media','author')){if($read.post.$key -ne $before.post.$key){throw ('Publication changed '+$key)}}
        if($read.post.title.raw -ne $before.post.title.raw -or $read.post.excerpt.raw -ne $before.post.excerpt.raw -or ($read.post.categories -join ',') -ne ($before.post.categories -join ',') -or ($read.post.tags -join ',') -ne ($before.post.tags -join ',')){throw 'Publication changed reviewed fields'}
        $read['state']=if($Mode -eq 'SchedulePost'){'verified_persisted_schedule'}else{'verified_persisted_publication'}
        if($Mode -eq 'SchedulePost'){$read['reviewed_publication_time']=$manifest.publication_time;$read['reviewed_timezone']=$manifest.timezone}
        Save-Json $read
        Write-Output ('Verified persisted '+$commitFields.status+' post '+$published.id+'; public checks follow actual publication')
    }
}finally{$headers=$null;$plain=$null;$credential=$null}
