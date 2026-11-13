---
name: diagnose-rendered-video-motion
description: Diagnose stepped, jerky, flickering or smeared motion in a rendered music video or Short. Compare decoded cadence with the object trajectory, native motion sampling, blur, shutter and visualiser history, then verify a bounded correction.
---

# Diagnose rendered video motion

Follow the [motion diagnosis workflow](https://github.com/kieransimkin/WorkflowMoves/blob/main/workflows/render-motion-diagnosis.md)
or the installed `Workflows/render-motion-diagnosis.md`.

1. Verify the exact encoded cadence. Watch the affected passage at normal
   speed and inspect adjacent frames at a fast passage, reversal or cue.
2. Isolate the object or effect. Compare its pose with the expected source
   clock and the pre-effect, post-effect and decoded frames when available.
   Use object motion evidence even if every whole-frame hash differs.
3. Change one cause at a time. Compare procedural sampling, trajectory
   rate or extent, scoped directional blur, temporal shutter or feedback
   history as the evidence warrants. Keep the approved timing and delivery
   rate through the audition.
4. Verify the exact encoded comparison at the relevant crop and playback
   speed, including adjacent captions, bounds and transitions. Use
   `revise-rendered-music-video` when the selected fix requires replacing
   footage in an existing film.
