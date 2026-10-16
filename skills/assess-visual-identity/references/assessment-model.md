# Visual identity assessment model

Use this reference to compare a collection and write a visual-language understanding report. Adapt the detail to the size and diversity of the supplied set.

## 1. Define the unit of evidence

Assign every item an ID such as `A01`. Record:

| Field | Purpose |
|---|---|
| Item ID and title | Stable report reference |
| Source | Path or link; do not expose secrets or signed tokens |
| Media and dimensions/duration | Explains format constraints |
| Observed date | Separates current and historical state |
| Declared role | Canonical, approved, live, draft, experiment, reference, legacy, rejected, unknown |
| Lineage/family | Groups crops, resizes, exports, and derivatives |
| Availability | Inspected, partial, inaccessible, corrupt, or not visually assessable |
| Authority | High, medium, low, with a short reason |

Count independent visual lineages when describing support. Ten crops from one master are one strong lineage with good format coverage, not ten independent confirmations.

## 2. Code the visual axes

For each inspectable item, make short observable notes before interpreting meaning.

| Axis | Observe |
|---|---|
| Palette and contrast | Dominant fields, accents, temperature, saturation, value range, colour roles, contrast behaviour |
| Typography and marks | Serif/sans/script/handmade qualities, case, weight, tracking, hierarchy, logo or title behaviour, image-baked versus live text |
| Subject and motifs | People, objects, symbols, settings, repeated narrative anchors, absences |
| Composition | Focal hierarchy, symmetry, axes, depth, negative space, density, framing, gaze, crop and safe zones |
| Medium and image-making | Photography, illustration, collage, 3D, generative/composite, documentary, painterly, editorial, interface treatment |
| Texture and material | Grain, paper, metal, fabric, glass, grime, polish, edge treatment, physical/digital tension |
| Light and grade | Direction, softness, time of day, bloom, shadow colour, atmosphere, grading style |
| Motion and interaction | Camera behaviour, object motion, transition type, loop, speed, amplitude, rhythm, hover/scroll response, static fallback |
| Tone and narrative | Emotional register, tension, progression, implied world, audience posture |
| People and representation | Identity visibility, anonymity, styling, pose, consent/privacy signals, documentary versus fictional framing |
| Channel and function | Cover, hero, social, press, thumbnail, UI, motion, internal reference; what the asset must accomplish |
| Accessibility and technical | Text contrast, legibility, reduced motion, responsive integrity, compression, artefacts, malformed generated text |
| Provenance and status | Ownership/rights evidence, approval, recency, supersession, uncertain origin |

Use `Strong`, `Present`, `Partial`, `Absent`, `Contradictory`, or `N/A` in the comparison matrix. Add a few words of evidence instead of filling cells with unsupported scores.

## 3. Infer the system

Derive the visual thesis from the intersection of high-authority evidence, not from the loudest isolated item. A useful thesis names:

- the depicted or designed world;
- its central visual tension;
- the emotional effect;
- the most distinctive recurring device;
- what it is not, when a nearby generic reading would mislead future work.

Then classify patterns:

### Core invariant

Repeated across multiple independent high-authority items or explicitly designated as canonical. It survives more than one format when the collection provides format diversity.

### Supporting pattern

Appears repeatedly and coherently but lacks enough independence, authority, or coverage to become a core rule.

### Controlled variable

Changes predictably by channel, audience, intensity, narrative phase, or functional need while preserving the identity. Record the invariant role and the permitted range.

### Negative rule

A clearly rejected direction, a repeated absence that is meaningful in context, or a treatment contradicted by stronger evidence. Do not infer negative rules from absence alone unless the collection or user context supports them.

### Unknown

No conclusion is justified. Name the missing or conflicting evidence instead of filling the gap with common design practice.

Support statements should look like `4 independent lineages / 5 assessable lineages` or list the relevant item IDs. Always make the denominator clear. Exact support is evidence, not an aesthetic score.

## 4. Detect clusters before declaring outliers

