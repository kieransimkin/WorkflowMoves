# Direct social scheduling

Own the calendar locally and use authenticated native platforms for upload and future scheduling. Keep exact approved media bytes, platform-specific copy and covers together. A local plan is preparation; a native queue is persistence evidence; later public playback is a separate result.

![Direct publication evidence flow](media/direct-social-scheduling.svg)

Generated contract illustration, not an upload receipt. Actual account screenshots and private media belong in the campaign evidence directory. A video of this static preflight adds no useful explanation; capture actual platform views for completed actions.

## Local preflight

Use Python 3.11+ with `requirements-workflows.txt` in a project-local environment. Windows needs the IANA `tzdata` package; Linux normally provides timezone data through the OS.

```powershell
python Tools/social_schedule_plan.py campaign/social-plan.json --output campaign/preflight.json --html campaign/calendar.html
```

The schema is `workflowmoves.social-plan.v1`, with an `items` list. Each item has `id`, `destination`, `account`, `state`, `local_time` without an offset, IANA `timezone`, explicit zero-offset `utc`, `files`, `settings`, `approval` and `queue_check`. Files map roles (`video`, `caption`, optional `cover` and `captions_srt`) to `path` and `sha256`; paths resolve beside the plan. Use `payload_hash(row)` to record the exact payload covered by already granted approval, with its local evidence path. Hashing never creates authorisation.

`queue_check` contains `observed_at` and local `evidence`. Reinspect the live queue at action time. Optional `replaces` entries need `state: cancelled_verified` and cancellation evidence. Optional `window` records the observed `last_selectable_date` and dated `next_check`; one observation is not a permanent platform limit. Reopen the same private draft when its desired date becomes selectable.

States: `prepared`, `uploading`, `mutation_pending`, `private_draft`, `scheduled`, `published`, `verified_live`, `terminal_hold`. Scheduled/public states need `native_receipt` with `id_or_url`, matching `utc` and local evidence. A terminal hold needs a precise `reason`.

The tool checks original file hashes, named-zone/UTC agreement including daylight-saving gaps and repeated hours, duplicate assets, account/slot collisions and retained receipts. It writes an escaped offline HTML calendar and source-plan hash. It never contacts a platform, changes an input state, approves copy or uploads anything. A valid report can contain holds: read each item's `action`, not just `valid`.

## Commit and reconcile

1. Inspect account-specific timing evidence and nearby native queue entries. Honour explicit artist choices and existing approval for unchanged payloads.
2. Before replacing a scheduler, identify exact jobs, obtain any needed cancellation authority, verify cancellation, then inspect the native queue. Preserve unrelated posts.
3. Begin applicable YouTube and TikTok routes. Upload unchanged approved video, captions and dedicated covers through supported controls. Read full duration, disclosure, visibility, slot and timezone before one commit.
4. Keep upload/save pending until acknowledged and independently verified. A delayed acknowledgement is not failure. Observe the existing attempt before any retry; preserve active forms and uploads.
5. Retain independent Scheduled/Planner and cover evidence. Distinguish a broker job, reminder, private draft and native schedule. Unsupported fields remain precise holds.
6. Closed windows retain one draft ID and a dated continuation. After publication verify playback and reconcile eligible media into the EPK. Scheduled/private material stays controlled.

## Recover and prove native persistence

An interrupted browser or closed transport does not establish whether a form was saved, scheduled, published or abandoned. Start recovery from the exact local asset/hash and approval packet, then inspect the current native queue before opening a new composer. If the expected item exists, verify its copy, media duration, cover, audience, disclosure, slot and timezone. If it does not, retain the prior attempt as unresolved until the platform state and upload processing are understood; do not blind-resubmit.

Use platform-supported input events. A script assigning an input's DOM `value`, an automation tool returning success or a field appearing filled can still leave the framework's native state blank. After text entry, blur or advance through the platform's normal validation path, then reread the platform-visible value. Where clipboard paste is the supported reliable route, use it only for the exact approved text and verify the native queue after the commit.

Do not navigate away while media is still processing. Require the platform's own accepted/complete state for video, cover, caption attachment and disclosure fields before one authorised save or schedule action. Treat `In progress`, delayed acknowledgement and disabled controls as the existing attempt still resolving. Wait and reinspect; never create a replacement merely because the UI is slow.

After the platform acknowledges the mutation, reopen Scheduled/Planner in a fresh view and verify the exact caption, native date/time/timezone, audience or visibility, media duration and platform-specific settings. Capture private evidence at useful transition points. Then close every completed job-created tab and released borrowed tab through supported controls and confirm with a fresh inventory; preserve any active upload or unsaved form with a named owner and next action.

## Lessons and sources

