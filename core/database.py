"""
Quản lý Cơ sở dữ liệu - Mẫu Singleton quản lý kết nối SQLite.
Xử lý nhóm kết nối, khởi tạo lược đồ và hỗ trợ transaction.
Có thể mở rộng để hỗ trợ PostgreSQL trong tương lai.
"""
import sqlite3
import os
import logging
from config.settings import DB_SETTINGS, SCHEMA_PATH, SEED_DATA_PATH, DATA_DIR

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Quản lý cơ sở dữ liệu (Singleton) cho SQLite.
    Quản lý các kết nối, khởi tạo lược đồ và cung cấp 
    một giao diện gọn gàng cho các thao tác CSDL.
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
        # Đảm bảo thư mục data tồn tại
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def get_connection(self):
        """Lấy hoặc tạo kết nối cơ sở dữ liệu."""
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._connection.execute("PRAGMA journal_mode = WAL")
        return self._connection

    def close(self):
        """Đóng kết nối cơ sở dữ liệu."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute(self, query, params=None):
        """Thực thi một câu truy vấn đơn và trả về cursor."""
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
        """Thực thi một truy vấn với nhiều bộ tham số."""
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
        """Thực thi truy vấn và trả về một kết quả đầu tiên."""
        conn = self.get_connection()
        if params:
            cursor = conn.execute(query, params)
        else:
            cursor = conn.execute(query)
        return cursor.fetchone()

    def fetch_all(self, query, params=None):
        """Thực thi truy vấn và trả về tất cả kết quả."""
        conn = self.get_connection()
        if params:
            cursor = conn.execute(query, params)
        else:
            cursor = conn.execute(query)
        return cursor.fetchall()

    def initialize_database(self):
        """
        Khởi tạo lược đồ cơ sở dữ liệu và dữ liệu mẫu.
        Chỉ chạy nếu các bảng chưa tồn tại.
        """
        conn = self.get_connection()

        # Kiểm tra xem CSDL đã được khởi tạo chưa
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        if cursor.fetchone():
            logger.info("Database already initialized.")
            return False

        # Chạy file lược đồ (schema)
        if os.path.exists(SCHEMA_PATH):
            logger.info("Initializing database schema...")
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            conn.executescript(schema_sql)
            logger.info("Schema created successfully.")
        else:
            logger.error(f"Schema file not found: {SCHEMA_PATH}")
            raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

        # Chạy dữ liệu mẫu (seed data)
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
        """Xóa và khởi tạo lại toàn bộ cơ sở dữ liệu."""
        self.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            logger.info("Database file deleted.")
        self.initialize_database()

    def table_exists(self, table_name):
        """Kiểm tra xem một bảng có tồn tại trong CSDL hay không."""
        result = self.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return result is not None

    def begin_transaction(self):
        """Bắt đầu một transaction."""
        conn = self.get_connection()
        conn.execute("BEGIN")

    def commit_transaction(self):
        """Commit (lưu) transaction hiện tại."""
        conn = self.get_connection()
        conn.commit()

    def rollback_transaction(self):
        """Rollback (hủy bỏ) transaction hiện tại."""
        conn = self.get_connection()
        conn.rollback()
