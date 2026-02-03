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

---

## EXECUTION INSTRUCTIONS

**⚠️ CRITICAL: This wizard MUST use AskUserQuestion for EACH step and WAIT for responses. Every question should have a way to skip or customize. Provide intelligent suggestions based on previous answers.**

When this command is invoked, execute these phases IN ORDER.

### Phase 0: Check Existing Configuration

**Action:** Use Glob to check for existing configuration.

1. Check if `.opal/schema.yaml` or `.opal/config.yaml` exists
2. If exists and no `--reconfigure` flag:
   ```
   ⚠️ OPAL is already configured in this directory.

   Use AskUserQuestion:
   questions: [{
     question: "An OPAL configuration already exists. What would you like to do?",
     header: "Existing Config",
     options: [
       {label: "Reconfigure", description: "Modify existing configuration"},
       {label: "View current", description: "Show current configuration and exit"},
       {label: "Start fresh", description: "Delete existing and start over"},
       {label: "Cancel", description: "Exit setup"}
     ]
   }]
   ```
   Handle response accordingly.

---

### Phase 1: Understanding Your Intent

**Goal:** Understand what the user wants to build so we can provide intelligent suggestions.

#### Step 1.1: Starting Point

**USE AskUserQuestion:**
```
questions: [{
  question: "Welcome to OPAL! How would you like to set up your knowledge base?",
  header: "Setup Mode",
  options: [
    {label: "Guide me (Recommended)", description: "Answer a few questions and I'll suggest a configuration"},
    {label: "Use a template", description: "Start from a pre-built configuration"},
    {label: "Import existing files", description: "Analyze your current files and generate a schema"},
    {label: "Minimal setup", description: "Just the basics, I'll configure as I go"}
  ]
}]
```

**WAIT FOR RESPONSE.**

- If "Guide me" → Continue to Step 1.2
- If "Use a template" → Jump to Template Flow
- If "Import existing" → Jump to Import Flow
- If "Minimal setup" → Jump to Minimal Flow

#### Step 1.2: Primary Use Case

**USE AskUserQuestion:**
```
questions: [{
  question: "What best describes what you'll be organizing?",
  header: "Use Case",
  options: [
    {label: "Personal knowledge", description: "Notes, ideas, things I'm learning"},
    {label: "Work & projects", description: "Meetings, clients, deliverables"},
    {label: "Research", description: "Papers, sources, citations"},
    {label: "Community knowledge", description: "Shared patterns, protocols, resources"}
  ]
}]
```

**WAIT FOR RESPONSE.** Store as `use_case`.

#### Step 1.3: Content Types Probe

Based on `use_case`, ask a targeted follow-up:

**For "Personal knowledge":**
```
questions: [{
  question: "What kinds of things do you capture? Select all that apply.",
  header: "Content",
  options: [
    {label: "Notes & ideas", description: "Quick thoughts, insights, connections"},
    {label: "Sources", description: "Books, articles, videos I learn from"},
    {label: "People", description: "People I learn from or want to remember"},
    {label: "Questions", description: "Things I'm curious about or researching"}
  ],
  multiSelect: true
}]
```

**For "Work & projects":**
```
questions: [{
  question: "What do you need to track? Select all that apply.",
  header: "Content",
  options: [
    {label: "Projects", description: "Work initiatives with timelines"},
    {label: "Meetings", description: "Notes from calls and discussions"},
    {label: "Clients/Contacts", description: "People and organizations you work with"},
    {label: "Documents", description: "Files, deliverables, references"}
  ],
  multiSelect: true
}]
```

**For "Research":**
```
questions: [{
  question: "What does your research involve? Select all that apply.",
  header: "Content",
  options: [
    {label: "Papers & articles", description: "Academic or professional literature"},
    {label: "Authors & researchers", description: "People whose work you follow"},
    {label: "Concepts & terms", description: "Domain-specific vocabulary"},
    {label: "Experiments & data", description: "Studies, datasets, findings"}
  ],
  multiSelect: true
}]
```

**For "Community knowledge":**
```
questions: [{
  question: "What kind of community knowledge? Select all that apply.",
  header: "Content",
  options: [
    {label: "Patterns & practices", description: "Reusable approaches and methods"},
    {label: "Protocols & processes", description: "Step-by-step procedures"},
    {label: "People & orgs", description: "Contributors and organizations"},
    {label: "Events & activities", description: "Gatherings, initiatives, grants"}
  ],
  multiSelect: true
}]
```

**WAIT FOR RESPONSE.** Store selections as `content_types`.

---

### Phase 2: Resource Types

**Goal:** Define what kinds of things the user will track. Use their Phase 1 answers to provide intelligent suggestions.

#### Step 2.1: Suggest Resource Types

