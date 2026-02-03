# OPAL - Open Protocol Agent Librarian

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-Plugin-7C3AED" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/KOI-Compatible-4CAF50" alt="KOI Compatible">
  <img src="https://img.shields.io/badge/Federation-Ready-blue" alt="Federation Ready">
</p>

<p align="center">
  <strong>Turn conversations, documents, and links into an interconnected knowledge commons.</strong>
</p>

<p align="center">
  <em>AI-powered knowledge extraction • Semantic search • Democratic governance • Federated sharing</em>
</p>

---

## The Problem

You have knowledge scattered everywhere:
- **Meeting transcripts** full of insights nobody can find later
- **Documents and PDFs** that disappear into folder hierarchies
- **Links shared in chat** that get lost in the scroll
- **Expertise in people's heads** that never gets captured

Traditional tools force you to do the work: tag everything, organize manually, remember where you put things. That doesn't scale.

## The Solution

**OPAL is an AI librarian that does the work for you.**

Drop content into your inbox. OPAL uses Claude to understand what you're talking about—the people, organizations, concepts, and relationships—and automatically organizes it into a searchable, interconnected knowledge base.

```
Meeting transcript → OPAL extracts → "Sarah mentioned Participatory Budgeting
                                       as a solution for the Community Council"

                                     Creates/updates:
                                     • Person: Sarah Chen
                                     • Pattern: Participatory Budgeting
                                     • Organization: Community Council
                                     • Links them all together
```

Then ask questions in natural language:

```
/ask What governance patterns has Sarah recommended?

→ Sarah Chen has recommended 3 governance patterns:
  1. Participatory Budgeting (mentioned 4 times)
  2. Consent-Based Decision Making (mentioned 2 times)
  3. Advice Process (mentioned 1 time)

  Sources: [meeting-2026-01-15], [meeting-2026-01-22]
```

---

## Quick Start

```bash
# Clone OPAL
git clone https://github.com/omniharmonic/opal.git my-knowledge-base
cd my-knowledge-base

# Open with Claude Code
claude

# Run the setup wizard
/setup
```

---

## Complete Command Reference

OPAL provides 23 commands organized into logical workflows. Here's what each one does in plain English:

### 🚀 Setup & Configuration

#### `/setup` — Interactive Setup Wizard
Guides you through configuring OPAL from scratch. Choose a template (or build your own schema), configure content sources, set up integrations, and create your directory structure. This is the first command you run.

```
/setup                    # Full interactive wizard
/setup --template regen   # Quick setup with specific template
```

#### `/profile` — Manage Multiple Contexts
Switch between different knowledge contexts. Maybe you have separate profiles for work, personal research, and a community project—each with its own schema and sources.

```
/profile list             # See all profiles
/profile use work         # Switch to work profile
/profile create research  # Create new profile
```

#### `/status` — What's Happening Right Now
Shows the complete state of your knowledge base: how many items are in inbox, what's staged for review, pending GitHub PRs, integration health, and suggested next actions.

```
/status                   # Full overview
/status inbox             # Just inbox status
/status github            # GitHub/PR status
/status integrations      # Check API connections
```

---

### 📥 Content Acquisition

#### `/sources` — Manage Where Content Comes From
Configure and manage all your content sources: transcript services, RSS feeds, Telegram channels, event platforms, and more. Add new sources, check their health, discover new ones based on your content.

```
/sources                  # List all sources
/sources add rss <url>    # Add RSS feed
/sources add telegram     # Add Telegram channel (interactive)
/sources add luma         # Add Luma events (interactive)
/sources add notion       # Sync from Notion
/sources test rss         # Check if sources are working
/sources discover         # Find sources based on your content
```

#### `/sync` — Pull Content from Sources
Fetches new content from all your configured sources (transcripts, RSS, Telegram, etc.) and puts it in your inbox for processing.

```
/sync                     # Sync all sources
/sync meetily             # Sync specific source
/sync --dry-run           # Preview what would be synced
```

