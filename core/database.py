"""
Database Manager - Singleton pattern for SQLite connection management.
Handles connection pooling, schema migration, and transaction support.
Can be extended to support PostgreSQL in the future.
"""
import sqlite3
import os
import logging
from config.settings import DB_SETTINGS, SCHEMA_PATH, SEED_DATA_PATH, DATA_DIR

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Singleton database manager for SQLite.
    Manages connections, schema initialization, and provides
    a clean interface for database operations.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._connection = None
        self.db_path = DB_SETTINGS["path"]
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def get_connection(self):
        """Get or create database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._connection.execute("PRAGMA journal_mode = WAL")
        return self._connection

    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute(self, query, params=None):
        """Execute a single query and return cursor."""
        conn = self.get_connection()
        try:
            if params:
                cursor = conn.execute(query, params)
            else:
                cursor = conn.execute(query)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise

    def execute_many(self, query, params_list):
        """Execute a query with multiple parameter sets."""
        conn = self.get_connection()
        try:
            cursor = conn.executemany(query, params_list)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise

    def fetch_one(self, query, params=None):
        """Execute query and fetch one result."""
        conn = self.get_connection()
        if params:
            cursor = conn.execute(query, params)
        else:
            cursor = conn.execute(query)
        return cursor.fetchone()

    def fetch_all(self, query, params=None):
        """Execute query and fetch all results."""
        conn = self.get_connection()
        if params:
            cursor = conn.execute(query, params)
        else:
            cursor = conn.execute(query)
        return cursor.fetchall()

    def initialize_database(self):
        """
        Initialize database schema and seed data.
        Only runs if tables don't exist yet.
        """
        conn = self.get_connection()

        # Check if database is already initialized
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        if cursor.fetchone():
            logger.info("Database already initialized.")
            return False

        # Run schema
        if os.path.exists(SCHEMA_PATH):
            logger.info("Initializing database schema...")
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            conn.executescript(schema_sql)
            logger.info("Schema created successfully.")
        else:
            logger.error(f"Schema file not found: {SCHEMA_PATH}")
            raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

        # Run seed data
        if os.path.exists(SEED_DATA_PATH):
            logger.info("Loading seed data...")
            with open(SEED_DATA_PATH, 'r', encoding='utf-8') as f:
                seed_sql = f.read()
            conn.executescript(seed_sql)
            logger.info("Seed data loaded successfully.")
        else:
            logger.warning(f"Seed data file not found: {SEED_DATA_PATH}")

        return True

    def reset_database(self):
        """Reset database by deleting and re-initializing."""
        self.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            logger.info("Database file deleted.")
        self.initialize_database()

    def table_exists(self, table_name):
        """Check if a table exists in the database."""
        result = self.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return result is not None

    def begin_transaction(self):
        """Begin a transaction."""
        conn = self.get_connection()
        conn.execute("BEGIN")

    def commit_transaction(self):
        """Commit current transaction."""
        conn = self.get_connection()
        conn.commit()

    def rollback_transaction(self):
        """Rollback current transaction."""
        conn = self.get_connection()
        conn.rollback()
