# Fireflies.ai Integration Design

**Date:** 2026-02-19
**Status:** Approved
**Author:** Claude (with user collaboration)

## Overview

Add Fireflies.ai as a transcript source for OPAL, enabling users to sync meeting transcripts from Fireflies.ai into the OPAL processing pipeline alongside existing Fathom and Meetily integrations.

## Goals

1. Pull meeting transcripts from Fireflies.ai GraphQL API
2. Match existing patterns (Fathom Python script, Meetily skill structure)
3. Integrate with `/sync` command for automatic source discovery
4. Output markdown files compatible with OPAL's `/process` pipeline

## Non-Goals

- MCP server implementation (direct API only for v1)
- Real-time webhook support
- Fireflies.ai write operations

## Architecture

### Approach

**Python Script Pattern** - Standalone Python script using stdlib only, mirroring `fathom_sync.py`.

This approach was chosen because:
- Matches existing Fathom integration exactly
- No external dependencies required
- Users can run standalone outside Claude Code
- Easy to test and debug

### File Structure

```
.claude/
├── skills/
│   └── sync-fireflies/
│       ├── SKILL.md                    # Execution instructions
│       └── scripts/
│           └── fireflies_sync.py       # GraphQL API client
├── commands/
│   └── sync-fireflies.md               # Slash command entry point

config/
└── integrations.yaml                   # Add fireflies config block (update)

.claude/commands/sync.md                # Update source mapping table
```

## API Design

### Authentication

- **Endpoint:** `https://api.fireflies.ai/graphql`
- **Method:** POST with GraphQL body
- **Auth:** Bearer token via `Authorization` header
- **API Key Env:** `FIREFLIES_API_KEY`

### GraphQL Queries

#### List Meetings (with pagination)

```graphql
query Transcripts($limit: Int, $skip: Int, $fromDate: DateTime) {
  transcripts(limit: $limit, skip: $skip, fromDate: $fromDate) {
    id
    title
    date
    duration
    speakers { id name }
    meeting_attendance { name }
  }
}
```

#### Get Single Transcript

```graphql
query Transcript($id: String!) {
  transcript(id: $id) {
    id
    title
    date
    duration
    speakers { id name }
    sentences { speaker_name text start_time end_time }
    summary { keywords action_items outline overview }
    meeting_attendance { name join_time leave_time }
    host_email
    organizer_email
    transcript_url
    audio_url
  }
}
```

### CLI Interface

```bash
# Pull last 7 days
python3 fireflies_sync.py --api-key KEY --output-dir _inbox/transcripts/fireflies --days 7

# List only (dry run)
python3 fireflies_sync.py --api-key KEY --list-only --days 30

# Pull specific meeting
python3 fireflies_sync.py --api-key KEY --output-dir DIR --meeting-id abc123

# With date folders
python3 fireflies_sync.py --api-key KEY --output-dir DIR --days 30 --date-folders

# Force overwrite existing
python3 fireflies_sync.py --api-key KEY --output-dir DIR --days 7 --overwrite
```

## Output Format

### Filename

`{date}_{slug}.md` (e.g., `2026-02-19_team-planning-session.md`)

### Markdown Structure

```markdown
---
source: fireflies
source_id: "{meeting_id}"
title: "{title}"
date: {iso_date}
synced_at: {current_timestamp}
duration_minutes: {duration}
type: transcript
host: "{host_email}"
attendees:
  - Name 1
  - Name 2
fireflies_url: "{transcript_url}"
audio_url: "{audio_url}"
---

# {title}

**Source:** Fireflies.ai
**Date:** {formatted_date}
**Duration:** {duration_formatted}
**Host:** {host_email}
**Attendees:** {comma_separated_names}

---

## Summary

{summary.overview}

### Outline

{summary.outline}

### Keywords

{summary.keywords as comma-separated list}

## Action Items

{for each item in summary.action_items:}
- [ ] {item}

---

## Transcript

{for each sentence:}
**{speaker_name}** ({timestamp})
{text}

```

## Configuration

### integrations.yaml Addition

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
    min_duration_minutes: 5
    max_age_days: 30

  output:
    directory: _inbox/transcripts/fireflies/
    include_summary: true
    include_action_items: true
```

### sync.md Source Mapping Update

Add to the source type -> skill mapping table:

| `fireflies` | `.claude/skills/sync-fireflies/SKILL.md` | Pull from Fireflies.ai GraphQL API |

## Error Handling

### API Errors

| Error | Handling |
|-------|----------|
| 401 Unauthorized | Print "Invalid API key", exit 1 |
| 403 Forbidden | Print "Access denied - check API permissions", exit 1 |
| 429 Rate Limited | Wait and retry with exponential backoff |
| Network Error | Print error, exit 1 |
| GraphQL Error | Parse error message, print, continue to next meeting |

### Data Errors

| Issue | Handling |
|-------|----------|
| Missing transcript | Skip meeting, log warning |
| Missing summary | Output with "Summary not available" placeholder |
| Invalid date | Use current date as fallback |

## Deduplication

- Track synced meeting IDs by scanning existing files for `source_id` in frontmatter
- Skip meetings already synced (unless `--overwrite` flag)
- Handle case where same meeting exists in multiple output locations (date folders vs flat)

## Testing Strategy

1. **Unit Tests:** Mock GraphQL responses, test parsing logic
2. **Integration Tests:** Test with real API key (optional, requires user setup)
3. **Manual Testing:** Run with `--list-only` first, then sync specific meeting

## Implementation Plan

1. Create `fireflies_sync.py` script (mirrors fathom_sync.py structure)
2. Create `SKILL.md` with execution instructions
3. Create `sync-fireflies.md` command
4. Update `config/integrations.yaml` with fireflies block
5. Update `.claude/commands/sync.md` source mapping

## References

- [Fireflies.ai API Documentation](https://docs.fireflies.ai/)
- [Transcripts Query Reference](https://docs.fireflies.ai/graphql-api/query/transcripts)
- Existing integrations: `fathom_sync.py`, `sync-meetily/SKILL.md`
