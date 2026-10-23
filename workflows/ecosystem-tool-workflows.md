# Run the relevant DanceFlow tool workflow

This map supplies task, input, output and acceptance contracts for every current component and the separate discovery toolkit. Read the selected capability reference for native commands, options, examples and platform requirements; use the installed runtime's matching version. A passing map check establishes documentation coverage, not execution or host acceptance.

![Generated lesson-to-workflow contract illustration](media/tool-learning-contract.svg)

Generated contract illustration, not a screenshot or proof of a completed run. Actual interface captures and videos belong with the selected tool's versioned examples and the task's evidence. Another generic interface video would not demonstrate all native hosts and is omitted.

Run `python tools/audit_workflow_coverage.py` from this package. The standard-library checker derives component membership from the maintained capability index and rejects absent tools, duplicate identities, missing local workflows and empty input/output/acceptance contracts. It makes no network requests and claims no external-link or runtime acceptance.

## Select the task and retained evidence

### StemLab

Analyse selected audio/MIDI evidence or edit supported timing lanes. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/stemlab.md).

**Inputs:** Master hash, source rate and canonical words; Saved analysis, selected detectors and explicit model choice.

**New outputs:** Source-bound analysis, timing proposals and uniquely named derivatives.

**Acceptance:** Compare original and offset beat grids, including half/double-time hypotheses; Hash original inputs before/after; review estimated lyrics and MIDI.

**Limits:** Detector confidence is not artist-approved BPM or transcription; A timeline control and its editor/gallery applications need their own package/runtime checks.

Use [stemlab-phrase-and-clip-evidence](stemlab-phrase-and-clip-evidence.md), [stemlab-fourier-frequency-bands](stemlab-fourier-frequency-bands.md).

### DanceRudiments

Select native movement or prepare a finite, typed rig recording. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/dancerudiments.md).

**Inputs:** Integer 64-pip source clock, rig profile and provenance; Reviewed target character and motion/calibration data.

**New outputs:** Native pattern selection or bounded recording with explicit retarget mapping.

**Acceptance:** Verify the requested target mesh and bind/profile hashes; Check start/end/seek, units and loop seams only where a loop is claimed.

**Limits:** Preview speed is not verified musical beat matching; Rig-tempo confidence and lyric-match thresholds are separate measures.

Use [stemlab-audio-motion-recordings](stemlab-audio-motion-recordings.md), [potbot-unity-integration](potbot-unity-integration.md).

### FrameRudiments

Compose a deterministic offline video or bounded preset experiment. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/framerudiments.md).

**Inputs:** Pinned audio, timing, artwork/font hashes and source offsets; Native movement and reviewed renderer/preset parameters.

**New outputs:** New encoded video, timing/frame ledger and optional response evidence.

**Acceptance:** Decode actual final bytes; inspect first frames, captions, crop, loop and soundtrack mapping; For feedback, replay preceding frames and compare programme/silence/probe conditions.

**Limits:** A controlled response or cached still does not prove musical quality; Do not rerun a full catalogue or analysis merely for documentation.

Use [framerudiments-rendering](framerudiments-rendering.md), [framerudiments-preset-profiling](framerudiments-preset-profiling.md).

### DanceMoves

Attach live web effects to a verified playback/input owner. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/dancemoves.md).

**Inputs:** Page-owned appearance and metadata-derived timing; Exact source/offset association and selected runtime.

**New outputs:** Bounded shared clock/controllers connected to painted consumers.

**Acceptance:** Exercise play/pause/seek/end, switches and reset/teardown; Verify actual pixels and pointer/phone routes; preserve full-page appearance.

**Limits:** A listener or loaded library is not a connected visual effect; Synthetic sensors and software rendering are not physical-device acceptance.

Use [epk-mobile-motion](epk-mobile-motion.md), [epk-evidence-gate](epk-evidence-gate.md).

### KeywordMoves

Research and reconcile source-specific keyword observations. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/keywordmoves.md).

**Inputs:** Canonical phrase register, exact source/window and reviewed exports; Explicit local/hosted model selection only when needed.

**New outputs:** Deduplicated phrases, attributed observations and separate hypotheses.

**Acceptance:** Re-import changed records and verify schema/deduplication; Keep literal text, demand, platform metric and inference distinct.