Metricool's [calendar guide](https://help.metricool.com/how-to-manage-your-calendar-in-metricool-xhlbw) describes a shared calendar, network filters, separate publication/approval statuses and warnings for partially delivered settings. Its [review workflow](https://help.metricool.com/how-to-send-posts-for-review-with-metricools-approval-system-yvdr0) resets review after edits. Useful principles are one calendar, separate evidence states and approval bound to exact content. This workflow applies those principles locally without a paid service dependency or proprietary code. Sources reviewed 23 October 2026.

Observed native workflows exposed rolling date windows, delayed save acknowledgement and broker jobs absent from native queues. Those findings motivate continuation and independent-receipt fields; they do not promise a universal platform window.

Observed recovery also showed that a visually populated framework field could persist as blank until entered through a native event path, and that leaving before upload processing completed could invalidate the attempt. These are bounded implementation lessons, not claims about every platform or browser version.

## Facebook Page video via Graph API

Use the [Page Video API](https://developers.facebook.com/docs/graph-api/reference/page/videos/) for new Facebook video uploads and scheduling. Use the Page's resumable start, transfer and finish phases on `graph.facebook.com`. Apply this route to full-length visualisers and short videos. Use the browser queue for readback when available.

Resolve the existing authorised Meta app and its supported credential route before deciding whether Page Video API access is available. If the shell has no Page credential, check the approved credential store or select the existing app in Meta Graph API Explorer. Verify the Page identity and the `CREATE_CONTENT` task with the app’s existing permissions. Keep raw tokens in memory and use a scoped, encrypted handoff when a local API client needs them. If verification fails, record the exact failed check and reconcile any existing upload before changing routes.

1. Verify the approved Page, exact video and cover hashes, copy, disclosures and local/UTC slot in the social plan. Check the Page access token with `GET /me?fields=id,name`, confirm the owner's content-creation access and inspect the current Page videos and scheduled posts for duplicates and slot conflicts. Keep access tokens out of commands, logs, screenshots and campaign records.
2. With the Page token, start `POST /{page-id}/videos` with `upload_phase=start`, the exact `file_size` and `published=false`. Retain the returned video ID, upload session ID and byte offsets privately. Use the app's supported Graph API version consistently for the attempt.
3. On the same edge, submit `upload_phase=transfer`, the session ID, `start_offset` and a multipart `video_file_chunk` containing the server-requested byte range. Verify contiguous acknowledgement through the original file size. If a transfer is interrupted, reconcile the existing session and server-confirmed offset before continuing.
4. Finish the same session with `upload_phase=finish`, `published=false` and `unpublished_content_type=DRAFT`. Submit the exact approved title, description, cover and supported disclosure settings. Verify the same video reads back as unpublished and ready, with the expected duration and copy, before scheduling. If the preferred thumbnail is still automatic, send the approved image to `POST /{video-id}/thumbnails` as `source` with `is_preferred=true` and verify the preferred thumbnail ID. Check any required captions and disclosures separately.
5. Recheck the Page queue, then update the existing video once with `POST /{video-id}`, `published=false` and the approved UTC epoch in `scheduled_publish_time`. Independently read the Video node and the Page's `/{page-id}/scheduled_posts` edge. Match the post and video IDs, exact copy, future timestamp and unpublished state. Save the native schedule receipt and check public playback after the slot.

An upload acknowledgement proves byte transfer. A ready unpublished video and a persisted schedule require their own readbacks. Keep the original master resolution, frame rate and duration. If the API route is unavailable, hold the existing item and record the precise blocker before changing routes. The full-length 4K60 case reached draft readiness and scheduling through Page-scoped chunks after app-level file-handle finalization failed and a single multipart upload returned HTTP 413. [Meta Video API overview](https://developers.facebook.com/documentation/video-api/overview) · [Meta Video API reference](https://developers.facebook.com/docs/graph-api/reference/video/)

## Potential problems

- Missing timezone data: install the declared dependency; never guess offsets. Explicit UTC disambiguates a repeated local hour.
- Changed caption, cover or slot: compare with actual approval scope. Refresh the stale payload hash only after obtaining any genuinely needed revised approval.
- A local ready result cannot detect later queue changes: inspect the live queue immediately before mutation.
- An empty queue during a pending save does not justify another upload or save.
- A private draft at release time is an unscheduled hold, not publication. Preserve its exact next action and existing notification policy.
- A field that looks populated but rereads blank is not ready to commit. Re-enter through the platform's supported event path and verify again.
- An interrupted or vanished tab is not a failure receipt. Inspect the native queue and existing attempt before opening a replacement composer.
- Do not leave an upload page until native processing and required platform checks are complete.
- Close completed job tabs and verify a fresh inventory; an empty tool inventory proves only what the selected connection can see.
