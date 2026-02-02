# /review Command

Review and approve staged changes before committing to the knowledge base.

## Usage

```
/review                    # Interactive review session
/review --list             # List staged items
/review --item <path>      # Review specific item
/review --approve-all      # Approve all (use with caution)
/review --type new         # Review only new entities
/review --type merge       # Review only merges
```

## What It Does

After `/process` stages changes, `/review` lets you:

1. **See proposed changes** - New entities, merges, updates
2. **Accept or reject** - Each change individually
3. **Edit before accepting** - Modify content
4. **Understand rationale** - See why changes were proposed

## Interactive Review Session

```
/review

📝 Review Session
━━━━━━━━━━━━━━━━━

8 items staged for review:
├── 4 new entities
├── 3 updates
└── 1 potential merge

Starting review...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1/8] NEW ENTITY: patterns/food-sovereignty.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source: food-council-2026-01-28.md
Confidence: 0.85

Preview:
┌─────────────────────────────────────────────
│ ---
│ type: pattern
│ name: Food Sovereignty
│ aliases: [food autonomy, community food control]
│ sectors: [environmental-sustainability, economic-resource-sharing]
│ scales: [neighborhood, bioregional]
│ ---
│
│ # Food Sovereignty
│
│ A framework for communities to control their own food systems,
│ including production, distribution, and consumption decisions...
│
│ ## Key Principles
│ - Local control over food policy
│ - Support for local producers
│ - Community-based food access
│ ...
└─────────────────────────────────────────────

Related existing entities:
• [[patterns/participatory-budgeting.md]] (related)
• [[organizations/bioregional-food-council.md]] (source)

Actions:
  [a] Accept - Add to knowledge base
  [r] Reject - Discard with reason
  [e] Edit   - Modify before accepting
  [s] Skip   - Review later
  [v] View   - See full content
  [?] Help   - Show options

Choice: a

✅ Accepted: patterns/food-sovereignty.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2/8] UPDATE: patterns/participatory-budgeting.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proposed changes:

+ Adding alias: "community budget process"
+ Adding related pattern: food-sovereignty
+ Adding mention from: food-council-2026-01-28.md

Diff preview:
┌─────────────────────────────────────────────
│ aliases:
│   - PB
│   - community budgeting
│ + - community budget process
│
│ related_patterns:
│   - consensus-decision-making
│ + - food-sovereignty
└─────────────────────────────────────────────

Actions: [a]ccept [r]eject [e]dit [s]kip [v]iew
Choice: a

✅ Accepted: Update to participatory-budgeting.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[5/8] MERGE: "Community Food Systems" → "Food Sovereignty"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proposed merge:

Source: "Community Food Systems" (newly extracted)
Target: "Food Sovereignty" (existing entity)

Confidence: 0.82
Rationale: Claude analysis indicates these describe the same
concept with different terminology.

Evidence:
• Source text: "community food systems approach to local production"
• Target desc: "framework for communities to control their own food"

If merged:
• "Community Food Systems" becomes alias of "Food Sovereignty"
• Source mentions get linked to target entity
• No content loss

Actions:
  [a] Accept merge
  [r] Reject - Keep as separate entities
  [e] Edit target before merging
  [s] Skip - Decide later

Choice: a

✅ Merged: "Community Food Systems" → patterns/food-sovereignty.md
   Added as alias to target entity
```

## List Staged Items

```
/review --list

📝 Staged Items
━━━━━━━━━━━━━━━

New entities (4):
├── _staging/new/patterns/food-sovereignty.md
├── _staging/new/protocols/seed-sharing-circle.md
├── _staging/new/people/elena-rodriguez.md
└── _staging/new/organizations/bioregional-food-council.md

Updates (3):
├── _staging/updates/participatory-budgeting.yaml
├── _staging/updates/sarah-chen.yaml
└── _staging/updates/community-garden-protocol.yaml

Merges (1):
└── _staging/merges/community-food-systems.yaml

Run /review to start reviewing.
```

## Batch Actions

```
# Approve all new entities (careful!)
/review --type new --approve-all

⚠️ About to approve 4 new entities:
├── patterns/food-sovereignty.md
├── protocols/seed-sharing-circle.md
├── people/elena-rodriguez.md
└── organizations/bioregional-food-council.md

Are you sure? This cannot be undone. [y/N]
> y

✅ Approved 4 new entities
   Ready for commit: /github commit
```

## After Review

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Review Session Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Results:
├── ✅ Accepted: 6
├── ❌ Rejected: 1
└── ⏭️ Skipped: 1

Rejected items moved to: _staging/rejected/
Skipped items remain in: _staging/

Ready to commit accepted changes.

Next steps:
• /github commit - Commit changes
• /github pr create - Create PR (commons mode)
• /review - Continue with skipped items
```

## Rejection Reasons

When rejecting, provide a reason:

```
Choice: r

Why are you rejecting this?
> Duplicate of existing entity, but merge confidence was too low

✅ Rejected: protocols/seed-sharing-circle.md
   Reason logged: "Duplicate of existing entity..."
   Moved to: _staging/rejected/seed-sharing-circle.md
```

## Edit Before Accept

```
Choice: e

Opening editor for: patterns/food-sovereignty.md

[Editor opens with content]

After editing, save and close.

Changes detected:
+ Added: "See also: [[patterns/agroecology]]"
+ Modified: Description expanded

Accept with these changes? [Y/n]
> y

✅ Accepted with edits: patterns/food-sovereignty.md
```
