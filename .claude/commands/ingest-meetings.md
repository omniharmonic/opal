---
description: Process pending meetings from inbox - extract entities, create wiki links, generate summaries, route to projects
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
argument-hint: [optional: specific file to process]
---

# Ingest Meetings

Process meeting transcripts from the inbox, enrich them with wiki-links, extract entities, and route to project folders.

## Overview

This command transforms raw meeting transcripts into rich, interconnected knowledge base entries by:
1. Scanning for unprocessed transcripts across all sources
2. **Proposing project matches for user confirmation**
3. Extracting and creating entity files (people, concepts, organizations)
4. Adding wiki-links throughout the content
5. Routing to the appropriate project folder

---

## Workflow

### Step 1: Find Pending Files

Scan ALL transcript sources in the inbox:

```
vault/_inbox/transcripts/fathom/*.md
vault/_inbox/transcripts/meetily/*.md
vault/_inbox/transcripts/otter/*.md
vault/_inbox/transcripts/*.md
vault/_inbox/meetings/*.md
```

Use Glob to find all markdown files. Include files that:
- Have `source: fathom|meetily|otter|read-ai|manual` in frontmatter
- OR have no `status: processed` field
- OR have `status: pending_enrichment`

If `$ARGUMENTS` provided, process only that specific file.

### Step 2: Load Project Context

Read all `vault/projects/*/PROJECT.md` files to build matching context:

For each project, extract:
- Project title and slug (directory name)
- Collaborators (names and emails)
- Tags and keywords
- Organization links

Build a matching dictionary:
```
{
  "opencivics": {
    "slug": "opencivics",
    "title": "OpenCivics",
    "keywords": ["opencivics", "civic innovation", "consortium", "delegate council", "managers council"],
    "people": ["Tim Archer", "Patricia Parkinson"],
    "emails": ["patricia@opencivics.co", "tim@..."]
  },
  ...
}
```

### Step 3: Propose Project Matches (INTERACTIVE)

**CRITICAL: Get user confirmation before processing.**

For each meeting file:
1. Scan title and attendees for project signals
2. Score against each project using the matching rules
3. Classify as High (>=8), Medium (4-7), Low (<4), or External

Present the matches in a **markdown table** sorted by:
1. **Confidence level** (High -> Medium -> Unclear -> External)
2. **Project** (clustered together within each confidence level)
3. **Date** (most recent first within each cluster)

```
PROJECT MATCHING PROPOSAL

HIGH CONFIDENCE
| Date | Meeting | Project |
|------|---------|---------|
| Jan 20 | OpenCivics General Assembly | opencivics |
| Jan 19 | OpenCivics Weekly Kick Off | opencivics |
| Jan 12 | OpenCivics Weekly Kick Off | opencivics |
| Jan 12 | Stefan x OpenCivics | opencivics |
| Feb 6 | Regen Commons | Identity & Presence | regen-commons |
| Feb 5 | Regen Commons | Steward Council | regen-commons |
| ... | ... | ... |

MEDIUM CONFIDENCE
| Date | Meeting | Project |
|------|---------|---------|
| Feb 3 | TrustGraph / Team Agreements | opencivics |
| ... | ... | ... |

UNCLEAR (need assignment)
| Date | Meeting | Proposed |
|------|---------|----------|
| Feb 6 | Category Research pt 2 | ??? |
| ... | ... | ... |

EXTERNAL (no project)
| Date | Meeting |
|------|---------|
| Jan 14 | Dialogue (Frank Sanborn) |
| ... | ... |

Legend:
  High — Auto-approve if user selects "Approve High" or "Approve Medium"
  Medium — Auto-approve if user selects "Approve Medium", otherwise ask
  Unclear — Always ask user to assign manually
  External — Route to vault/meetings/ (no project match)
```

Then use AskUserQuestion to get approval:

**Question:** "How would you like to handle project assignments?"
**Options:**
- **Approve High** — Auto-approve high-confidence matches only; I'll ask about the rest
- **Approve Medium** — Auto-approve high + medium confidence; I'll ask about low/unclear
- **Manual** — Walk me through each meeting assignment one by one

Based on the user's choice:
- If "Approve High": Process high-confidence, then ask about each medium/low/unclear
- If "Approve Medium": Process high + medium, then ask about low/unclear
- If "Manual": Ask about every single meeting

For meetings needing manual assignment, use AskUserQuestion with the available projects as options (plus "External/No project" and "Skip").

### Step 4: Process Each Approved Meeting

For each meeting with a confirmed project assignment:

---

## Entity Extraction (CRITICAL)

Analyze the transcript and identify ALL entities:

### People
- Names mentioned in speech
- Email addresses referenced
- Speakers in the conversation
- Anyone assigned action items

### Organizations
- Companies mentioned
- Institutions referenced
- Partner organizations

### Concepts
- Technical terms discussed
- Methodologies mentioned
- Frameworks referenced
- Domain-specific terminology

### Tools/Platforms
- Software tools discussed
- Platforms mentioned
- Services referenced

**Output a list of all extracted entities with their type.**

---

## Entity File Creation

### For Each Person

Check if `vault/people/{Name}.md` exists. If not, create using the person template:

```markdown
---
title: "{Full Name}"
type: person
role: "{if mentioned}"
organizations:
  - "[[vault/organizations/{Org}]]"
projects:
  - "[[vault/projects/{project}]]"
contact:
  email: "{if known}"
  phone: ""
location: ""
first-met: "[[{path to this meeting}]]"
last-contact: "{meeting date}"
tags: []
---

# {Full Name}

## Context

First encountered in [[{path to this meeting}]]. {Brief note about role/context.}

## Relationship Notes


## Commitments

### Theirs to Me


### Mine to Them

```