Based on `use_case` and `content_types`, generate suggested resource types.

**Build suggestion list.** Example for "Work & projects" + ["Projects", "Meetings", "Clients"]:

```
Based on what you've told me, I suggest these resource types:

📁 Suggested Structure
━━━━━━━━━━━━━━━━━━━━━━

  projects/     → Track work initiatives
                  Fields: title, client, status, start_date, description

  meetings/     → Capture discussions and decisions
                  Fields: title, date, attendees, project, notes, action_items

  clients/      → Organizations you work with
                  Fields: name, industry, contacts, notes

  people/       → Individual contacts
                  Fields: name, role, organization, email, notes
```

**USE AskUserQuestion:**
```
questions: [{
  question: "Here's a suggested structure based on your needs. What would you like to do?",
  header: "Structure",
  options: [
    {label: "Looks good!", description: "Accept these resource types"},
    {label: "Add more types", description: "I need to track additional things"},
    {label: "Remove some", description: "This is more than I need"},
    {label: "Start over", description: "Let me describe what I need differently"}
  ]
}]
```

**WAIT FOR RESPONSE.**

- If "Looks good!" → Store types, continue to Step 2.3
- If "Add more types" → Go to Step 2.2
- If "Remove some" → Ask which to remove, then continue
- If "Start over" → Return to Phase 1

#### Step 2.2: Add Custom Types

**USE AskUserQuestion:**
```
questions: [{
  question: "What else do you want to track? Think about the NOUNS in your domain.",
  header: "Add Types",
  options: [
    {label: "Tasks/To-dos", description: "Action items and things to do"},
    {label: "Resources/Links", description: "URLs, articles, references"},
    {label: "Events", description: "Meetings, conferences, deadlines"},
    {label: "Notes/Ideas", description: "Freeform thoughts and insights"}
  ],
  multiSelect: true
}]
```

Note: User can also select "Other" to type custom types.

**WAIT FOR RESPONSE.** Add selected types to the list.

#### Step 2.3: Configure Each Type (With Smart Defaults)

For each resource type, provide intelligent field suggestions and let user approve/modify.