#### `/ingest` — Manually Add Content
Add individual files, URLs, or clipboard content to your inbox. Use this for one-off additions rather than recurring sources.

```
/ingest file ~/document.pdf     # Add a file
/ingest url https://example.com # Fetch and add a URL
/ingest clipboard               # Add from clipboard
/ingest transcript otter        # Pull from Otter.ai
```

#### `/watch` — Monitor RSS Feeds
Subscribe to RSS/Atom feeds and get notified of new content. Review pending items and selectively ingest what's relevant.

```
/watch https://blog.example.com/feed  # Subscribe to feed
/watch list                            # Show subscriptions
/watch pending                         # See new items
/watch ingest <item-id>                # Add item to inbox
```

---

### ⚙️ Processing Pipeline

#### `/process` — Extract Knowledge from Content
The core intelligence of OPAL. Takes items from your inbox and:
1. Classifies what type of content it is
2. Cleans up transcripts (fixes speech-to-text errors)
3. Extracts entities (people, organizations, concepts) using Claude
4. Reconciles against existing entities (deduplication)
5. Stages changes for your review

```
/process                  # Process all inbox items
/process --dry-run        # Preview what would happen
/process --item <path>    # Process specific item
/process --type transcript # Only process transcripts
```

#### `/review` — Approve Extracted Knowledge
Human-in-the-loop review of what OPAL extracted. Accept, reject, or edit entities before they're committed to your knowledge base. Nothing gets added without your approval.

```
/review                   # Interactive review session
/review --list            # List staged items
/review --approve-all     # Approve everything (use carefully)
```

#### `/cleanup` — Tidy Up After Processing
Removes processed source files from inbox. Deletes audio after transcription confirmed, archives old transcripts, cleans up failed items. Keeps your inbox from growing forever.

```
/cleanup                  # Interactive cleanup
/cleanup --auto           # Apply configured rules
/cleanup --dry-run        # Preview what would be cleaned
```

---

### 🔍 Search & Discovery

#### `/search` — Find Entities
Hybrid semantic + keyword search across your knowledge base. Finds conceptually related content even if exact words don't match.

```
/search governance approaches        # Semantic search
/search --type pattern governance    # Filter by type
/search --sector civic-engagement    # Filter by dimension
```

#### `/ask` — Question & Answer
Ask questions in natural language and get synthesized answers with citations. OPAL searches your knowledge base and constructs an answer from what it finds.

```
/ask What is consent-based decision making?
/ask How do we handle disagreements in our process?
/ask What has Sarah said about budgeting?
```

#### `/graph` — Visualize Relationships
Generate interactive visualizations of how entities connect. See clusters of related concepts, identify bridge entities, find orphaned content.

```
/graph                            # Full knowledge graph
/graph patterns/consent.md        # Graph centered on entity
/graph --type pattern             # Only show patterns
/graph --stats                    # Just show statistics
```

#### `/coverage` — Find Gaps in Your Knowledge
Analyzes how well your knowledge base covers your taxonomy. Identifies underrepresented areas and suggests where to focus curation efforts.

```
/coverage                         # Full coverage report
/coverage --sector governance     # Specific sector
/coverage --gaps                  # Only show gaps
```

---

### 📤 Publishing & Output

#### `/publish` — Build a Static Website
Transforms your markdown knowledge base into a beautiful, searchable website using Quartz or Hugo. Includes wiki-style backlinks, knowledge graph visualization, full-text search.

```
/publish site             # Build and deploy
/publish preview          # Local preview server
/publish --generator hugo # Use Hugo instead of Quartz
```

**Deployment options:** GitHub Pages, Netlify, Vercel, or custom rsync.

#### `/digest` — Generate Activity Summaries
Creates reports of recent activity: new entities, updates, merged PRs, coverage changes. Send via email, Slack, or Telegram on schedule.

```
/digest preview           # Preview next digest
/digest generate --type weekly
/digest send --channel slack
```

---

### 🔀 GitHub & Governance

#### `/github` — Repository Management
Manage GitHub integration: create PRs for changes, vote on pending contributions, merge approved PRs. Essential for commons mode where changes require community approval.