**Limits:** An extraction score is not measured audience demand; A source import or roadmap does not imply a native live provider.

### RasterMoves

Prepare a reviewed upscale or bounded refinement comparison. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/rastermoves.md).

**Inputs:** Authorised source image, target dimensions and alpha/crop policy; Selected plugin/model revision under project-local models/.

**New outputs:** New image candidates and runtime/model settings.

**Acceptance:** Inspect actual delivered dimensions, alpha, edges and crop; Compare target-size candidates against the original.

**Limits:** A model catalogue entry is not an installed or useful model; No blanket model downloads or original-image overwrite.

### LikenessForge

Repair likeness or train/use a specifically authorised identity profile. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/likenessforge.md).

**Inputs:** Authorised reference identity and source composition; Pinned compatible model/LoRA, seed and bounded settings.

**New outputs:** Private comparison candidates and reproducible profile evidence.

**Acceptance:** Review likeness, blend and complete composition at delivery size; Verify actual optional dependencies and one relevant inference.

**Limits:** Installed core CLI is not qualified face processing or training; A successful inference does not establish likeness approval or public-use rights.

### PixelCue

Measure visual assets or serve a bounded local analysis request. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/pixelcue.md).

**Inputs:** Exact media bytes and requested measurements; Explicit optional model profile and actual service/runtime identity.

**New outputs:** Statistics, selected model observations and request-scoped receipts.

**Acceptance:** Verify health and the actual analysis route; retain unavailable model states; Preserve deterministic measurements independently of semantic hypotheses.

**Limits:** Do not duplicate its analysis engine in callers; A loaded model/service is not evidence of a completed request.

Use [prismmoves-visual-analysis](prismmoves-visual-analysis.md).

### PrismMoves

Synthesize an image profile or temporal-first preset description. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/prismmoves.md).

**Inputs:** PixelCue measurements and condition/frame lineage; Time intervals, programme/silence/probes and selected semantic evidence.

**New outputs:** Evidence-labelled profile, response families and retained comparisons.

**Acceptance:** Inspect chronological condition sheets and isolated selected outputs; Use content-addressed output identity; retain history before revised reports.

**Limits:** Similar frames do not become independent evidence; A model interpretation is not a measured identity or one universal quality score.

Use [prismmoves-visual-analysis](prismmoves-visual-analysis.md), [framerudiments-preset-profiling](framerudiments-preset-profiling.md).

### ThumbMoves

Request a thumbnail already present in the operating-system cache. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/thumbmoves.md).

**Inputs:** Selected local file, cache backend and requested format/size.

**New outputs:** Cache-hit thumbnail or explicit miss/backend result.

**Acceptance:** Verify actual cache evidence and bounded failures; Return miss honestly where no public backend exists.

**Limits:** A cache miss is not permission to decode the source; Do not infer macOS cache support from another platform.

### React Timeline Sequence

Build a selected-source audio/timing editor or inspection timeline. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/react-timeline-sequence.md).

**Inputs:** Stable asset identity, source rate and controlled transport; Beat, line/word/cue or MIDI lanes with explicit coordinate units.

**New outputs:** Callbacks, sample-frame loop/seek edits and source-bound audition.

**Acceptance:** Verify controlled callback persistence, seek/loop bounds and selected-source lyrics; Confirm package consumers and asset changes reset the correct owner.

**Limits:** A reusable control is distinct from its editor application; Do not let view coordinates or a second clock alter original source time.

Use [stemlab-phrase-and-clip-evidence](stemlab-phrase-and-clip-evidence.md).

### EPK Social Metadata

Stage canonical Open Graph, X and Schema.org music/page facts. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/epk-social-metadata.md).

**Inputs:** Fresh canonical release/page/audio facts and eligible public media.

**New outputs:** Reviewed minimal metadata fields and anonymous source evidence.

**Acceptance:** Read back exact persisted values and public rendered tags; Preserve WordPress ownership of title/canonical/robots/sitemap.

**Limits:** Correct markup does not prove social-card display or ranking; Public saves retain their exact approval and source gates.

Use [epk-evidence-gate](epk-evidence-gate.md).

### WorkflowMoves

