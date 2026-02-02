# OPAL Testing Guide

Comprehensive end-to-end testing procedures for the Open Protocol Agent Librarian.

## Test Environment

### Prerequisites

Before testing, ensure you have:

1. **Claude Code** installed and configured
2. **Ollama** running locally (for embeddings and local LLM)
3. **OpenAI Whisper** installed (for audio transcription - separate from Ollama)
4. **Git** configured for the repository
5. **Required Ollama models** pulled:
   ```bash
   ollama pull nomic-embed-text  # For embeddings (768 dimensions)
   ollama pull llama3.2          # For entity extraction and Q&A
   ```
6. **Whisper installation** (Python library):
   ```bash
   pip install openai-whisper   # Audio transcription
   ```

### Test Scripts

OPAL includes automated test scripts for validating your environment:

```bash
# Test Ollama integration (embeddings + LLM)
python tests/test_ollama.py

# Test Whisper integration (audio transcription)
python tests/test_whisper.py

# Test Whisper with a real audio file
python tests/test_whisper.py /path/to/audio.mp3
```

### Test Data Provided

The following test data has been pre-populated:

**Inbox Content:**
- `_inbox/transcripts/sample-meeting-governance.md` - 45-minute governance meeting
- `_inbox/transcripts/sample-podcast-commons.md` - 1-hour podcast episode

**Existing Entities:**
- `patterns/consent-based-decision-making.md`
- `protocols/sociocracy.md`
- `protocols/participatory-budgeting.md`
- `people/maria-chen.md`
- `organizations/neighborhood-governance-council.md`

**Populated Indexes:**
- `_index/entities.json` - 5 entities
- `_index/relationships.json` - 8 relationships

---

## Test Procedures

### 1. Setup Wizard Test

**Test:** Verify the setup wizard works correctly.

```bash
/setup
```

**Expected:**
1. Welcome message explaining OPAL
2. Mode selection (Personal/Team/Commons)
3. Taxonomy selection (OPL preset should be available)
4. Integration configuration prompts
5. Configuration files created/updated

**Verify:**
- [ ] `config/settings.yaml` contains selected mode
- [ ] `taxonomy/opl.yaml` is loaded
- [ ] `PROJECT.md` is created with context

---

### 2. Status Command Test

**Test:** Check current commons status.

```bash
/status
```

**Expected:**
- Inbox count (should show 2 transcripts)
- Staging count (should be 0 initially)
- Entity counts by type
- Recent activity

---

### 3. Ingestion Pipeline Test

**Test:** Process the sample transcripts through the full pipeline.

```bash
/process
```

**Expected Flow:**
1. CLASSIFY - Identifies as "transcript"
2. PREPROCESS - Cleans up text (if needed)
3. EXTRACT - Extracts entities (expect: patterns, protocols, people)
4. RECONCILE - Matches against existing entities
5. STAGE - Moves to staging for review

**Verify:**
- [ ] New entities appear in `_staging/entities/`
- [ ] Existing entity matches are flagged
- [ ] Confidence scores are assigned
- [ ] Relationships are suggested

**Expected Entities from Meeting Transcript:**
- Pattern: Advice Process (mentioned)
- Pattern: Round Robin (mentioned)
- Pattern: Double-Linking (mentioned)
- Person: James Wilson
- Person: Priya Patel
- Person: David Kim
- Possible: Municipal Governance concepts

**Expected Entities from Podcast:**
- Protocol: Holacracy (mentioned)
- Pattern: Quadratic Voting/Funding (mentioned)
- Tool/Utility: Pol.is, Decidim, Loomio
- Person: Dr. Elinor Blake, Sarah Martinez
- Organization: Participatory Budgeting Project

---

### 4. Review Command Test

**Test:** Review staged entities.

```bash
/review
```

**Expected:**
- List of staged items with confidence scores
- Ability to accept, reject, or edit
- Merge suggestions for duplicates

```bash
/review batch
```

**Expected:**
- Batch review interface
- Keyboard navigation (j/k)
- Quick accept/reject (a/r)

---

### 5. Search Command Test

**Test:** Search for entities.

```bash
/search consent decision making
```

**Expected:**
- Returns "Consent-Based Decision Making" pattern
- Relevance score shown
- Related entities suggested

```bash
/search governance --type protocol
```

**Expected:**
- Returns "Sociocracy" and "Participatory Budgeting"
- Filtered by type

---

### 6. Ask Command Test (Q&A)

**Test:** Ask questions about the commons.

```bash
/ask What is consent-based decision making?
```

**Expected:**
- Synthesized answer from corpus
- Citations to specific entities
- Related content suggestions

```bash
/ask How does sociocracy relate to participatory budgeting?
```

