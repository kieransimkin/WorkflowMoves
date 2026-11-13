## Review lyric timing and revisions

Use [lyric timing review](lyric-timing-review.md) when the wording is known
and the timestamps are estimated or awaiting correction. For changes to a
rendered video, use [video revision](rendered-video-revision.md) to choose the
audition, check temporal dependencies and verify any retained footage and audio.
The `review-lyric-timing` and `revise-rendered-music-video` skills provide the
corresponding entry points.

Before a full render with a custom caption adapter, exercise the visible,
fully faded or cleared, and re-entry states. Return an empty bounds sequence
when the adapter paints nothing. See the [caption preflight](https://github.com/kieransimkin/WorkflowMoves/blob/main/workflows/framerudiments-rendering.md#preflight-caption-clears-and-gaps).
