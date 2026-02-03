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

## Key Features

### 🎯 Domain-Aware Extraction

Unlike generic NER tools, OPAL understands *your* domain. Define what matters to you—whether that's civic patterns, research papers, or creative projects—and Claude extracts exactly those concepts.

```yaml
# Your schema defines what OPAL looks for
resource_types:
  - pattern      # Reusable solutions
  - protocol     # Step-by-step processes
  - person       # People in your network
  - organization # Groups and institutions
```

### 🔍 Semantic Search & Q&A

Don't remember the exact words? Ask naturally:

```
/search governance approaches for small teams
/ask How do we handle disagreements in our community?
/graph consent-decision-making  # Visualize connections
```

### 🏛️ Democratic Governance (Commons Mode)

For shared knowledge bases, OPAL supports democratic contribution:

- Contributors submit changes via PR
- Community votes (3+ approvals required)
- Transparent history and attribution
- No single point of control

### 🌐 Federation with Other Commons

Share knowledge across communities without centralization:

- **Publish** your patterns to the broader network
- **Subscribe** to topics from other knowledge commons
- **Bridge** different taxonomies (e.g., civic ↔ ecological)
- **KOI Compatible** - Federate with Regen Network's 64K+ document index

---

## Quick Start

### 1. Install

```bash
# Clone OPAL
git clone https://github.com/omniharmonic/opal.git my-knowledge-base
cd my-knowledge-base

# Open with Claude Code
claude
```

### 2. Setup

```
/setup
```

Choose your template:

| Template | Best For | What You Get |
|----------|----------|--------------|
| `minimal` | Starting fresh | Just notes |
| `zettelkasten` | Personal knowledge | Notes, concepts, sources, questions |
| `research` | Academic work | Papers, authors, concepts, projects |
| `opl` | Civic innovation | Patterns, protocols, playbooks |
| `regen` | Ecological work | Methodologies, projects, claims, evidence |
| `life-archive` | Personal history | Memories, people, places, events |

### 3. Add Content

```bash
# Copy a transcript to the inbox
cp ~/Downloads/meeting-notes.md _inbox/

# Or sync from connected sources
/sync meetily    # Local meeting transcripts
/sync otter      # Otter.ai transcripts
/sync telegram   # Links from Telegram channels
```

### 4. Process

```
/process
```

OPAL will:
1. **Classify** the content type
2. **Extract** entities based on your schema
3. **Reconcile** against existing entities (deduplication)
4. **Stage** changes for your review

### 5. Review & Approve

```
/review

📝 Review Session
━━━━━━━━━━━━━━━━━

[1/4] NEW: patterns/participatory-budgeting.md
      Confidence: 0.92
      Extracted from: meeting-2026-01-15.md

      Actions: [a]ccept [r]eject [e]dit [s]kip
```

### 6. Search & Explore

```
/search participatory budgeting
/ask What patterns work for municipal governance?
/graph --type pattern
/coverage  # See what's well-covered vs. gaps
```

---

## Real-World Use Cases

### 🏘️ Community Organization

**Problem**: Your neighborhood council has 2 years of meeting notes but nobody can find past decisions.

**Solution**:
```
/setup --template opl
cp meeting-archives/*.md _inbox/
/process
/ask What did we decide about the community garden?
```

### 🔬 Research Team

**Problem**: Your lab reads hundreds of papers but insights aren't shared across projects.

**Solution**:
```
/setup --template research
# Import Zotero exports, PDF papers, meeting notes
/process
/ask What methods have been used for soil carbon measurement?
```

### 🌱 Regenerative Projects

**Problem**: Your ecological project needs to document methodologies for carbon credit verification.

**Solution**:
```
/setup --template regen
# OPAL extracts claims, evidence, and methodology references
/koi publish  # Share with Regen Network's knowledge commons
```

### 📚 Personal Knowledge Garden

**Problem**: You've been taking notes for years but can't find connections between ideas.

**Solution**:
```
/setup --template zettelkasten
# Import from Obsidian, Notion, or plain markdown
/process
/graph  # Visualize your knowledge network
```

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
│ • Otter.ai      │      │ • Extract       │      │ • Notion        │
│ • Fathom        │      │ • Reconcile     │      │ • GitHub        │
│ • Telegram      │      │ • Generate      │      │ • KOI/RDF       │
│ • Luma Events   │      │ • Translate     │      │ • Quartz        │
│ • RSS/Atom      │      │   (taxonomy)    │      │                 │
│ • Manual drops  │      │                 │      │                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          KNOWLEDGE BASE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  _index/entities.json    Your schema     Markdown files     Federation  │
│  (deduplication)         (.opal/)        (searchable)       (outbox)    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Processing Pipeline

```
INBOX → CLASSIFY → PREPROCESS → EXTRACT → RECONCILE → STAGE → REVIEW → COMMIT
  │         │           │           │          │          │        │        │
  │         │           │           │          │          │        │        │
  ▼         ▼           ▼           ▼          ▼          ▼        ▼        ▼
Raw      What is    Clean up,    Claude      Check      Prepare  Human    Apply
content  this?      convert      extracts    for dups   changes  reviews  changes
```

