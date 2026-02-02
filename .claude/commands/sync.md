# /sync Command

Pull content from configured sources into the inbox.

## Usage

```
/sync                       # Sync all enabled sources
/sync <source>              # Sync specific source
/sync <source1> <source2>   # Sync multiple sources
/sync --status              # Show sync status for all sources
/sync --dry-run             # Preview what would be fetched
/sync --since <date>        # Override time range (ISO date)
/sync --force               # Ignore cursor, refetch all
/sync --retry-failed        # Retry previously failed items
```

## Available Sources

| Source | Type | Description |
|--------|------|-------------|
| `fathom` | Transcript | Video call transcripts from Fathom |
| `otter` | Transcript | Meeting transcripts from Otter.ai |
| `read` | Transcript | Meeting transcripts from Read.ai |
| `telegram` | Links | URLs shared in monitored channels |
| `rss` | Feed | Articles from RSS/Atom feeds |
| `youtube` | Transcript | Video transcripts from YouTube |
| `podcast` | Transcript | Episode transcripts from podcasts |

## Example: Sync All Sources

```
/sync

Syncing Content Sources

[1/4] Fathom
      ├── Checking for new transcripts...
      ├── Last sync: 2026-02-01T10:00:00Z
      ├── Found: 3 new transcripts
      │   ├── team-standup-2026-02-02.md (12 min)
      │   ├── product-review-2026-02-02.md (45 min)
      │   └── customer-call-2026-02-01.md (28 min)
      └── ✅ Synced 3 items → _inbox/transcripts/fathom/

[2/4] Otter
      ├── Checking for new transcripts...
      ├── Last sync: 2026-02-01T10:00:00Z
      └── ✅ No new items

[3/4] Telegram
      ├── Checking monitored channels...
      ├── Channels: #opencivics-links (2 new), #resources (5 new)
      ├── Fetching URL content for 7 links...
      │   ├── ✅ https://example.com/governance-article
      │   ├── ✅ https://research.org/paper.pdf
      │   ├── ✅ https://event.io/conference-2026
      │   ├── ✅ https://toolkit.org/guide
      │   ├── ✅ https://coalition.net/about
      │   ├── ✅ https://grants.gov/opportunity
      │   └── ❌ https://broken.link (404 Not Found)
      └── ✅ Synced 6 items → _inbox/links/telegram/

[4/4] RSS
      ├── Checking 3 feeds...
      ├── Found: 2 new articles
      └── ✅ Synced 2 items → _inbox/links/rss/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
• Sources checked: 4
• Items synced: 11
• Failed: 1 (see _inbox/failed/)
• Total inbox items: 24

Next: Run /process to analyze new content
```

## Example: Sync Status

```
/sync --status

Sync Status

┌─────────────┬─────────┬─────────────────────┬────────┬────────┐
│ Source      │ Enabled │ Last Sync           │ Synced │ Errors │
├─────────────┼─────────┼─────────────────────┼────────┼────────┤
│ fathom      │ ✅      │ 2 hours ago         │ 145    │ 0      │
│ otter       │ ✅      │ 6 hours ago         │ 89     │ 0      │
│ read        │ ❌      │ never               │ 0      │ -      │
│ telegram    │ ✅      │ 30 minutes ago      │ 312    │ 3      │
│ rss         │ ✅      │ 2 hours ago         │ 67     │ 0      │
│ youtube     │ ❌      │ never               │ 0      │ -      │
│ podcast     │ ❌      │ never               │ 0      │ -      │
└─────────────┴─────────┴─────────────────────┴────────┴────────┘

Configured channels (telegram):
• #opencivics-links - 156 items synced
• #resources - 98 items synced
• #activities - 58 items synced

Configured feeds (rss):
• Open Civics Blog - 34 items synced
• Governance Weekly - 33 items synced

Next sync scheduled: telegram in 12 minutes
```

## Example: Sync Specific Source

