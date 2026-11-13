# Prepare and review lyric timing

Use this when the lyric wording is known and the recording still needs a
reviewable line or word timing file. For a recording with an already accepted
LRC, validate its identity and use it for line display. Gather fresh word
evidence if the job also needs sung-word highlighting.

## Establish the recording and the words

Pin the exact master or approved mix, its SHA-256, sample rate and sample count.
Retain the canonical lyric source and wording in performed order. Label where
the timestamps came from. A plain lyric field, a worksheet displaying the
words, and an exported timestamp file provide different evidence. Keep the
line, word, clear and musical cue tracks distinct on the master clock.

Reuse saved StemLab alignments and vocals where available. Check that each
alternate audio view matches the master clock before using its onsets. An
alternate take can help identify words. Derive timing on the target recording
or from a stem with verified alignment to it. For disputed rows, compare a
bounded window around the expected occurrence with the master and the aligned
vocal. Runs from the same model lineage share one family even on different
stems. A local onset and an entire repeated phrase can both match acoustically,
so confirm the occurrence and vocal part before combining evidence.

## Compare saved word alignments

Check the current release, installed import and command help. The
`lyric-ensemble` route starts with StemLab 1.14.1. Use one exact master WAV,
canonical lyrics, and saved word evidence from the master or full-length
stems verified against its clock.

The My Songs launcher uses its existing Python 3.11 analysis environment and
the verified versioned wheel under `Tools/stemlab/models/runtimes/stemlab-1.14.2`.
Install the matching official distribution and confirm the imported version
before applying the launcher update. On other installations, use the
verified `stemlab` executable in the chosen environment.

1. Start with free recognition and the surrounding lyric order to anchor
   each occurrence. Preserve uncertain words, repeated hooks and simultaneous
   parts. Try the optional local letter-level CTC route or Qwen known-text
   alignment where it can resolve a missing or disputed edge. Preserve free
   recognition alongside forced matches. The same Whisper lineage still
   supplies one family across free and forced passes.
2. Map each observed onset and release to a native master frame. Give the
   request one row per canonical word in physical lyric line order, with
   empty edge lists where there is no observation. Record the master hash,
   native rate and frame count, the model family, source/view, checkpoints
   and crop-to-master mapping. The CLI checks the supplied master and words.
   The caller verifies every observation's source mapping. Use the tagged
   request example to assemble the inputs.
3. For an edge near a decode limit, repeat the same occurrence on the same
   view with more real audio at that side. Save both decode limits and the
   remapped repeat edge as `crop_repeat`. A flagged edge remains visible and
   contributes neither corroboration nor complete-span support. Stability
   across two crops is evidence about that decode, with a single family vote.
4. Review the selected onset and release, competing alternatives and
   original whole-span support. Keep short or unsupported words in the
   audition list. Use FireRed AED activity for entrances and gaps and vocal
   energy or pitch to inspect releases. A pitched trace can include backing
   vocals or bleed. Unvoiced consonants can start before pitch is present.
   Use these traces to guide listening around the word and its neighbours.

```text
stemlab lyric-ensemble request.json --master master.wav --output ensemble-review.json
```

For singing activity, use the optional FireRed adapter on a verified audio
view or saved analysis. Retain `events.json` and `activity-scores.npz` with their
source mapping. Its 10 ms score spacing describes sampling, while its detected
events can span multiple words. Provision the model under the owning project's
ignored `models/` and install its dependencies in the worker interpreter,
which starts in Python isolation mode. Use StemLab 1.14.2 or later for the
evidence model-path and backend-Python CLI options.

```powershell
stemlab evidence vocals.wav --output singing-activity --model firered_aed --device cpu `
  --model-path "firered_aed=models/FireRedVAD/AED" `
  --backend-python "firered_aed=PATH_TO_WORKER_PYTHON"
```

