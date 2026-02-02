# /status Command

Show the current state of the knowledge commons.

## Usage

```
/status              # Full status overview
/status inbox        # Just inbox status
/status staging      # Just staging status
/status github       # GitHub and PR status
/status index        # Entity index statistics
/status integrations # Integration health
```

## Full Status Output

```
📚 OPAL Status Report
━━━━━━━━━━━━━━━━━━━━━

Mode: Commons (Open Protocol Library)
Repository: omniharmonic/open-protocol-library
Branch: main (up to date)
Last sync: 2 hours ago

📥 Inbox: 5 items awaiting processing
   ├── 3 transcripts (Otter, Fathom)
   ├── 2 links (Telegram)
   └── Oldest: 3 days ago

📝 Staging: 8 items awaiting review
   ├── 4 new entities
   ├── 3 updates to existing
   ├── 1 potential merge
   └── Ready for: /review

🔀 GitHub: 2 PRs pending
   ├── PR #42: Add participatory budgeting pattern
   │   └── Votes: 2/3 (needs 1 more) ⏳ 18h remaining
   └── PR #41: Update food sovereignty protocol
       └── Votes: 3/3 ✅ Ready to merge

📊 Entity Index
   ├── Total entities: 342
   ├── By type: 89 patterns, 45 protocols, 28 playbooks, 180 other
   ├── Last updated: 30 minutes ago
   └── Index health: ✅ Good

🔌 Integrations
   ├── Notion: ✅ Connected (last sync: 1h ago)
   ├── GitHub: ✅ Connected
   ├── Otter.ai: ✅ Connected (3 new transcripts)
   └── Telegram: ✅ Connected (2 new links)

━━━━━━━━━━━━━━━━━━━━━
Suggested actions:
• /process - Process 5 inbox items
• /review - Review 8 staged items
• /github vote 42 approve - Cast your vote
• /github merge 41 - Merge approved PR
```

## Inbox Status

```
/status inbox

📥 Inbox Status
━━━━━━━━━━━━━━━

Total: 5 items

By type:
├── transcripts/: 3 files
│   ├── food-council-2026-01-28.md (3 days old)
│   ├── bioregional-planning-2026-01-25.md (6 days old)
│   └── garden-workshop-2026-01-22.md (9 days old)
│
├── links/: 2 files
│   ├── telegram-2026-01-28-001.md (3 days old)
│   └── telegram-2026-01-27-003.md (4 days old)
│
└── documents/: 0 files

Recommendations:
• 2 items over 1 week old - consider processing soon
• Run /process to start pipeline
```

## Staging Status

```
/status staging

📝 Staging Status
━━━━━━━━━━━━━━━━━

Total: 8 items ready for review

New entities (4):
├── patterns/food-sovereignty.md
│   └── Extracted from: food-council-2026-01-28.md
├── protocols/seed-sharing-circle.md
│   └── Extracted from: garden-workshop-2026-01-22.md
├── people/elena-rodriguez.md
│   └── Mentioned in: 2 transcripts
└── organizations/bioregional-food-council.md
    └── Extracted from: food-council-2026-01-28.md

Updates (3):
├── patterns/participatory-budgeting.md
│   └── Adding: new mention, 2 relationships
├── people/sarah-chen.md
│   └── Adding: new role, organization link
└── protocols/community-garden-protocol.md
    └── Adding: 3 new steps from workshop

Merges (1):
└── "Community Food Systems" → "Food Sovereignty"
    └── Confidence: 0.82 (needs human review)

Run /review to process these items.
```

## GitHub Status

```
/status github

🔀 GitHub Status
━━━━━━━━━━━━━━━━

Repository: omniharmonic/open-protocol-library
Branch: main
Status: ✅ Up to date with remote

Open Pull Requests: 2

PR #42: Add participatory budgeting pattern
├── Author: @sarah-chen
├── Created: 3 days ago
├── Files: 2 changed (+145, -3)
├── Votes: ✅✅⬜ (2/3 required)
│   ├── @marcus-j: approved
│   └── @elena-r: approved
├── Deadline: 18 hours remaining
└── Action: /github vote 42 approve

PR #41: Update food sovereignty protocol
├── Author: @marcus-j
├── Created: 5 days ago
├── Files: 1 changed (+23, -8)
├── Votes: ✅✅✅ (3/3 required)
│   ├── @sarah-chen: approved
│   ├── @elena-r: approved
│   └── @ben-l: approved
└── Action: /github merge 41

Your pending reviews:
• PR #42 - awaiting your vote
```

## Integration Health

```
/status integrations

🔌 Integration Health
━━━━━━━━━━━━━━━━━━━━

Notion
├── Status: ✅ Connected
├── Workspace: Open Civic Commons
├── Last sync: 1 hour ago
├── Databases: 12 synced
└── Pending changes: 0

GitHub
├── Status: ✅ Connected
├── Repository: omniharmonic/open-protocol-library
├── Permissions: push, pull, admin
└── API calls remaining: 4,832/5,000

Otter.ai
├── Status: ✅ Connected
├── New transcripts: 3 available
├── Last check: 10 minutes ago
└── Quota: 42/100 hours this month

Fathom
├── Status: ⚠️ API key expiring
├── Expires: 7 days
├── New transcripts: 0
└── Action: Update API key in config/secrets.local

Telegram
├── Status: ✅ Connected
├── Bot: @opal_ingest_bot
├── Monitored channels: 3
└── New links: 2 available

Ollama
├── Status: ✅ Running
├── Endpoint: http://localhost:11434
├── Models: mistral:7b, llama3.2:7b
└── Used for: transcript cleanup, classification
```
