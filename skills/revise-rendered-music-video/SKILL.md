---
name: revise-rendered-music-video
description: Revise a specific title, lyric, scene or effect in a rendered music video. Use for bounded previews, choosing a safe render boundary, or proving a splice preserves the expected footage and soundtrack.
---

# Revise a rendered music video

Use the [video revision workflow](https://github.com/kieransimkin/WorkflowMoves/blob/main/workflows/rendered-video-revision.md)
or the installed `Workflows/rendered-video-revision.md`.

1. Pin the accepted parent and its source clock. Map the requested change to
   layers, inputs, frames and later temporal dependencies. Keep earlier
   creative decisions in the revised brief.
2. Compare the same source frames. Use stills for layout and alpha. Use a
   sequential encoded sample for motion, feedback, flicker and audio timing.
3. Choose the smallest verified render scope. Use the native prefix/replay
   contract for a matching interrupted job. Use a new revision for a changed
   project. Consider a stream-copy splice only with an independently
   decodable compatible boundary and verified unchanged timing.
4. Check decoded seams, the retained video and soundtrack, full decode and
   frame timestamps against the parent and revised sources. Bind review to
   the revised file hash and use the [encoded verification workflow](https://github.com/kieransimkin/WorkflowMoves/blob/main/workflows/rendered-video-verification.md).
