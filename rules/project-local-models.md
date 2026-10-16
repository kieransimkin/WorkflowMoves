# Project-local models for every DanceFlow project

Standing instruction from Kieran, 16 October 2026: install all downloaded model weights and model-specific caches in a `models/` directory within the owning project, and add `models/` to that project's `.gitignore`.

- Apply to every DanceFlow component, new project, integration, chat, agent and recurring workflow. Resolve the actual owning project before installing; do not default downloads to C:, a user profile, an unrelated project or a global model cache.
- Route framework download/cache settings, adapter model paths and trained-data locations beneath that project-local models root. Keep model identity, revision, licence and file-hash manifests there where supported. Weights, caches and private model evidence stay out of Git, wheels, source archives and public release assets.
- Download only models useful for the authorised task and permitted by existing licence/cost/privacy/download requirements. The storage rule does not require a catalogue-wide download or another model run.
- Before migrating existing weights, inventory current references and consumers, preserve originals and manifests, stage the new location, verify actual loading and update references. Do not silently move/delete existing models or claim every running chat has adopted a saved rule.
