# Collecting QQ evidence

The host needs the extended `history.py` CLI. Check `/opt/bot-venv/bin/python /opt/bot/history.py --help` once if unsure. If a flag is unavailable, use bounded `--user`, dates, `--limit` and `--offset` queries and disclose that sampling/context are limited; do not install packages or change the bot.

Examples (replace QQ_ID and dates with the resolved target/range):

```sh
/opt/bot-venv/bin/python /opt/bot/history.py --members --name '昵称'
/opt/bot-venv/bin/python /opt/bot/history.py --stats --user QQ_ID --start YYYY-MM-DD --end YYYY-MM-DD
/opt/bot-venv/bin/python /opt/bot/history.py --user QQ_ID --start YYYY-MM-DD --end YYYY-MM-DD --sample 120 --seed qq-profile-v1 --context 2 --output ./distilly-evidence.jsonl
/opt/bot-venv/bin/python /opt/bot/history.py --message-id 'snowluma:MESSAGE_ID' --context 3
```

The export is a NEW file; choose a new filename on subsequent collections. It contains a metadata record, selected target messages, and separately tagged context messages. Read slices with ordinary file tools. The helper's JSON stdout reports the actual selected count and truncation flags without printing the whole export.

- Sampling selects one seeded message per active day in rounds before taking second/third messages from those days. If there are more days than the sample size, it selects seeded days. It is a stylistic sample, not a frequency estimate or exhaustive review. The same seed is reproducible for the same archive state.
- `coverage` describes the whole group archive; `total` is the count matching the query. `--stats --user` gives the target's actual first/last timestamps and active days. Member names are historical aliases, not a live QQ roster.
- `context_ids` link to other selected/context records; `reply_to` preserves original message IDs. Context can be outside the selected date range and belong to other people. Missing replies and context truncation are explicitly marked.
- Ordinary text is capped at 2000 characters per message and the combined selection/context at 60,000 text characters. If `text_truncated` matters, fetch that message by ID (up to 16,000 characters), not the same page repeatedly.
- `--contains` includes ready voice transcripts. A voice placeholder without a transcript is not evidence of what was said. Images/files are references, not their contents; inspect only relevant available attachments with the host tools.
- For a recent-only sketch use `--order desc`. For exhaustive review use ordinary paging and follow `next_offset`; clearly state partial coverage when stopping. Avoid a full-group dump for one person's profile.

Keep a small evidence JSON file for the writer:

```json
{
  "group_id": 123456789,
  "user_id": 123456,
  "period": {"start": "2026-10-01", "end": "2026-10-13"},
  "sample_count": 80,
  "seed": "qq-profile-v1",
  "claims": [
    {"claim": "Often answers with a short code example", "kind": "observed", "message_ids": ["snowluma:123", "snowluma:456"]},
    {"claim": "Seems to prefer concrete examples", "kind": "inference", "message_ids": ["snowluma:123"]}
  ],
  "limitations": ["Only recorded messages in this group", "Some audio had no transcript"]
}
```

Use actual IDs and counts, never copy the illustrative values. Keep claims short. The writer verifies that cited IDs are selected messages by the target in the exported dataset; it cannot verify an inference's semantic correctness. Fetch and merge a larger bounded dataset if necessary rather than citing absent records.
