---
description: Extract action items from a meeting note and optionally create tasks
allowed-tools: Read, Write, Edit
argument-hint: <path to meeting note>
---

# Extract Action Items

Scan a meeting transcript for commitments and tasks, create structured action items.

## Usage

Provide the path to a meeting note:
```
/extract-actions projects/opencivics/meetings/2024-01-07-planning.md
```

## Detection Patterns

Look for phrases indicating action items:
- "[Name] will [verb]..."
- "[Name] to [verb]..."
- "Action item: ..."
- "TODO: ..."
- "Next step: ..."
- "By [date], [name] should..."
- "Can you [verb]..." (implies commitment from addressee)

## Extraction Format

For each action item, extract:

| Field | Description |
|-------|-------------|
| task | The action to be taken |
| assignee | Person responsible (as wiki-link) |
| deadline | Due date if mentioned (ISO format) |
| context | Surrounding transcript excerpt |
| confidence | high, medium, or low |

## Confidence Levels

- **High**: Clear assignee + explicit deadline + action verb
- **Medium**: Assignee + action but no deadline
- **Low**: Vague reference to future work, unclear ownership

## Output

Add or update the Action Items section in the meeting note:

```markdown
## Action Items

- [ ] **[[people/Benjamin]]**: Draft technical spec *(due: 2024-01-14)* `high`
  > Context: "Benjamin will draft the TrustGraph technical spec by next week"

- [ ] **[[people/Jane]]**: Recruit 10 pilot participants *(due: 2024-01-21)* `high`
  > Context: "Jane, can you recruit pilot participants for the expert network?"

- [ ] **[[people/Team]]**: Review proposal `medium`
  > Context: "We should all review the proposal before the next meeting"
```

## After Extraction

1. Show summary of action items found
2. Ask if user wants to create tasks in external system (Notion, etc.)
3. Suggest running `/send-followups` to notify assignees

