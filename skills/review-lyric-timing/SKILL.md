---
name: review-lyric-timing
description: Prepare a review LRC from estimated lyric onsets, flag uncertain lines for listening, or adopt an artist-corrected LRC for a specific recording. Use when the lyric text is known and line or word timing still needs evidence or review.
---

# Review lyric timing

Follow the [lyric timing workflow](https://github.com/kieransimkin/WorkflowMoves/blob/main/workflows/lyric-timing-review.md)
or the installed `Workflows/lyric-timing-review.md`.

1. Pin the target master, canonical lyric wording and any existing timing
   authority. Reuse saved StemLab evidence and clock-verified vocal stems.
2. Compare doubtful onsets in bounded windows. Track the lyric occurrence as
   well as the words. Export a versioned review LRC and listening notes with
   alternate onsets where relevant. Mark each proposed timing as estimated.
3. After a timing decision, read back and hash the accepted LRC with its source
   and authority. Verify words, order, clears and timing bounds. Reconcile
   affected word markers and lyric-driven cues on the same master clock.
4. Verify the renderer's frame ledger and relevant decoded frames when the
   timing feeds a video. Keep technical checks and attended listening in
   the handoff. Use the existing accepted timing directly when it is already
   established for this recording.
