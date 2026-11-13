# Verify an exact rendered music video

Use this after a native FrameRudiments render or when a render appears to have stopped. Keep the original project, audio, timing, fonts, assets, runtime and interrupted attempts unchanged. This guide diagnoses and verifies existing work; it does not authorise new generation, a restart, reduced quality or publication.

![Separate render, verification, human review and publication](media/rendered-video-verification.svg)

*Generated contract illustration, not evidence that a job passed.*

## Identify the job before acting

Read the owning job's instructions, private coordination and active-attempt record. Record the exact operating-system task/service, run directory, worker and launcher PIDs, creation times, command lines, live ancestry, frozen-input hashes and state/log paths. Process names alone do not establish ownership. Preserve other campaigns and development checkouts.

Check released, installed and imported component identities separately. Use the native FrameRudiments renderer/verification, saved StemLab source evidence and DanceRudiments motion contracts. Keep campaign art in adapters. Do not install a new version into a running job or change frozen files to make a check pass.

## Diagnose a long verification phase

Read file modification times and sizes, current native health/manifest, frame-analysis or chunk receipts, and the exact owned child's command line. Compare two bounded observations of CPU time and I/O counters when necessary. Distinguish encoding, count/probe, every-frame timestamps, full decode, source probing, checkpoint extraction, metadata reporting and manifest writing.

A status file can remain at an earlier phase until finalisation. A changing process phase or finalized checkpoint family can prove progress even when that status is old. Conversely, a live PID or increasing CPU alone does not prove useful progress or a correct output. Read the exact runtime call order rather than guessing from filenames.

A metadata-only executable startup such as `ffmpeg -version` can hold final manifest creation after decoding has passed. Record its elapsed time separately from video-processing time. Read aggregate memory/disk pressure and the owned process priority only when useful. Such observations suggest contributors; they do not diagnose an OS loader, security product or disk defect. A priority adjustment followed by completion is not proof of causation. Normal priority for an exactly identified owned job is a narrow recovery choice, not a default instruction to raise every process.

