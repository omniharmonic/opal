# /setup Command

Run the interactive setup wizard to configure OPAL.

## Usage

```
/setup                # Start fresh setup
/setup resume         # Resume incomplete setup
/setup reconfigure    # Modify existing configuration
/setup integrations   # Just configure integrations
/setup taxonomy       # Just configure taxonomy
```

## What It Does

The setup wizard guides you through:

1. **Mode Selection** - Personal, Team, or Commons
2. **Taxonomy Configuration** - Preset or custom
3. **Resource Types** - What you'll be organizing
4. **Classification** - How to categorize content
5. **Integrations** - Connect your tools
6. **Federation** - Link with other commons
7. **Generate** - Create all files

## Quick Start

```
/setup

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Welcome to OPAL Setup Wizard 🦉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'll help you configure your knowledge commons.
This takes about 5-10 minutes.

Let's start with a fundamental question:

How will you be using OPAL?

  1. Personal Knowledge Garden
     → For your own learning and research

  2. Team Knowledge Base
     → Shared among a defined group

  3. Open Knowledge Commons
     → Public, federated, democratically governed

Enter 1, 2, or 3 (or type to ask questions):
> 3

Great choice! Open Knowledge Commons means:
• GitHub as your source of truth
• Democratic PR moderation (3+ votes to merge)
• Public Notion frontend
• Federation with other commons

Let's continue...
```

## Resume Setup

If setup was interrupted:

```
/setup resume

📋 Resuming Setup Wizard
━━━━━━━━━━━━━━━━━━━━━━━━

Found incomplete setup from 2 hours ago.

Completed:
✅ Mode: Open Knowledge Commons
✅ Taxonomy: Open Protocol Library preset
✅ Resource Types: 7 configured

Remaining:
⬜ Classification dimensions
⬜ Integrations
⬜ Federation
⬜ Generate files

Continue from Classification? [Y/n]
> y
```

## Quick Integrations

Just set up integrations:

```
/setup integrations

🔌 Integration Setup
━━━━━━━━━━━━━━━━━━━━

Current integrations:
├── Notion: ✅ Configured
├── GitHub: ✅ Configured
├── Otter.ai: ⚠️ Not configured
├── Fathom: ⚠️ Not configured
└── Telegram: ⚠️ Not configured

Which would you like to configure?

  1. Otter.ai - Meeting transcripts
  2. Fathom - Video call transcripts
  3. Read.ai - Meeting transcripts
  4. Telegram - Link ingestion
  5. All unconfigured

Enter choice:
> 1

━━━━━━━━━━━━━━━━━━━━
Configuring Otter.ai
━━━━━━━━━━━━━━━━━━━━

To connect Otter.ai, I need your API key.
You can find it at: https://otter.ai/settings/api

Enter API key (or 'skip' to configure later):
> sk-otter-abc123...

Testing connection...
✅ Connected to Otter.ai!
   Account: benjamin@opencivics.co
   Workspaces: 2 found

Which workspaces should OPAL monitor?

  [x] Open Civics (default)
  [ ] Personal

Press Enter to confirm, or type to change:
>

✅ Otter.ai configured!
   Saved to: config/secrets.local
   Config: config/integrations.yaml
```

## Generated Files

After setup completes:

```
✅ Setup Complete!
━━━━━━━━━━━━━━━━━━

Created files:

Configuration:
├── config/settings.yaml
├── config/integrations.yaml
├── config/governance.yaml
├── config/llm.yaml
└── config/secrets.local (git-ignored)

Taxonomy:
└── taxonomy/opl.yaml

Templates:
├── _templates/pattern.md
├── _templates/protocol.md
├── _templates/playbook.md
├── _templates/primitive.md
├── _templates/artifact.md
├── _templates/person.md
└── _templates/organization.md

Directories:
├── _inbox/transcripts/
├── _inbox/links/
├── _inbox/documents/
├── _staging/new/
├── _staging/merges/
├── _staging/updates/
├── _index/
├── _federation/
├── patterns/
├── protocols/
├── playbooks/
└── ...

Initial files:
├── _index/entities.json
├── _index/pipeline-state.json
├── PROJECT.md
└── .gitignore

━━━━━━━━━━━━━━━━━━
Next steps:

1. Add any missing API keys to config/secrets.local
2. Run /ingest to add your first content
3. Run /process to start the pipeline
4. Run /help if you need guidance

Happy knowledge commoning! 📚
```

## Reconfiguration

Modify existing setup:

```
/setup reconfigure

⚙️ Reconfigure OPAL
━━━━━━━━━━━━━━━━━━

Current configuration:
├── Mode: Open Knowledge Commons
├── Taxonomy: Open Protocol Library
├── Resource Types: 7
├── Integrations: 3 active
└── Federation: 2 sources

What would you like to change?

  1. Switch mode (Personal/Team/Commons)
  2. Change taxonomy
  3. Add/remove resource types
  4. Update integrations
  5. Modify federation sources
  6. Update governance rules

Enter choice (or 'q' to quit):
>
```
