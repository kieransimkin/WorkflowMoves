# Asset prompt pack: {asset ID} / {variant} / {release}

Complete every field before generation; replace these placeholders with the actual asset brief. This is one asset/required variant, not a campaign-wide moodboard.

## Asset and source decision

Type and shot IDs: {background, sprite, model, rigged character, texture, footage or other; shots}.
Narrative/visual-hook purpose: {what this asset contributes}.
Decision: {reuse, source, generate, or source plus generated concept/texture}; reason: {fit/gap}.
Required files: {actual image/mesh/rig/material/animation formats and compatible consumer}.
Native consumer/effect: {current FrameRudiments feature/configuration, exact version/tagged contract, linked StemLab control evidence/source clock, layer order and alpha/depth/overscan requirements; unverified dependencies labelled}.
Existing/sourced file and evidence: {paths, hashes, author, source page/file URLs, licence and attribution; or exact missing dependency}.
Current state: {required, sourced, prompts_ready, baseline_generated, baseline_reviewed, production_ready or blocked}.

## Supplied reference images and usage notes

| Reference ID / attachment order | Actual local file / hash / dimensions | Origin, licence and permitted reference use | Borrow | Exclude / preserve independently | Target-specific mapping |
| --- | --- | --- | --- | --- | --- |
| {R1 / 1} | {path, SHA-256, width x height} | {cover or original online item, author/date/licence URL; eligibility} | {palette, material, shape, pose or lighting} | {cover text, background, other subjects; independent constraints} | {ordinary label and supported provider token/role if verified} |

Cover-crop evidence: {parent path/hash/dimensions; crop x,y,width,height in top-left pixels; method; resulting path/hash/dimensions; or not applicable}.
Reference previews: {embed or link the actual selected images with captions and alt text}.
Missing references: {exact IDs and resolution, or none; do not claim missing files were attached}.

## Shared visual and production specification

Subject/number, silhouette, pose/action and identity: {precise details}.
Composition, perspective/camera and crop/overscan: {specific scene geometry}.
Palette, materials, texture and light/shadow direction: {campaign-grounded constraints}.
Canvas/aspect, intended display size and output/layer/alpha: {requirements; actual API settings separate}.
Lyric-safe quiet area and layer order: {bounds and what must remain empty}.
Continuity: {named subjects, viewpoint, wardrobe/props, shared anchors across shots}.
Exclusions: {unwanted words/logos, merged backgrounds, extra people/objects, baked shadows or other relevant negatives}.
Acceptance: {observable checks; image baseline and actual mesh/rig/motion requirements distinguished}.

## Nano Banana prompt — complete still-image brief

{Write the full prompt: create this specific asset, identify every supplied reference and its distinct role, describe framing/subject/material/light, keep the required quiet region and alpha/layer intent, and state relevant exclusions. No unfilled template markers.}

Target family/version and supported settings: {prepared target; verify before later execution}.

## Seedance prompt — asset/keyframe plus motion plan

{Write the same asset appearance and reference mapping in full, then the intended shot duration/context, subject motion, camera onset/development/end, light continuity, ending/hold and excluded changes. For a still asset specify a locked still/keyframe design and keep any proposed motion variant separate.}

Input role: {exact first frame or appearance/style reference; supported mapping to be verified}.
Target family/version and supported settings: {prepared video target; no execution implied}.

## GPT built-in image prompt — exact baseline call text

{Write the complete still-image prompt for the same asset and actual reference set. Translate provider tokens and choose one reviewable key pose from any motion plan. This must be ready to pass to the built-in image tool, not a summary of the other prompts.}

Tool reference arguments: {all-local paths or supported conversation-image mechanism; not both}.
Transparency: {true for required cutout, false otherwise; preserve existing alpha for edits}.
Adaptations from the still brief: {what changed and why, or none}.

## Execution, saved files and review

Prompt files/hashes and reference hashes/order saved before call: {evidence}.
GPT call/result identity and actual output location: {evidence or pending}.
Campaign baseline file / SHA-256 / actual dimensions / alpha result: {verified readback}.
Review: {identity, composition, text-free/quiet area, crop, edges, layer fit and remaining corrections}.
Provider execution state: {Seedance prepared; Nano Banana prepared; GPT generated/reviewed or exact hold}.
Production state: {actual mesh/rig/motion readiness and evidence; never infer from a baseline still}.
Next action/owner: {remaining specific work or complete}.
