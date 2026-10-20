# WorkflowMoves agent guidance

## Full ecosystem and release preflight

Before every new workflow run, check the latest stable official release and observe the actual runtime used by the job. Follow [the shared preflight](https://github.com/kieransimkin/DanceFlow/blob/main/docs/workflows/release-preflight.md), this project's [people-and-agent guide](docs/ECOSYSTEM.md), the selected route manifest and each relevant Potential problems section.

Review the complete relevant capability inventory rather than only a familiar command. Use and compose every DanceFlow component that materially serves the authorised task: FrameRudiments for offline video composition, StemLab for audio and timing evidence, DanceRudiments for native movement, DanceMoves for live web motion, PrismMoves and PixelCue for visual evidence, and the other maintained packages through their supported file or API contracts. Preserve independent tool identities, exact source/package identity, clocks, privacy, costs and separate deployment gates.

Run the additive installer with `--check` first. Preserve surrounding project text and private evidence. A passing preview does not prove installation; a written rule does not prove adoption. Implement and verify the smallest reusable improvement when the work reveals a real shared gap, or record why existing capabilities suffice when no change is justified.

Downloaded model weights and model caches belong under `models/` in the owning DanceFlow project and remain ignored by Git. No catalogue checklist expands task scope or authorises model downloads, training or publication.

## Preflight temporary-directory access

Before any long, costly, model-backed, media-rendering, build, test, packaging or release command that creates private or atomic temporary directories, run a disposable preflight with the exact runtime, user or sandbox, and intended output parent. The probe must create a unique directory, write and read a file, atomically rename it, then remove the file and directory.

Keep temporary data and caches under the owning project on `Z:`; model weights and model-specific caches remain under that project's ignored `models/`. If the probe returns `WinError 5`, access denied, a rename failure or a cleanup failure, stop before the expensive command. Preserve the exact error and use the documented narrowly approved unrestricted recovery from the outset only when the task requires it. Use a fresh output directory and do not repeat the already-failing full job in the restricted shell.

After any unrestricted recovery, verify that the final output is readable and writable from the normal managed environment. If it is not, copy the completed bytes into a pre-created project-local directory that passed the probe, verify hashes, and retain the original failure and recovery evidence. Do not edit global ACLs, switch caches to `C:`, terminate unrelated processes or claim the underlying permission problem is fixed. Repositories that own temporary-directory creation should provide and test a reusable preflight helper rather than relying only on this instruction.