When several items differ together on multiple axes, test whether they form a coherent sub-family. Useful cluster signals include:

- shared palette roles plus shared motif or setting;
- stable type/composition rules across one channel;
- a full-intensity and placement-safe pair;
- a chronological redesign;
- separate product, campaign, audience, or narrative phases.

Name a plural or layered identity when warranted. Do not average incompatible families into vague language such as “eclectic”.

## 5. Classify outliers

An outlier differs materially from the dominant or expected pattern on one or more axes. Compare it to the relevant cluster and role, not blindly to the whole collection.

| Class | Meaning | Report treatment |
|---|---|---|
| Intentional extension | Novel but preserves enough core grammar | Name what remains coherent and what is new |
| Channel adaptation | Difference follows functional constraints | Treat as controlled variation, not a defect |
| Legacy/superseded | Belongs to an earlier identity state | Preserve chronology; do not use as current rule |
| Experimental branch | Tests an unadopted direction | Keep separate from established language |
| Technical/export anomaly | Crop, colour shift, artefact, malformed text, missing media, or encoding issue | Describe observable issue and source context |
| Provenance mismatch | Source role or rights/status differs from the rest | Do not equate visual fit with permission to reuse |
| Contradictory item | High-authority evidence conflicts with the apparent system | Surface the conflict; do not hide it in an average |
| Unexplained outlier | Difference is real but intent/status is unknown | State uncertainty and request the smallest useful clarification |

For each outlier, record:

- item ID and declared role;
- differing axes;
- comparison baseline or cluster;
- magnitude: mild, material, or identity-breaking;
- observed evidence;
- likely explanation, explicitly labelled as interpretation;
- disposition: preserve, treat as channel-specific, quarantine from the current profile, investigate, or user decision required.

“Quarantine” means exclude from inference until status is resolved; it does not mean delete the asset.

## 6. Report structure

Use this structure unless the evidence calls for a shorter equivalent.

```markdown
# Visual identity assessment — [collection]

Assessment date: [date and timezone if relevant]
Scope: [what was and was not included]

## Executive visual thesis
[One evidence-labelled synthesis paragraph and overall confidence.]

## Evidence ledger
[Compact table using stable item IDs, roles, lineages, dates, availability, and authority.]

## Limitations and evidence quality
[Inaccessible links, missing formats, uncertain dates/status, sampling limits, duplicate lineages.]

## Core consistencies
[Rule, observed support, confidence, exceptions, practical implication.]

## Controlled variation and sub-families
[Channel adaptations, intensity variants, narrative phases, or clusters. Say when none are found.]

## Cross-asset comparison
[Compact matrix across the most discriminating visual axes.]

## Outlier register
| Item | Classification | Differing axes | Evidence and rationale | Disposition |
|---|---|---|---|---|

## Visual-language profile
### Colour and contrast
### Typography and marks
### Imagery, motifs, and setting
### Composition, hierarchy, and crop
### Medium, texture, material, light, and grade
### Motion and interaction
### Tone, narrative, people, and representation
### Accessibility, technical, and provenance boundaries

## Rules for future work
### Preserve
### Vary within these ranges
### Avoid or verify first

## Unknowns, conflicts, and next evidence
[Only the smallest useful clarifications, source assets, or controlled tests.]
```

## 7. Quality checks

Before delivering the report, verify that:

- every supplied item appears in the ledger, including inaccessible items;
- every major conclusion points to named evidence or an explicit support count;
- duplicates and derivatives have not inflated consensus;
- current, canonical, draft, reference, and legacy evidence remain distinct;
- interpretations and proposals are not phrased as observed fact;
- clusters were considered before labelling items as outliers;
- every outlier is contextualised rather than merely criticised;
- variable rules explain how the identity adapts without demanding sameness;
- exact palette values are called measured, sampled, or approximate as appropriate;
- rights, consent, and provenance gaps are not converted into unsupported claims;
- the report does not imply permission to alter or publish source assets.
