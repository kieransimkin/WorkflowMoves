---
name: direct-social-scheduling
description: Prepare, recover, commit and verify approved multi-platform social schedules directly in native platform queues, with exact media/copy/cover identity, interrupted-session recovery and persisted readback. Use for authorised YouTube, TikTok, Meta, LinkedIn or comparable native scheduling; do not treat visible form values, uploads or local plans as persisted schedules.
---

# Schedule social posts directly

Use the maintained [direct social scheduling workflow](https://github.com/kieransimkin/WorkflowMoves/blob/main/workflows/direct-social-scheduling.md), or the installed `Workflows/direct-social-scheduling.md`. Also read the owning campaign's rights, approval, platform-order, timing, disclosure, hashtag and browser-control rules.

## Facebook video publishing

Use the Facebook Page Video API by default for My Songs video uploads. Send the exact approved master in Page-scoped resumable chunks, verify it as a ready unpublished draft, then schedule the same video ID and read back the Page's saved schedule. Follow the Facebook section in `Workflows/direct-social-scheduling.md`.

1. Bind each destination to exact approved media, caption, cover, disclosure settings, account and named-zone/UTC slot. Run `Tools/social_schedule_plan.py`; its output is preparation only.
2. Inspect the native queue immediately before a commit. Preserve unrelated posts and resolve replacements/cancellations before taking responsibility from another scheduler.
3. On recovery, inspect the current native queue and retained attempt evidence before reopening a composer. Never infer that an interrupted tab saved, failed or published.
4. Use platform-native input events and readback. A DOM property, automation return value or visually filled field is not persistence evidence if the platform later reads it as blank or changed.
5. Wait for upload processing and cover/caption/disclosure acceptance before navigation. Make one authorised commit, then independently reopen the native Scheduled/Planner view and verify exact copy, media duration, audience, slot and timezone.
6. Treat `In progress`, delayed acknowledgement and pending saves as unresolved existing attempts. Observe them; do not blindly resubmit.
7. Record local plan, upload, draft, schedule, publication and verified public playback separately. After publication, reconcile eligible campaign media into its EPK.
8. Close every completed job-created or released borrowed tab through supported controls and confirm with a fresh inventory. Preserve unsaved or active work with a named owner and next action.

Use the supported browser/connector for the workspace. This skill grants no account access, publication approval, rights clearance, spending or immediate-post authority.
