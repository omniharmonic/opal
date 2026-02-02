# OPAL - Open Protocol Agent Librarian

<p align="center">
  <strong>AI-Powered Knowledge Commons Steward</strong>
</p>

<p align="center">
  <em>Transform transcripts, documents, and links into organized, interconnected knowledge using Claude-powered entity extraction and democratic governance.</em>
</p>

---

## Table of Contents

- [What is OPAL?](#what-is-opal)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Detailed Usage](#detailed-usage)
- [Command Reference](#command-reference)
- [Processing Pipeline](#processing-pipeline)
- [Modes of Operation](#modes-of-operation)
- [Configuration](#configuration)
- [Integrations](#integrations)
- [Federation](#federation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## What is OPAL?

OPAL is a Claude Code plugin that turns any markdown repository into an intelligent, federated knowledge commons. Whether you're building a personal knowledge garden or a community-governed protocol library, OPAL provides the tools to:

- **Ingest** content from multiple sources (transcripts, documents, audio, links)
- **Extract** domain-aware entities using Claude's understanding
- **Reconcile** and deduplicate against your existing knowledge base
- **Generate** structured wiki pages with proper cross-references
- **Govern** changes democratically with PR-based voting
- **Federate** knowledge between repositories

---

## Prerequisites

Before using OPAL, ensure you have the following installed:

### Required

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Claude Code** | Core runtime | `npm install -g @anthropic-ai/claude-code` |
| **Git** | Version control | [git-scm.com](https://git-scm.com) |

### Recommended

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Ollama** | Local LLM for embeddings & cleanup | [ollama.ai](https://ollama.ai) |
| **Whisper** | Audio transcription | `pip install openai-whisper` or `brew install openai-whisper` |
| **GitHub CLI** | GitHub integration | `brew install gh` or [cli.github.com](https://cli.github.com) |

### Verifying Prerequisites

```bash
# Check Ollama
ollama --version
ollama list  # Should show available models

# Check Whisper
whisper --help

# Check GitHub CLI
gh auth status
```

### Setting Up Ollama Models

OPAL uses Ollama for embeddings and transcript cleanup:

```bash
# Install required models
ollama pull nomic-embed-text   # For semantic search embeddings
ollama pull llama3.2           # For transcript cleanup (optional)

# Verify models are available
ollama list
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/omniharmonic/opal.git my-commons
cd my-commons
```

### 2. Open with Claude Code

```bash
claude
```

### 3. Run the Setup Wizard

```
/setup
```

The wizard will guide you through:
- Choosing your mode (Personal / Team / Commons)
- Selecting or creating a taxonomy
- Configuring integrations
- Setting up federation (optional)

---

## Quick Start

### Process Your First Content

```bash
# 1. Add content to the inbox
cp ~/Documents/meeting-transcript.md _inbox/transcripts/

# 2. Open Claude Code
claude

# 3. Process the content
/process

# 4. Review extracted entities
/review

# 5. Check status
/status
```

### Process Audio Files

```bash
# 1. Add audio file to inbox
cp ~/Downloads/meeting.mp4 _inbox/

# 2. Process (OPAL will transcribe with Whisper)
/process

# 3. Review the transcript and extracted entities
/review
```

---

## Detailed Usage

### Adding Content to the Inbox

Content can be added to the `_inbox/` directory for processing:

```
_inbox/
├── transcripts/          # Meeting transcripts (.md, .txt)
├── documents/            # PDFs, Word docs
├── links/                # URL references
└── [audio/video files]   # Will be transcribed automatically
```

**Supported formats:**
- Text: `.md`, `.txt`
- Documents: `.pdf`, `.docx`
- Audio: `.mp3`, `.mp4`, `.m4a`, `.wav`, `.webm`
- Links: `.md` files with URL frontmatter

### Processing Content

The `/process` command runs content through the full pipeline:

```
/process                    # Process all inbox items
/process --dry-run          # Preview what would happen
/process --item <path>      # Process specific item
/process --type transcript  # Process only transcripts
/process --limit 5          # Process up to 5 items
```

**Example output:**
```
Processing Inbox

Found 2 items to process.

[1/2] transcripts/meeting-2026-01-15.md
      ├── Classified: transcript (confidence: 0.95)
      ├── Extracted: 12 entities, 5 relationships
      ├── Reconciled: 8 existing, 4 new
      └── Staged 4 new entities for review

[2/2] audio.mp4
      ├── Classified: audio (confidence: 0.98)
      ├── Transcribed: whisper-turbo (402 segments)
      ├── Extracted: 8 entities
      └── Staged 2 new entities for review

Summary:
• Processed: 2 items
• New entities: 6
• Review needed: 6 items

Next: Run /review to review staged changes
```

### Reviewing Staged Changes

The `/review` command lets you approve, edit, or reject extracted entities:

```
/review                    # Interactive review session
/review --list             # List staged items
/review --item <path>      # Review specific item
/review --approve-all      # Approve all (use with caution)
```

**During review, you can:**
- `[a]` Accept - Add entity to knowledge base
- `[r]` Reject - Discard with reason
- `[e]` Edit - Modify before accepting
- `[s]` Skip - Review later
- `[v]` View - See full content

### Searching the Knowledge Base

```
/search <query>                           # Hybrid search
/search governance --type pattern         # Filter by type
/search community --sector civic-engagement  # Filter by sector
/search --semantic-only                   # Only semantic matching
```

### Asking Questions

```
/ask What is consent-based decision making?
/ask How does sociocracy differ from consensus?
/ask What patterns exist for community governance?
```

### Checking Status

```
/status              # Full status overview
/status inbox        # Just inbox status
/status staging      # Just staging status
/status github       # GitHub and PR status
/status index        # Entity index statistics
```

### Visualizing Relationships

```
/graph                                    # Full commons graph
/graph pattern-consent --depth 3          # Local graph for entity
/graph --stats                            # Show statistics only
/graph --export svg                       # Export as image
```

### Analyzing Coverage

```
/coverage                                 # Full coverage report
/coverage --gaps                          # Show gaps only
/coverage --sector governance             # Specific sector
/coverage --scale municipal               # Specific scale
```

---

## Command Reference

| Command | Description | Common Options |
|---------|-------------|----------------|
| `/setup` | Run configuration wizard | - |
| `/status` | Show current state | `inbox`, `staging`, `github`, `index` |
| `/process` | Process inbox items | `--dry-run`, `--item`, `--type`, `--limit` |
| `/review` | Review staged changes | `--list`, `--item`, `--approve-all` |
| `/search` | Search knowledge base | `--type`, `--sector`, `--scale`, `--semantic-only` |
| `/ask` | Q&A with citations | `--detailed`, `--sources-only` |
| `/graph` | Visualize relationships | `--depth`, `--export`, `--stats` |
| `/coverage` | Analyze gaps | `--gaps`, `--sector`, `--scale`, `--quality` |
| `/digest` | Generate activity digest | `--type`, `--preview`, `--send` |
| `/github` | GitHub operations | `pr create`, `pr vote`, `pr merge`, `commit` |
| `/federate` | Federation operations | `pull`, `publish`, `add`, `remove` |
| `/ingest` | Ingest from sources | `transcript`, `file`, `url` |

---

## Processing Pipeline

```
INBOX → CLASSIFY → PREPROCESS → EXTRACT → RECONCILE → STAGE → REVIEW → COMMIT → NOTIFY
```

| Step | Description | Tools Used |
|------|-------------|------------|
| **CLASSIFY** | Determine content type | Claude |
| **PREPROCESS** | Clean/convert content | Whisper (audio), Ollama (cleanup) |
| **EXTRACT** | Entity extraction | Claude with taxonomy context |
| **RECONCILE** | Deduplicate entities | Entity index + semantic matching |
| **STAGE** | Prepare for review | File system |
| **REVIEW** | Human approval | Interactive CLI |
| **COMMIT** | Git commit changes | Git |
| **NOTIFY** | Update federation/sync | Webhooks, APIs |

---

## Modes of Operation

### Personal Mode
For individual knowledge management:
- Local-first processing
- Optional GitHub backup
- Single Notion workspace per project
- No voting required

### Team Mode
For small team collaboration:
- GitHub for version control
- Shared Notion workspace
- PR-based updates (no voting)
- Shared entity index

### Commons Mode
For community-governed knowledge:
- **GitHub as source of truth**
- **Democratic PR moderation** (3+ approvals required)
- Public Notion frontend
- Federation with other commons
- Transparent governance

---

## Configuration

### Main Settings (`config/settings.yaml`)

```yaml
mode: commons  # personal | team | commons

taxonomy:
  preset: opl  # Open Protocol Library
  custom_path: null

defaults:
  confidence_threshold: 0.7
  auto_merge_threshold: 0.9
  review_required: true
```

### Integrations (`config/integrations.yaml`)

```yaml
integrations:
  notion:
    enabled: true
    workspace_id: your-workspace-id

  github:
    enabled: true
    mode: commons

  ollama:
    enabled: true
    endpoint: http://localhost:11434
    models:
      embeddings: nomic-embed-text
      cleanup: llama3.2
```

### Governance (`config/governance.yaml`)

```yaml
pr_moderation:
  required_approvals: 3
  voting_period_hours: 72
  auto_merge_on_approval: true
```

### LLM Routing (`config/llm.yaml`)

```yaml
llm:
  default_provider: claude

  routing:
    classify: claude
    cleanup_transcript: ollama
    extract: claude
    reconcile: claude
    embeddings: ollama
```

---

## Integrations

### Transcript Sources

| Service | Setup | Command |
|---------|-------|---------|
| **Otter.ai** | API key in `config/secrets.local` | `/ingest transcript otter` |
| **Fathom** | API key | `/ingest transcript fathom` |
| **Read.ai** | API key | `/ingest transcript read` |
| **Manual** | Copy to `_inbox/transcripts/` | `/process` |

### Audio Transcription

OPAL uses OpenAI Whisper for audio transcription:

```bash
# Supported formats
.mp3, .mp4, .m4a, .wav, .webm, .ogg

# Models available (configure in settings)
whisper-tiny    # Fastest, less accurate
whisper-base    # Good balance
whisper-small   # Better accuracy
whisper-medium  # High accuracy
whisper-turbo   # Best speed/accuracy (default)
whisper-large   # Highest accuracy, slowest
```

### Notion

Connect to Notion for a visual frontend:

1. Create a Notion integration at [notion.so/my-integrations](https://notion.so/my-integrations)
2. Add the integration token to `config/secrets.local`
3. Share your workspace with the integration
4. Run `/setup` to configure database mapping

### GitHub

For version control and PR-based governance:

```bash
# Authenticate with GitHub CLI
gh auth login

# Create a PR for staged changes
/github pr create

# Vote on pending PRs
/github pr vote 42 approve

# Merge approved PRs (commons mode)
/github pr merge 42
```

---

## Federation

Connect your commons to others for knowledge sharing:

### Subscribe to a Source

```yaml
# _federation/sources.yaml
sources:
  - name: open-protocol-library
    repo: omniharmonic/open-protocol-library
    subscribe_to:
      - patterns/*
      - protocols/*
    auto_merge: false
```

### Federation Commands

```
/federate                  # Show federation status
/federate pull             # Pull from all sources
/federate pull <source>    # Pull from specific source
/federate publish          # Update outbox with recent commits
/federate add <repo>       # Add new source subscription
```

### Attribution

All federated content includes proper attribution:

```yaml
---
federation:
  source_repo: omniharmonic/open-protocol-library
  source_commit: abc123
  imported: 2026-02-01
  license: CC-BY-SA-4.0
---
```

---

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
│   ├── settings.yaml      # Main settings
│   ├── integrations.yaml  # Service connections
│   ├── governance.yaml    # PR moderation rules
│   ├── llm.yaml           # LLM routing
│   └── secrets.local      # API keys (gitignored)
│
├── taxonomy/              # Taxonomy definitions
│   └── opl.yaml           # Open Protocol Library preset
│
├── _templates/            # Resource type templates
├── _index/                # Entity index and state
│   ├── entities.json      # Master entity registry
│   ├── aliases.json       # Alias mappings
│   └── pipeline-state.json
│
├── _inbox/                # Incoming content
│   ├── transcripts/
│   ├── documents/
│   └── links/
│
├── _staging/              # Pending review
│   ├── new/               # New entities
│   ├── updates/           # Updates to existing
│   └── merges/            # Proposed merges
│
├── _federation/           # Federation config
│   ├── sources.yaml
│   └── outbox/
│
└── [knowledge dirs]/      # Your content
    ├── patterns/
    ├── protocols/
    ├── playbooks/
    ├── people/
    ├── organizations/
    └── ...
```

---

## Troubleshooting

### Common Issues

**"Ollama not running"**
```bash
# Start Ollama service
ollama serve

# Or on macOS, ensure Ollama app is running
```

**"Model not found"**
```bash
# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2
```

**"Whisper command not found"**
```bash
# Install Whisper
pip install openai-whisper

# Or on macOS
brew install openai-whisper
```

**"Permission denied" on hooks**
```bash
# Make hooks executable
chmod +x .claude/hooks/*.sh
```

**"GitHub CLI not authenticated"**
```bash
gh auth login
gh auth status
```

### Pipeline Issues

**Entities not being extracted**
- Check that the content is in a supported format
- Verify the taxonomy matches your domain
- Try lowering the confidence threshold in settings

**Duplicates not being detected**
- Ensure `_index/entities.json` is up to date
- Check that aliases are properly configured
- Run `/process` with semantic reconciliation enabled

**Federation not syncing**
- Verify source repository is accessible
- Check network connectivity
- Ensure you have read permissions on the source

### Getting Help

```
/help              # General help
/help <command>    # Help for specific command
```

---

## Taxonomy: Open Protocol Library (OPL)

OPAL ships with the OPL taxonomy for civic innovation:

### Resource Types (12)
- **Pattern** - Reusable solution to common problem
- **Protocol** - Step-by-step process
- **Playbook** - Comprehensive guide
- **Primitive** - Fundamental building block
- **Artifact** - Document or template
- **Person** - Individual contributor
- **Organization** - Group or institution
- **Activity** - Event or initiative
- **System** - Interconnected components
- **Utility** - Tool or platform
- **Sector** - Domain area
- **Scale** - Geographic/organizational level

### Civic Sectors (13)
Governance, Economic, Environmental, Health, Education, Housing, Food, Transportation, Communication, Cultural, Legal, Safety, Civic Engagement

### Civic Scales (7)
Individual → Household → Neighborhood → Municipal → Bioregional → National → Planetary

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repo
git clone https://github.com/omniharmonic/opal.git
cd opal

# Run tests
# See testing.md for comprehensive test procedures
```

---

## License

MIT License - See [LICENSE](LICENSE)

---

<p align="center">
  <em>OPAL is part of the Open Civics ecosystem</em><br>
  <a href="https://commons.opencivics.co">commons.opencivics.co</a>
</p>
