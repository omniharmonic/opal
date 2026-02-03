# OPAL Sources - Intelligent Content Acquisition

OPAL can intelligently gather content from a diverse array of sources. This document covers all supported source types, configuration, and how to add custom sources.

## Philosophy

**Pull, don't push.** OPAL proactively pulls content from your subscribed sources rather than waiting for you to manually add it. Configure your sources once, then let `/sync` do the work.

**Intelligent routing.** OPAL doesn't just dump content into your inbox—it classifies, deduplicates, and routes content based on your schema.

**Agentic fetching.** For URLs and feeds, OPAL acts as an intelligent agent: fetching content, extracting readable text, handling pagination, and even following relevant links.

---

## Source Categories

### 1. Transcript Sources
Meeting recordings that need transcription or have transcripts available.

| Source | Auth | How It Works |
|--------|------|--------------|
| **Meetily** | None (local) | Reads directly from local SQLite database |
| **Fathom** | API Key | Pulls transcripts via API |
| **Otter.ai** | API Key | Pulls transcripts via API |
| **Read.ai** | API Key | Pulls transcripts via API |
| **Fireflies** | API Key | Pulls transcripts via API |

### 2. Communication Sources
Messages and links from chat platforms.

| Source | Auth | How It Works |
|--------|------|--------------|
| **Telegram** | Bot Token | Monitors channels for links, fetches content |
| **Discord** | Bot Token | Monitors channels for links |
| **Slack** | App Token | Monitors channels via Slack API |

### 3. Feed Sources
RSS, Atom, and structured feeds.

| Source | Auth | How It Works |
|--------|------|--------------|
| **RSS/Atom** | None | Polls feeds on schedule, fetches full content |
| **Substack** | None | RSS feed parsing with newsletter support |
| **Medium** | None | RSS feed with full content extraction |

### 4. Web Sources
URLs and web content that need scraping.

| Source | Auth | How It Works |
|--------|------|--------------|
| **URL List** | None | Scrapes list of URLs on schedule |
| **Sitemap** | None | Monitors sitemaps for new pages |
| **Web Watch** | None | Monitors pages for changes |

### 5. Media Sources
Video and audio that need transcription.

| Source | Auth | How It Works |
|--------|------|--------------|
| **YouTube** | API Key | Pulls captions or transcribes via Whisper |
| **Podcast** | None | Fetches episodes, transcribes via Whisper |
| **Vimeo** | API Key | Pulls transcripts if available |

### 6. Document Sources
Files and documents from cloud services.

| Source | Auth | How It Works |
|--------|------|--------------|
| **Google Drive** | OAuth | Monitors folders for new docs |
| **Dropbox** | OAuth | Monitors folders for files |
| **Notion** | API Key | Exports selected databases |
| **Filesystem** | None | Watches local directories |

### 7. API Sources
Custom data from any API.

| Source | Auth | Varies | How It Works |
|--------|------|--------|--------------|
| **Custom API** | Configurable | Polls endpoints, transforms responses |
| **Webhook** | None | Receives POST requests |
| **GraphQL** | Configurable | Executes queries on schedule |

---

## Configuration

### Basic Source Configuration

Sources are configured in `.opal/sources.yaml` (user-specific) or `config/integrations.yaml` (system defaults).

```yaml
# .opal/sources.yaml
sources:
  # Enable with minimal config
  meetily:
    enabled: true

  # Enable with filters
  telegram:
    enabled: true
    channels:
      - name: my-links-channel
        id: -1001234567890

  # Enable with full config
  rss:
    enabled: true
    feeds:
      - url: https://blog.example.com/feed
        name: Example Blog
        tags: [technology, innovation]
```

### Source Structure

Every source has these common fields:

```yaml
source_name:
  # Required
  enabled: true/false
  type: transcript | links | feed | document | api

  # Scheduling
  sync:
    schedule: manual | "cron expression" | "*/30 * * * *"

  # Filtering
  filters:
    max_age_days: 30
    exclude_titles: []
    include_only: []

  # Output
  output:
    directory: _inbox/source_name/
    filename_format: "{date}_{slug}.md"

  # Classification hints
  routing:
    prefer_type: note           # Default resource type
    tags: [auto-imported]       # Auto-applied tags
```

---

## Detailed Source Configuration

### Meetily (Local Transcription)

Meetily stores transcripts in a local SQLite database. OPAL reads directly from it—no API needed.

```yaml
meetily:
  enabled: true

  database:
    path: auto  # Auto-detect, or specify path
    # Standard locations:
    # macOS: ~/Library/Application Support/com.meetily.ai/meeting_minutes.sqlite
    # Linux: ~/.local/share/com.meetily.ai/meeting_minutes.sqlite

  sync:
    schedule: manual
    track_synced: true

  filters:
    min_duration_minutes: 5
    exclude_titles:
      - standup
      - 1:1
      - daily sync

  output:
    directory: _inbox/meetings/
    include_summary: true
    include_action_items: true
```

