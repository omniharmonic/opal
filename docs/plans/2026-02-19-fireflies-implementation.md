# Fireflies.ai Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add Fireflies.ai as a meeting transcript source that syncs via GraphQL API into OPAL's inbox pipeline.

**Architecture:** Python script (`fireflies_sync.py`) handles GraphQL API calls with pagination and deduplication. SKILL.md provides execution instructions for Claude. Command file enables `/sync fireflies` invocation. Config block in `integrations.yaml` defines user settings.

**Tech Stack:** Python 3 stdlib only (urllib, json, argparse), GraphQL POST requests, YAML config

---

## Task 1: Create Python Sync Script

**Files:**
- Create: `.claude/skills/sync-fireflies/scripts/fireflies_sync.py`

**Step 1: Create directory structure**

Run: `mkdir -p ".claude/skills/sync-fireflies/scripts"`
Expected: Directory created (no output)

**Step 2: Write the sync script**

Create `.claude/skills/sync-fireflies/scripts/fireflies_sync.py` with this content:

```python
#!/usr/bin/env python3
"""
Fireflies.ai -> OPAL Sync
=========================
Pulls meeting transcripts and AI summaries from the Fireflies.ai GraphQL API
and saves them as formatted markdown files.

Uses only Python standard library - no pip installs needed.

Usage:
    # Pull last 7 days of meetings
    python3 fireflies_sync.py --api-key YOUR_KEY --output-dir _inbox/transcripts/fireflies --days 7

    # List meetings without saving (dry run)
    python3 fireflies_sync.py --api-key YOUR_KEY --list-only --days 30

    # Pull a specific meeting
    python3 fireflies_sync.py --api-key YOUR_KEY --output-dir DIR --meeting-id abc123

Security:
    - API key is only sent to api.fireflies.ai over HTTPS
    - Only query operations - nothing in your Fireflies account is modified
    - Data goes straight from Fireflies to local files, nowhere else
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ---------------------------------------------------------------------------
# Fireflies GraphQL API client
# ---------------------------------------------------------------------------

GRAPHQL_URL = "https://api.fireflies.ai/graphql"


def graphql_query(query: str, variables: dict, api_key: str) -> dict:
    """
    Execute a GraphQL query against the Fireflies API.

    Args:
        query: GraphQL query string
        variables: Query variables dict
        api_key: Fireflies API key

    Returns:
        Parsed JSON response data
    """
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")

    req = Request(GRAPHQL_URL, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")

    try:
        with urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if "errors" in result:
                for err in result["errors"]:
                    print(f"GraphQL Error: {err.get('message', err)}", file=sys.stderr)
                if not result.get("data"):
                    sys.exit(1)
            return result.get("data", {})
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Error: Fireflies API returned {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Error: Could not reach Fireflies API: {e.reason}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# GraphQL Queries
# ---------------------------------------------------------------------------

LIST_TRANSCRIPTS_QUERY = """
query Transcripts($limit: Int, $skip: Int, $fromDate: DateTime) {
  transcripts(limit: $limit, skip: $skip, fromDate: $fromDate) {
    id
    title
    date
    duration
    speakers {
      id
      name
    }
    meeting_attendance {
      name
    }
  }
}
"""

GET_TRANSCRIPT_QUERY = """
query Transcript($id: String!) {
  transcript(id: $id) {
    id
    title
    date
    duration
    speakers {
      id
      name
    }
    sentences {
      speaker_name
      text
      start_time
      end_time
    }
    summary {
      keywords
      action_items
      outline
      overview
    }
    meeting_attendance {
      name
      join_time
      leave_time
    }
    host_email
    organizer_email
    transcript_url
    audio_url
  }
}
"""


def list_meetings(api_key: str, from_date: str = None, limit: int = 50) -> list:
    """
    Fetch all meetings, handling pagination automatically.

    Args:
        api_key: Fireflies API key
        from_date: ISO timestamp - only return meetings after this date
        limit: Max results per page (API max is 50)

    Returns:
        List of meeting dicts
    """
    all_meetings = []
    skip = 0

    while True:
        variables = {"limit": min(limit, 50), "skip": skip}
        if from_date:
            variables["fromDate"] = from_date

        data = graphql_query(LIST_TRANSCRIPTS_QUERY, variables, api_key)
        meetings = data.get("transcripts", [])

        if not meetings:
            break

        all_meetings.extend(meetings)

        # If we got fewer than requested, we've reached the end
        if len(meetings) < variables["limit"]:
            break

        skip += len(meetings)

        # Respect rate limits
        time.sleep(0.5)

    return all_meetings


def get_transcript(api_key: str, meeting_id: str) -> dict:
    """
    Fetch full transcript details for a single meeting.

    Args:
        api_key: Fireflies API key
        meeting_id: The meeting ID

    Returns:
        Full transcript dict with sentences, summary, etc.
    """
    data = graphql_query(GET_TRANSCRIPT_QUERY, {"id": meeting_id}, api_key)
    return data.get("transcript", {})


# ---------------------------------------------------------------------------
# Markdown formatting
# ---------------------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """Remove characters that are unsafe for filenames."""
    cleaned = re.sub(r'[\\/:*?"<>|]', "-", name)
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip(" -.")[:50]


def format_timestamp(seconds) -> str:
    """Convert seconds to human-readable timestamp like 1:23:45 or 0:45."""
    if seconds is None:
        return ""
    try:
        seconds = int(float(seconds))
    except (ValueError, TypeError):
        return str(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def format_duration(seconds) -> str:
    """Format duration as Xh Ym or just Ym."""
    if not seconds:
        return "Unknown"
    try:
        minutes = int(float(seconds)) // 60
    except (ValueError, TypeError):
        return "Unknown"

    if minutes >= 60:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m"
    return f"{minutes}m"


def parse_meeting_datetime(meeting: dict) -> datetime:
    """Extract datetime from meeting's date field."""
    date_str = meeting.get("date")
    if date_str:
        try:
            if date_str.endswith("Z"):
                date_str = date_str[:-1] + "+00:00"
            return datetime.fromisoformat(date_str)
        except ValueError:
            pass
    return datetime.now(timezone.utc)


def format_meeting_markdown(meeting: dict, transcript_data: dict) -> str:
    """
    Build the full markdown content for a meeting note.

    Structure:
        - YAML frontmatter
        - Summary section
        - Action Items
        - Transcript (speaker-labeled, timestamped)
    """
    dt = parse_meeting_datetime(meeting)
    title = meeting.get("title") or "Untitled Meeting"
    meeting_id = meeting.get("id", "")
    duration = meeting.get("duration")

    # Get attendees
    attendees = []
    for att in transcript_data.get("meeting_attendance") or []:
        name = att.get("name")
        if name:
            attendees.append(name)

    # Get host/organizer
    host = transcript_data.get("host_email") or transcript_data.get("organizer_email") or ""

    # URLs
    transcript_url = transcript_data.get("transcript_url") or ""
    audio_url = transcript_data.get("audio_url") or ""

    # --- Frontmatter ---
    fm_lines = [
        "---",
        "source: fireflies",
        f'source_id: "{meeting_id}"',
        f'title: "{title}"',
        f"date: {dt.strftime('%Y-%m-%d')}",
        f"synced_at: {datetime.now(timezone.utc).isoformat()}",
    ]

    if duration:
        try:
            fm_lines.append(f"duration_minutes: {int(float(duration)) // 60}")
        except (ValueError, TypeError):
            pass

    fm_lines.append("type: transcript")

    if host:
        fm_lines.append(f'host: "{host}"')

    if attendees:
        fm_lines.append("attendees:")
        for att in attendees:
            fm_lines.append(f'  - "{att}"')

    if transcript_url:
        fm_lines.append(f'fireflies_url: "{transcript_url}"')
    if audio_url:
        fm_lines.append(f'audio_url: "{audio_url}"')

    fm_lines.append("---")

    sections = ["\n".join(fm_lines)]

    # --- Header ---
    header_lines = [f"\n# {title}\n"]
    header_lines.append(f"**Source:** Fireflies.ai")
    header_lines.append(f"**Date:** {dt.strftime('%B %d, %Y at %I:%M %p')}")
    header_lines.append(f"**Duration:** {format_duration(duration)}")
    if host:
        header_lines.append(f"**Host:** {host}")
    if attendees:
        header_lines.append(f"**Attendees:** {', '.join(attendees)}")

    sections.append("\n".join(header_lines))

    # --- Summary ---
    summary = transcript_data.get("summary") or {}

    sections.append("\n---\n\n## Summary")

    overview = summary.get("overview")
    if overview:
        sections.append(f"\n{overview}")
    else:
        sections.append("\n*Summary not available.*")

    # Outline
    outline = summary.get("outline")
    if outline:
        sections.append(f"\n### Outline\n\n{outline}")

    # Keywords
    keywords = summary.get("keywords")
    if keywords:
        if isinstance(keywords, list):
            keywords = ", ".join(keywords)
        sections.append(f"\n### Keywords\n\n{keywords}")

    # --- Action Items ---
    action_items = summary.get("action_items") or []
    if action_items:
        items_md = "\n".join(f"- [ ] {item}" for item in action_items)
        sections.append(f"\n## Action Items\n\n{items_md}")

    # --- Transcript ---
    sections.append("\n---\n\n## Transcript")

    sentences = transcript_data.get("sentences") or []
    if sentences:
        transcript_lines = []
        for sent in sentences:
            speaker = sent.get("speaker_name") or "Unknown"
            text = (sent.get("text") or "").strip()
            start_time = sent.get("start_time")
            ts_str = format_timestamp(start_time)

            if ts_str:
                transcript_lines.append(f"\n**{speaker}** ({ts_str})")
            else:
                transcript_lines.append(f"\n**{speaker}**")
            transcript_lines.append(text)

        sections.append("\n".join(transcript_lines))
    else:
        sections.append("\n*Transcript not available.*")

    return "\n".join(sections) + "\n"


# ---------------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------------

def existing_meeting_ids(output_dir: str) -> set:
    """
    Scan existing markdown files for source_id in frontmatter.
    Returns set of meeting IDs already synced.
    """
    ids = set()
    if not os.path.isdir(output_dir):
        return ids

    for root, _, files in os.walk(output_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    in_frontmatter = False
                    for line in f:
                        line = line.strip()
                        if line == "---":
                            if not in_frontmatter:
                                in_frontmatter = True
                                continue
                            else:
                                break
                        if in_frontmatter and line.startswith("source_id:"):
                            mid = line.split(":", 1)[1].strip().strip('"').strip("'")
                            if mid:
                                ids.add(mid)
                            break
            except (IOError, UnicodeDecodeError):
                continue

    return ids


def save_meeting(markdown: str, meeting: dict, output_dir: str, date_folders: bool = False) -> str:
    """Save meeting markdown to output directory."""
    dt = parse_meeting_datetime(meeting)
    title = meeting.get("title") or "Untitled Meeting"
    safe_title = sanitize_filename(title)
    filename = f"{dt.strftime('%Y-%m-%d')}_{safe_title}.md"

    if date_folders:
        folder = os.path.join(output_dir, dt.strftime("%Y"), dt.strftime("%m"))
    else:
        folder = output_dir

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)

    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pull Fireflies.ai meeting transcripts as markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Pull last 7 days
  python3 fireflies_sync.py --api-key KEY --output-dir _inbox/transcripts/fireflies --days 7

  # Dry run - list meetings only
  python3 fireflies_sync.py --api-key KEY --list-only --days 30

  # Pull one specific meeting
  python3 fireflies_sync.py --api-key KEY --output-dir DIR --meeting-id abc123
        """,
    )

    parser.add_argument(
        "--api-key",
        default=os.environ.get("FIREFLIES_API_KEY"),
        help="Fireflies API key (or set FIREFLIES_API_KEY env variable)",
    )
    parser.add_argument(
        "--output-dir",
        help="Path to folder where markdown files will be saved",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Pull meetings from the last N days (default: 7)",
    )
    parser.add_argument(
        "--since",
        help="Pull meetings after this date (ISO format, e.g., 2026-02-01)",
    )
    parser.add_argument(
        "--meeting-id",
        help="Pull a specific meeting by its ID",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Just list meetings - don't save anything",
    )
    parser.add_argument(
        "--date-folders",
        action="store_true",
        help="Organize files into YYYY/MM subfolders",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files for the same meeting",
    )

    args = parser.parse_args()

    # --- Validate inputs ---
    if not args.api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Use --api-key YOUR_KEY or set the FIREFLIES_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    if not args.list_only and not args.output_dir:
        print("Error: --output-dir is required when saving files.", file=sys.stderr)
        sys.exit(1)

    # --- Determine date filter ---
    if args.since:
        from_date = args.since
        if "T" not in from_date:
            from_date += "T00:00:00Z"
    else:
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
        from_date = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")

    # --- Fetch meetings ---
    print(f"Fetching meetings since {from_date}...")
    meetings = list_meetings(args.api_key, from_date=from_date)

    if not meetings:
        print("No meetings found in that time range.")
        return

    print(f"Found {len(meetings)} meeting(s).\n")

    # --- If specific meeting requested, filter ---
    if args.meeting_id:
        meetings = [m for m in meetings if m.get("id") == args.meeting_id]
        if not meetings:
            print(f"No meeting found with ID: {args.meeting_id}")
            return

    # --- List-only mode ---
    if args.list_only:
        print(f"{'Date':<14} {'Title':<50} {'ID'}")
        print("-" * 90)
        for m in meetings:
            dt = parse_meeting_datetime(m)
            title = (m.get("title") or "Untitled")[:48]
            mid = m.get("id", "")[:20]
            print(f"{dt.strftime('%Y-%m-%d'):<14} {title:<50} {mid}")
        return

    # --- Check for duplicates ---
    existing = set()
    if not args.overwrite:
        existing = existing_meeting_ids(args.output_dir)

    # --- Process each meeting ---
    saved = 0
    skipped = 0

    for i, meeting in enumerate(meetings):
        meeting_id = meeting.get("id", "")
        title = meeting.get("title") or "Untitled"

        # Skip duplicates
        if meeting_id in existing and not args.overwrite:
            print(f"  Skipping (already exists): {title}")
            skipped += 1
            continue

        print(f"  [{i + 1}/{len(meetings)}] Processing: {title}...")

        # Fetch full transcript
        transcript_data = get_transcript(args.api_key, meeting_id)
        time.sleep(0.5)  # Pace API calls

        if not transcript_data:
            print(f"    Warning: Could not fetch transcript for {title}")
            continue

        # Format and save
        markdown = format_meeting_markdown(meeting, transcript_data)
        filepath = save_meeting(markdown, meeting, args.output_dir, args.date_folders)

        print(f"    Saved: {filepath}")
        saved += 1

    print(f"\nDone! Saved {saved} meeting(s), skipped {skipped} duplicate(s).")


if __name__ == "__main__":
    main()
```

