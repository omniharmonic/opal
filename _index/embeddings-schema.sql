-- OPAL Embeddings Schema
-- SQLite with sqlite-vec extension for vector similarity search

-- Enable required extensions (run at connection time)
-- .load vec0

-- Entity Embeddings
-- Stores the primary embedding for each entity
CREATE TABLE IF NOT EXISTS entity_embeddings (
    id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL UNIQUE,
    entity_type TEXT NOT NULL,
    title TEXT NOT NULL,
    embedding BLOB NOT NULL,  -- Vector stored as blob
    dimensions INTEGER NOT NULL,
    model TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (entity_id) REFERENCES entities(id)
);

-- Chunk Embeddings
-- Stores embeddings for content chunks (for long documents)
CREATE TABLE IF NOT EXISTS chunk_embeddings (
    id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding BLOB NOT NULL,
    dimensions INTEGER NOT NULL,
    model TEXT NOT NULL,
    start_offset INTEGER,
    end_offset INTEGER,
    created_at TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (entity_id) REFERENCES entities(id),
    UNIQUE(entity_id, chunk_index)
);

-- Relationship Embeddings
-- Stores embeddings for relationship descriptions
CREATE TABLE IF NOT EXISTS relationship_embeddings (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    description TEXT,
    embedding BLOB NOT NULL,
    dimensions INTEGER NOT NULL,
    model TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    discovered_by TEXT,  -- 'manual' | 'semantic' | 'extraction'
    created_at TEXT DEFAULT (datetime('now')),

    UNIQUE(source_id, target_id, relationship_type)
);

-- Suggested Relationships (pending human review)
CREATE TABLE IF NOT EXISTS suggested_relationships (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    similarity_score REAL NOT NULL,
    reasoning TEXT,
    status TEXT DEFAULT 'pending',  -- pending | approved | rejected
    reviewed_by TEXT,
    reviewed_at TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Search History (for analytics and improvement)
CREATE TABLE IF NOT EXISTS search_history (
    id TEXT PRIMARY KEY,
    query TEXT NOT NULL,
    query_embedding BLOB,
    results_count INTEGER,
    top_result_id TEXT,
    top_result_similarity REAL,
    latency_ms INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Embedding Jobs Queue (for background processing)
CREATE TABLE IF NOT EXISTS embedding_jobs (
    id TEXT PRIMARY KEY,
    entity_id TEXT,
    job_type TEXT NOT NULL,  -- 'create' | 'update' | 'delete' | 'reindex'
    priority INTEGER DEFAULT 5,
    status TEXT DEFAULT 'pending',  -- pending | processing | completed | failed
    error_message TEXT,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    created_at TEXT DEFAULT (datetime('now')),
    started_at TEXT,
    completed_at TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_entity_embeddings_type ON entity_embeddings(entity_type);
CREATE INDEX IF NOT EXISTS idx_entity_embeddings_updated ON entity_embeddings(updated_at);
CREATE INDEX IF NOT EXISTS idx_chunk_embeddings_entity ON chunk_embeddings(entity_id);
CREATE INDEX IF NOT EXISTS idx_relationship_embeddings_source ON relationship_embeddings(source_id);
CREATE INDEX IF NOT EXISTS idx_relationship_embeddings_target ON relationship_embeddings(target_id);
CREATE INDEX IF NOT EXISTS idx_suggested_relationships_status ON suggested_relationships(status);
CREATE INDEX IF NOT EXISTS idx_embedding_jobs_status ON embedding_jobs(status, priority);

-- Virtual table for vector similarity search (sqlite-vec)
-- Note: Actual creation depends on sqlite-vec extension being loaded
-- CREATE VIRTUAL TABLE IF NOT EXISTS entity_vectors USING vec0(
--     id TEXT PRIMARY KEY,
--     embedding FLOAT[768]  -- Adjust dimensions based on model
-- );

-- Metadata table for tracking index state
CREATE TABLE IF NOT EXISTS embedding_metadata (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Initialize metadata
INSERT OR IGNORE INTO embedding_metadata (key, value) VALUES
    ('schema_version', '1.0'),
    ('total_entities', '0'),
    ('total_chunks', '0'),
    ('total_relationships', '0'),
    ('last_full_reindex', NULL),
    ('embedding_model', 'nomic-embed-text'),
    ('embedding_dimensions', '768');
