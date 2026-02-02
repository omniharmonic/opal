# /process Command

Process items in the inbox through the knowledge pipeline.

## Usage

```
/process                    # Process all inbox items
/process --dry-run          # Preview what would happen
/process --item <path>      # Process specific item
/process --type transcript  # Process only transcripts
/process --limit 5          # Process up to 5 items
```

## What It Does

1. **Scans inbox** for items to process (`_inbox/` directory)
2. **Classifies** each item to determine type and routing
3. **Preprocesses** based on type (transcript cleanup, PDF conversion, etc.)
4. **Extracts entities** using Claude-powered domain-aware extraction
5. **Reconciles** against entity index for deduplication
6. **Stages** proposed changes for review
7. **Reports** summary of processing results

## Pipeline Flow

```
📥 _inbox/
    ├── transcripts/meeting-2026-01-15.md
    ├── links/telegram-link-001.md
    └── documents/paper.pdf
         │
         ▼
    [CLASSIFY] → Determine type, suggest category
         │
         ▼
    [PREPROCESS] → Clean, convert, prepare
         │
         ▼
    [EXTRACT] → Identify entities with Claude
         │
         ▼
    [RECONCILE] → Check for duplicates
         │
         ▼
📝 _staging/
    ├── new/patterns/food-sovereignty.md
    ├── merges/participatory-budgeting.yaml
    └── updates/sarah-chen.yaml
```

## Example Output

```
📚 Processing Inbox
━━━━━━━━━━━━━━━━━━

Found 3 items to process.

[1/3] transcripts/meeting-2026-01-15.md
      ├── Classified: transcript (confidence: 0.95)
      ├── Cleaned: 3,421 → 3,189 words (7% reduction)
      ├── Extracted: 12 entities, 5 relationships
      ├── Reconciled: 8 existing, 4 new, 0 merges
      └── ✅ Staged 4 new entities for review

[2/3] links/telegram-link-001.md
      ├── Classified: link → artifact (confidence: 0.8)
      ├── Fetched: "Community Land Trust Handbook" (PDF, 45 pages)
      ├── Extracted: 8 entities, 3 relationships
      ├── Reconciled: 6 existing, 2 new, 0 merges
      └── ✅ Staged 2 new entities for review

[3/3] documents/paper.pdf
      ├── Classified: document → artifact (confidence: 0.9)
      ├── Converted: PDF → Markdown (12,340 words)
      ├── Extracted: 23 entities, 12 relationships
      ├── Reconciled: 18 existing, 3 new, 2 potential merges
      └── ✅ Staged 5 items for review (3 new, 2 merges)

━━━━━━━━━━━━━━━━━━
Summary:
• Processed: 3 items
• New entities: 9
• Updates: 32
• Potential merges: 2
• Review needed: 11 items

Next: Run /review to review staged changes
```

## Dry Run Mode

```
/process --dry-run
```

Shows what would happen without making changes:

```
📚 Processing Preview (Dry Run)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would process 3 items:

[1] transcripts/meeting-2026-01-15.md
    → Would classify as: transcript
    → Would extract entities using: claude
    → Estimated new entities: 3-5

[2] links/telegram-link-001.md
    → Would classify as: link
    → Would fetch URL and convert
    → Estimated new entities: 1-3

[3] documents/paper.pdf
    → Would classify as: document
    → Would convert PDF (45 pages)
    → Estimated processing time: 2-3 minutes

Total estimated:
• Processing time: 5-8 minutes
• API calls: ~15 (Claude)
• New entities: 5-10

Run without --dry-run to proceed.
```

## Error Handling

```
⚠️ Processing Error

[2/3] links/telegram-link-001.md
      └── ❌ Failed: Could not fetch URL (404 Not Found)
          Action: Moved to _inbox/failed/
          Reason logged: _inbox/failed/telegram-link-001.error.log

Continuing with remaining items...
```

## Options Reference

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview without changes |
| `--item <path>` | Process specific item |
| `--type <type>` | Filter by content type |
| `--limit <n>` | Process up to n items |
| `--skip-reconcile` | Skip deduplication (faster, less accurate) |
| `--verbose` | Show detailed progress |
| `--quiet` | Minimal output |