**Step 3: Make script executable**

Run: `chmod +x ".claude/skills/sync-fireflies/scripts/fireflies_sync.py"`
Expected: No output

**Step 4: Commit**

```bash
git add .claude/skills/sync-fireflies/scripts/fireflies_sync.py
git commit -m "feat(fireflies): add Python sync script for Fireflies.ai API"
```

---

## Task 2: Create SKILL.md

**Files:**
- Create: `.claude/skills/sync-fireflies/SKILL.md`

**Step 1: Write the skill file**

Create `.claude/skills/sync-fireflies/SKILL.md` with this content:

```markdown
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
```

**Step 2: Commit**

```bash
git add .claude/skills/sync-fireflies/SKILL.md
git commit -m "feat(fireflies): add SKILL.md execution instructions"
```

---

## Task 3: Create Slash Command

**Files:**
- Create: `.claude/commands/sync-fireflies.md`

**Step 1: Write the command file**

Create `.claude/commands/sync-fireflies.md` with this content:

```markdown
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
```

**Step 2: Commit**

```bash
git add .claude/commands/sync-fireflies.md
git commit -m "feat(fireflies): add /sync-fireflies slash command"
```

---

## Task 4: Update integrations.yaml

**Files:**
- Modify: `config/integrations.yaml`

**Step 1: Add fireflies config block**