**Expected:**
- Comparative answer
- Multiple source citations
- Relationship explanation

```bash
/ask Do we have anything about blockchain governance?
```

**Expected:**
- Acknowledges limited/no content
- Suggests related topics that exist
- Identifies as potential gap

---

### 7. Graph Command Test

**Test:** Generate knowledge graph.

```bash
/graph
```

**Expected:**
- Graph data generated
- Node count: 5 entities
- Edge count: 8 relationships
- Cluster detection

```bash
/graph pattern-consent-based-decision-making
```

**Expected:**
- Local graph centered on entity
- Connected entities shown
- Relationship types labeled

```bash
/graph --stats
```

**Expected:**
- Graph statistics
- Most connected entities
- Density metrics

---

### 8. Coverage Command Test

**Test:** Analyze commons coverage.

```bash
/coverage
```

**Expected:**
- Coverage by sector (should show gaps)
- Coverage by scale (should show gaps)
- Quality metrics
- Recommendations

```bash
/coverage governance-and-political-systems
```

**Expected:**
- Sector-specific analysis
- Entity list for sector
- Sub-area coverage

```bash
/coverage --gaps
```

**Expected:**
- Only gap analysis shown
- Priority recommendations

---

### 9. Digest Command Test

**Test:** Generate activity digest.

```bash
/digest preview
```

**Expected:**
- Preview of weekly digest
- New entities listed
- Updates shown
- Statistics included

---

### 10. Publish Command Test

**Test:** Generate static site.

```bash
/publish preview
```

**Expected:**
- Local server starts
- Site accessible at localhost:1313
- All entities rendered
- Graph visualization included

---

### 11. GitHub Integration Test

**Test:** Commit changes (if git is configured).

```bash
/github commit
```

**Expected:**
- Structured commit message
- Changes summarized
- PR creation option

---

### 12. Federation Test

**Test:** Check federation status.

```bash
/federate status
```

**Expected:**
- Configured sources shown
- Sync status displayed

---

## Validation Checklist

### Core Pipeline

- [ ] Transcripts are correctly classified
- [ ] Entities are extracted with reasonable confidence
- [ ] Deduplication correctly identifies matches
- [ ] Staging area receives processed items
- [ ] Review allows accept/reject/edit
- [ ] Accepted items move to appropriate directories
- [ ] Entity index is updated
- [ ] Relationships are tracked

### Discovery Features

- [ ] Semantic search returns relevant results
- [ ] Q&A provides cited answers
- [ ] Graph visualization is generated
- [ ] Coverage analysis identifies gaps

### Publishing Features

- [ ] Static site builds successfully
- [ ] All entities are rendered
- [ ] Navigation works
- [ ] Search is functional

### Governance Features

- [ ] Commits are structured correctly
- [ ] PR creation works (if GitHub configured)
- [ ] Vote tracking (if in Commons mode)

---

## Common Issues

### Ollama Not Running

```
Error: Connection refused to localhost:11434
```

**Fix:** Start Ollama with `ollama serve`

### Whisper Model Download Failed

```
Error: Tunnel connection failed: 403 Forbidden
```

**Cause:** Network restrictions or proxy blocking model downloads.

**Fix:** Download models on a machine with direct internet access:
```bash
# Pre-download models (they cache in ~/.cache/whisper/)
python -c "import whisper; whisper.load_model('turbo')"
```

### Missing Embedding Model

```
Error: Model nomic-embed-text not found
```

**Fix:** `ollama pull nomic-embed-text`

### Empty Search Results

**Possible causes:**
- Embedding index not populated
- Query too specific

**Fix:** Run `/process reindex-embeddings` to rebuild index

### Classification Errors

**Possible causes:**
- Content format not recognized
- Missing context

**Fix:** Check content against expected patterns in `classify` skill

---

## Performance Benchmarks

| Operation | Expected Time |
|-----------|---------------|
| Process single transcript | 30-60 seconds |
| Entity extraction | 10-20 seconds per entity |
| Embedding generation | 2-5 seconds per entity |
| Full site build | 10-30 seconds |
| Search query | 1-3 seconds |
| Q&A response | 5-15 seconds |

---

## Reporting Issues

When reporting issues, include:

1. Command that failed
2. Error message (full text)
3. Contents of relevant files
4. Ollama status (`ollama list`)
5. Configuration snippets

---

## Test Data Reset

To reset test data to initial state:

```bash
# Clear staging
rm -rf _staging/entities/* _staging/pages/*

# Reset indexes (keep structure)
# Edit entities.json to remove test entities
# Edit relationships.json to remove test relationships

# Keep inbox content for re-testing
```

---

*Last updated: 2026-02-02*
*OPAL Version: 1.2.0*
