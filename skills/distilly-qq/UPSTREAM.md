# Upstream provenance

Derived from https://github.com/titanwings/distilly at commit
`0afc45c29c360ba7bc8260f1bb0bf34e9155f4fa` (MIT, copyright 2026 titanwings).

Unmodified files:

- `tools/upstream/skill_writer.py` ← `tools/skill_writer.py`
- `tools/upstream/skill_schema.py` ← `tools/skill_schema.py`
- `tools/upstream/skill_presets.py` ← `tools/skill_presets.py`
- `references/upstream-persona-analyzer.md` ← `prompts/colleague/persona_analyzer.md`
- `references/upstream-work-analyzer.md` ← `prompts/shared/work_analyzer.md`
- `LICENSE` ← `LICENSE`

This is a focused derivative, not the full upstream distribution. QQ-specific files
are maintained separately; external collectors, personal-owner setup and host
installers are intentionally not bundled. `tools/qq_writer.py` calls the upstream
artifact engine with a QQ renderer; it does not edit those vendored files.

To update: review upstream changes, replace only the recorded files, update this
commit pin, run tests and validate the package with the bot's `load_bundle`.
Do not commit group exports, generated personas, credentials or private archives.