```
/github pr create         # Create PR for staged changes
/github pr list           # List open PRs
/github vote 42 approve   # Vote on PR #42
/github merge 41          # Merge approved PR
```

**Commons mode:** PRs require 3+ approvals before merging, enabling democratic governance of shared knowledge.

---

### 🌐 Federation

#### `/federate` — Share Knowledge Across Commons
Enable cosmo-local knowledge sharing. Subscribe to other knowledge commons, publish your contributions, sync updates bidirectionally.

```
/federate                 # Show federation status
/federate pull            # Pull from subscribed sources
/federate publish         # Push to outbox for subscribers
/federate add <repo>      # Subscribe to another commons
```

#### `/koi` — Regen Network Integration
Connect to Regen Network's Knowledge Organization Infrastructure (KOI)—64K+ indexed documents about ecological regeneration. Search, publish, sync, and verify against on-chain data.

```
/koi                      # Show KOI status
/koi search <query>       # Search KOI network
/koi publish              # Publish entities to KOI
/koi sync                 # Pull from KOI subscriptions
/koi verify <entity>      # Verify against Regen Ledger
```

#### `/bridge` — Cross-Taxonomy Translation
Manage taxonomy bridges that translate between different classification systems (e.g., OPL civic taxonomy ↔ Regen ecological ontology). Essential for federation across communities with different vocabularies.

```
/bridge                   # List available bridges
/bridge status            # Show bridge coverage
/bridge translate <entity># Preview translation
/bridge validate <bridge> # Check bridge integrity
```

---

### 📅 Calendar Integration

#### `/calendar` — Meeting Context & Writeback
Bidirectional integration with Google Calendar. Before processing transcripts, looks up who was in the meeting (attendees become `known_speakers` for better extraction). After processing, writes meeting summary and action items back to the calendar event.

```
/calendar                 # Show integration status
/calendar sync            # Write pending notes to calendar
/calendar lookup <path>   # Test attendee lookup
/calendar writeback <path># Write specific transcript
/calendar rollback <id>   # Undo a writeback
```

**Why this matters:** "Speaker 1" in a transcript becomes "Alice Smith" because OPAL knows Alice was on the calendar invite.

---

### 🛠 Utilities

#### `/embeddings` — Manage Semantic Search Index
Build and maintain the vector embeddings that power semantic search. Uses Ollama locally or can fall back to cloud providers.

```
/embeddings build         # Build full index
/embeddings update        # Update changed entities
/embeddings status        # Show index health
```

#### `/help` — Get Contextual Help
Get help on any command, concept, or workflow. OPAL knows what you're working on and provides relevant guidance.

```
/help                     # General help
/help process             # Help with /process command
/help federation          # Learn about federation
```

---

## Skills (Internal Processing)

Behind the commands, OPAL uses specialized skills for each processing step:

| Skill | Purpose |
|-------|---------|
| **classify** | Determines what type of content something is (transcript, document, link, etc.) |
| **cleanup-transcript** | Fixes speech-to-text errors, normalizes speaker labels, removes filler words |
| **extract-entities** | Claude-powered extraction of people, organizations, concepts, and relationships |
| **reconcile** | Checks extracted entities against existing ones for deduplication |
| **meeting-context** | Queries Google Calendar for attendees before transcript processing |
| **calendar-writeback** | Writes summaries and action items back to calendar after commit |
| **generate-wiki** | Creates markdown pages from extracted entities |
| **embed-content** | Generates vector embeddings for semantic search |
| **qa-corpus** | Answers questions by searching and synthesizing from knowledge base |
| **generate-graph** | Builds graph visualizations of entity relationships |
| **analyze-coverage** | Analyzes how well knowledge base covers the taxonomy |
| **generate-site** | Builds static websites using Quartz or Hugo |
| **generate-digest** | Creates activity summary reports |
| **taxonomy-bridge** | Translates entities between different taxonomy systems |
| **notion-sync** | Synchronizes with Notion workspaces |
| **federate-sync** | Handles federation with other knowledge commons |
| **process-pdf** | Extracts text and structure from PDF documents |
| **transcribe-audio** | Transcribes audio/video using Whisper |
| **monitor-rss** | Polls RSS feeds and stages new items |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              YOU                                         │
│                   Drop content, ask questions                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         OPAL COORDINATOR                                 │
│              Orchestrates the pipeline, manages state                    │
└─────────────────────────────────────────────────────────────────────────┘
         │                          │                          │
         ▼                          ▼                          ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   INGESTION     │      │   PROCESSING    │      │     OUTPUT      │
