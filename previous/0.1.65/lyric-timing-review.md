# Prepare and review lyric timing

Use this when the lyric wording is known and the recording still needs a
reviewable line or word timing file. For a recording with an already accepted
LRC, validate its identity and import it directly.

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
vocal. Agreement between runs of the same model on different stems is
corroboration. A local onset and an entire repeated phrase can both match
acoustically, so confirm which occurrence the phrase belongs to.

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
- **A corrected LRC changes a word-driven effect.** Rebuild its timing
  inputs and compare the derived frame positions before rerendering. A
  passing line-count check leaves word and cue timing open.
- **The prepared clip has an unexpected first line.** Resolve the excerpt's
  start sample and active line on the source clock. Check the last event
  before the cut, including a clear, and inspect the encoded first frame.
