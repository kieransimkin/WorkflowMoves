## Default route

For complementary lyric candidates, use native `stemlab fuse-lyrics REQUEST
--output NEW_DIRECTORY` once its source/release identity is verified. Current
implementation: `Repositories/stemlab-lyric-fusion-20261024`, branch
`feature/lyric-evidence-fusion`; it is not yet a published release. The canonical
`docs/lyric-fusion.md` specifies source/text/clock gates, correlated view grouping,
explicit artist locks, observed-only chronological selection and draft exports.
Retain all alternatives, disagreements and untimed words. No averaging,
interpolation or beat snapping; no automatic EPK timing replacement. Follow
`Workflows/stemlab-lyric-timing-audition.md` and require listening QA separately
from canonical coverage. Do not duplicate this selector in release adapters.
