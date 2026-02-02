# OPAL - Open Protocol Agent Librarian

<p align="center">
  <strong>🦉 AI-Powered Knowledge Commons Steward</strong>
</p>

<p align="center">
  <em>Transform transcripts, documents, and links into organized, interconnected knowledge using Claude-powered entity extraction and democratic governance.</em>
</p>

---

## What is OPAL?

OPAL is a Claude Code plugin that turns any markdown repository into an intelligent, federated knowledge commons. Whether you're building a personal knowledge garden or a community-governed protocol library, OPAL provides the tools to:

- **📥 Ingest** content from multiple sources (transcripts, documents, links)
- **🔍 Extract** domain-aware entities using Claude's understanding
- **🔗 Reconcile** and deduplicate against your existing knowledge base
- **📝 Generate** structured wiki pages with proper cross-references
- **🗳️ Govern** changes democratically with PR-based voting
- **🌐 Federate** knowledge between repositories

## Quick Start

### 1. Clone and Setup

```bash
# Clone the OPAL starter
git clone https://github.com/omniharmonic/opal.git my-commons
cd my-commons

# Open with Claude Code
claude
```

### 2. Run the Setup Wizard

```
/setup
```

The wizard will guide you through:
- Choosing your mode (Personal / Team / Commons)
- Selecting or creating a taxonomy
- Configuring integrations
- Setting up federation

### 3. Start Ingesting Knowledge

```bash
# Pull transcripts from your meeting tools
/ingest transcript otter

# Add a document
/ingest file ~/Documents/research-paper.pdf

# Process everything
/process
```

### 4. Review and Commit

```bash
# Review extracted entities
/review

# Commit approved changes
/github commit

# Create PR for team review (commons mode)
/github pr create
```

## Core Commands

| Command | Description |
|---------|-------------|
| `/setup` | Run the configuration wizard |
| `/ingest <source>` | Add content to inbox |
| `/process` | Process inbox through pipeline |
| `/review` | Review and approve staged changes |
| `/status` | Show current state |
| `/github` | Manage GitHub PRs and voting |
| `/federate` | Sync with federated repos |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        COORDINATOR AGENT                             │
│                 (Orchestrates pipeline, manages state)               │
└─────────────────────────────────────────────────────────────────────┘
                                    │
     ┌──────────────────────────────┼──────────────────────────────────┐
     │                              │                                  │
     ▼                              ▼                                  ▼
┌─────────────┐            ┌─────────────────┐              ┌─────────────────┐
│   INPUT     │            │   PROCESSING    │              │    OUTPUT       │
│   LAYER     │            │     LAYER       │              │    LAYER        │
│             │            │                 │              │                 │
│ • Otter     │───────────▶│ • Classify      │─────────────▶│ • Vault         │
│ • Fathom    │            │ • Cleanup       │              │ • Notion        │
│ • Read.ai   │            │ • Extract       │              │ • GitHub        │
│ • Telegram  │            │ • Reconcile     │              │ • Federation    │
│ • Manual    │            │ • Generate      │              │                 │
└─────────────┘            └─────────────────┘              └─────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
     ┌──────────────────────────┐    ┌──────────────────────────┐
     │      ENTITY INDEX        │    │    TAXONOMY LAYER        │
     │  Dedup + Semantic Match  │    │  Resource types, sectors │
     └──────────────────────────┘    └──────────────────────────┘
```

## Processing Pipeline

```
INBOX → CLASSIFY → PREPROCESS → EXTRACT → RECONCILE → STAGE → REVIEW → COMMIT → NOTIFY
```

1. **INBOX**: Raw content enters from various sources
2. **CLASSIFY**: Determine content type and initial categorization
3. **PREPROCESS**: Clean transcripts, convert PDFs, prepare content
4. **EXTRACT**: Claude-powered entity extraction with taxonomy context
5. **RECONCILE**: Match against existing entities, identify duplicates
6. **STAGE**: Prepare proposed changes for review
7. **REVIEW**: Human reviews and approves changes
8. **COMMIT**: Apply changes, create git commits
9. **NOTIFY**: Update federation, sync to Notion

## Modes of Operation

### 🧑 Personal Mode
- Local-first knowledge management
- Optional GitHub backup
- Single Notion workspace per project

### 👥 Team Mode
- GitHub for collaboration
- Shared Notion workspace
- PR-based updates without voting

### 🌐 Commons Mode
- GitHub as source of truth
- Democratic PR moderation (3+ votes)
- Public Notion frontend
- Federation with other commons

## Democratic Governance

In commons mode, all changes require community approval:

```
PR #42: Add participatory budgeting pattern
├── Votes: ✅✅✅ (3/3 required)
├── Status: Ready to merge
└── /github merge 42
```

- **3 approvals** required to merge
- **Any rejection** blocks until addressed
- **72-hour** voting window
- **Contributors** = anyone with GitHub permissions

## Integrations

| Integration | Purpose | Setup |
|-------------|---------|-------|
| **Otter.ai** | Meeting transcripts | API key |
| **Fathom** | Video call transcripts | API key |
| **Read.ai** | Meeting transcripts | API key |
| **Notion** | Frontend / workspace | Integration token |
| **GitHub** | Source of truth | gh CLI |
| **Telegram** | Link ingestion | Bot token |
| **Ollama** | Local LLM fallback | Local install |

## Taxonomy Presets

### Open Protocol Library (OPL)
For civic innovation and community organizing:
- **Resource Types**: Patterns, Protocols, Playbooks, Primitives, Artifacts...
- **Sectors**: Governance, Economic, Environmental, Health, Education...
- **Scales**: Individual → Neighborhood → Municipal → Bioregional → Planetary

### Custom Taxonomy
Define your own:
```yaml
resource_types:
  - name: Technique
    description: A specific method or approach
    directory: techniques/

civic_sectors:
  - id: my-domain
    name: My Domain
    keywords: [keyword1, keyword2]
```

## Directory Structure

```
my-commons/
├── CLAUDE.md              # OPAL context for Claude
├── PROJECT.md             # Project-specific config
├── README.md              # This file
│
├── .claude/               # Plugin structure
│   ├── commands/          # Slash commands
│   ├── skills/            # Processing skills
│   ├── hooks/             # Event hooks
│   └── agents/            # Coordinator agent
│
├── config/                # Configuration
│   ├── settings.yaml
│   ├── integrations.yaml
│   ├── governance.yaml
│   └── llm.yaml
│
├── taxonomy/              # Taxonomy definitions
│   └── opl.yaml
│
├── _templates/            # Resource templates
├── _index/                # Entity index
├── _inbox/                # Incoming content
├── _staging/              # Pending review
├── _federation/           # Federation config
│
└── [knowledge dirs]/      # Your content
    ├── patterns/
    ├── protocols/
    └── ...
```

## Federation

Connect your commons to others:

```yaml
# _federation/sources.yaml
sources:
  - name: open-protocol-library
    repo: omniharmonic/open-protocol-library
    subscribe_to:
      - patterns/*
      - protocols/*
```

When subscribed repos update, OPAL can:
- Pull new content into your inbox
- Translate to your taxonomy
- Maintain attribution

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE)

---

<p align="center">
  <em>OPAL is part of the Open Civics ecosystem</em><br>
  <a href="https://commons.opencivics.co">commons.opencivics.co</a>
</p>
