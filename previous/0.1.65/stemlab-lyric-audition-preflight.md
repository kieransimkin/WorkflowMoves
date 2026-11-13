## Release preflight and the retired interpolation route

Resolve current official GitHub and registry releases before every new workflow
run, then verify the actual import path, version and source. Retain failures as
unavailable; use the supported network route to complete the check before model
inference. The 2 November 2026 recovery verified StemLab 1.12.1, release commit
`307062e2b1e97a44d9194453ac1b4b360182229a`, after an earlier run wrongly reused
1.11.1 source. These version numbers are historical evidence, not a future pin.

The old `.timing-tools/align_lyrics.py` and `run_alignments_isolated.py` silently
interpolated unsupported lines and ranked whole-song scores. Their exact originals
are archived under `.timing-tools/archive/2026-11-02-before-line-gates`; both active
paths now delegate to the line-gated StemLab API or stop visibly if it is absent.
Never restore the archived scripts to bypass a held export.

The new APIs and regression coverage are currently source-only in
`Repositories/stemlab-lyric-timing-20261102`, based on the verified 1.12.1 release:
`python -m stemlab.lyric_batch`, optional `python -m stemlab.lyric_acoustic`, and
`stemlab.lyric_parts.assemble_lines`. Check their PR/release state before claiming
they are present in an official installation. The ordinary 1.12.1 package remains
separate from this tested source extension. See its `docs/lyric-line-gates.md` and
actual synthetic overlap diagram. Source tests and a version number do not prove
artist listening, distinct voice identity or public software publication.

Before using a retained estimate, check every line and difficult section against
its actual evidence. Reject interpolation, cross-gap phrases, missing first-word
anchors, rounded onset collisions and implausible compression. Preserve explicit
late anchors as review evidence. A global match ratio cannot override a failed
section, and audio duration comes from headers rather than the last ASR word.

Keep simultaneous vocal parts separate. An LRC delivery can sort explicit part
onsets while its evidence table retains canonical occurrence IDs and written
block order. Reusing one observation for repeated written blocks is an artist
review hypothesis, never proof that both phrases were sung independently.
Neither the single-track fusion preview nor 1.12.1's phrase-loop boundary fix
detects or solves vocal identity. Karaoke with no usable vocal content cannot
supply missing lyric anchors. Keep all canonical words unchanged and retain
unplaced/ambiguous occurrences rather than inventing a serial timeline.

## Establish authority before editing

When candidates cover different sections well, use StemLab's native
`fuse-lyrics REQUEST --output NEW_DIRECTORY` workflow rather than choosing one
whole transcript or averaging timestamps. See the canonical
[fusion guide](https://github.com/kieransimkin/stemlab/blob/feature/lyric-evidence-fusion/docs/lyric-fusion.md)
and reproducible synthetic source-selection diagram. This feature is currently
source-only on the named branch; verify its eventual release before using a
released-version claim. Do not infer availability in the existing launcher.

Verify each candidate's exact master, canonical text and original full-source
clock. Group correlated decodes of the same stem under one `view_id`, retain
explicit artist locks, and exclude unverified crop/Suno/master mappings. The
native selector uses corroborated actual observations and compatible gap fills,
retaining provenance, alternatives, disagreements and every untimed word. It
does not average, interpolate, beat-snap or move existing source times. Its
heuristic ranking is not a confidence percentage. Keep the new LRC/SRT/word
bundle provisional until context listening; preserve existing selected EPK
timing attachments and cues. Use its all-word JSON/TSV to review missing line
edges and conflicts before promoting any result.

1. Identify the exact master by path, SHA-256, sample rate, frame count and
   duration. Identify canonical lyric text, existing artist-timed line/word files,
   cues, prior saved edits and the WordPress-selected timing attachment when an
   EPK is affected. Presence or a familiar filename is not authority.
2. Load the complete song and complete canonical lyric set. Do not improve only
   the reported phrase and then call the result whole-song timing. Preserve
   backing-vocal words and overlaps as separate performed evidence; do not force
   them onto a lead-vocal onset merely because the text repeats.
3. Keep line boundaries, word onsets/ends and display policy distinct. A line may
   intentionally appear a few declared ticks before its first word, but it must
   contain every child word and clear at an explicit reviewed time.
4. Keep model alignment, detector evidence, artist edits and attended listening
   as separate states. Automated timing can propose boundaries and diagnostics;
   it never silently replaces approved timing.
