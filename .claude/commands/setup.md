# /setup Command

Initialize and configure an OPAL knowledge base.

## Usage

```
/setup                      # Interactive setup wizard
/setup --template <name>    # Quick setup with template
/setup --import <path>      # Import existing structure
/setup --reconfigure        # Modify existing configuration
/setup --list-templates     # Show available templates
```

## Philosophy

OPAL is a **toolkit**, not a template. The setup wizard helps you define:
- What kinds of things you track (resource types)
- How you categorize them (dimensions)
- Where content comes from (sources)
- How things connect (relationships)

Templates are accelerators, not requirements. Start with one and customize, or build from scratch.

## Interactive Setup Wizard

### Step 1: Starting Point

```
/setup

Welcome to OPAL - Your Knowledge Toolkit

OPAL helps you collect, organize, and connect your knowledge.
It works with any structure you define.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

How would you like to begin?

  [1] Start from a template (recommended)
      Pre-built configurations for common use cases

  [2] Build from scratch
      Define your own resource types and structure

  [3] Import existing structure
      Analyze your current files and generate a schema

  [4] Quick start
      Minimal setup, configure as you go

Choice:
```

### Step 2: Choose Template

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What kind of knowledge are you managing?

  Personal & Learning
  ───────────────────
  [1] Personal Knowledge Garden
      Notes, ideas, connections. Zettelkasten-inspired.
      → notes, concepts, sources, people, questions

  [2] Life Archive
      Memories, relationships, personal history.
      → memories, people, places, events, artifacts, journal

  [3] Research Library
      Academic work, papers, citations.
      → papers, authors, concepts, notes, citations

  Work & Projects
  ───────────────
  [4] Project Documentation
      Work projects, meetings, decisions.
      → projects, meetings, decisions, tasks, people

  [5] Creative Portfolio
      Works, ideas, inspirations.
      → works, ideas, inspirations, references

  Community & Civic
  ─────────────────
  [6] Open Protocol Library
      Civic patterns, protocols, playbooks.
      → patterns, protocols, playbooks, people, organizations

  [7] Activity Index
      Events, grants, initiatives.
      → grants, gatherings, initiatives, courses, alliances

  Minimal
  ───────
  [8] Minimal
      Just notes. Build from there.

Choice:
```

### Step 3: Customize (optional)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Template: Personal Knowledge Garden

This template includes:

  Resource Types:
  ✓ Note      - Atomic ideas and observations
  ✓ Concept   - Larger themes and topics
  ✓ Source    - Books, articles, references
  ✓ Person    - People and their ideas
  ✓ Question  - Open inquiries

  Dimensions:
  ✓ Status    - seedling, growing, evergreen, archived
  ✓ Confidence - speculation, hypothesis, belief, knowledge

Would you like to customize?

  [1] Use as-is (recommended for getting started)
  [2] Add resource types
  [3] Remove resource types
  [4] Modify dimensions
  [5] See full schema details

Choice:
```

### Step 4: Content Sources

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Where will your content come from?

  Transcripts
  [ ] Fathom - Video call transcripts
  [ ] Otter - Meeting transcripts
  [ ] Read.ai - Meeting transcripts
  [ ] Meetily - Local transcription (no cloud)

  Communication
  [ ] Telegram - Links from channels

  Feeds
  [ ] RSS - Articles and blogs

  Local
  [ ] Filesystem - Watch folders for files

  Manual
  [✓] Manual - Add things yourself (always available)

Select sources (space to toggle, Enter when done):
```

### Step 5: Source Configuration

For each selected source:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Configure: Meetily

Meetily stores transcripts in a local database.
OPAL reads directly from this database.

Checking for database...
✓ Found: ~/Library/Application Support/com.meetily.ai/meeting_minutes.sqlite

Options:
  • Sync on /sync command? [Y/n] y
  • Minimum meeting duration? [5 minutes]
  • Exclude titles containing? (comma-separated) [standup, 1:1]

✅ Meetily configured
```

### Step 6: Generate Structure

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to create your knowledge base!

Configuration:
  Template: Personal Knowledge Garden
  Resource types: 5 (note, concept, source, person, question)
  Dimensions: 2 (status, confidence)
  Sources: Meetily, filesystem

Will create:

  .opal/
  ├── config.yaml           # Main configuration
  ├── schema.yaml           # Your knowledge schema
  ├── sources.yaml          # Content sources
  └── templates/            # Templates for each type
      ├── note.md
      ├── concept.md
      ├── source.md
      ├── person.md
      └── question.md

  _inbox/                   # Incoming content
  _staging/                 # Pending review
  _index/                   # Search index

  notes/                    # Your notes
  concepts/                 # Concepts
  sources/                  # Sources
  people/                   # People
  questions/                # Questions

Create this structure? [Y/n]
```

### Step 7: Complete

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Knowledge base created!

Your configuration:
  Schema:    .opal/schema.yaml
  Sources:   .opal/sources.yaml
  Templates: .opal/templates/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quick Start:

  1. Add content
     • Drop files in _inbox/
     • Run /sync to pull from Meetily

  2. Process content
     • /process analyzes and classifies
     • Uses your schema to extract entities

  3. Review and approve
     • /review shows staged items
     • Accept, edit, or reject

  4. Explore your knowledge
     • /search <query>
     • /ask <question>
     • /graph

Need help? Just ask!
```

