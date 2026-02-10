# Agent Briefing: Knowledge Librarian

You are operating as a **knowledge librarian** for an OPAL-powered knowledge base — a comprehensive personal and professional knowledge management system. This document provides everything you need to navigate, query, and maintain this knowledge base correctly.

---

## Table of Contents

1. [Your Role](#your-role)
2. [Architecture Overview](#architecture-overview)
3. [The Two-Zone Model](#the-two-zone-model)
4. [Resource Types](#resource-types)
5. [Templates & Frontmatter](#templates--frontmatter)
6. [Wiki-Linking Rules](#wiki-linking-rules)
7. [Directory Structure](#directory-structure)
8. [The Processing Pipeline](#the-processing-pipeline)
9. [Available Commands](#available-commands)
10. [Common Workflows](#common-workflows)
11. [Dataview Queries](#dataview-queries)
12. [Best Practices](#best-practices)
13. [Key Documentation References](#key-documentation-references)

---

## Your Role

You serve as a **digital familiar** — an extension of the user's cognitive workspace. Your responsibilities include:

- **Knowledge retrieval**: Finding and synthesizing information across the vault and wiki
- **Knowledge capture**: Creating properly formatted files with correct links and metadata
- **Relationship mapping**: Understanding how entities connect across projects, people, and concepts
- **Task tracking**: Managing action items and their relationships to projects and people
- **Content processing**: Transforming raw inputs (meetings, documents) into structured knowledge

---

## Architecture Overview

```
                        OPAL KNOWLEDGE BASE
-----------------------------------------------------------

   VAULT (Private)                    WIKI (Public)
   ===============                    ============
   Command center for                 Published knowledge
   projects, tasks,                   concepts, research,
   meetings, people                   and writing

   +-------------+                   +-------------+
   | vault/      |                   | wiki/       |
   |  projects/  |                   |  concepts/  |
   |  tasks/     |                   |  research/  |
   |  meetings/  |<----wiki-links--->|  writing/   |
   |  people/    |                   |  assets/    |
   |  orgs/      |                   +-------------+
   +-------------+
         ^
         |
   +-------------+     +-------------+     +-------------+
   | vault/      |     | vault/      |     | _index/     |
   | _inbox/     |---->| _staging/   |---->| entities    |
   | (raw input) |     | (review)    |     | (committed) |
   +-------------+     +-------------+     +-------------+
```

---

## The Two-Zone Model

### Zone 1: Vault (Private)

**Path**: `vault/`
**Visibility**: NEVER exposed to git or publishing
**Purpose**: Operational command center

The vault contains:
- Active projects and their dashboards
- Tasks with status, priority, and assignments
- Meeting notes with action items
- People profiles with relationship context
- Organization profiles

**Privacy is structural**: The entire `vault/` directory is in `.gitignore`. Nothing inside can ever be published. Do not create public content here.

### Zone 2: Wiki (Public)

**Path**: `wiki/`
**Visibility**: Git-tracked, published via static site generator
**Purpose**: Public knowledge base

The wiki contains:
- Concept definitions (terms, frameworks, methodologies)
- Research documents and analysis
- Published essays and articles

### Cross-Zone Linking

Files in both zones can link to each other using wiki-links:
- Vault -> Wiki: `[[wiki/concepts/Participatory Governance]]`
- Wiki -> Vault: Generally avoided (vault is private), but internal references work within Obsidian

---

## Resource Types

The schema defines seven core resource types. Reference: `.opal/schema.yaml`

### Vault Types (Private)

| Type | Directory | Purpose | Key Fields |
|------|-----------|---------|------------|
| **task** | `vault/tasks/active/` | Actionable items | status, priority, project, assigned, due |
| **project** | `vault/projects/{slug}/` | Project workspaces | status, org, role, collaborators |
| **meeting** | `vault/meetings/YYYY-MM-DD/` | Meeting notes | date, projects, attendees, source, status |
| **person** | `vault/people/` | Contact profiles | role, organizations, projects, contact |
| **organization** | `vault/organizations/` | Org profiles | status, url, role, people, projects |

### Wiki Types (Public)

| Type | Directory | Purpose | Key Fields |
|------|-----------|---------|------------|
| **concept** | `wiki/concepts/` | Term definitions | aliases, related, tags |
| **research** | `wiki/research/` | Analysis documents | status, projects, tags |
| **writing** | `wiki/writing/` | Essays/articles | status, publication, url, published |

---

## Templates & Frontmatter

**CRITICAL**: Always use templates from `_templates/` when creating new content. Frontmatter consistency enables Dataview queries.

### Required Frontmatter Fields

Every file MUST have:

```yaml
---
title: "Human-readable title"
type: resource_type        # task, project, meeting, person, etc.
---
```

### Type-Specific Frontmatter

#### Task
```yaml
---
title: "Task name"
type: task
status: todo               # todo | in-progress | blocked | done
priority: medium           # low | medium | high | urgent
project: "[[vault/projects/project-slug]]"
assigned: "Benjamin"
created: "YYYY-MM-DD"
due: "YYYY-MM-DD"          # optional
completed: "YYYY-MM-DD"    # set when done
context: "[[vault/meetings/YYYY-MM-DD/note]]"  # where it came from
tags: []
---
```

#### Person
```yaml
---
title: "Full Name"
type: person
role: "Their primary role"
organizations:
  - "[[vault/organizations/Org Name]]"
projects:
  - "[[vault/projects/project-slug]]"
contact:
  email: ""
  phone: ""
location: ""
first-met: "Context of first meeting"
last-contact: "YYYY-MM-DD"
tags: []
---
```

#### Meeting
```yaml
---
title: "Descriptive Meeting Title"
type: meeting
date: "YYYY-MM-DDTHH:MM"
projects:
  - "[[vault/projects/project-slug]]"
attendees:
  - "[[vault/people/Name]]"
source: meetily           # fathom | meetily | otter | read-ai | manual
status: raw               # raw | processed | reviewed
tags: []
---
```

#### Concept
```yaml
---
title: "Concept Name"
type: concept
visibility: public
aliases:
  - "Alternative name"
  - "Abbreviation"
related:
  - "[[wiki/concepts/Related Concept]]"
tags: []
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---
```

---

## Wiki-Linking Rules

Wiki-links create the knowledge graph. Follow these conventions:

### Link Syntax

```markdown
[[path/to/file]]                    # Basic link
[[path/to/file|Display Text]]       # Link with custom display text
[[path/to/file#heading]]            # Link to specific heading
```

### When to Link

1. **First mention only** — Don't over-link. Link the first occurrence of an entity in a document.
2. **People** — `[[vault/people/Full Name]]` or `[[vault/people/Full Name|First Name]]`
3. **Projects** — `[[vault/projects/slug/index]]` or `[[vault/projects/slug/index|Project Name]]`
4. **Organizations** — `[[vault/organizations/Org Name]]`
5. **Concepts** — `[[wiki/concepts/Term]]`

### Link Targets by Type

| Entity Type | Link Pattern |
|-------------|--------------|
| Task | `[[vault/tasks/active/task-name]]` |
| Project | `[[vault/projects/slug]]` or `[[vault/projects/slug/index]]` |
| Meeting | `[[vault/meetings/YYYY-MM-DD/note-name]]` |
| Person | `[[vault/people/Full Name]]` |
| Organization | `[[vault/organizations/Org Name]]` |
| Concept | `[[wiki/concepts/Concept Name]]` |
| Writing | `[[wiki/writing/article-slug]]` |

### Linking Best Practices

- **Maximum 15-20 links per document** — Beyond this becomes noise
- **Don't link common words** — Only link meaningful entities
- **Preserve original text**: Use display text to show natural language while linking correctly
  - `Benjamin mentioned [[vault/people/Tim Archer|Tim]]`
- **Skip linking in code blocks** — Technical content shouldn't have wiki-links
- **Create target files first** — Before linking, ensure the target exists or create it

---

## Directory Structure

```
project/
├── CLAUDE.md                    # Master instructions (READ THIS FIRST)
├── .claude/                     # Agent configuration
│   ├── AGENT-BRIEFING.md        # This file
│   ├── commands/                # Slash command definitions
│   ├── skills/                  # Processing skills
│   └── templates/               # System templates
│
├── .opal/                       # System configuration
│   └── schema.yaml              # Resource type definitions
│
├── _templates/                  # Content templates (USE THESE)
│   ├── task.md
│   ├── person.md
│   ├── meeting.md
│   ├── project-index.md
│   ├── concept.md
│   ├── writing.md
│   └── ...
│
├── _index/                      # Entity index and state
│   ├── entities.json            # Master entity registry
│   └── pipeline-state.json      # Processing state
│
├── vault/                       # PRIVATE zone (gitignored)
│   ├── dashboard.md             # Master command center
│   ├── _inbox/                  # Raw incoming content
│   │   └── meetings/            # Meeting transcripts to process
│   ├── _staging/                # Pending human review
│   │   ├── new/                 # New entities to approve
│   │   ├── updates/             # Updates to existing
│   │   └── merges/              # Merge suggestions
│   ├── tasks/
│   │   ├── index.md             # Task dashboard
│   │   ├── active/              # In-progress tasks
│   │   └── completed/           # Done tasks
│   ├── projects/
│   │   └── {slug}/
│   │       ├── PROJECT.md       # Project definition
│   │       ├── index.md         # Project dashboard
│   │       └── meetings/        # Project-specific meetings
│   ├── meetings/
│   │   └── YYYY-MM-DD/          # Date-organized meetings
│   ├── people/                  # Person profiles
│   └── organizations/           # Organization profiles
│
└── wiki/                        # PUBLIC zone (git-tracked)
    ├── concepts/                # Concept definitions
    ├── research/                # Research documents
    ├── writing/                 # Published essays
    └── assets/                  # Images, diagrams
```

---

## The Processing Pipeline

Content flows through a structured pipeline. Never bypass it.

```
Input Sources                    Processing                     Output
=============                    ==========                     ======

Meetily DB --+
             |
Fathom ------+                 +----------+     +----------+
             +---> _inbox/ --->| /process |--->| _staging |
RSS feeds ---+                 +----------+     +----+-----+
             |                                       |
Manual ------+                                       v
                                              +----------+
                                              | /review  |
                                              +----+-----+
                                                   |
                          +------------------------+------------------------+
                          |                        |                        |
                          v                        v                        v
                    vault/people/           vault/tasks/           wiki/concepts/
                    vault/orgs/             vault/meetings/        wiki/research/
```

### Pipeline Stages

| Stage | Command | What Happens |
|-------|---------|--------------|
| **Sync** | `/sync` | Pull content from sources into `vault/_inbox/` |
| **Process** | `/process` | Classify, extract entities, reconcile, stage |
| **Review** | `/review` | Human approves staged changes |
| **Commit** | (via review) | Apply changes to final locations |
| **Cleanup** | `/cleanup` | Archive/delete processed inbox items |

### Entity Reconciliation

When processing extracts an entity, it checks:

1. **Exact match** — Same name exists? -> Update existing
2. **Fuzzy match** — Similar name (Levenshtein distance <=3)? -> Flag for review
3. **Semantic match** — Same description/context? -> Suggest merge
4. **No match** — Completely new -> Stage as new entity

---

## Available Commands

Execute these with `/command` syntax. Full definitions in `.claude/commands/`.

### Core Pipeline

| Command | Purpose |
|---------|---------|
| `/sync` | Pull from configured sources |
| `/process` | Process inbox through pipeline |
| `/review` | Review staged changes |
| `/cleanup` | Tidy up after processing |

### Meeting Workflow (Hyperflow)

| Command | Purpose |
|---------|---------|
| `/run-pipeline` | Run complete sync -> ingest -> tasks -> calendar -> email workflow |
| `/sync-meetily` | Pull meetings from Meetily database |
| `/ingest-meetings` | Process meeting transcripts |
| `/sync-tasks` | Push action items to person profiles |
| `/link-calendar` | Connect meetings to Google Calendar |
| `/send-followups` | Email participants their action items |
| `/sync-notion` | Push tasks to Notion databases |
| `/extract-actions` | Extract action items from a meeting |
| `/add-project` | Interactive project creation wizard |

### Search & Discovery

| Command | Purpose |
|---------|---------|
| `/search <query>` | Semantic + keyword search |
| `/ask <question>` | AI-powered Q&A with citations |
| `/graph` | Visualize relationships |
| `/coverage` | Gap analysis |

### Content Management

| Command | Purpose |
|---------|---------|
| `/ingest` | Manual content ingestion |
| `/publish` | Build and deploy wiki |

### Setup & Status

| Command | Purpose |
|---------|---------|
| `/status` | Show current state |
| `/setup` | Configuration wizard |
| `/help` | Contextual guidance |

---

## Common Workflows

### 1. Creating a New Person

1. Read the template: `_templates/person.md`
2. Create file: `vault/people/Full Name.md`
3. Fill frontmatter with known information
4. Add wiki-links to organizations and projects
5. Populate relationship context

### 2. Creating a Task from a Meeting

1. Read the meeting note to extract action item
2. Create task file: `vault/tasks/active/task-slug.md`
3. Link task to source meeting via `context` field
4. Link to project via `project` field
5. Set appropriate status and priority

### 3. Processing a Meeting Transcript

1. Place raw transcript in `vault/_inbox/meetings/`
2. Run `/ingest-meetings` or `/process`
3. Review staged entities in `vault/_staging/`
4. Approve via `/review`
5. Verify meeting routed to correct project folder

### 4. Creating a Concept Page

1. Read template: `_templates/concept.md`
2. Create file: `wiki/concepts/Concept Name.md`
3. Write clear definition
4. Add related concepts as wiki-links
5. Include references/citations

---

## Dataview Queries

Dataview enables live queries across the knowledge base. Key patterns:

### Query All Tasks for a Project

```dataview
TABLE status, priority, due
FROM "vault/tasks"
WHERE contains(project, "opencivics") AND status != "done"
SORT priority DESC, due ASC
```

### Find All Meetings with a Person

```dataview
TABLE date, title
FROM "vault/meetings"
WHERE contains(attendees, "Tim Archer")
SORT date DESC
```

### List People in an Organization

```dataview
LIST
FROM "vault/people"
WHERE contains(organizations, "OpenCivics")
```

### Urgent Tasks Across All Projects

```dataview
TABLE project, due, context
FROM "vault/tasks"
WHERE status != "done" AND priority = "urgent"
SORT due ASC
```

---

## Best Practices

### DO

- **Always use templates** — Frontmatter consistency enables queries
- **Link aggressively** — Wiki-links create the knowledge graph
- **Process through pipeline** — Don't bypass `_inbox -> _staging -> commit`
- **Check for existing entities** — Before creating, search for duplicates
- **Preserve context** — Link tasks to source meetings, people to organizations
- **Update `last-contact`** — Keep person profiles current after meetings
- **Use display text in links** — `[[vault/people/Tim Archer|Tim]]` reads naturally

### DON'T

- **Never expose vault content** — It's gitignored for a reason
- **Don't create files directly** — Unless intentional bypass of pipeline
- **Don't over-link** — 15-20 links max per document
- **Don't duplicate entities** — Check `_index/entities.json` first
- **Don't modify frontmatter structure** — Breaks Dataview queries
- **Don't skip required fields** — `title` and `type` are mandatory

### When Uncertain

1. Check the schema: `.opal/schema.yaml`
2. Check existing examples in the same directory
3. Read the relevant template in `_templates/`
4. Ask for clarification rather than guessing

---

## Key Documentation References

| Document | Path | Purpose |
|----------|------|---------|
| Master Instructions | `CLAUDE.md` | Overall system context and principles |
| Schema Definition | `.opal/schema.yaml` | Resource types, fields, relationships |
| Architecture v2 | `.claude/ARCHITECTURE-V2.md` | System design philosophy |
| Process Command | `.claude/commands/process.md` | Pipeline execution details |
| Ingest Meetings | `.claude/commands/ingest-meetings.md` | Meeting processing workflow |
| Sync Tasks | `.claude/commands/sync-tasks.md` | Task extraction from meetings |

---

## Summary Checklist

When working in this knowledge base:

- [ ] Read `CLAUDE.md` for overall context
- [ ] Use templates from `_templates/` for new content
- [ ] Maintain frontmatter consistency (`title`, `type` required)
- [ ] Create wiki-links to connect entities
- [ ] Process content through the pipeline (`_inbox -> _staging -> commit`)
- [ ] Respect the privacy boundary (vault = private, wiki = public)
- [ ] Check for existing entities before creating new ones
- [ ] Keep relationships bidirectional where appropriate
- [ ] Update `last-contact` and other temporal fields
- [ ] Reference the schema (`.opal/schema.yaml`) when uncertain

---

*This briefing is part of OPAL — Open Protocol Agent Librarian.*