The command combines existing observations. Decode the required audio views
before assembling the request. It selects observed edges and keeps alternatives
and untimed rows. Keep the master, saved inference and approved timing untouched.
[Tagged request and CTC instructions](https://github.com/kieransimkin/stemlab/blob/v1.14.1/docs/lyric-boundaries.md)
· [Tagged FireRed and pitch routes](https://github.com/kieransimkin/stemlab/blob/v1.14.2/docs/evidence-models.md)

![Actual synthetic crop-test output showing an estimate moving with the crop while the selected onset stays fixed](https://kieransimkin.co.uk/wp-content/uploads/2026/11/crop-stability-demo-still.png)

The synthetic replay shows the orange estimate moving from 0.99 to 0.54
seconds while the selected onset stays at 1.00 second. The published example
includes the silent captioned 60 fps video and its illustrated article.
[Watch the crop test](https://kieransimkin.co.uk/2026/11/13/when-the-word-moves-with-the-crop/)

## Compare line visibility

`lyric-display` takes the ensemble draft or StemLab's reconciled
`word-timings.json` and writes a new review JSON. Compare the plain first-word
baseline with the default long-pickup adjustment. If the line is meant to stay
visible through a short gap, preview an explicit hold. Use a separate output
for each policy.

```text
stemlab lyric-display ensemble-review.json --output display-unshifted.json --no-pickup-adjustment
stemlab lyric-display ensemble-review.json --output display-comparison.json --reference-lrc artist.lrc --hold-until-next-within 1.5
```

The second command shows an optional 1.5-second policy on a verified
same-recording artist LRC. The LRC supplies display starts and explicit blank-tag
clears for scoring, including intentional visibility after the last sung word.
Missing or ambiguous clears stay unscored. Keep the original acoustic word
edges, both display proposals and coverage. When tuning a policy, compare
whole-song holdouts, common paired rows, median and tail errors and missing
coverage. Word accuracy requires separate word annotations.

## Audition the proposed word and line timing

Use the complete [StemEdit audition](https://github.com/kieransimkin/stemlab/blob/v1.14.1/docs/lyric-audition.md)
on the exact master or a verified full-length stem. Keep the ensemble and
display JSON as review evidence. Stage a separate source-frame timing document
for the editor with stable line and word IDs, verified source identity and
original word edges. Check that each word fits its editor line. If the display
proposal would hide a word at its beginning, retain the proposal separately
and resolve the difference in context before exporting.

![Actual StemEdit audition showing the active word on the source clock](https://raw.githubusercontent.com/kieransimkin/stemlab/v1.14.1/docs/screenshots/lyric-audition-active-word.png)

The screenshot shows an actual UI check on synthetic audio and text. Check
seek/play, the active word, holds, overlaps, short pickups and the downloadable
timing bundle. Listen to every uncertain boundary before marking it reviewed.
[Silent editor demonstration](https://github.com/kieransimkin/stemlab/blob/v1.14.1/docs/lyric-audition.md#verification-and-recording)

## Give the reviewer a usable LRC

- Export a separately named UTF-8 review LRC with all canonical lines in order.
  Keep deliberate empty events where the display needs to clear. Record
  ambiguities in a companion table with line index, proposed timestamp, source
  interval, reason to listen and any competing onset. Keep review notes out of
  the lyric text.
- Prioritise weak pickups, joined or repeated phrases, processed voices,
  zero-duration model spans and the last lyric before an instrumental. Check
  both the start and clear of a line. Mark the proposed anchors as estimated
  and retain their evidence without smoothing away audible disagreements.
- If a preview helps, use a short encoded clip with the actual recorded audio,
  a few disputed lines and enough lead-in to hear their onsets. Retain the
  source sample bounds, candidate LRC hash and relevant decoded frame numbers.
  A technically verified preview still needs the timing decision.

For example, a synthetic excerpt beginning at 12.000 seconds can already
display a line whose onset was 11.840. Keep 11.840 in the master LRC, then
verify that the excerpt displays the carried-in line at output frame zero and
clears at the intended point. A reviewer can then distinguish an incorrect
onset from an excerpt that starts within an existing line.

![Encoded synthetic timing comparison with two motion tracks on the same source clock](https://raw.githubusercontent.com/kieransimkin/FrameRudiments/v0.4.28/docs/media/beat-alignment.png)

*Actual synthetic output. The motion phases differ while the source timing
stays fixed.* [Play the 60 fps example](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.28/docs/media/beat-alignment.mp4) · [Fixture source and timing notes](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.28/examples/beat-alignment/generate.py)

## Adopt the corrected timing

When the artist or designated timing owner supplies or approves a revision,
retain that exact LRC and bind its hash to the master and approval. Read the
file back as UTF-8. Compare all performed lines, order, punctuation, clears
and bounds with the authoritative inputs. If the renderer needs a derived
copy, document any header removal or formatting change and compare every
timed event with the accepted file.

Reconcile affected word onsets, lyric markers and lyric-driven effect cues
against the corrected lines. Musical cues with independent source anchors
retain their own evidence. Check the prepared frame ledger and a decoded
sample around an affected onset, clear and any excerpt carry-in. When word
timing remains provisional, use the confirmed line timing alone where the
brief allows or hold the dependent word-synchronised treatment. Record which
revision the render, caption exports and motion use. Confirm production
timing before spending a full render on an estimated pass unless the artist
requests a clearly marked draft.

## Potential problems

- **The aligner chose the wrong repetition.** Compare the neighbouring lyric
  order and a bounded waveform or spectrogram around both occurrences. Leave
  the disputed anchor flagged until listening resolves it.
- **A timestamp moves when its crop moves.** Retain both native-frame estimates
  and the crop check in the draft. Give the occurrence more verified context
  or audition it with another model family.
- **FireRed or Qwen rejects a valid local model override.** Check the imported
  StemLab version. The CLI in 1.14.1 checked the MIDI model list. Use 1.14.2
  or the 1.14.1 Python evidence API with an isolated worker environment.
- **A line stays up after singing ends.** Preserve the display clear and the
  final word release as separate times. Compare the LRC against display
  proposals and keep word evidence on the master clock.
- **A corrected LRC changes a word-driven effect.** Rebuild its timing
  inputs and compare the derived frame positions before rerendering. A
  passing line-count check leaves word and cue timing open.
- **The prepared clip has an unexpected first line.** Resolve the excerpt's
  start sample and active line on the source clock. Check the last event
  before the cut, including a clear, and inspect the encoded first frame.
