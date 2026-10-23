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

## Lessons and sources

Metricool's [calendar guide](https://help.metricool.com/how-to-manage-your-calendar-in-metricool-xhlbw) describes a shared calendar, network filters, separate publication/approval statuses and warnings for partially delivered settings. Its [review workflow](https://help.metricool.com/how-to-send-posts-for-review-with-metricools-approval-system-yvdr0) resets review after edits. Useful principles are one calendar, separate evidence states and approval bound to exact content. This workflow applies those principles locally without a paid service dependency or proprietary code. Sources reviewed 23 October 2026.

Observed native workflows exposed rolling date windows, delayed save acknowledgement and broker jobs absent from native queues. Those findings motivate continuation and independent-receipt fields; they do not promise a universal platform window.

## Potential problems

- Missing timezone data: install the declared dependency; never guess offsets. Explicit UTC disambiguates a repeated local hour.
- Changed caption, cover or slot: compare with actual approval scope. Refresh the stale payload hash only after obtaining any genuinely needed revised approval.
- A local ready result cannot detect later queue changes: inspect the live queue immediately before mutation.
- An empty queue during a pending save does not justify another upload or save.
- A private draft at release time is an unscheduled hold, not publication. Preserve its exact next action and existing notification policy.