---

## Commands Reference

### Setup & Status

| Command | Description |
|---------|-------------|
| `/setup` | Interactive setup wizard |
| `/status` | Current state overview |
| `/profile` | Manage multiple knowledge contexts |

### Content Acquisition

| Command | Description |
|---------|-------------|
| `/sync` | Pull from all configured sources |
| `/sync <source>` | Pull from specific source |
| `/ingest <path>` | Manually ingest a file |

### Processing

| Command | Description |
|---------|-------------|
| `/process` | Process inbox through pipeline |
| `/review` | Review and approve staged changes |
| `/cleanup` | Clean up processed inbox items |

### Search & Discovery

| Command | Description |
|---------|-------------|
| `/search <query>` | Semantic search |
| `/ask <question>` | Q&A with citations |
| `/graph` | Visualize entity relationships |
| `/coverage` | Analyze schema coverage gaps |

### Publishing & Federation

| Command | Description |
|---------|-------------|
| `/github pr create` | Create PR for changes (commons mode) |
| `/federate` | Federation status and operations |
| `/koi` | Regen Network KOI integration |
| `/bridge` | Taxonomy bridge management |
| `/digest` | Generate activity summaries |

---

## Federation & Interoperability

### Share Knowledge Across Communities

OPAL supports federated knowledge sharing without centralization:

```yaml
# .opal/sources.yaml
federation:
  # Subscribe to other knowledge commons
  sources:
    - name: open-protocol-library
      repo: omniharmonic/open-protocol-library
      patterns: patterns/*, protocols/*

    - name: bioregional-commons
      repo: consortium/bioregional-commons
      patterns: playbooks/bioregional/*

  # Publish your contributions
  publish:
    enabled: true
    include: patterns/*, protocols/*
    license: CC-BY-SA-4.0
```

### KOI Integration (Regen Network)

OPAL is compatible with Regen Network's Knowledge Organization Infrastructure:

```
/koi search participatory budgeting    # Search 64K+ documents
/koi publish                           # Share to KOI network
/koi sync                              # Pull from subscriptions
```

### Taxonomy Bridges

Different communities use different vocabularies. Bridges translate between them:

```
/bridge status                         # Show bridge coverage
/bridge translate patterns/consent.md  # Preview translation
/bridge validate opl-to-regen.yaml     # Validate a bridge
```

---

## Content Sources

OPAL can ingest from multiple sources:

| Source | Type | Setup |
|--------|------|-------|
| **Meetily** | Local transcripts | Auto-detected |
| **Otter.ai** | Cloud transcripts | API key |
| **Fathom** | Video calls | API key |
| **Read.ai** | Meetings | API key |
| **Telegram** | Links from chats | Bot token |
| **Luma** | Events | API key |
| **RSS/Atom** | Articles | Feed URLs |
| **Filesystem** | Local files | Watch paths |

Configure during `/setup` or in `config/integrations.yaml`.

---

## Templates

### Minimal
Starting from scratch with just notes.

### Zettelkasten
Personal knowledge management with atomic notes, concepts, sources, and questions.

### Research
Academic work with papers, authors, concepts, and projects.

### Open Protocol Library (OPL)
Civic innovation patterns, protocols, playbooks, and organizational knowledge.

### Regen Network
Ecological regeneration with methodologies, credit classes, projects, claims, and evidence. KOI-compatible for federation.

### Life Archive
Personal history with memories, people, places, events, and artifacts.

### Activity Index
Events tracking with grants, initiatives, alliances, courses, and gatherings.

### Creative Portfolio
Creative work with projects, ideas, inspirations, and references.

---

## Philosophy

### Knowledge as Commons

OPAL is designed for **shared stewardship** of knowledge. Features like democratic PR governance, federation, and transparent provenance support communities managing knowledge collectively.

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
| Semantic Q&A | ✅ | ❌ | ❌ | ❌ |
| Self-hosted | ✅ | ✅ | ❌ | ❌ |

**OPAL is for you if:**
- You have lots of unstructured content (transcripts, documents, links)
- You want AI to do the organizing, not just store files
- You need semantic search and Q&A, not just keyword matching
- You want to share knowledge with other communities
- You care about data ownership and plain text formats

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
│   ├── sources.yaml       # Content sources & federation
│   └── bridges/           # Taxonomy bridges
│
├── .claude/               # OPAL implementation
│   ├── commands/          # Slash commands
│   ├── skills/            # Processing skills
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

## Troubleshooting

### Common Issues

**"Claude Code not found"**
```bash
npm install -g @anthropic-ai/claude-code
```

**"Ollama not running"**
```bash
ollama serve
ollama pull nomic-embed-text
```

**"No entities extracted"**
- Check that your schema is defined in `.opal/schema.yaml`
- Ensure content is in `_inbox/` directory
- Run `/status` to verify configuration

### Getting Help

```
/help              # General help
/help <command>    # Help for specific command
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
