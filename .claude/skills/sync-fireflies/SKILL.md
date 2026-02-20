# Fireflies.ai Source Processor

Extract meeting transcripts from Fireflies.ai via GraphQL API.

## Overview

Fireflies.ai provides AI-powered meeting transcription with summaries and action items. This skill syncs transcripts via their GraphQL API and creates properly formatted markdown files in the OPAL inbox.

## Invocation

This skill is automatically invoked by `/sync` when `fireflies` is configured as a source.

Direct invocation:
```
/sync fireflies
/sync fireflies --force    # Ignore cursor, resync all
/sync fireflies --limit 5  # Only sync 5 most recent
```

---

## EXECUTION INSTRUCTIONS

When syncing from Fireflies.ai, execute these steps IN ORDER.

### Step 1: Check API Key

**Action:** Verify API key is available.

1. Check for `FIREFLIES_API_KEY` environment variable
2. Check `.env.local` file in project root

```bash
source .env.local 2>/dev/null
test -n "$FIREFLIES_API_KEY" && echo "API key found" || echo "API key missing"
```

**If not found:**
```
Fireflies API key not found.

Set your API key:
  export FIREFLIES_API_KEY="your-key-here"

Or add to .env.local:
  FIREFLIES_API_KEY=your-key-here

Get your API key from: https://app.fireflies.ai/integrations/custom
```
STOP.

### Step 2: Load Sync State

**Action:** Read current sync cursor.

1. Read `_index/sync-state.json`
2. Get `sources.fireflies.cursor` (last synced meeting date)
3. Get `sources.fireflies.last_sync` (timestamp)

### Step 3: Get Filters

**Action:** Load filter configuration from `config/integrations.yaml`.

```yaml
fireflies:
  filters:
    min_duration_minutes: 5
    max_age_days: 30
    exclude_titles:
      - standup
      - 1:1
      - daily sync
```

Default filters if not specified:
- `min_duration_minutes`: 5
- `max_age_days`: 30
- `exclude_titles`: []

### Step 4: Run Sync Script

**Action:** Execute the Python sync script.

```bash
source .env.local 2>/dev/null

# Determine days to sync
DAYS=${MAX_AGE_DAYS:-30}

# Run the sync
python3 .claude/skills/sync-fireflies/scripts/fireflies_sync.py \
  --api-key "$FIREFLIES_API_KEY" \
  --output-dir "_inbox/transcripts/fireflies" \
  --days "$DAYS"
```

**With specific arguments:**
- `--force` flag: Add `--overwrite` to the script
- `--limit N` flag: Fetch all then take first N results
- `--meeting-id ID`: Add `--meeting-id ID` to the script

### Step 5: Apply Title Filters

**Action:** Check synced files against title exclusion filters.

For each file in `_inbox/transcripts/fireflies/`:
1. Read the frontmatter `title` field
2. Check against `exclude_titles` list (case-insensitive)
3. If match, move file to `_inbox/transcripts/fireflies/.excluded/`

### Step 6: Update Sync State

**Action:** Update `_index/sync-state.json`.

```json
{
  "sources": {
    "fireflies": {
      "enabled": true,
      "last_sync": "{current_timestamp}",
      "cursor": "{most_recent_meeting_date}",
      "items_synced": {previous + new_count},
      "errors": {error_count}
    }
  }
}
```

### Step 7: Summary

```
Fireflies.ai Sync Complete

Meetings synced: {count}
Duration covered: {total_minutes} minutes
Output: _inbox/transcripts/fireflies/

New files:
{for each file:}
  - {filename}

Next: Run /process to extract entities
```

---

## Error Handling

### Invalid API Key
```
Error: Fireflies API returned 401

Your API key appears to be invalid. Check:
1. Key is correct in FIREFLIES_API_KEY
2. Key has not expired
3. Key has transcript read permissions

Get a new key: https://app.fireflies.ai/integrations/custom
```

### Rate Limited
```
Warning: Rate limited by Fireflies API

Waiting 60 seconds before retry...
```
Script handles this automatically with exponential backoff.

### No Meetings Found
```
No meetings found in the last {days} days.

Check:
- Your Fireflies account has recorded meetings
- The date range is correct (--days or --since)
- Your API key has access to the workspace
```

---

## Configuration Reference

Full configuration in `config/integrations.yaml`:

```yaml
fireflies:
  enabled: true
  type: transcript
  prefer_mcp: false
  api_key_env: FIREFLIES_API_KEY
  api_endpoint: https://api.fireflies.ai/graphql

  sync:
    schedule: "0 */6 * * *"  # Every 6 hours

  filters:
    exclude_titles:
      - standup
      - 1:1
      - daily sync
      - check-in
    min_duration_minutes: 5
    max_age_days: 30

  output:
    directory: _inbox/transcripts/fireflies/
    include_summary: true
    include_action_items: true
    date_folders: false  # Set to true for YYYY/MM organization
```

---

## Integration with /process

After syncing, transcripts are in `_inbox/transcripts/fireflies/` ready for processing:

```
/process

[1/3] fireflies/2026-02-19_team-planning.md
      - Type: transcript (confidence: 0.98)
      - Extracted: 12 entities, 5 relationships
        - People: Alice, Bob, Charlie, Dana
        - Projects: Q1 Planning, Website Redesign
        - Action items: 8
      - Staged for review
```

The `/process` command will:
1. Classify as transcript (already marked in frontmatter)
2. Extract entities using domain-aware extraction
3. Match against existing entities
4. Stage for review