├─────────────────┤      ├─────────────────┤      ├─────────────────┤
│ • Meetily       │      │ • Classify      │      │ • Markdown      │
│ • Otter.ai      │      │ • Cleanup       │      │ • Notion        │
│ • Fathom        │      │ • Extract       │      │ • GitHub        │
│ • Telegram      │      │ • Reconcile     │      │ • Quartz/Hugo   │
│ • Luma Events   │      │ • Generate      │      │ • KOI/RDF       │
│ • RSS/Atom      │      │ • Translate     │      │ • Calendar      │
│ • Google Cal    │      │   (taxonomy)    │      │                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

### Processing Pipeline

```
INBOX → CLASSIFY → CALENDAR → CLEANUP → EXTRACT → RECONCILE → STAGE → REVIEW → COMMIT → WRITEBACK
  │         │         │           │         │          │          │        │        │        │
  ▼         ▼         ▼           ▼         ▼          ▼          ▼        ▼        ▼        ▼
Raw      What is   Who was    Fix STT    Claude    Check     Prepare  Human    Apply   Update
content  this?     there?     errors     extracts  for dups  changes  reviews  changes calendar
```

---

## Templates

Start with a pre-built schema or create your own:

| Template | Best For | What You Get |
|----------|----------|--------------|
| **minimal** | Starting fresh | Just notes |
| **zettelkasten** | Personal knowledge | Notes, concepts, sources, questions |
| **research** | Academic work | Papers, authors, concepts, projects |
| **opl** | Civic innovation | Patterns, protocols, playbooks, organizations |
| **regen** | Ecological work | Methodologies, projects, claims, evidence (KOI-compatible) |
| **life-archive** | Personal history | Memories, people, places, events |
| **activity-index** | Events tracking | Grants, initiatives, alliances, gatherings |
| **creative** | Portfolio | Projects, ideas, inspirations, references |

---

## Content Sources

OPAL can ingest from:

| Source | Type | What It Does |
|--------|------|--------------|
| **Meetily** | Transcripts | Reads from local SQLite database |
| **Otter.ai** | Transcripts | Pulls via API |
| **Fathom** | Transcripts | Pulls via API |
| **Read.ai** | Transcripts | Pulls via API |
| **Telegram** | Links | Monitors channels for shared links, fetches content |
| **RSS/Atom** | Articles | Polls feeds, extracts full content |
| **Luma** | Events | Monitors calendars and hosts |
| **Eventbrite** | Events | Monitors organizers and searches |
| **YouTube** | Video | Fetches captions or transcribes with Whisper |
| **Podcasts** | Audio | Downloads and transcribes episodes |
| **Google Calendar** | Context | Enriches transcripts with attendee info |
| **Notion** | Databases | Syncs selected databases |
| **Custom API** | Any | Poll any REST endpoint |
| **Webhooks** | Any | Receive pushed content |

---

## Real-World Use Cases

### 🏘️ Community Organization
Your neighborhood council has 2 years of meeting notes but nobody can find past decisions.
```
/setup --template opl
cp meeting-archives/*.md _inbox/
/process
/ask What did we decide about the community garden?
```

### 🔬 Research Team
Your lab reads hundreds of papers but insights aren't shared across projects.
```
/setup --template research
/process                  # Process imported papers
/ask What methods have been used for soil carbon measurement?
```

