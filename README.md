# Distilly QQ

A standalone, optional QQ group skill derived from [Distilly](https://github.com/titanwings/distilly).
It analyzes a member's recorded chat style and produces evidence-backed, reusable imitation personas.
No Distilly code is bundled into qq-dsh-bot; this repository uses its generic history and skill tools.

## Install in a group

A group owner, administrator or configured skill manager can send:

> @豆包 安装这个 skill：https://github.com/GuruGuru-SEU/distilly-qq

The bot should download the repository archive, inspect it and install the `skills/distilly-qq/` subfolder through
`skills.py`. Do not pass a Git checkout containing `.git` to the installer; use a clean archive/extracted
skill subfolder, or the release's `distilly-qq.zip` asset. Do not run upstream installers or pip scripts.
Each group installs separately; it takes effect on the next request.

## Use

- `@豆包 用 Distilly 分析我最近30天的聊天风格`
- `@豆包 蒸馏一下 @某某，先给我看看画像`
- After preview: `@豆包 确认，保存这个人物 skill` (requires a group skill manager)
- `@豆包 模仿某某的语气解释一下这个问题`

Analysis is available to ordinary members. Persistent persona installation keeps the bot's existing admin permissions.
The skill does not automatically profile everyone, rewrite group memories or replace the bot's normal identity.
Profile claims retain message IDs; synthetic examples are labeled, and missing history is acknowledged.

## Host requirements

[qq-dsh-bot](https://github.com/GuruGuru-SEU/qq-dsh-bot), with its generic per-group skill registry and the extended
`history.py` flags `--members`, `--stats`, `--sample`, `--context`, `--order`, and `--output`.
Current implementation is on the bot's `migration/snowluma` branch. Python 3.11+ is enough for this bundle;
no additional Python dependencies, collector credentials, browser or external service are required.

The saved profile is per group + QQ ID. Generated SKILL files are registered through the bot helper and survive
container restarts. Draft evidence remains in the task's workspace, never in this public repository.

## Development

```sh
python3 -m unittest discover -s tests -v
python3 tools/package.py --output /tmp/distilly-qq.zip
```

The archive excludes Git metadata, tests and caches, contains one SKILL.md and preserves the MIT license.
See [UPSTREAM.md](skills/distilly-qq/UPSTREAM.md) for the pinned source and update procedure.
