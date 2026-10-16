# PrismMoves visual analysis with PixelCue

PrismMoves composes PixelCue analysis into an evidence-labelled image profile. Engines belong to PixelCue; improve its public APIs rather than copying them into report or campaign code.

```powershell
& 'Z:/My Songs/Tools/PrismMoves.ps1' 'path/cover.png' --out 'path/analysis-new'
& 'Z:/My Songs/Tools/PrismMoves.ps1' 'path/cover.png' --models clip dinov2 blip ocr --out 'path/analysis-models-new'
& 'Z:/My Songs/Tools/PrismMoves.ps1' 'path/cover.png' --pixelcue-url http://127.0.0.1:8765 --out 'path/analysis-service-new'
```

Verify released and installed PixelCue 0.9.0+ identities, or inspect `/health.visual_analysis`. Local HTTP uses server-local paths and loopback only. No hosted inference/image upload occurs. Neural adapters load local weights by default. OCR needs pytesseract plus Tesseract. Existing PixelCue VLMs use `--pixelcue-models PROFILE` and require explicit `--allow-download` because their loader may download on first use. Preserve existing model/licence/privacy/cost permissions; do not enable downloads to fill missing receipts.

Outputs are analysis.json, report.md, report.html and checksums in a new directory. Exit 0 means completion, 2 means unavailable inputs/models retained in a report, 1 means configuration/backend failure. Preserve hashes, raster/matte/ICC handling, individual receipts and unknowns. Inspect the original alongside the report. Model interpretations are not verified facts.

For collection conclusions use assess-visual-identity: keep declared roles, canonical authority, dates and independent lineages, review clusters before outliers, and avoid counting derivatives as independent support. PixelCue compare_profiles supplies axis-specific distances and duplicate evidence without an invented brand score. One image supports an individual profile, not recurring identity rules.

## Ecosystem applicability

PixelCue supplies decoding, statistics, models, tags and comparisons. RasterMoves is conditional on an authorised derivative/restoration; ThumbMoves on collection browsing; KeywordMoves on source-backed campaign language. FrameRudiments, DanceRudiments, DanceMoves, StemLab and React Timeline Sequence apply only to real video/motion/audio/timing work. LikenessForge requires an authorised likeness task. EPK Social Metadata and DanceVault require actual page/private-delivery work. None is invoked merely to fill an inventory. Short Shifter stays independent of DanceFlow.

## Potential problems

- Old PixelCue lacks /v1/analysis; upgrade its backend rather than duplicate analysis.
- Missing cached weights or Tesseract yields unavailable receipts. Synthetic untrained model-interface checks do not prove pretrained accuracy on artwork.
- Matte, resize, ICC and frame-zero sampling influence measurements. Use matching conditions for comparisons.
- Signal novelty is not gaze; palette contrast is not actual text contrast; CLIP cosine is not probability. Intent, rights, consent, provenance and audience response need separate evidence.
- A client timeout does not cancel server inference; inspect active work before repeating or cleanup.
- In restricted Windows tests use workspace TEMP/TMP and pytest basetemp. The shared launcher overlays immutable published wheels on the existing PixelCue dependency runtime without replacing its source or installed package.

Canonical sources: Repositories/PrismMoves and upstream PixelCue. Skill: prismmoves. Software publication is separate from live-site/social publishing. Keep private inputs, reports, weights and coordination outside public packages.

## Project-local model storage

The launcher uses Repositories/PrismMoves/models. Downloaded weights and model caches belong there; models/ is gitignored. PixelCue's explicit installer writes clip/, dinov2/ and blip/ with revision/hash/licence manifests. Use --models-dir for another owning project's models/; default direct-API root is the working project's models/. Existing keyword taggers use the service process's project root. Shared DanceFlow project/global instructions now require the same convention for all component projects; existing caches are not automatically moved.
