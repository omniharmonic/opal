# OPAL Development TODOs

## High Priority

### README Overhaul
- [ ] **Vastly improve the README** to help people understand what a powerful tool OPAL is and how exactly it can be used
  - Add compelling introduction explaining the value proposition
  - Include visual diagrams of the processing pipeline
  - Add quick-start guide for common use cases:
    - Personal knowledge management
    - Team/community knowledge commons
    - Federation with other knowledge commons (KOI, OPL)
  - Document key features with concrete examples:
    - Automated entity extraction from transcripts
    - Semantic search and Q&A over your knowledge base
    - Democratic PR-based governance for commons mode
    - Taxonomy bridges for cross-commons federation
    - Multi-source ingestion (Otter, Fathom, Notion, Luma, etc.)
  - Add comparison to similar tools (Obsidian, Notion, etc.) showing differentiation
  - Include testimonials or use case stories
  - Add badges for docs, license, contributions
  - Create "Getting Started in 5 Minutes" section

## Medium Priority

### Documentation
- [ ] Add more examples to command documentation
- [ ] Create video walkthrough of setup wizard
- [ ] Document all available presets in detail

### Features
- [ ] Implement real-time federation sync
- [ ] Add support for more ingestion sources
- [ ] Enhance embedding-based search

## Completed

- [x] Add KOI integration strategy (`.claude/KOI-INTEGRATION.md`)
- [x] Add `/koi` command for Regen Network federation
- [x] Create Regen Network preset template
- [x] Implement taxonomy bridge skill for cross-taxonomy federation
- [x] Add `/bridge` command for bridge management
- [x] Add Luma events as ingestion source
- [x] Add schema-aware link processing
