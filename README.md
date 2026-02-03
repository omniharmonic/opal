# OPAL - Open Protocol Agent Librarian

<p align="center">
  <strong>A Composable Knowledge Management Toolkit</strong>
</p>

<p align="center">
  <em>Transform transcripts, documents, and links into organized, interconnected knowledge using Claude-powered entity extraction and user-defined schemas.</em>
</p>

---

## Table of Contents

- [What is OPAL?](#what-is-opal)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Templates](#templates)
- [Commands](#commands)
- [Processing Pipeline](#processing-pipeline)
- [Configuration](#configuration)
- [Integrations](#integrations)
- [Profiles](#profiles)
- [Troubleshooting](#troubleshooting)

---

## What is OPAL?

**OPAL is a toolkit, not a template.**

OPAL is a Claude Code plugin that turns any markdown repository into an intelligent knowledge base. Unlike opinionated systems, OPAL lets you define your own structure:

- **Schema-agnostic**: You define what kinds of things you track
- **Template-based**: Start with a template or build from scratch
- **Multi-profile**: Manage different knowledge contexts (work, personal, research)
- **Source-flexible**: Ingest from meetings, documents, links, and more

### Core Capabilities

- **Ingest** content from multiple sources (Meetily, Fathom, Otter, Telegram, RSS)
- **Extract** domain-aware entities using Claude with your schema
- **Reconcile** and deduplicate against your existing knowledge
- **Generate** structured pages with proper cross-references
- **Search** with semantic understanding
- **Federate** knowledge between repositories

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
| **Ollama** | Local embeddings & cleanup | [ollama.ai](https://ollama.ai) |
| **Whisper** | Audio transcription | `pip install openai-whisper` |
| **GitHub CLI** | GitHub integration | `brew install gh` |

### Setting Up Ollama

```bash
# Install required model for embeddings
ollama pull nomic-embed-text

# Verify
ollama list
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/omniharmonic/opal.git my-knowledge-base
cd my-knowledge-base
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
- Choosing a template (or building from scratch)
- Defining your resource types and dimensions
- Configuring content sources
- Setting up your directory structure

---

## Quick Start

### 1. Run Setup

```
/setup
```

Choose a template or build your own schema.

### 2. Add Content

```bash
# Copy files to inbox
cp ~/Documents/meeting-notes.md _inbox/

# Or sync from configured sources
/sync
```

### 3. Process Content

```
/process
```

OPAL will:
- Classify the content type
- Extract entities based on your schema
- Check for duplicates
- Stage changes for review

### 4. Review and Approve

```
/review
```

Accept, edit, or reject extracted entities.

### 5. Search and Explore

```
/search <query>
/ask <question>
/graph
```

---

## Templates

OPAL includes pre-built templates for common use cases:

| Template | Use Case | Resource Types |
|----------|----------|----------------|
| `minimal` | Starting from scratch | note |
| `zettelkasten` | Personal knowledge garden | note, concept, source, person, question |
| `life-archive` | Personal history | memory, person, place, event, artifact, journal |
| `research` | Academic work | paper, author, concept, note, project |
| `creative` | Portfolio | work, idea, inspiration, reference, collection |
| `opl` | Civic innovation | pattern, protocol, playbook, person, organization |
| `activity-index` | Events tracking | grant, initiative, alliance, course, gathering |

### Using a Template

```
/setup --template zettelkasten
```

### Building from Scratch

```
/setup
# Choose "Build from scratch"
# Define your own resource types, dimensions, and relationships
```

---

## Commands

### Setup & Configuration

| Command | Description |
|---------|-------------|
| `/setup` | Interactive setup wizard |
| `/profile` | Manage configuration profiles |
| `/status` | Show current state |

### Content Acquisition

| Command | Description |
|---------|-------------|
| `/sync` | Pull from configured sources |
| `/cleanup` | Clean up inbox after processing |

### Processing

| Command | Description |
|---------|-------------|
| `/process` | Process inbox through pipeline |
| `/review` | Review staged changes |

### Search & Discovery

| Command | Description |
|---------|-------------|
| `/search <query>` | Search the knowledge base |
| `/ask <question>` | Q&A with citations |
| `/graph` | Visualize relationships |
| `/coverage` | Analyze schema coverage |

### Publishing

| Command | Description |
|---------|-------------|
| `/github` | GitHub operations |
| `/federate` | Federation operations |
| `/digest` | Generate activity digests |

### Utilities

| Command | Description |
|---------|-------------|
| `/embeddings` | Manage semantic search |
| `/help` | Get help |

---

## Processing Pipeline

```
INBOX → CLASSIFY → PREPROCESS → EXTRACT → RECONCILE → STAGE → REVIEW → COMMIT
```

| Step | Description |
|------|-------------|
| **CLASSIFY** | Determine content type |
| **PREPROCESS** | Clean/convert (transcribe audio, etc.) |
| **EXTRACT** | Entity extraction using your schema |
| **RECONCILE** | Deduplicate against existing entities |
| **STAGE** | Prepare for human review |
| **REVIEW** | Accept, edit, or reject |
| **COMMIT** | Apply changes to knowledge base |

---

## Configuration

After setup, your configuration lives in `.opal/`:

```
.opal/
├── config.yaml      # Main configuration
├── schema.yaml      # Your resource types and dimensions
├── sources.yaml     # Content sources
└── templates/       # Per-type templates
```

### Schema Example

```yaml
# .opal/schema.yaml
resource_types:
  - id: note
    name: Note
    directory: notes/
    fields:
      - name: title
        type: string
        required: true
      - name: tags
        type: list

dimensions:
  - id: status
    values: [draft, published, archived]

relationships:
  - id: relates_to
    bidirectional: true
```

---

## Integrations

### Content Sources

| Source | Type | Configuration |
|--------|------|---------------|
| **Meetily** | Local transcription | Auto-detected SQLite database |
| **Fathom** | Video calls | API key |
| **Otter.ai** | Meetings | API key |
| **Read.ai** | Meetings | API key |
| **Telegram** | Links | Bot token |
| **RSS** | Articles | Feed URLs |
| **Filesystem** | Local files | Watch paths |

Configure during `/setup` or edit `config/integrations.yaml`.

### Sync from Sources

```
/sync                  # Sync all configured sources
/sync meetily          # Sync specific source
/sync --list           # List available sources
```

---

## Profiles

Manage multiple knowledge contexts:

```
/profile list          # List profiles
/profile use work      # Switch to work profile
/profile create research --template research
```

Each profile has its own:
- Schema (resource types, dimensions)
- Content sources
- Knowledge base directory

---

## Directory Structure

After setup:

```
my-knowledge-base/
├── CLAUDE.md              # Toolkit context
├── README.md              # This file
│
├── .opal/                 # Your configuration
│   ├── config.yaml
│   ├── schema.yaml
│   ├── sources.yaml
│   └── templates/
│
├── .claude/               # Toolkit implementation
│   ├── commands/          # Slash commands
│   ├── skills/            # Processing skills
│   └── templates/         # Pre-built templates
│
├── config/                # System configuration
│   ├── integrations.yaml
│   ├── llm.yaml
│   └── embeddings.yaml
│
├── _inbox/                # Incoming content
├── _staging/              # Pending review
├── _index/                # Entity index
│
└── [your directories]/    # Based on your schema
```

---

## Troubleshooting

### Common Issues

**"Ollama not running"**
```bash
ollama serve
```

**"Model not found"**
```bash
ollama pull nomic-embed-text
```

**"Whisper command not found"**
```bash
pip install openai-whisper
# or
brew install openai-whisper
```

### Getting Help

```
/help              # General help
/help <command>    # Help for specific command
```

---

## Architecture

For detailed architecture documentation, see:
- `.claude/ARCHITECTURE-V2.md` - Composable toolkit design
- `.claude/EMBEDDINGS.md` - Embeddings and semantic search
- `.claude/SYNC-ARCHITECTURE.md` - Content source integration

---

## License

MIT License

---

<p align="center">
  <em>OPAL - A composable knowledge management toolkit</em>
</p>
