# MediaSlide: complete capability reference

Canonical source: https://github.com/kieransimkin/react-mediaslide. The product name is **MediaSlide**; package and repository identifiers remain `react-mediaslide`.

Before each workflow, compare the latest stable GitHub release, npm `latest` and the package version actually imported. Historical tags reached 1.1.25 while npm remained at 1.0.24, so one source alone is insufficient.

MediaSlide provides list, details, adjustable thumbnails and double-buffered slide views; a responsive selection detail panel; custom item, detail and active-file renderers; initial selection; pointer, touch, wheel and arrow-key input; ResizeObserver layout; and bidirectional IntersectionObserver pagination.

Use it as collection UI. Keep app data, visual identity and HTML trust policy in adapters. Compose DanceMoves, React Timeline Sequence, ThumbMoves, PixelCue, PrismMoves, RasterMoves or FrameRudiments through their own supported contracts.

## Potential problems

- Mount client-side and test observer/event teardown in the consuming React app.
- Accept `slideReady` only from the expected embedded frame and trusted origin.
- Component stage expansion is not the browser Fullscreen API.
- Default item anchors navigate; use custom renderers when selection must remain in-place.
- A generated overview explains architecture but is not evidence of an actual application render.