Propagate reviewed shared lessons without replacing project instructions. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/workflowmoves.md).

**Inputs:** Exact maintained route manifest and fresh target bytes; Public-safe lesson verified against source and execution evidence.

**New outputs:** Preview/apply/repeat receipts and matching released workflow package.

**Acceptance:** Require known managed block identity and unchanged surrounding bytes; Check full ecosystem workflow coverage, then run owning release tests.

**Limits:** Installed guidance does not prove adoption by another running chat; Private chat transcripts and scheduler definitions stay outside releases.

Use [tool-development-lessons](tool-development-lessons.md).

### DanceVault

Prepare authorised encrypted delivery on a qualified destination host. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/dancevault.md).

**Inputs:** Exact approved source bytes, recipient/expiry policy and private credentials.

**New outputs:** Encrypted container, independent source/container hashes and delivery evidence.

**Acceptance:** Verify the exact Apache/nginx/WordPress host route and actual access behaviour; Exercise expiry/revocation and fail-closed error paths within authorised scope.

**Limits:** Test-host acceptance is not destination-host deployment acceptance; No plaintext fallback, sensitive upload or access-policy expansion.

### MediaSlide

Compose a media browser with stable selection and explicit pagination. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/mediaslide.md).

**Inputs:** Stable item IDs, bounded fixtures and an explicitly sized host; Controlled mode/selection/page state and real pagination callbacks.

**New outputs:** List/details/thumbnails/slide rendering with retained request evidence.

**Acceptance:** Exercise all four modes, selection, custom rendering and Previous/Next; Record observer requests without autonomous fixture page changes.

**Limits:** A deterministic harness must still observe the real callback; Tagged package, main demo, WordPress ZIP and deployed site are distinct.

### Potbot

Use durable native coding tasks/jobs on a qualified host. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/potbot.md).

**Inputs:** Registered workspace/sandbox, exact repository/candidate and task contract; Qualified provider/model, budget and effect authority.

**New outputs:** Durable jobs, retained candidate artifacts and verification/usage receipts.

**Acceptance:** Verify actual host isolation, workspace containment and interrupted-run reconciliation; Keep private custody qualification separate from published verification-key checks.

**Limits:** Source preview; registered models and planned MCP routes are not implementation; No unrestricted execution fallback or automatic host/account changes.

Use [potbot-unity-integration](potbot-unity-integration.md).

### DanceFlow for Unity

Import the reviewed UPM package and run a source-bound clock/rig sample. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/danceflow-unity.md).

**Inputs:** Exact Unity/package identity, approved sample, master clock and rig profile; Qualified target mesh/GPU and independent finite recording clock.

**New outputs:** Native Editor/Player sample evidence with exact source and consumer identities.

**Acceptance:** Test the actual package import and requested visible character/materials; Verify play/pause/seek, finite bounds and source mapping in the native host.

**Limits:** Managed tests or a subset-copy CI consumer do not qualify whole-root UPM import; Deployed WebGL and software rendering do not prove physical GPU or musical alignment.

Use [potbot-unity-integration](potbot-unity-integration.md).

### DanceFlow toolkit

Discover useful components and compose their supported contracts. [Native commands and examples](https://github.com/kieransimkin/WorkflowMoves/blob/v0.1.41/workflows/danceflow/capabilities/toolkit.md).

**Inputs:** Current catalogue, exact releases and observed runtime/host identities.

**New outputs:** Purpose-specific plan, typed discovery/adapters and explicit availability states.

**Acceptance:** Run the no-service discovery example and check the actual invoked adapter; Keep seventeen member engines separate from the discovery/composition toolkit.

**Limits:** Discovery is not execution or native-host qualification; Short Shifter remains independent; no blanket model or service setup.

Use [scheduled-danceflow-tool-use](scheduled-danceflow-tool-use.md), [potbot-unity-integration](potbot-unity-integration.md).

## Recover and generalise a lesson

Use [the development-learning workflow](tool-development-lessons.md). Retain original user intent, observed failure, current source, relevant test and the route updated. A past chat assertion is a lead until verified. Keep unreturned messages and inaccessible bodies explicit; do not label a partial search exhaustive. Private source transcripts, photos, credentials and correspondence do not belong in this public package.
