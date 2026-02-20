---
description: Sync meeting transcripts from Fireflies.ai API
allowed-tools: Bash, Read, Write, Glob
argument-hint: [--force to resync all, --list to show meetings, --days N]
---

# Sync Fireflies Meetings

Export meeting transcripts from Fireflies.ai to the vault inbox.

## Execution

Run the sync script located in this repo:

```bash
source .env.local 2>/dev/null
python3 .claude/skills/sync-fireflies/scripts/fireflies_sync.py \
  --api-key "${FIREFLIES_API_KEY}" \
  --output-dir "_inbox/transcripts/fireflies" \
  $ARGUMENTS
```

**Arguments:**
- (none): Export only new/unsynced meetings from last 7 days
- `--days N`: Look back N days instead of 7
- `--force` or `--overwrite`: Re-export all meetings (ignore duplicates)
- `--list-only`: List meetings in Fireflies without exporting
- `--meeting-id ID`: Export a specific meeting

## After Syncing

1. Report how many meetings were exported
2. List the new files in `_inbox/transcripts/fireflies/`
3. Suggest running `/process` to extract entities

## Troubleshooting

If "API key not found":
1. Set `FIREFLIES_API_KEY` environment variable
2. Or add to `.env.local` file: `FIREFLIES_API_KEY=your-key`
3. Get your key from: https://app.fireflies.ai/integrations/custom

If "No meetings found":
1. Verify your Fireflies account has recordings
2. Try a longer date range: `--days 30`
3. Check API key has proper permissions