### 🌱 Ecological Projects
Document methodologies for carbon credit verification and share with Regen Network.
```
/setup --template regen
/process                  # Extract claims, evidence, methodologies
/koi publish              # Share to KOI network
```

### 📚 Personal Knowledge
You've been taking notes for years but can't find connections between ideas.
```
/setup --template zettelkasten
/process                  # Extract concepts and connections
/graph                    # Visualize your knowledge network
```

---

## Philosophy

### Knowledge as Commons
OPAL is designed for **shared stewardship** of knowledge. Democratic PR governance, federation, and transparent provenance support communities managing knowledge collectively.

### Local-First, Federate Globally
Your knowledge lives in **plain markdown files** you control. Federation is opt-in. You decide what to share and with whom.

### AI-Assisted, Human-Directed
Claude does the heavy lifting of extraction and organization, but **humans review and approve** every change. The AI proposes; you decide.

### Schema Freedom
No forced structure. Define resource types, dimensions, and relationships that make sense for **your** domain.

---

## Comparison

| Feature | OPAL | Obsidian | Notion | Roam |
|---------|------|----------|--------|------|
| AI entity extraction | ✅ | ❌ | ❌ | ❌ |
| Custom schemas | ✅ | Partial | Partial | ❌ |
| Plain markdown | ✅ | ✅ | ❌ | ❌ |
| Democratic governance | ✅ | ❌ | ❌ | ❌ |
| Federation | ✅ | ❌ | ❌ | ❌ |
| Transcript processing | ✅ | ❌ | ❌ | ❌ |
| Calendar integration | ✅ | ❌ | ❌ | ❌ |
| Static site generation | ✅ | ✅ | ❌ | ❌ |
| Semantic Q&A | ✅ | ❌ | ❌ | ❌ |
| Self-hosted | ✅ | ✅ | ❌ | ❌ |

---

## Prerequisites

### Required

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Claude Code** | Core runtime | `npm install -g @anthropic-ai/claude-code` |
| **Git** | Version control | [git-scm.com](https://git-scm.com) |

### Recommended

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Ollama** | Local embeddings | [ollama.ai](https://ollama.ai) |
| **Whisper** | Audio transcription | `pip install openai-whisper` |
| **GitHub CLI** | GitHub integration | `brew install gh` |

---

## Directory Structure

```
my-knowledge-base/
├── CLAUDE.md              # OPAL context for Claude
├── README.md              # This file
│
├── .opal/                 # Your configuration
│   ├── config.yaml        # Main settings
│   ├── schema.yaml        # Your resource types
│   ├── sources.yaml       # Content sources
│   └── bridges/           # Taxonomy bridges
│
├── .claude/               # OPAL implementation
│   ├── commands/          # All 23 slash commands
│   ├── skills/            # 18+ processing skills
│   └── templates/         # Pre-built templates
│
├── _inbox/                # Incoming content
├── _staging/              # Pending review
├── _index/                # Entity index
├── _federation/           # Federation outbox/inbox
│
└── [your directories]/    # Based on your schema
    ├── patterns/
    ├── protocols/
    ├── people/
    └── ...
```

---

## Contributing

OPAL is open source and welcomes contributions:

1. Fork the repository
2. Create a feature branch
3. Submit a PR with your changes

For the OPAL knowledge commons itself (patterns, protocols):
- PRs require 3+ community approvals
- All contributions attributed via git history

---

## Community

- **GitHub Issues**: [omniharmonic/opal/issues](https://github.com/omniharmonic/opal/issues)
- **Discussions**: [omniharmonic/opal/discussions](https://github.com/omniharmonic/opal/discussions)

### Federated Communities
- [Open Protocol Library](https://github.com/omniharmonic/open-protocol-library) - Civic innovation patterns
- [Regen Network KOI](https://github.com/regen-network/koi-research) - Ecological knowledge commons

---

## License

MIT License - Use freely, contribute back if you can.

---

<p align="center">
  <strong>OPAL - Your AI librarian for the knowledge commons</strong>
</p>

<p align="center">
  <em>Transform scattered information into interconnected wisdom.</em>
</p>