```
/sync telegram

Syncing: Telegram

Checking monitored channels...
├── #opencivics-links
│   ├── Last message ID: 98765
│   ├── Found 3 new messages with links
│   └── Fetching content...
│
├── #resources
│   ├── Last message ID: 87654
│   ├── Found 1 new message with links
│   └── Fetching content...
│
└── #activities
    ├── Last message ID: 76543
    └── No new messages

Fetched URLs:
├── ✅ https://participatory-budgeting.org/guide
│   └── Saved: _inbox/links/telegram/msg-98766.md
├── ✅ https://events.opencivics.co/summit-2026
│   └── Saved: _inbox/links/telegram/msg-98767.md
├── ✅ https://grants.foundation/civic-tech
│   └── Saved: _inbox/links/telegram/msg-98768.md
└── ✅ https://toolkit.commons.co/facilitation
    └── Saved: _inbox/links/telegram/msg-87655.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
• Channels checked: 3
• New links found: 4
• Successfully fetched: 4
• Failed: 0

Cursor updated: telegram → msg-98768
```

## Example: Dry Run

```
/sync --dry-run

Sync Preview (Dry Run)

Would sync from 4 sources:

[1] Fathom
    ├── Would check transcripts since: 2026-02-01T10:00:00Z
    ├── Estimated new items: 2-5
    └── Destination: _inbox/transcripts/fathom/

[2] Otter
    ├── Would check transcripts since: 2026-02-01T08:00:00Z
    ├── Estimated new items: 0-2
    └── Destination: _inbox/transcripts/otter/

[3] Telegram
    ├── Would check 3 channels
    ├── Estimated new links: 5-10
    ├── Would fetch URL content for each
    └── Destination: _inbox/links/telegram/

[4] RSS
    ├── Would check 3 feeds
    ├── Estimated new articles: 1-3
    └── Destination: _inbox/links/rss/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Estimated total: 8-20 new items
Run without --dry-run to proceed.
```

## Configuration

Sources are configured in `config/integrations.yaml`:

```yaml
sources:
  telegram:
    enabled: true
    bot_token_env: TELEGRAM_BOT_TOKEN
    sync:
      schedule: "*/30 * * * *"    # Every 30 minutes
    channels:
      - id: -1001234567890
        name: opencivics-links
        monitor_type: links
      - id: -1009876543210
        name: resources
        monitor_type: links
    link_handling:
      auto_fetch: true
      fetch_timeout: 30
    filters:
      exclude_domains: [twitter.com, x.com]
```

## State Tracking

Sync state is stored in `_index/sync-state.json`:

```json
{
  "sources": {
    "telegram": {
      "enabled": true,
      "last_sync": "2026-02-02T15:00:00Z",
      "cursor": {
        "per_channel": {
          "opencivics-links": 98768,
          "resources": 87655
        }
      },
      "items_synced": 316
    }
  }
}
```

## Inbox Item Format

Synced items include standardized metadata:

```yaml
---
source: telegram
source_id: msg-98766
channel: opencivics-links
sender: @civic_enthusiast
sent_at: 2026-02-02T14:30:00Z
synced_at: 2026-02-02T15:00:00Z
url: https://participatory-budgeting.org/guide
url_title: "Complete Guide to Participatory Budgeting"
url_domain: participatory-budgeting.org
fingerprint: sha256:abc123...
---

# Complete Guide to Participatory Budgeting

## Telegram Context

Shared by @civic_enthusiast in #opencivics-links:
> "Great resource for anyone implementing PB in their community!"

## Content

[Fetched and converted content...]
```

## Error Handling

Failed items are logged and can be retried:

```
/sync --retry-failed

Retrying 3 failed items...

[1/3] telegram/msg-12345
      ├── Original error: 404 Not Found
      ├── URL: https://example.com/moved
      └── ❌ Still failing (404)

[2/3] fathom/call-xyz789
      ├── Original error: Rate limit exceeded
      ├── Retrying...
      └── ✅ Success → _inbox/transcripts/fathom/

[3/3] rss/article-abc
      ├── Original error: Connection timeout
      ├── Retrying...
      └── ✅ Success → _inbox/links/rss/

Summary: 2 recovered, 1 still failing
```

## Relationship to Other Commands

```
/sync      → Pulls content from sources → _inbox/
/ingest    → Manually adds items to → _inbox/
/process   → Analyzes _inbox/ → _staging/
/review    → Approves _staging/ items
```

Use `/sync` for automated source pulling.
Use `/ingest` for manual one-off additions.

## Related Commands

- `/process` - Process inbox items through pipeline
- `/ingest` - Manual content ingestion
- `/status inbox` - View inbox contents
- `/watch sync` - Continuous sync monitoring