**For each type, display suggestion and ask:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Configuring: {type_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Directory: {type_name}s/

Suggested fields:
  • title (required) - The name of this {type}
  • {field2} - {description}
  • {field3} - {description}
  ...
```

**USE AskUserQuestion:**
```
questions: [{
  question: "How do these fields look for {type_name}?",
  header: "{Type}",
  options: [
    {label: "Perfect", description: "Use these fields as-is"},
    {label: "Add fields", description: "I need more fields"},
    {label: "Remove fields", description: "This is too detailed"},
    {label: "Skip this type", description: "I don't need {type_name} after all"}
  ]
}]
```

**WAIT FOR RESPONSE.** Process each type.

**If "Add fields":**
```
questions: [{
  question: "What additional fields do you need for {type_name}?",
  header: "Add Fields",
  options: [
    {label: "Tags/Categories", description: "Flexible labels for filtering"},
    {label: "Status", description: "Track state (draft, active, complete)"},
    {label: "Priority", description: "Importance level"},
    {label: "Due date", description: "Deadline or target date"}
  ],
  multiSelect: true
}]
```

---

### Phase 3: Dimensions (Cross-Cutting Categories)

**Goal:** Define ways to categorize across resource types. Suggest based on chosen types.

#### Step 3.1: Suggest Dimensions

Analyze the configured types. If any have status fields or similar, suggest dimensions.

```
📊 Cross-Type Categories (Dimensions)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dimensions let you filter across different types.
For example, "status" could apply to projects, meetings, AND tasks.

Based on your types, I suggest:

  status
  ├── Applies to: projects, tasks, documents
  └── Values: draft, active, on_hold, complete, archived

  priority
  ├── Applies to: projects, tasks
  └── Values: low, medium, high, urgent
```

**USE AskUserQuestion:**
```
questions: [{
  question: "Would you like to use these cross-type categories?",
  header: "Dimensions",
  options: [
    {label: "Yes, use both", description: "Add status and priority dimensions"},
    {label: "Just status", description: "I only need status tracking"},
    {label: "Just priority", description: "I only need priority levels"},
    {label: "Neither", description: "I'll categorize differently"},
    {label: "Skip for now", description: "I can add these later"}
  ]
}]
```

**WAIT FOR RESPONSE.** Store dimension configuration.

---

### Phase 4: Relationships

**Goal:** Define how types connect to each other. Auto-detect from reference fields.

#### Step 4.1: Detect and Suggest Relationships

Analyze types for reference fields (e.g., project → client, meeting → project).

```
🔗 Relationships Between Types
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I detected these connections based on your fields:

  project → client
  "A project belongs to a client"

  meeting → project
  "A meeting is about a project"

  meeting → person (attendees)
  "People attend meetings"

  task → project
  "Tasks are part of projects"
```

**USE AskUserQuestion:**
```
questions: [{
  question: "These relationships will help you navigate between connected items. Accept them?",
  header: "Relationships",
  options: [
    {label: "Accept all", description: "Use all suggested relationships"},
    {label: "Review each", description: "Let me approve one by one"},
    {label: "Skip relationships", description: "I'll manage connections manually"}
  ]
}]
```

**WAIT FOR RESPONSE.**

If "Review each", loop through each relationship with accept/reject.

---

### Phase 5: Content Sources

**Goal:** Configure where content will come from.

#### Step 5.1: Source Categories

**USE AskUserQuestion:**
```
questions: [{
  question: "Where will your content come from? Select all that apply.",
  header: "Sources",
  options: [
    {label: "Meeting recordings", description: "Transcripts from Otter, Fathom, Meetily, etc."},
    {label: "Chat apps", description: "Links from Telegram, Discord, Slack"},
    {label: "RSS/Blogs", description: "Articles from feeds you follow"},
    {label: "Files", description: "Documents from local folders or cloud storage"}
  ],
  multiSelect: true
}]
```

**WAIT FOR RESPONSE.** Store as `source_categories`.

#### Step 5.2: Configure Selected Sources

For each selected category, offer specific source options.

**If "Meeting recordings" selected:**
```
questions: [{
  question: "Which meeting transcription service do you use?",
  header: "Meetings",
  options: [
    {label: "Meetily", description: "Local transcription app (free)"},
    {label: "Otter.ai", description: "Cloud transcription service"},
    {label: "Fathom", description: "Video call transcription"},
    {label: "None yet", description: "I'll add this later"}
  ]
}]
```

**If "Chat apps" selected:**
```
questions: [{
  question: "Which chat app do you want to capture links from?",
  header: "Chat Links",
  options: [
    {label: "Telegram", description: "Monitor channels for shared links"},
    {label: "Discord", description: "Capture links from Discord channels"},
    {label: "Slack", description: "Watch Slack channels for links"},
    {label: "Skip for now", description: "I'll configure this later"}
  ]
}]
```

For each selection, note if it requires configuration (API keys, etc.) and offer to skip.

**USE AskUserQuestion for each source that needs setup:**
```
questions: [{
  question: "Telegram requires a bot token. Do you have one ready?",
  header: "Telegram Setup",
  options: [
    {label: "Yes, configure now", description: "I have my bot token ready"},
    {label: "Skip for now", description: "I'll set this up later with /sources add telegram"},
    {label: "How do I get one?", description: "Show me instructions"}
  ]
}]
```

---

### Phase 6: Review and Create

**Goal:** Show summary and confirm before creating files.

#### Step 6.1: Display Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 Configuration Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resource Types: {N}
  ├── projects/ (6 fields)
  ├── meetings/ (5 fields)
  ├── clients/ (4 fields)
  └── people/ (4 fields)

Dimensions: {N}
  ├── status: draft, active, complete, archived
  └── priority: low, medium, high, urgent

Relationships: {N}
  ├── project → client
  ├── meeting → project
  └── meeting → person

Sources: {N} configured
  ├── ✅ Meetily (ready)
  ├── ⏸️ Telegram (needs setup)
  └── ✅ RSS feeds (ready)

Will create:
  .opal/
  ├── config.yaml
  ├── schema.yaml
  ├── sources.yaml
  └── templates/ (4 templates)

  _inbox/, _staging/, _index/
  projects/, meetings/, clients/, people/
```

**USE AskUserQuestion:**
```
questions: [{
  question: "Ready to create your knowledge base?",
  header: "Confirm",
  options: [
    {label: "Create it!", description: "Generate configuration and directories"},
    {label: "Go back", description: "I want to change something"},
    {label: "Export only", description: "Show me the YAML files but don't create yet"},
    {label: "Cancel", description: "Exit without creating anything"}
  ]
}]
```

**WAIT FOR RESPONSE.**

- If "Create it!" → Proceed to creation
- If "Go back" → Ask what to change, return to appropriate phase
- If "Export only" → Display YAML content, then ask again
- If "Cancel" → Exit

#### Step 6.2: Create Configuration

**Action:** Use Write tool to create all configuration files.

1. Create `.opal/config.yaml`
2. Create `.opal/schema.yaml` with all types, dimensions, relationships
3. Create `.opal/sources.yaml` with configured sources
4. Create `.opal/templates/{type}.md` for each type
5. Create directories: `_inbox/`, `_staging/`, `_index/`, and type directories
6. Create `_index/entities.json` (empty)
7. Create `_index/pipeline-state.json` (empty)
8. Create `_index/sync-state.json` (empty)

**Output:**
```
✅ Creating your knowledge base...

  ✓ .opal/config.yaml
  ✓ .opal/schema.yaml
  ✓ .opal/sources.yaml
  ✓ .opal/templates/ (4 files)
  ✓ _inbox/, _staging/, _index/
  ✓ projects/, meetings/, clients/, people/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎉 Your knowledge base is ready!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quick Start:
  /sync      Pull content from configured sources
  /ingest    Add content manually
  /process   Analyze and extract entities
  /review    Review staged changes
  /status    See current state

Tip: Drop files into _inbox/ and run /process to get started!
```

---

## Template Flow

If user selected "Use a template" in Phase 1:

**USE AskUserQuestion:**
```
questions: [{
  question: "Which template fits your needs?",
  header: "Template",
  options: [
    {label: "Personal Notes (Zettelkasten)", description: "Notes, concepts, sources, questions"},
    {label: "Work & Projects", description: "Projects, meetings, clients, documents"},
    {label: "Research Library", description: "Papers, authors, citations, notes"},
    {label: "Community Commons", description: "Patterns, protocols, organizations"}
  ]
}]
```

**WAIT FOR RESPONSE.**

Then ask:
```
questions: [{
  question: "Would you like to customize this template or use it as-is?",
  header: "Customize",
  options: [
    {label: "Use as-is", description: "Create with default settings"},
    {label: "Customize first", description: "Let me adjust types and fields"},
    {label: "See what's included", description: "Show me the details first"}
  ]
}]
```

- If "Use as-is" → Create from template directly
- If "Customize" → Load template as starting point, go to Phase 2
- If "See details" → Display template contents, ask again

---

## Import Flow

If user selected "Import existing files":

1. Ask for path or use current directory
2. Use Glob to scan for `.md`, `.pdf`, `.txt` files
3. Analyze frontmatter to detect existing types/fields
4. Generate suggested schema from detected structure
5. Present for approval/modification using AskUserQuestion

---

## Minimal Flow

If user selected "Minimal setup":

Create only:
- `.opal/config.yaml` (basic)
- `.opal/schema.yaml` with just `notes` type
- `_inbox/`, `_staging/`, `_index/`, `notes/`

```
✅ Minimal setup complete!

Created a simple structure with just notes/.
Add more types anytime with /setup --reconfigure.
```

---

## Error Handling

If any step fails:
1. Report the error clearly
2. Use AskUserQuestion to offer recovery options:
   - Retry
   - Skip this step
   - Abort setup

---

## Interactive Setup Wizard

### Step 1: Starting Point

```
/setup

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Welcome to OPAL - Your Knowledge Toolkit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPAL helps you collect, organize, and connect your knowledge.
It works with any structure you define.

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

### Step 2a: Choose Template

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What kind of knowledge are you managing?

Personal & Learning
───────────────────
  [1] Personal Knowledge Garden (zettelkasten)
      Notes, ideas, connections. Zettelkasten-inspired.
      → notes, concepts, sources, people, questions

  [2] Life Archive
      Memories, relationships, personal history.
      → memories, people, places, events, artifacts, journal

  [3] Research Library
      Academic work, papers, citations.
      → papers, authors, concepts, notes, projects

Work & Projects
───────────────
  [4] Project Documentation
      Work projects, meetings, decisions.
      → projects, meetings, decisions, tasks, people

  [5] Creative Portfolio
      Works, ideas, inspirations.
      → works, ideas, inspirations, references, collections

Community & Civic
─────────────────
  [6] Open Protocol Library
      Civic patterns, protocols, playbooks.
      → patterns, protocols, playbooks, people, organizations

  [7] Activity Index
      Events, grants, initiatives.
      → grants, gatherings, initiatives, courses, alliances

Ecological & Regenerative
─────────────────────────
  [8] Regen Network
      Carbon credits, methodologies, ecological projects.
      KOI-compatible for federation with Regen knowledge commons.
      → methodologies, credit_classes, projects, claims, evidence

Minimal
───────
  [9] Minimal
      Just notes. Build from there.
      → notes

Choice:
```

### Step 2b: Build From Scratch (Schema Design)

```
Choice: 2 (Build from scratch)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Schema Design Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Let's design your knowledge structure. I'll guide you through:
  1. Resource Types - What kinds of things you track
  2. Fields - What information each type contains
  3. Dimensions - How you categorize across types
  4. Relationships - How things connect

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 1: Resource Types
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What kinds of things will you track?

Think about the NOUNS in your knowledge domain:
  • People you learn from or work with
  • Documents, articles, or sources
  • Projects or initiatives
  • Ideas, notes, or insights
  • Events or activities

Examples by domain:
  • Recipes app: recipes, ingredients, restaurants, cookbooks
  • Book notes: books, authors, quotes, insights
  • Research: papers, authors, datasets, experiments
  • Business: clients, projects, meetings, documents

Enter your resource types (comma-separated):
> projects, clients, meetings, documents, people

Great! Let me help you define each one.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Defining: Project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/5] Project

Basic Info:
  • Display name? [Project]
  • Plural form? [Projects]
  • Description? [Work initiatives and engagements]

Directory Structure:
  Where should projects live?

  Recommendations:
  ├── projects/          # Simple, flat structure
  ├── work/projects/     # Nested under category
  └── clients/{client}/  # Organized by relationship

  Directory path: [projects/]
  > projects/

Fields (what info does a project have?):

  Common fields for projects:
  ✓ title (always included)
  [ ] client - Link to client (reference)
  [ ] status - Current state (dimension)
  [ ] start_date - When it began
  [ ] end_date - When it completed
  [ ] budget - Financial info
  [ ] description - Details

  Toggle fields (space), or add custom:
  > title, client, status, start_date, description, deliverables

  Custom field "deliverables":
    Type? [text/list/date/number/reference]: list
    Description? [Key outputs and milestones]

  ✓ Project configured
    Directory: projects/
    Fields: 6

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Defining: Client
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2/5] Client

Basic Info:
  • Display name? [Client]
  • Plural form? [Clients]
  • Description? [Organizations I work with]

Directory Structure:
  Directory path: [clients/]
  > clients/

Fields:
  > name, industry, website, contacts, notes

  ✓ Client configured
    Directory: clients/
    Fields: 5

[Continue for meetings, documents, people...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 2: Dimensions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dimensions are ways to categorize ACROSS resource types.

For example, "status" might apply to:
  • Projects: planning → active → complete → archived
  • Documents: draft → review → final → archived
  • Meetings: scheduled → completed → cancelled

This lets you ask: "Show me everything that's archived"

Based on your resource types, I suggest:

  [1] status
      Values: planning, active, on_hold, complete, archived
      Applies to: project, document, meeting

  [2] priority
      Values: low, medium, high, urgent
      Applies to: project, document

Add these dimensions? [Y/n/customize]

Add another dimension?
  • Name: client_type
  • Values: enterprise, startup, nonprofit, individual
  • Applies to: client

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 3: Relationships
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Relationships connect your resource types.

I detected these potential relationships:

  [1] project → client (belongs_to)
      "A project belongs to a client"

  [2] meeting → project (part_of)
      "A meeting is part of a project"

  [3] document → project (relates_to)
      "A document relates to a project"

  [4] person → client (works_at)
      "A person works at a client"

Accept these? [Y/n/customize]

Add custom relationship?
  • Name: attended_by
  • From: meeting → person
  • Bidirectional? [y/N] n
  • Inverse name: attended

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 4: Directory Structure Review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Here's your proposed directory structure:

  my-knowledge-base/
  │
  ├── .opal/                  # Configuration (hidden)
  │   ├── config.yaml
  │   ├── schema.yaml
  │   ├── sources.yaml
  │   └── templates/
  │       ├── project.md
  │       ├── client.md
  │       ├── meeting.md
  │       ├── document.md
  │       └── person.md
  │
  ├── _inbox/                 # Incoming content
  ├── _staging/               # Pending review
  ├── _index/                 # Search index
  │
  ├── projects/               # Your projects
  ├── clients/                # Your clients
  ├── meetings/               # Meeting notes
  ├── documents/              # Documents
  └── people/                 # People directory

Directory Structure Best Practices:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Flat by default - Easier to navigate and link
✓ Consistent naming - All lowercase, hyphens for spaces
✓ One directory per type - Clear organization
✓ No deep nesting - 1-2 levels maximum

Alternative Structures:
  [1] Current (flat by type) ← Recommended
  [2] By client: clients/{client}/projects/, clients/{client}/meetings/
  [3] By date: 2026/projects/, 2026/meetings/
  [4] Hybrid: active/, archive/

Keep current structure? [Y/n/2/3/4]
```

### Step 3: Content Sources

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Content Sources
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Where will your content come from?

OPAL can automatically pull content from many sources.
Select the ones you use (configure details later):

Transcripts (meeting recordings)
  [ ] Meetily - Local transcription (no cloud)
  [ ] Fathom - Video call transcripts
  [ ] Otter.ai - Meeting transcripts
  [ ] Read.ai - Meeting transcripts

Links & Articles
  [ ] Telegram - Links from channels
  [ ] RSS Feeds - Subscribe to blogs/news
  [ ] URL Watch - Monitor specific pages

Media
  [ ] YouTube - Video transcripts
  [ ] Podcasts - Audio transcription

Documents
  [ ] Local folders - Watch directories
  [ ] Google Drive - Monitor folders
  [ ] Notion - Export databases

Manual
  [✓] Manual - Add content yourself (always available)

Toggle with space, Enter when done:

Selected: Meetily, Telegram, RSS Feeds, Local folders

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Configure: Meetily
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Meetily stores transcripts in a local SQLite database.
OPAL reads directly from this database (no API needed).

Checking for Meetily...
✓ Found database at:
  ~/Library/Application Support/com.meetily.ai/meeting_minutes.sqlite

Options:
  • Minimum meeting duration to sync? [5 minutes]
  • Exclude meetings containing: [standup, 1:1, daily]
  • Auto-sync on /sync command? [Y/n]

Where should meeting transcripts go?
  Based on your schema, I suggest: meetings/
  Or create new inbox subdirectory: _inbox/meetings/

  [1] meetings/ - Process directly into meetings
  [2] _inbox/meetings/ - Stage for review first (recommended)

Choice: 2

✅ Meetily configured
   Source: Local SQLite database
   Output: _inbox/meetings/
   Filter: >5min, exclude standup/1:1/daily

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Configure: Telegram
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Telegram can monitor channels for shared links.

To set up Telegram:
  1. Create a bot via @BotFather
  2. Add the bot to channels you want to monitor
  3. Set your bot token

Bot token configured? [y/N]
> n

Skipping Telegram for now.
Run /sources add telegram later to configure.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Configure: RSS Feeds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Subscribe to RSS/Atom feeds to automatically pull articles.

Add feeds now, or later with /sources add rss

Add a feed URL (or Enter to skip):
> https://blog.example.com/feed

Checking... ✅ Valid RSS feed
  Title: Example Blog
  Items: 47 articles

Add another feed? [y/N]
> n

✅ RSS configured
   Feeds: 1
   Schedule: Every 2 hours
   Output: _inbox/feeds/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Configure: Local Folders
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Watch local folders for new files.

What folders should OPAL watch?

  Suggested:
  [ ] ~/Downloads/*.pdf - PDFs from downloads
  [ ] ~/Documents/OPAL/ - Dedicated folder

  Custom path:
  > ~/Dropbox/Research/*.pdf

File types to watch: [pdf, md, txt, docx]

✅ Filesystem watching configured
   Watching: ~/Dropbox/Research/*.pdf
   Output: _inbox/documents/
```

### Step 4: Generate Structure

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Ready to Create!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Configuration Summary:

  Schema:
    Resource types: 5 (project, client, meeting, document, person)
    Dimensions: 2 (status, client_type)
    Relationships: 5

  Sources:
    ✓ Meetily (local transcription)
    ✓ RSS (1 feed)
    ✓ Filesystem (1 watch path)
    ○ Telegram (not configured)

  Structure:
    projects/
    clients/
    meetings/
    documents/
    people/

Will create:

  .opal/
  ├── config.yaml           # Main configuration
  ├── schema.yaml           # Your knowledge schema
  ├── sources.yaml          # Content sources
  └── templates/            # Templates for each type
      ├── project.md
      ├── client.md
      ├── meeting.md
      ├── document.md
      └── person.md

  _inbox/                   # Incoming content
  ├── meetings/             # From Meetily
  ├── feeds/                # From RSS
  └── documents/            # From filesystem

  _staging/                 # Pending review
  _index/                   # Search index

  projects/                 # Your projects
  clients/                  # Your clients
  meetings/                 # Meeting notes
  documents/                # Documents
  people/                   # People directory

Create this structure? [Y/n]
```

### Step 5: Complete

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Knowledge Base Created!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your configuration:
  Schema:    .opal/schema.yaml
  Sources:   .opal/sources.yaml
  Templates: .opal/templates/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quick Start Guide:

  1. SYNC content from sources
     /sync                    # Pull from Meetily, RSS, etc.

  2. ADD content manually
     Drop files in _inbox/
     Or use /ingest <file>

  3. PROCESS the inbox
     /process                 # Analyze and extract entities

  4. REVIEW staged changes
     /review                  # Accept, edit, or reject

  5. SEARCH your knowledge
     /search <query>
     /ask <question>

  6. ADD more sources later
     /sources add telegram
     /sources add rss <url>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Helpful Commands:
  /status           See current state
  /sources          Manage content sources
  /help             Get assistance

Ready to go! Try /sync to pull your first content.
```

---

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

---

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

Ecological & Regenerative
  regen            Regen Network (methodologies, credits, projects, claims)
                   KOI-compatible for knowledge federation

Use: /setup --template <name>
```

---

## Import Existing Structure

Analyze existing files:

```
/setup --import .

Analyzing current directory...

Found:
  • 156 markdown files
  • 23 PDFs
  • Frontmatter in 89 files

Detected structure:
  notes/        → 67 files (fields: title, tags, date)
  projects/     → 23 files (fields: title, status, client)
  references/   → 45 files (fields: title, author, url)
  journal/      → 21 files (fields: date, mood)

Suggested Schema:

  resource_types:
    - note (67 files in notes/)
    - project (23 files in projects/)
    - reference (45 files in references/)
    - journal_entry (21 files in journal/)

  dimensions:
    - status: draft, active, complete, archived
    - client: (12 unique values from projects)

  relationships:
    - project → client (detected in 18 files)
    - note → reference (detected in 34 files)

Accept this schema? [Y/n/edit]
> y

Generating configuration...
✅ Created .opal/schema.yaml
✅ Created .opal/config.yaml
✅ Created .opal/sources.yaml

Your existing files are ready to use!

Next steps:
  /process --reindex    Build search index from existing files
  /sources add          Configure content sources
```

---

## Notion Import

Import an existing Notion workspace export to bootstrap your OPAL schema.

### Step 1: Export from Notion

1. Open Notion → Settings → Export
2. Choose **Markdown & CSV** format
3. Select **Include subpages**
4. Download and unzip the export

### Step 2: Import to OPAL

```
/setup --import-notion ~/Downloads/Notion-Export/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Notion Import Wizard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analyzing Notion export at: ~/Downloads/Notion-Export/

Found:
  • 342 markdown files
  • 15 directories (potential databases)
  • 89 CSV files (database exports)
  • 156 embedded images

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Detected Notion Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Notion Databases Detected:

  [1] Projects (45 pages)
      │ CSV: Projects abc123.csv
      ├── Properties: Name, Status, Client, Due Date, Priority
      ├── Status values: Planning, Active, On Hold, Complete
      └── Suggested OPAL type: project

  [2] People (78 pages)
      │ CSV: People def456.csv
      ├── Properties: Name, Email, Company, Role, Notes
      └── Suggested OPAL type: person

  [3] Meeting Notes (123 pages)
      │ CSV: Meeting Notes ghi789.csv
      ├── Properties: Title, Date, Attendees, Project, Action Items
      ├── Attendees → links to People database
      ├── Project → links to Projects database
      └── Suggested OPAL type: meeting

  [4] Resources (56 pages)
      │ CSV: Resources jkl012.csv
      ├── Properties: Title, URL, Type, Tags, Notes
      ├── Type values: Article, Video, Book, Tool
      └── Suggested OPAL type: resource

  [5] Journal (40 pages)
      │ No CSV (inline database or pages)
      ├── Detected fields: date (from filename), content
      └── Suggested OPAL type: journal_entry

Standalone Pages: 23 (will become notes)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Proposed Schema
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on your Notion structure, I suggest:

Resource Types:
  ┌─────────────┬────────────────┬───────┬─────────────────────────────┐
  │ Type        │ From Notion    │ Count │ Fields                      │
  ├─────────────┼────────────────┼───────┼─────────────────────────────┤
  │ project     │ Projects       │ 45    │ title, status, client, due  │
  │ person      │ People         │ 78    │ name, email, company, role  │
  │ meeting     │ Meeting Notes  │ 123   │ title, date, attendees      │
  │ resource    │ Resources      │ 56    │ title, url, type, tags      │
  │ journal     │ Journal        │ 40    │ date, content               │
  │ note        │ (standalone)   │ 23    │ title, content, tags        │
  └─────────────┴────────────────┴───────┴─────────────────────────────┘

Dimensions:
  • status: planning, active, on_hold, complete (from Projects)
  • priority: low, medium, high, urgent (from Projects)
  • resource_type: article, video, book, tool (from Resources)

Relationships:
  • meeting → project (123 links detected)
  • meeting → person (attendees, 456 links)
  • project → person (client contacts, 89 links)
  • resource → project (34 links)

Accept this schema? [Y/n/customize]
> y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Import Options
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

How should I handle the Notion content?

  [1] Copy files (recommended)
      Copy markdown files to OPAL directories
      ✓ Preserves original Notion export
      ✓ Files organized by detected type

  [2] Move files
      Move files from Notion export to OPAL
      ⚠️ Modifies original export

  [3] Link only (schema only)
      Just create schema from Notion structure
      Content stays in original location

Choice: 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Processing Notion Export
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Converting Notion pages...

[1/5] Projects (45 pages)
      ├── Converting CSV properties to YAML frontmatter
      ├── Fixing Notion-style links → OPAL wiki-links
      ├── Cleaning up Notion IDs from filenames
      └── ✅ Copied to projects/

[2/5] People (78 pages)
      ├── Converting properties to frontmatter
      ├── Extracting profile info from page content
      └── ✅ Copied to people/

[3/5] Meeting Notes (123 pages)
      ├── Converting date formats
      ├── Converting @mentions to [[person]] links
      ├── Preserving action item checkboxes
      └── ✅ Copied to meetings/

[4/5] Resources (56 pages)
      ├── Validating URLs
      ├── Adding fetched metadata where missing
      └── ✅ Copied to resources/

[5/5] Journal + Standalone (63 pages)
      ├── Parsing dates from filenames
      ├── journal/ → journal entries (40)
      ├── Other → notes (23)
      └── ✅ Copied to journal/ and notes/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Link Conversion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Converting Notion links to OPAL format...

Notion format:  [Project Name](Projects%20abc123/Project%20Name%20def456.md)
OPAL format:    [[projects/project-name]]

Converted: 892 internal links
Preserved: 156 external URLs
Broken links: 3 (logged to _import/broken-links.log)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Notion Import Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created:
  .opal/
  ├── config.yaml         # Configuration
  ├── schema.yaml         # Schema from Notion structure
  ├── sources.yaml        # Sources (Notion sync enabled)
  └── templates/          # Templates for each type

Imported:
  ├── projects/           # 45 files
  ├── people/             # 78 files
  ├── meetings/           # 123 files
  ├── resources/          # 56 files
  ├── journal/            # 40 files
  └── notes/              # 23 files

Total: 365 files imported

Import log: _import/notion-import.log
Broken links: _import/broken-links.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:

  1. REVIEW the imported content
     ls projects/ | head -10

  2. BUILD the search index
     /process --reindex

  3. SET UP ongoing Notion sync (optional)
     /sources edit notion
     # Configure to sync changes from Notion

  4. ADD other content sources
     /sources add meetily
     /sources add telegram

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Notion Import Options

```
/setup --import-notion <path> [options]

Options:
  --schema-only       Only create schema, don't copy files
  --no-convert        Don't convert Notion links to wiki-links
  --preserve-ids      Keep Notion IDs in filenames
  --dry-run           Preview import without changes
  --merge             Merge with existing OPAL content
```

### Handling Notion-Specific Features

**Databases → Resource Types**
- Notion databases become OPAL resource types
- CSV exports provide property schemas
- Relations become OPAL relationships

**Properties → Fields**
- Text, Number, Date → Direct mapping
- Select, Multi-select → Dimensions or tags
- Person → Reference to people type
- Relation → Reference to linked type
- Formula, Rollup → Computed (not imported)

**Links**
- `[Page](Page%20abc123.md)` → `[[type/page-name]]`
- `@mentions` → `[[people/person-name]]`
- External URLs → Preserved as-is

**Embedded Content**
- Images → Copied to `_assets/`
- Files → Copied to `_attachments/`
- Embeds (videos, etc.) → Converted to links

---

## Reconfigure Existing Setup

```
/setup --reconfigure

Current Configuration
━━━━━━━━━━━━━━━━━━━━━

  Template: custom (built from scratch)
  Resource types: 5
  Dimensions: 2
  Sources: 3 enabled

What would you like to change?

  Schema
  ──────
  [1] Add resource types
  [2] Remove resource types
  [3] Modify fields
  [4] Add/modify dimensions
  [5] Add/modify relationships

  Sources
  ───────
  [6] Add content source
  [7] Remove content source
  [8] Configure existing source

  Structure
  ─────────
  [9] Change directory structure
  [10] Rename directories

  Other
  ─────
  [11] View current schema
  [12] Export configuration
  [13] Reset to template

Choice:
```

---

## Configuration Files Reference

### .opal/config.yaml

```yaml
# OPAL Configuration
version: "2.0"
name: "My Knowledge Base"
created: 2026-02-02

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
name: "My Knowledge Base"
version: "1.0"

resource_types:
  - id: project
    name: Project
    plural: Projects
    directory: projects/
    description: Work initiatives
    template: project.md
    fields:
      - name: title
        type: string
        required: true
      - name: client
        type: reference
        to: client
      - name: status
        type: dimension
        dimension: status

dimensions:
  - id: status
    name: Status
    values:
      - id: planning
        name: Planning
      - id: active
        name: Active
      - id: complete
        name: Complete

relationships:
  - id: belongs_to
    name: Belongs To
    inverse: has
```

### .opal/sources.yaml

```yaml
# Content Sources
sources:
  meetily:
    enabled: true
    database: auto
    output: _inbox/meetings/
    filters:
      min_duration_minutes: 5

  rss:
    enabled: true
    feeds:
      - url: https://blog.example.com/feed
        name: Example Blog
    output: _inbox/feeds/
```

---

## Related Commands

- `/profile` - Manage configuration profiles
- `/sources` - Manage content sources
- `/sync` - Pull content from sources
- `/process` - Process inbox content
- `/help` - Get help with OPAL
