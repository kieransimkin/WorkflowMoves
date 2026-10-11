# My Songs workflows

Private, versioned project rules and workflow additions for Kieran's local My Songs workspace. This repository contains maintained instructions, routing fragments and a tool launcher. Song audio, artwork, reports, credentials, correspondence and rights evidence stay outside it.

Version: 0.1.0. StemLab runtime baseline: released 1.4.0 with native DanceRudiments 0.2.4. The runtime wheel, model dependencies and source checkout are separately installed and are not bundled here.

`workflows/stemlab-rudiment-motion-selection.md` is the shared motion-selection contract. `routes.json` defines additive insertions into the existing video, EPK, analysis, sprite, Canvas and shared-template workflows and their discoverable skill copies. `rules/github-publication.md` is the project-wide GitHub completion rule. `tools/StemLab.ps1` installs to the workspace's Tools directory.

Use `python install.py --root "Z:\My Songs" --check` to inspect integration status and `python install.py --root "Z:\My Songs"` to apply missing additive blocks. The installer validates every route before writes, preserves existing text and fails on ambiguous anchors or modified managed blocks. It does not install Python packages, publish pages or upload media. Review filesystem permissions and ownership before applying to installed skills.

Run `python -m unittest discover -s tests -v` for the preservation, conflict and repeat-run checks. Release archives contain these exact source files and a checksum manifest.
