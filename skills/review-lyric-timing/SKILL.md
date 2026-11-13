---
name: review-lyric-timing
description: Compare StemLab word alignments, review sung boundaries and line visibility, or adopt an artist-corrected LRC. Use when known lyrics need line or word timing evidence for a specific recording.
---

# Review lyric timing

Follow the [lyric timing workflow](https://github.com/kieransimkin/WorkflowMoves/blob/main/workflows/lyric-timing-review.md)
or the installed `Workflows/lyric-timing-review.md`.

1. Pin the target master, canonical lyric wording and any existing timing
   authority. Reuse saved StemLab evidence and clock-verified vocal stems.
2. Verify the released runtime. Combine saved, occurrence-matched onsets and
   releases with `stemlab lyric-ensemble` when independent evidence can help.
   Keep one vote per model family and replay suspect crops with more context.
   Retain alternatives, missing edges and listening flags.
3. Use `stemlab lyric-display` for display drafts. Treat intentional line holds
   and approved LRC comparisons as visibility evidence. Keep acoustic word
   edges and approved timing files intact. Audition the draft on the source clock.
4. After a timing decision, read back and hash the accepted LRC with its source
   and authority. Verify words, order, clears and timing bounds. Reconcile
   affected word markers and lyric-driven cues on the same master clock.
5. Verify the renderer's frame ledger and relevant decoded frames when the
   timing feeds a video. Keep technical checks and attended listening in
   the handoff. Use the existing accepted timing directly when it is already
   established for this recording.
