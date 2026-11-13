## Release preflight and the retired interpolation route

Check the current stable release and the actual imported runtime before starting.
StemLab 1.14.1 exposes the released word ensemble and display review commands.
Use the installed `Tools/StemLab.ps1` if it imports the verified release and shows
both commands. An older environment needs the matching official package.
[Current My Songs launcher release](https://github.com/kieransimkin/stemlab/releases/tag/v1.14.2)

Use the [released line gates](https://github.com/kieransimkin/stemlab/blob/v1.14.1/docs/lyric-line-gates.md)
for `python -m stemlab.lyric_batch`, optional `stemlab.lyric_acoustic` and explicit
part assembly. The archived timing scripts interpolated unsupported lines and
ranked whole-song scores. Keep held exports visible. Reject cross-gap phrases,
missing first-word anchors, onset collisions and implausible compression.
Preserve late anchors as review evidence. Read the programme length from the
audio header and verify difficult sections before export.

Keep simultaneous parts and repeated occurrences distinct. A single audio
observation cannot establish that a phrase was sung by two voices. Record
unplaced words and preserve canonical wording. A karaoke track needs audible
vocal evidence to supply an acoustic lyric anchor.

## Establish authority before editing

1. Identify the exact master by SHA-256, sample rate and frame count. Locate
   the canonical lyrics, approved line and word timings, cues and any selected
   WordPress timing attachment. Use an approved same-recording LRC directly
   for line display, and use it read-only when comparing a new display policy.
2. For new word timing, load all canonical occurrences. Use `lyric-ensemble`
   for saved observations and `lyric-display` for separate visibility drafts.
   Retain model families, chosen endpoints, crop flags, missing edges and
   uncertain parts. Review the native word onset and release separately from
   optional pickup or hold policies.
3. Stage the proposed edits in a separate source-frame timing document. Keep
   the stable line and word IDs, preserve all child word intervals within the
   corresponding editor line, and review any separate display suggestion that
   would hide a sung word. A line can remain visible after its last word ends.
4. Keep approved timings, model hypotheses and attended listening distinct.
   Review the full song before using a proposed timing as an approved source.
   [Commands and acceptance checks](lyric-timing-review.md)
