-- ============================================================
-- Legal Expert System - Database Schema
-- SQLite compatible, designed for future PostgreSQL migration
-- ============================================================

-- ============================================================
-- Users & Authentication
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'staff' CHECK(role IN ('admin', 'staff', 'expert', 'guest')),
    full_name TEXT NOT NULL,
    email TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS role_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    permission_id INTEGER NOT NULL,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE(role, permission_id)
);

-- ============================================================
-- Legal Documents & Articles
-- ============================================================
CREATE TABLE IF NOT EXISTS legal_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    domain TEXT NOT NULL DEFAULT 'dat_dai',
    description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS legal_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    article_number TEXT NOT NULL,
    clause TEXT,
    content TEXT NOT NULL,
    keywords TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (document_id) REFERENCES legal_documents(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS legal_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_article_id INTEGER NOT NULL,
    related_article_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL DEFAULT 'reference' CHECK(relation_type IN ('reference', 'amendment', 'supplement', 'replace', 'detail')),
    FOREIGN KEY (source_article_id) REFERENCES legal_articles(id) ON DELETE CASCADE,
    FOREIGN KEY (related_article_id) REFERENCES legal_articles(id) ON DELETE CASCADE
);

-- ============================================================
-- Fuzzy Rules
-- ============================================================
CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    name TEXT NOT NULL,
    condition_json TEXT NOT NULL,  -- JSON: list of {variable, term} pairs
    conclusion TEXT NOT NULL,       -- Output term name
    weight REAL NOT NULL DEFAULT 1.0,
    legal_article_id INTEGER,
    is_active INTEGER NOT NULL DEFAULT 1,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (legal_article_id) REFERENCES legal_articles(id) ON DELETE SET NULL
);

-- ============================================================
-- Consultation Cases & History
-- ============================================================
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    module TEXT NOT NULL,
    input_data TEXT NOT NULL,    -- JSON: input values
    result_data TEXT NOT NULL,   -- JSON: output score, conclusion, explanation
    matched_rules TEXT,          -- JSON: list of matched rule IDs
    score REAL,
    conclusion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- Indexes for performance
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_legal_articles_document ON legal_articles(document_id);
CREATE INDEX IF NOT EXISTS idx_legal_articles_keywords ON legal_articles(keywords);
CREATE INDEX IF NOT EXISTS idx_rules_module ON rules(module);
CREATE INDEX IF NOT EXISTS idx_rules_active ON rules(is_active);
CREATE INDEX IF NOT EXISTS idx_cases_user ON cases(user_id);
CREATE INDEX IF NOT EXISTS idx_cases_module ON cases(module);
CREATE INDEX IF NOT EXISTS idx_cases_created ON cases(created_at);