Keep a progressing job with its current owner. For a real failure, retain the errors, confirm the exact owned process exited, verify the inputs and identify the failed operation. Physically reserve the complete replacement attempt plus 2%. Choose foreground or operating-system ownership from the [existing render policy](framerudiments-rendering.md#choose-foreground-or-operating-system-render-ownership). Release each matching stage immediately before replacement bytes are written and retain the margin through technical QA.

## Recover only the failed stage

| Evidence | Recovery |
| --- | --- |
| The encoder stopped and the render has a verified contiguous chunk prefix. | Inspect the native resume plan, the canonical input hashes, encoder settings, chunk receipts and verified prefix. Use native resume to replay the prefix from frame zero and encode the missing frames. For a cache relocation, preserve the complete retained job, verify it after transfer and keep the final output path. FrameRudiments 0.4.25 introduced portable cache plans for newly prepared jobs. An older plan may still depend on the original root. Use a matching native plan or a verified migration for that exact job. |
| All chunks passed, but the assembled H.264 file failed exact CFR at joins. | Compare each chunk receipt and the joined timestamps before recomposing. If the failure is concat rounding, use the FrameRudiments 0.4.24+ frame-grid assembly correction with independently rounded PTS and DTS. Preserve the failed candidate and original chunks. Re-verify every output timestamp, both decoded pictures at each seam, the audio and the final hash. |
| Encoding completed and an owned verifier failed or wedged. | Identify its exact phase. After confirming exit and a finalized, stable file, run the maintained verifier on the file or a hash-verified copy in a healthy location. Preserve the original failure and require fresh passing evidence. The presence of an MP4 alone leaves review on hold. |
| The requested change alters the prepared project or a dependency. | Treat it as a [new revision](rendered-video-revision.md). Determine the affected range and temporal dependencies before deciding whether any existing video can be reused. |

When a run reports a wrapper error after encoding, locate the first failed
stage in the native receipts. Read the file, chunk and QA states alongside the
wrapper exit. A failed cleanup can coexist with an intact encoded file, which
still needs its own passing QA before delivery. If authorised independent scene
diagnostics share a failing prerequisite, stop that diagnostic batch once the
same failure is established. Keep any independently rendered scenes separate
from the continuous candidate. A reset feedback scene cannot establish the
state it would have inherited in the continuous film.

Keep the original composition/runtime identity in the receipt. If a newer tool
performs assembly or verification, record that version and the specific
operation separately. See the [released FrameRudiments chunking and cache contract](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.28/docs/chunked-rendering.md).

![Measured synthetic H.264 join timestamp error before and after the frame-grid correction](https://raw.githubusercontent.com/kieransimkin/FrameRudiments/v0.4.28/docs/media/chunk-timestamp-drift.png)

*Actual measurements from a synthetic encoded fixture. The timestamp graph
exposes the sub-frame error that is difficult to see in playback.*

## Verify the exact final bytes

Require the native final manifest and `candidate-health.json` permitting review.
For `framerudiments.candidate-health.v1`, check the schema, `technical_qa: "passed"`,
`review_allowed: true`, `affected_by_error: false` and absence of an error.
Use these structured fields for machine decisions and retain the human-readable
state for diagnosis. Check the exact candidate's independent SHA-256 against the
manifest. Keep review on hold for a missing, contradictory or failed record.

A completed verification receipt can follow an exact byte copy when it identifies
the whole verified file. Recompute the source and delivery SHA-256 independently,
compare them with the verified identity, and record the original verifier and
receipt. Recheck destination-specific properties separately. If the source is
unstable, the hash differs or a required check never finished, verify the
delivered file directly. A matching hash cannot complete a missing check.

Inspect native evidence for dimensions, native frame rate, decoded frame count, every-frame CFR timestamps from zero, full-stream decode, expected channels/sample rate, and source/master identity. Verify start-inclusive/end-exclusive sample bounds and the actual trim/repeat/fade filters against the authorised programme. AAC is a derivative: correct sample mapping is not bit equality with PCM. For chunked output, require the contiguous finalized prefix, replay from zero for temporal/feedback state, exact coverage, decoded seam checks, canonical audio muxed once and full assembled-stream QA.

Preserve the artist's final resolution/frame-rate/spatial/temporal quality contract. Duplicated or interpolated frames do not establish native frame rate. Verify sequential feedback counts and actual source-time sampling; installed libraries alone do not establish integration.

## Inspect encoded behaviour

Use actual decoded frames from the exact final file, not composition previews. Include frame zero, the final frames, every lyric/cue state, adjacent boundary frames, prop entry/exit boundaries and the important authored trajectory points. Batch checkpoint extraction with the maintained renderer where supported. Keep frame number, output seconds, source seconds and signed lyric quantisation error distinct.

Inspect at native size and phone size. Check title/artist identity, canonical words and punctuation, contrast, safe areas, faces, sprite alpha edges and the ending. A contact sheet supports sampled visual review, not continuous-motion or attended-listening approval. Inspect real destination overlays and the exact native upload preview before scheduling; an offline text rectangle alone does not prove platform fit.

### Bind decoded checkpoints to the current encode

1. Pin the encoded file by hash. Request checkpoints by zero-based decoded
   frame index, including frame zero and the last verified video frame. Use
   FrameRudiments' native encoded checkpoints when they cover the request.
   For a custom extraction, create a fresh output directory for that file and
   request the exact indices with frame sync set to passthrough.
2. Require the requested count, readable images and a mapping from image to
   encoded file hash, frame index and video presentation timestamp. Hash any
   stills that will be reused. Build the contact sheet from that list after
   checking the images. Reuse a prior sheet only when its source and image
   hashes and checkpoint mapping still match.
3. Use the actual decoded frame table for variable-rate, offset or rounded
   streams. For a zero-based CFR encode of N frames at rate f, the last
   picture starts at (N − 1) / f seconds. A visual cycle of N output frames
   reaches its endpoint at N / f. Check the expected phase step over the
   wrap and watch the repeated encoded seam with audio. The first and last
   stills can differ by one frame of expected motion.

A seek near the container's end can return zero without writing a single
image. A previously existing PNG at that path may survive unchanged. Treat
an end-relative seek as a tail sample until its decoded index is established.
The following command extracts frame 119 from a verified 120-frame file.
Create the destination directory before running it.

```sh
ffmpeg -n -nostdin -v error -xerror -abort_on empty_output_stream -i verified.mp4 -map 0:v:0 -vf "select=eq(n\,119)" -fps_mode passthrough -frames:v 1 -update 1 fresh-qa/encoded-00000119.png
```

Use the verified local executable directly if a shell shim fails. Check
FFmpeg and FFprobe identities independently when the utilities come from
different installs. For syntax and output handling see the [FFmpeg command
reference](https://ffmpeg.org/ffmpeg.html) and [select filter reference](https://ffmpeg.org/ffmpeg-filters.html#select_002c-aselect).

![A stale still titled Prior ending beside frame 119 from the exact Current ending encode](media/ending-frame-comparison.png)

The synthetic 60 fps fixture reproduced exit code zero with an unchanged
PNG after a seek within five milliseconds of the end. The last video frame
started at 1.983333 seconds. A guarded empty extraction failed and an exact
index extraction wrote the current ending. [Play the current two-second encode](media/ending-frame-demo.mp4) · [Verification receipt](media/ending-frame-evidence.json) · [Reproduction source](https://github.com/kieransimkin/WorkflowMoves/blob/main/examples/verify-ending-frames.py)

If a new derivative takes visual cues from a finished edit, sample the
approved edit in sequence and around the relevant transitions. Record
decoded frame identity or the approximate time shown by the published player.
Use the asset inventory to trace provenance and the finished frames to show
what appeared. One still supports a claim about that moment alone.

### Check captions, prop bounds and effect regions

For a centred caption panel, compare the panel centre with the painted ink,
stroke and shadow of the complete wrapped block. Nominal line heights can
leave the visible text high or low. Verify short, long and wrapped states
in decoded frames after changing alignment.

Eight-source-time shutter integration can blend adjacent lyric states in a boundary frame. Inspect the actual preceding/onset/following frames and record the observed behaviour; do not silently move canonical onsets or call a sampled blend an unrelated text corruption.

Check transformed bounds for each moving prop. Reports may contain only the visible intersection with the canvas, so an extent ending at canvas width does not prove the whole transformed sprite stayed inside. Document deliberate exits by layer, interval and direction, and inspect encoded entry/tip/fall/exit points. Distinguish intended canvas exits from accidental clipping of faces, lyrics or artwork. Do not turn one creative exit into a general clipping exception.

For contained effects, compare actual pre/post-effect checkpoint pairs and the encoded result. Measure the declared region and representative outside regions, retaining frame, pixel coordinates, scale and differences. Composition, supersampling and antialiasing can affect comparisons; do not claim outside-region stability or musical response merely from loading a shader or recording its configuration.

### Prove visualiser routing in the encoded output

Record the expected input, clean overlay and visibility window for each
important layer. When an element must stay readable through a beat reveal,
inspect it before, at and after that reveal. Check the count and shape of
required foreground elements as well as the changing effect. A layer that
exists in the project may still be occluded or visible only inside feedback.

In FrameRudiments 0.4.29, `qa/composed-*` is captured before optional
visualiser processing. `qa/source-*` is captured after processing and final
antialiasing, before encoding. `qa/encoded-*` comes from the decoded video.
Use the installed version's capture order to label evidence. Match those
checkpoints by frame index, then play the sequential encoded transition.
If the routing is correct but the motion looks jerky, follow the
[motion diagnosis workflow](render-motion-diagnosis.md).

When the visualiser should reveal a plate, check the stage's output alpha,
matte or opacity. Opaque black can still hide the plate. Inspect the
beginning, middle and end of the transition and the layers that should stay
outside the effect. The [native underlay comparison](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.29/docs/visualisers.md#isolated-underlay)
includes sampled composition checkpoints and a two-second synthetic encode.

### Verify the effect-graph backend and samples

For a project using `effect_graph`, read
`composition.effect_graph_backend` in its native manifest. Match the
requested backend, actual context and renderer to the pinned run, then
inspect `last_dispatch` and `last_transport` for work on the GPU and CPU.
An attached GPU context can accompany CPU fallback. With temporal
supersampling, `sampling.scope: last_subframe` limits those counters to
the last evaluated subframe. Keep the sample rate and encoded rate with the
receipt. Allocation/reuse counts and retained RGBA payload describe the
renderer pool. An optional driver query has its own reported scope.

Check the effect at the authored seam, extrema and transitions in the exact
encoded file. For a fallback, retain the affected setting, driver and
available dispatch evidence alongside the rendered comparison. Use a
separate bounded project preflight when a sampled manifest leaves an
important state unobserved. `qa/composed-*` may already include the effect
graph, since that capture precedes the optional feedback engine. Use a
matched graph-disabled comparison when a pre-graph image is needed.
[Feature selection and backend evidence](https://github.com/kieransimkin/WorkflowMoves/blob/main/workflows/framerudiments-rendering-features.md#choose-and-verify-the-effect-graph-backend).

### Check planned motion variants

When a brief calls for a reduced-motion export, keep the intended audio
interval, information, lyric order and cue mapping consistent across the
standard and reduced-motion versions. Where both use the same layout, keep
their text timing aligned. Compare the decoded opening, maximum movement,
caption changes and ending at phone size. Verify readable information in the
static treatment and record the separate hashes and review status of both
files. Keep the destination's accessibility and publication review with the
exact variant being delivered.

## Keep canonical caption exports

Retain native SRT/ASS and the native frame ledger. If a destination displays HTML-escaped apostrophes literally, create a separately named upload SRT by unescaping the native text. Verify its complete text and interval mapping against the canonical ledger/native export, hash it and retain both originals and derivative. Do not rewrite canonical words or treat a burned-in caption as proof that an attached subtitle file is correct.

Verify the performed sequence before timing a long alignment that stacks
many words or repeats the wrong chorus. Resolve omitted, reordered or
substituted lines against the exact recorded arrangement with targeted
listening, then retain the approved text and regenerate the dependent
timings. Keep campaign slogans, release cards and other editorial overlays
as separately identified visual events. Time the performed captions from
the accepted recording and check their export against that lyric track.

## Deliver and continue without conflating states

Record technical QA, sampled creative review, continuous motion, attended listening, artist exact-file approval, cover check, copy audit, upload, persisted schedule and independently public playback separately. Source-excerpt approval does not approve a materially new generator. A playable exact-file handoff and the user's actual approval are evidence; do not invent listening the agent did not perform.

Present a technically verified film promptly for its authorised review. A future schedule remains separate from publication. Preserve native AI/provenance declarations, current copy/keyword checks, named-zone/UTC time, existing queues, exclusions, exact approval and the public-save gate for later EPK reconciliation. Never backdate or substitute immediate publication or a replacement upload for an unavailable scheduling route.

Complete the owning task's Blogworthiness PASS/FAIL assessment with evidence. A passing creative/technical story retains its angle, current published/pending-draft duplicate review, exact media/public-use blocker and named continuation. Keep private masters, unreleased images, account captures and operational records outside public workflow packages.

## Public demonstration and evidence limits

![Actual synthetic FrameRudiments output before and after full-frame effects](https://raw.githubusercontent.com/kieransimkin/FrameRudiments/v0.1.4/docs/media/full-frame-comparison.png)

*Actual public synthetic FrameRudiments 0.1.4 output, not evidence for a later private render or this recovery.*

[Play the public native pipeline demonstration with controls](https://kieransimkin.github.io/DanceFlow/framerudiments.html) and read its [transcript](https://github.com/kieransimkin/FrameRudiments/blob/v0.1.4/docs/media/demo-transcript.md). Dynamic inspection requires an actual demonstration; the diagram above only explains the gate sequence. Reuse public-safe native examples rather than disclosing a private song to illustrate a workflow.

## Potential problems

- **Old health timestamp:** corroborate with exact processes, call order and finalized artifacts; do not overwrite native health to unblock review.
- **Very slow executable startup:** separate startup from decode duration, retain bounded observations and the successful/failed exit. Do not blame the artwork or a security product without evidence.
- **A renderer has no callback for finalisation progress:** retain an independent monitoring receipt rather than editing a frozen runtime. Route a reusable telemetry improvement to its canonical owner after the job.
- **A launcher rejects a scene receipt that the renderer wrote:** verify the recorded path and the receipt/video pair before declaring the scene missing. In Windows PowerShell, variables that differ only in case can overwrite the receipt directory with a filename. Test the repaired wrapper with multiple receipts and a native command that writes to stderr but exits zero. Base the exit check on the native exit code and verified output.
- **Invisible RGB outside sprite alpha:** a tool preview may show hidden RGB differently. Inspect actual RGBA/alpha and composite the sprite on the intended scene before altering pixels. Preserve originals.
- **Technical checks pass but motion/sound is unreviewed:** hand off the exact file with those states explicit. Do not fabricate an artistic pass.
