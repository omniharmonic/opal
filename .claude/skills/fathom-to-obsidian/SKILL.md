---
name: fathom-to-obsidian
description: >
  Pull meeting transcripts and AI summaries from Fathom and save them as
  formatted markdown files in an Obsidian vault. Use this skill whenever the
  user mentions Fathom meetings, transcripts, meeting notes, or wants to sync
  their meeting recordings into Obsidian. Also trigger when the user asks
  about recent meetings, wants to review what was discussed, or says things
  like "pull my latest meetings", "save my transcripts", or "sync Fathom".
---

# Fathom -> Obsidian Transcript Sync

This skill pulls meeting transcripts and AI summaries from the Fathom API
and saves them as clean, well-structured markdown files into the user's
Obsidian vault.

## Prerequisites

Before running, you need two things from the user:

1. **Fathom API key** — generated at Fathom -> User Settings -> API Access.
   Pass it via the `--api-key` flag or set the `FATHOM_API_KEY` env variable.
2. **Obsidian vault path** — transcripts save to:
   `vault/_inbox/transcripts/fathom`

If the API key is missing, ask the user for it before proceeding.

## Invocation

This skill is automatically invoked by `/sync` when `fathom` is configured as a source.

Direct invocation:
```
/sync fathom
/sync fathom --force    # Ignore cursor, resync all
/sync fathom --days 30  # Sync last 30 days
```

---

## EXECUTION INSTRUCTIONS

When syncing from Fathom, execute these steps IN ORDER.

### Step 1: Load API Key

**Action:** Load the Fathom API key.

1. Check `.env.local` in project root for `FATHOM_API_KEY`
2. If not found, check environment variable `FATHOM_API_KEY`
3. Read `.opal/sources.yaml` for any custom configuration

**If not found:**
```
Fathom API key not found.

Set it in .env.local:
  FATHOM_API_KEY=your_key_here

Or generate one at: Fathom -> User Settings -> API Access
```
STOP.

### Step 2: Load Sync Configuration

**Action:** Read configuration from `.opal/sources.yaml`.

```yaml
fathom:
  enabled: true
  default_days: 14
  filters:
    min_duration_minutes: 5
    exclude_titles:
      - impromptu
```

### Step 3: Execute Sync Script

**Action:** Run the Python sync script.

```bash
cd "{project_root}"
source .env.local 2>/dev/null
python3 .claude/skills/fathom-to-obsidian/scripts/fathom_sync.py \
  --api-key "$FATHOM_API_KEY" \
  --output-dir "vault/_inbox/transcripts/fathom" \
  --days {default_days from config, or 14}
```

**Flags:**
- `--days N` — Sync meetings from last N days
- `--since YYYY-MM-DD` — Sync meetings since specific date
- `--force` — Overwrite existing files
- `--list-only` — Dry run, show what would be synced

### Step 4: Report Results

Parse script output and report:
```
Fathom Sync Complete

Meetings synced: {count}
Output: vault/_inbox/transcripts/fathom/

New files:
{for each file:}
  - {filename}

Next: Run /ingest-meetings to process into projects
```

### Step 5: Update Sync State

**Action:** Update `_index/sync-state.json`.

```json
{
  "sources": {
    "fathom": {
      "enabled": true,
      "last_sync": "{current_timestamp}",
      "items_synced": {previous + new_count},
      "errors": {error_count}
    }
  }
}
```

---

## How It Works

The script `scripts/fathom_sync.py` does all the heavy lifting:

1. Calls the Fathom API to list recent meetings
2. For each meeting, fetches the AI summary and full transcript
3. Formats everything as a markdown file with YAML frontmatter
4. Saves each file to the user's chosen subfolder in their vault

The API calls are simple GET requests using only Python's standard library.
No pip installs needed. The user can read the entire script and understand
exactly what's happening with their data.

## Running the Skill

### Pull recent meetings (most common)

```bash
python3 scripts/fathom_sync.py \
  --api-key "$FATHOM_API_KEY" \
  --output-dir "vault/_inbox/transcripts/fathom" \
  --days 7
```

Pulls all meetings from the last 7 days. Adjust `--days` to widen the window,
or use `--since 2026-02-01` for an exact start date.

### List meetings without saving (dry run)

```bash
python3 scripts/fathom_sync.py \
  --api-key "$FATHOM_API_KEY" \
  --list-only \
  --days 30
```

Prints a table of meetings with IDs, titles, and dates — helpful for the
user to preview what will be pulled.

### Pull a specific meeting

```bash
python3 scripts/fathom_sync.py \
  --api-key "$FATHOM_API_KEY" \
  --output-dir "vault/_inbox/transcripts/fathom" \
  --meeting-id "rec_abc123"
```

### Use date-based subfolders

```bash
python3 scripts/fathom_sync.py \
  --api-key "$FATHOM_API_KEY" \
  --output-dir "vault/_inbox/transcripts/fathom" \
  --days 7 \
  --date-folders
```

Creates folders like `Meetings/2026/02/` instead of saving flat.

## Output Format

Each meeting becomes a markdown file named like:
`2026-02-09 - Weekly Team Standup.md`

```markdown
---
title: "Weekly Team Standup"
date: 2026-02-09
time: "10:00 AM"
duration_minutes: 32
attendees:
  - Alice Smith (alice@example.com)
  - Bob Jones (bob@example.com)
source: fathom
recording_id: "rec_abc123"
fathom_url: "https://fathom.video/..."
---

## Summary

[AI-generated summary from Fathom]

## Action Items

- [ ] Alice to follow up on the proposal by Friday
- [ ] Bob to schedule the client call

---

## Transcript

**Alice Smith** (0:00)
Hey everyone, let's get started...

**Bob Jones** (0:45)
Sure, I wanted to give an update on...
```

The YAML frontmatter makes these notes searchable in Obsidian with plugins
like Dataview. Every field comes directly from the Fathom API.

## Edge Cases

- **Duplicates**: The script checks if a file with the same recording_id
  already exists (by scanning frontmatter). Skips unless `--overwrite` is used.
- **Missing summaries**: Notes this in the file; user can re-run later.
- **Bad characters in titles**: Slashes, colons, etc. are replaced with dashes.
- **Rate limits**: Fathom allows 60 calls/min. The script paces itself.

## Security

- The API key is never written to any file or logged.
- Only GET requests — cannot modify anything in Fathom.
- Data goes from Fathom -> local markdown files. Nothing else.

## API Reference

For details on the Fathom endpoints used, see `references/fathom_api.md`.

