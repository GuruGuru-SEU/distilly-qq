# Save and install

After the requester approves a concrete preview, create a draft bundle using the QQ writer. Get group ID and target QQ ID from the request context, not filenames guessed from nicknames. `ROOT` below means the absolute loaded skill directory, not a literal shell variable that is preconfigured.

```sh
/opt/bot-venv/bin/python ROOT/tools/qq_writer.py --group GROUP_ID --user QQ_ID --name 'Display name' --work ./work.md --persona ./persona.md --evidence ./evidence.json --source ./distilly-evidence.jsonl --output ./persona-draft-v1
```

The output directory must be new. The writer generates a single installable `SKILL.md` using a stable name `qq-persona-GROUP_ID-QQ_ID`, plus upstream-format artifacts and evidence metadata for local review. It does not install anything or call any network API. Group and sender evidence must match the source export. The generated SKILL contains compact claim references and sample limitations, not raw history or local source paths.

Install only the generated `SKILL.md` file, not the entire draft tree (which contains version artifacts and private working material):

```sh
/opt/bot-venv/bin/python /opt/bot/skills.py list
/opt/bot-venv/bin/python /opt/bot/skills.py install ./persona-draft-v1/SKILL.md --key persona-save-1
```

If this stable skill name already exists, use its current revision:

```sh
/opt/bot-venv/bin/python /opt/bot/skills.py install ./persona-draft-v2/SKILL.md --revision CURRENT_REVISION --key persona-update-1
```

A registered persona takes effect on the next run and persists with the group's skill registry, including when foreground/background workspaces change. Use the existing revision and one stable key per mutation; do not bypass a permissions error. Non-admins can obtain a draft/preview and ask an administrator to install it. Background jobs return the absolute draft SKILL path so an authorized foreground run can use the existing helper's path handling.

For updates, read the installed persona, collect the requested additional evidence, distinguish explicit corrections from new inference, and preview the complete replacement. Use a new local output directory and replace only that persona's current registry revision. Do not promise automatic incremental updating or rollback: the host registry controls supported management operations. Remove through `skills.py remove NAME --revision CURRENT_REVISION --key ...` only when requested.

After installation, users can ask “@豆包 模仿某某的语气回答……”. The generated persona requires an explicit imitation request and a brief “模仿：” label. It is not the real member speaking and has no cross-group scope. Plain analysis without saving still works for every ordinary member.