Add the following block after the `meetily:` section (around line 168) in `config/integrations.yaml`:

```yaml
  fireflies:
    enabled: false
    type: transcript
    prefer_mcp: false
    api_key_env: FIREFLIES_API_KEY
    api_endpoint: https://api.fireflies.ai/graphql

    sync:
      schedule: "0 */6 * * *"  # Every 6 hours

    filters:
      exclude_titles:
        - "standup"
        - "1:1"
        - "daily sync"
        - "check-in"
      min_duration_minutes: 5
      max_age_days: 30

    output:
      directory: _inbox/transcripts/fireflies/
      include_summary: true
      include_action_items: true
      date_folders: false
```

**Step 2: Commit**

```bash
git add config/integrations.yaml
git commit -m "feat(fireflies): add config block in integrations.yaml"
```

---

## Task 5: Update sync.md Source Mapping

**Files:**
- Modify: `.claude/commands/sync.md`

**Step 1: Add fireflies to source mapping table**

In `.claude/commands/sync.md`, find the "Source Type -> Skill Mapping" table (around line 68) and add:

```markdown
| `fireflies` | `.claude/skills/sync-fireflies/SKILL.md` | Pull from Fireflies.ai GraphQL API |
```

**Step 2: Add fireflies dispatch case**

After the `**FOR fathom:**` section (around line 108), add:

```markdown
**FOR fireflies:**
1. Read `.claude/skills/sync-fireflies/SKILL.md`
2. Load API key from `.env.local` or environment variable `FIREFLIES_API_KEY`
3. Execute the sync script:
   ```bash
   source .env.local 2>/dev/null
   python3 .claude/skills/sync-fireflies/scripts/fireflies_sync.py \
     --api-key "$FIREFLIES_API_KEY" \
     --output-dir "_inbox/transcripts/fireflies" \
     --days 14
   ```
4. Report synced meetings count and any errors
5. Write to `_inbox/transcripts/fireflies/`
```

**Step 3: Commit**

```bash
git add .claude/commands/sync.md
git commit -m "feat(fireflies): add to /sync command dispatch"
```

---

## Task 6: Create Output Directory

**Files:**
- Create: `_inbox/transcripts/fireflies/.gitkeep`

**Step 1: Create directory with gitkeep**

```bash
mkdir -p _inbox/transcripts/fireflies
touch _inbox/transcripts/fireflies/.gitkeep
```

**Step 2: Commit**

```bash
git add _inbox/transcripts/fireflies/.gitkeep
git commit -m "chore: add fireflies transcript inbox directory"
```

---

## Task 7: Final Integration Test

**Step 1: Verify file structure**