### Telegram

Monitor channels for shared links and fetch their content.

```yaml
telegram:
  enabled: true
  bot_token_env: TELEGRAM_BOT_TOKEN

  sync:
    schedule: "*/30 * * * *"  # Every 30 minutes

  channels:
    - id: -1001234567890
      name: research-links
      monitor_type: links

    - id: -1009876543210
      name: news-feed
      monitor_type: links
      tags: [news]

  link_handling:
    auto_fetch: true
    fetch_timeout: 30
    convert_to_markdown: true
    extract_metadata: true

  filters:
    exclude_domains:
      - twitter.com
      - x.com
```

### RSS Feeds

Monitor multiple RSS/Atom feeds.

```yaml
rss:
  enabled: true

  sync:
    schedule: "0 */2 * * *"  # Every 2 hours

  feeds:
    - url: https://news.example.com/feed
      name: Example News
      category: news

    - url: https://blog.example.com/rss
      name: Example Blog
      category: articles
      tags: [technology]

    - url: https://research.org/atom.xml
      name: Research Papers
      category: research
      routing:
        prefer_type: paper

  filters:
    max_age_days: 14

  output:
    directory: _inbox/feeds/
    fetch_full_content: true
    extract_images: false
```

### URL Lists (Web Scraping)

Monitor specific URLs for content.

```yaml
urls:
  enabled: true
  type: scrape

  sync:
    schedule: "0 6 * * *"  # Daily at 6am

  # Static list of URLs to check
  watch_urls:
    - url: https://grants.gov/recent
      name: Grants.gov Recent
      selector: ".grant-listing"  # CSS selector for content

    - url: https://events.example.com
      name: Example Events
      follow_links: true  # Follow links on page
      link_selector: ".event-link"
      max_depth: 1

  # Or reference a file
  urls_file: config/watch-urls.txt

  scraping:
    respect_robots: true
    rate_limit_ms: 1000
    user_agent: "OPAL Knowledge Bot"

  output:
    directory: _inbox/scraped/
    track_changes: true  # Only save when content changes
```

### Sitemaps

Monitor website sitemaps for new content.

```yaml
sitemaps:
  enabled: true
  type: sitemap

  sync:
    schedule: "0 4 * * *"  # Daily at 4am

  sites:
    - sitemap_url: https://docs.example.com/sitemap.xml
      name: Example Docs
      include_patterns:
        - "/guides/*"
        - "/tutorials/*"
      exclude_patterns:
        - "/api/*"

    - sitemap_url: https://wiki.example.org/sitemap.xml
      name: Example Wiki

  output:
    directory: _inbox/sitemaps/
    only_new: true  # Only fetch pages not seen before
```

### YouTube

Monitor channels/playlists and get transcripts.

```yaml
youtube:
  enabled: true
  api_key_env: YOUTUBE_API_KEY

  sync:
    schedule: "0 8 * * *"  # Daily at 8am

  channels:
    - id: UCxxxxxxxx
      name: Tech Talks

  playlists:
    - id: PLxxxxxxxx
      name: Conference 2026

  # Specific videos (one-time)
  videos:
    - url: https://youtube.com/watch?v=xxxxx

  transcription:
    prefer: captions  # captions | whisper | both
    fallback_to_whisper: true
    whisper_model: medium

  filters:
    min_duration_minutes: 5
    max_duration_minutes: 120
    require_captions: false

  output:
    directory: _inbox/youtube/
    include_description: true
    include_chapters: true
```

### Podcasts

Subscribe to podcasts and transcribe episodes.

```yaml
podcasts:
  enabled: true

  sync:
    schedule: "0 6 * * *"  # Daily at 6am

  feeds:
    - url: https://podcast.example.com/feed.xml
      name: Example Podcast
      transcription: whisper
      whisper_model: medium

    - url: https://other.podcast.com/rss
      name: Other Podcast
      # Skip transcription, just get metadata
      transcription: none

  filters:
    max_age_days: 30
    min_duration_minutes: 10
    max_duration_minutes: 180

  output:
    directory: _inbox/podcasts/
    keep_audio: false  # Delete after transcription
```

### Custom API

Poll any REST API and transform the response.

```yaml
custom_api:
  enabled: true

  endpoints:
    - name: grants-api
      url: https://api.grants.gov/v1/opportunities
      method: GET
      headers:
        Authorization: "Bearer ${GRANTS_API_KEY}"
      params:
        status: open
        limit: 100

      # Transform response to markdown
      transform:
        items_path: "data.opportunities"
        title_field: "title"
        content_fields:
          - "description"
          - "eligibility"
        date_field: "deadline"
        url_field: "application_url"

      output:
        directory: _inbox/grants/

    - name: events-api
      url: https://api.events.co/upcoming
      schedule: "0 */6 * * *"
      transform:
        items_path: "events"
        template: |
          # {{title}}

          **Date:** {{date}}
          **Location:** {{location}}

          {{description}}

          [Register]({{registration_url}})
```