### For Each Concept

Check if `wiki/concepts/{Concept}.md` exists. If not, create:

```markdown
---
title: "{Concept Name}"
type: concept
visibility: public
aliases:
  - "{any alternative names}"
related: []
tags: []
created: "{meeting date}"
updated: "{meeting date}"
---

# {Concept Name}

## Definition

{Brief definition based on meeting context, or leave as TODO}

## Significance


## Related Concepts


## References

- First mentioned in [[{path to this meeting}]]
```

### For Each Organization

Check if `vault/organizations/{Org}.md` exists. If not, create:

```markdown
---
title: "{Organization Name}"
type: organization
status: active
url: "{if mentioned}"
role: ""
people: []
projects: []
tags: []
---

# {Organization Name}

## Overview

{Brief description based on context}

## Structure


## My Involvement

First encountered in [[{path to this meeting}]].
```

---

## Meeting File Enrichment

Transform the meeting file to have this structure:

```markdown
---
title: "{Cleaned descriptive title}"
type: meeting
date: "{ISO date}"
projects:
  - "[[vault/projects/{matched}]]"
attendees:
  - "[[vault/people/Person One]]"
  - "[[vault/people/Person Two]]"
source: fathom
status: processed
themes:
  - {theme-1}
  - {theme-2}
tags:
  - meeting
  - {project-slug}
processed_at: "{current ISO timestamp}"
confidence: {high|medium|low}
---

# {Meeting Title}

> **Project:** [[vault/projects/{project}]]
> **Date:** {formatted date}
> **Participants:** [[vault/people/Person One|First]], [[vault/people/Person Two|First]]

## Summary

{Keep existing summary from Fathom/Meetily, or generate from transcript}

## Key Insights

- {Most important insight or decision}
- {Second key insight}
- {Third key insight}

## Action Items

- [ ] {Action item 1} - @[[vault/people/Assignee|Name]] (due: {date if mentioned})
- [ ] {Action item 2} - @[[vault/people/Assignee|Name]]

## Decisions Made

- {Decision 1 and its context}

## Topics Discussed

### {Topic 1}

{Brief summary with [[wiki-links]] to relevant concepts}

## Next Steps

- {Next step 1}
- {Next step 2}

---

## Full Transcript

{Original transcript with wiki-links added for first occurrence of:
- People -> [[vault/people/Name|FirstName]]
- Projects -> [[vault/projects/slug|Display Name]]
- Concepts -> [[wiki/concepts/Term]]
- Organizations -> [[vault/organizations/Name]]
}
```

---

## Wiki-Linking Rules

### What to Link
- **People:** First mention of each person -> `[[vault/people/Full Name|First Name]]`
- **Projects:** Project names/aliases -> `[[vault/projects/slug|Display Name]]`
- **Concepts:** Technical terms, methodologies -> `[[wiki/concepts/Term]]`
- **Organizations:** Companies, institutions -> `[[vault/organizations/Name]]`

### Linking Guidelines
- Link first occurrence only (don't over-link)
- Maximum 15-20 links per document
- Don't link common words or obvious terms
- Preserve original text in display: `[[vault/people/Benjamin Life|Benjamin]]`
- Skip linking inside code blocks or quotes

---

## Project Matching Scoring

Score each project based on content:

| Signal | Weight |
|--------|--------|
| Project name in title | +5 |
| Project name in content | +3 |
| Project alias mentioned | +4 |
| Team member as attendee | +3 |
| Team member name in transcript | +2 |
| Project keyword found | +2 |
| Project tag found | +1 |

**Thresholds:**
- >=8 points: **High confidence** -> auto-route if user approves
- 4-7 points: **Medium confidence** -> ask user to confirm
- <4 points: **Low/Unclear** -> manual assignment needed
- External signals (non-project emails, external org names): **External** -> route to `vault/meetings/`

---

## File Placement

After enrichment, move the file:

**If project matched:**
```
vault/projects/{project-slug}/meetings/YYYY-MM-DD_{descriptive-slug}.md
```

**If no project (external):**
```
vault/meetings/YYYY-MM-DD/{descriptive-slug}.md
```

Create the destination directory if it doesn't exist.

---

## Quality Checklist

Before marking a meeting complete, verify:
- [ ] Summary section is populated
- [ ] Key Insights has 2-5 items
- [ ] Action Items extracted (if any mentioned)
- [ ] All participants have wiki-links
- [ ] Person files created for new people
- [ ] Concept files created for key terms
- [ ] Project correctly matched
- [ ] File moved to destination folder
- [ ] Status updated to `processed`

---

## Example Output

After processing batch:

```
INGEST COMPLETE
==================================================

Processed: 24 meetings
  -> opencivics: 6 meetings
  -> regen-commons: 3 meetings
  -> spirit-of-the-front-range: 3 meetings
  -> localism-fund: 2 meetings
  -> ethereum-localism: 4 meetings
  -> external (no project): 6 meetings

Entities created:
  12 people
  5 concepts
  3 organizations

Wiki-links added: ~180

Skipped: 0
Errors: 0
==================================================
```

---

## Error Handling

If any step fails:
1. Do not delete original file from inbox
2. Update file status to `error`
3. Add `error_message` to frontmatter
4. Continue with next file
5. Report errors in final summary

