# /ingest Command

Add content to the inbox for processing.

## Usage

```
/ingest <source>           # Ingest from configured source
/ingest file <path>        # Ingest specific file
/ingest url <url>          # Ingest from URL
/ingest transcript <source># Pull transcripts from service
/ingest telegram           # Pull links from Telegram
/ingest clipboard          # Ingest from clipboard
```

## Sources

### File Ingestion

```
/ingest file ~/Documents/meeting-notes.md
/ingest file ./paper.pdf
/ingest file /path/to/transcript.txt
```

Copies file to appropriate inbox subdirectory based on type detection.

### URL Ingestion

```
/ingest url https://example.com/article
/ingest url https://arxiv.org/pdf/2024.12345.pdf
```

Fetches content, converts to markdown, stores in `_inbox/links/`.

### Transcript Sources

```
/ingest transcript otter     # Pull from Otter.ai
/ingest transcript fathom    # Pull from Fathom
/ingest transcript readai    # Pull from Read.ai
/ingest transcript meetily   # Pull from local Meetily DB
/ingest transcript --all     # Pull from all configured sources
```

Uses MCP servers or API fallback to fetch recent transcripts.

### Telegram Links

```
/ingest telegram             # Pull new links from configured channels
/ingest telegram --since 7d  # Links from last 7 days
/ingest telegram --channel "Consortium Chat"  # Specific channel
```

Fetches links shared in Telegram channels via bot integration.

### Clipboard

```
/ingest clipboard            # Ingest clipboard contents
```

Takes current clipboard text, creates file in inbox.

## Example Output

```
📥 Ingesting Content
━━━━━━━━━━━━━━━━━━━

Source: Otter.ai (last 7 days)

Found 4 new transcripts:

[1] Food Council Meeting - Jan 28, 2026
    ├── Duration: 47 minutes
    ├── Speakers: 4 identified
    └── ✅ Saved to: _inbox/transcripts/food-council-2026-01-28.md

[2] Bioregional Planning Session - Jan 25, 2026
    ├── Duration: 1h 12m
    ├── Speakers: 6 identified
    └── ✅ Saved to: _inbox/transcripts/bioregional-planning-2026-01-25.md

[3] Weekly Standup - Jan 24, 2026
    ├── Duration: 15 minutes
    ├── Speakers: 3 identified
    └── ⏭️ Skipped: matches exclusion filter "standup"

[4] Community Garden Workshop - Jan 22, 2026
    ├── Duration: 2h 5m
    ├── Speakers: 8 identified
    └── ✅ Saved to: _inbox/transcripts/garden-workshop-2026-01-22.md

━━━━━━━━━━━━━━━━━━━
Ingested: 3 transcripts
Skipped: 1 (filter match)

Next: Run /process to extract entities
```

## Filtering

Configure ingestion filters in `config/integrations.yaml`:

```yaml
otter:
  enabled: true
  filters:
    exclude_titles:
      - "standup"
      - "1:1"
      - "daily sync"
    min_duration_minutes: 10
    max_age_days: 30
```

## Inbox Organization

Ingested content is automatically sorted:

```
_inbox/
├── transcripts/           # From Otter, Fathom, Read.ai, Meetily
│   ├── food-council-2026-01-28.md
│   └── bioregional-planning-2026-01-25.md
├── links/                 # From Telegram, manual URLs
│   ├── telegram-2026-01-28-001.md
│   └── arxiv-paper-12345.md
├── documents/             # PDFs, Word docs, etc.
│   └── handbook.pdf
└── clippings/             # Quick captures, clipboard
    └── clipboard-2026-01-28-1430.md
```

## Metadata Preservation

Each ingested file includes source metadata:

```yaml
---
source: otter
source_id: abc123
ingested: 2026-01-28T14:30:00Z
original_title: "Food Council Meeting"
duration: 47:23
speakers:
  - Sarah Chen
  - Marcus Johnson
  - Elena Rodriguez
  - Unknown Speaker 1
---

[transcript content...]
```

## Options Reference

| Option | Description |
|--------|-------------|
| `--since <duration>` | Only content newer than duration (e.g., 7d, 24h) |
| `--limit <n>` | Ingest at most n items |
| `--dry-run` | Show what would be ingested |
| `--force` | Ingest even if already exists |
| `--project <name>` | Tag with project for routing |