### Webhooks

Receive content pushed to OPAL.

```yaml
webhooks:
  enabled: true

  endpoints:
    - path: /ingest/zapier
      auth: bearer_token
      token_env: ZAPIER_WEBHOOK_TOKEN
      transform:
        title_field: "subject"
        content_field: "body"
      output:
        directory: _inbox/zapier/

    - path: /ingest/github
      auth: github_signature
      secret_env: GITHUB_WEBHOOK_SECRET
      events:
        - issues.opened
        - issues.labeled
      output:
        directory: _inbox/github-issues/
```

---

## Agentic Fetching

When OPAL fetches URLs, it acts as an intelligent agent:

### Content Extraction

```yaml
fetching:
  # Readability extraction
  extract_content: true
  remove_navigation: true
  remove_ads: true

  # Metadata extraction
  extract_metadata:
    title: true
    author: true
    date: true
    description: true
    image: true

  # Convert to clean markdown
  output_format: markdown

  # Handle different content types
  handlers:
    pdf: extract_text
    docx: convert_to_markdown
    video: fetch_transcript
    audio: transcribe
```

### Link Following

```yaml
link_following:
  enabled: true
  max_depth: 2

  # Only follow links matching these patterns
  follow_patterns:
    - "/article/*"
    - "/post/*"
    - "/paper/*"

  # Never follow these
  exclude_patterns:
    - "/login"
    - "/signup"
    - "/privacy"

  # Stay within domain
  same_domain_only: true
```

### Pagination Handling

```yaml
pagination:
  enabled: true

  strategies:
    # URL parameter pagination
    url_param:
      param: page
      start: 1
      max_pages: 10

    # "Load more" button
    load_more:
      selector: ".load-more-btn"
      max_clicks: 5
      wait_ms: 1000

    # Infinite scroll
    infinite_scroll:
      scroll_count: 10
      wait_ms: 2000
```

---

## Source Discovery

OPAL can help discover new sources:

```
/sources discover

🔍 Source Discovery
━━━━━━━━━━━━━━━━━━━

Based on your schema and existing content, I found potential sources:

RSS Feeds Found:
├── https://blog.example.com/feed (referenced 12 times)
├── https://news.domain.org/rss (referenced 8 times)
└── https://research.edu/atom.xml (referenced 5 times)

Suggested Based on Schema:
├── ArXiv RSS (for research papers)
├── Hacker News RSS (for technology news)
└── Google Scholar Alerts (for citations)

Add sources? [y/n/select]
```

---

## Sync Commands

### Basic Sync

```bash
/sync                    # Sync all enabled sources
/sync telegram           # Sync specific source
/sync telegram rss       # Sync multiple sources
```

### Advanced Options

```bash
/sync --dry-run          # Preview what would be fetched
/sync --since 2026-01-01 # Override time range
/sync --force            # Ignore cursor, refetch all
/sync --retry-failed     # Retry previously failed items
```

### Sync Status

```bash
/sync --status

Source Status
━━━━━━━━━━━━━

┌─────────────┬─────────┬─────────────────────┬────────┐
│ Source      │ Enabled │ Last Sync           │ Items  │
├─────────────┼─────────┼─────────────────────┼────────┤
│ meetily     │ ✅      │ 2 hours ago         │ 45     │
│ telegram    │ ✅      │ 30 min ago          │ 312    │
│ rss         │ ✅      │ 2 hours ago         │ 89     │
│ youtube     │ ❌      │ never               │ 0      │
└─────────────┴─────────┴─────────────────────┴────────┘
```

---

## Adding Custom Sources

### Via Configuration

Add to `.opal/sources.yaml`:

```yaml
my_custom_source:
  enabled: true
  type: api

  # Your configuration...
```

### Via Skill

Create a custom sync skill in `.claude/skills/sync-custom/`:

```python
# SKILL.md describes the skill
# sync.py implements the logic

async def sync(config, state):
    """Pull content from custom source."""
    # Fetch data
    items = fetch_from_source(config)

    # Transform to OPAL format
    for item in items:
        yield {
            'title': item.title,
            'content': item.body,
            'source': 'my_custom_source',
            'source_id': item.id,
            'metadata': {...}
        }
```

---

## Best Practices

### 1. Start Small
Enable 1-2 sources first. Add more once you've established a review workflow.

### 2. Set Appropriate Schedules
- High-volume sources: Less frequent (daily)
- Low-volume sources: More frequent (hourly)
- Meeting transcripts: Manual or post-meeting

### 3. Use Filters Liberally
Filter out noise at the source level rather than during review.

### 4. Monitor Inbox Size
If inbox grows faster than you can process, adjust filters or schedules.

### 5. Review Failed Items
Run `/sync --retry-failed` periodically to recover transient failures.

---

## Related Commands

- `/setup` - Configure sources during initial setup
- `/sync` - Pull content from sources
- `/sources` - Manage source subscriptions
- `/process` - Process inbox items
- `/status inbox` - View inbox state