## Quick Setup with Template

Skip the wizard:

```bash
/setup --template zettelkasten

Using template: Personal Knowledge Garden

Creating structure...
  ✓ .opal/config.yaml
  ✓ .opal/schema.yaml
  ✓ .opal/sources.yaml
  ✓ .opal/templates/
  ✓ notes/, concepts/, sources/, people/, questions/
  ✓ _inbox/, _staging/, _index/

✅ Done!

Next: Add content to _inbox/ or run /sync
```

## Available Templates

```
/setup --list-templates

Available Templates
━━━━━━━━━━━━━━━━━━━

Personal & Learning
  minimal          Just notes - build from there
  zettelkasten     Personal knowledge garden (notes, concepts, sources)
  life-archive     Personal history (memories, people, places, events)
  research         Academic work (papers, authors, citations)

Work & Projects
  projects         Work documentation (projects, meetings, decisions)
  creative         Portfolio (works, ideas, inspirations)

Community & Civic
  opl              Open Protocol Library (patterns, protocols, playbooks)
  activity-index   Event tracking (grants, gatherings, initiatives)

Use: /setup --template <name>
```

## Build From Scratch

Define your own structure:

```
/setup

Choice: 2 (Build from scratch)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Let's define your knowledge structure.

What kinds of things will you track?
(Examples: notes, projects, recipes, books, contacts)

Enter resource types (comma-separated):
> recipes, restaurants, trips, cooking-notes

Great! I'll help you define each one.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/4] Recipes

  • Plural name? [Recipes]
  • Directory? [recipes/]
  • Description? [Cooking recipes I want to make or have made]

  What fields should a recipe have?
  (Common: title, cuisine, difficulty, time, ingredients, source)

  Fields (comma-separated):
  > title, cuisine, difficulty, prep_time, ingredients, source_url, rating

  ✓ Recipe type configured

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2/4] Restaurants
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Now let's define how you categorize things.

Dimensions are ways to classify across all types.
(Examples: status, priority, cuisine type)

Add dimension:
  • Name: cuisine
  • Values (comma-separated): italian, mexican, asian, indian, american, other

Add another? [y/N]
```

## Import Existing

Analyze existing files:

```
/setup --import .

Analyzing current directory...

Found:
  • 156 markdown files
  • 23 PDFs
  • Frontmatter in 89 files

Detected structure:
  notes/        → 67 files (title, tags, date)
  projects/     → 23 files (title, status, client)
  references/   → 45 files (title, author, url)
  journal/      → 21 files (date, mood)

Suggested schema:

  resource_types:
    - note (notes/)
    - project (projects/)
    - reference (references/)
    - journal_entry (journal/)

  dimensions:
    - status: draft, active, complete, archived
    - client: (extracted from projects)

Accept this schema? [Y/n/edit]
> y

Generating configuration...
✅ Created .opal/schema.yaml
✅ Created .opal/config.yaml

Your existing files are ready to use!
Run /process to build the search index.
```

## Reconfigure

Modify existing setup:

```
/setup --reconfigure

Current Configuration
━━━━━━━━━━━━━━━━━━━━━

  Template: zettelkasten (customized)
  Resource types: 6
  Dimensions: 3
  Sources: meetily, filesystem

What would you like to change?

  [1] Add resource types
  [2] Remove resource types
  [3] Add/modify dimensions
  [4] Configure sources
  [5] Change processing settings
  [6] View current schema
  [7] Reset to template defaults

Choice:
```

## Configuration Files

### .opal/config.yaml

```yaml
# OPAL Configuration
version: "2.0"
name: "My Knowledge Base"
created: 2026-02-02

# From template (for reference)
template: zettelkasten
template_version: "1.0"

# Processing
processing:
  auto_classify: true
  auto_extract: true
  confidence_threshold: 0.7
  create_backlinks: true

# Embeddings
embeddings:
  provider: ollama
  model: nomic-embed-text

# Output
output:
  commit_after_review: true
```

### .opal/schema.yaml

```yaml
# Knowledge Schema
name: "Personal Knowledge Garden"
version: "1.0"

resource_types:
  - id: note
    name: Note
    plural: Notes
    directory: notes/
    description: Atomic ideas and observations
    template: note.md
    fields:
      - name: title
        type: string
        required: true
      - name: tags
        type: list
      - name: status
        type: dimension
        dimension: status
      - name: source
        type: reference
        to: source

dimensions:
  - id: status
    name: Status
    values:
      - id: seedling
        name: Seedling
      - id: growing
        name: Growing
      - id: evergreen
        name: Evergreen
      - id: archived
        name: Archived

relationships:
  - id: relates_to
    name: Relates To
    bidirectional: true
```

### .opal/sources.yaml

```yaml
# Content Sources
sources:
  meetily:
    enabled: true
    database: auto
    sync_schedule: manual
    filters:
      min_duration_minutes: 5
      exclude_titles: [standup, 1:1]

  filesystem:
    enabled: true
    watch:
      - path: ~/Downloads/*.pdf
        type: source
```

## Related Commands

- `/profile` - Manage configuration profiles
- `/sync` - Pull content from sources
- `/process` - Process inbox content
- `/help` - Get help with OPAL