Run:
```bash
ls -la .claude/skills/sync-fireflies/
ls -la .claude/skills/sync-fireflies/scripts/
ls -la .claude/commands/sync-fireflies.md
```

Expected: All files exist

**Step 2: Verify script syntax**

Run:
```bash
python3 -m py_compile .claude/skills/sync-fireflies/scripts/fireflies_sync.py && echo "Syntax OK"
```

Expected: "Syntax OK"

**Step 3: Test --help**

Run:
```bash
python3 .claude/skills/sync-fireflies/scripts/fireflies_sync.py --help
```

Expected: Help text with all arguments documented

**Step 4: Test list-only (requires API key)**

If user has FIREFLIES_API_KEY available:
```bash
source .env.local 2>/dev/null
python3 .claude/skills/sync-fireflies/scripts/fireflies_sync.py --list-only --days 7
```

Expected: Either list of meetings OR "No meetings found" OR "API key not provided" error

---

## Summary

After completing all tasks, the Fireflies.ai integration includes:

| Component | Path | Purpose |
|-----------|------|---------|
| Python Script | `.claude/skills/sync-fireflies/scripts/fireflies_sync.py` | GraphQL API client |
| Skill File | `.claude/skills/sync-fireflies/SKILL.md` | Execution instructions |
| Command | `.claude/commands/sync-fireflies.md` | `/sync fireflies` entry |
| Config | `config/integrations.yaml` | User configuration |
| Dispatch | `.claude/commands/sync.md` | Auto-dispatch from `/sync` |
| Output Dir | `_inbox/transcripts/fireflies/` | Synced transcripts |
