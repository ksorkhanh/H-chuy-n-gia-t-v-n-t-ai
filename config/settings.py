"""
System configuration for Legal Expert System.
Centralized settings for database, application, roles & permissions.
"""
import os

# ============================================================
# Application Settings
# ============================================================
APP_NAME = "Hệ Thống Chuyên Gia Tư Vấn Pháp Lý"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Hệ thống tư vấn pháp lý thông minh sử dụng Fuzzy Logic"
DEBUG = True

# ============================================================
# Path Settings
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODULES_DIR = os.path.join(BASE_DIR, "modules")
DB_PATH = os.path.join(DATA_DIR, "legal_expert.db")
SCHEMA_PATH = os.path.join(DATA_DIR, "schema.sql")
SEED_DATA_PATH = os.path.join(DATA_DIR, "seed_data.sql")

# ============================================================
# Database Settings
# ============================================================
DB_SETTINGS = {
    "type": "sqlite",
    "path": DB_PATH,
    # Future: PostgreSQL settings
    # "host": "localhost",
    # "port": 5432,
    # "name": "legal_expert",
    # "user": "admin",
    # "password": "secret"
}

# ============================================================
# Authentication Settings
# ============================================================
PASSWORD_SALT_LENGTH = 32
SESSION_TIMEOUT_MINUTES = 60

# ============================================================
# Roles & Permissions
# ============================================================
ROLES = {
    "admin": "Quản trị viên",
    "staff": "Nhân viên",
    "expert": "Chuyên gia",
    "guest": "Khách"
}

PERMISSIONS = {
    "manage_legal": "Quản lý văn bản pháp lý",
    "manage_rules": "Quản lý luật suy diễn",
    "manage_users": "Quản lý người dùng",
    "run_consultation": "Thực hiện tư vấn",
    "view_results": "Xem kết quả tư vấn",
    "view_history": "Xem lịch sử tư vấn",
    "import_export": "Import/Export dữ liệu",
    "propose_rules": "Đề xuất luật mới"
}

ROLE_PERMISSIONS = {
    "admin": [
        "manage_legal", "manage_rules", "manage_users",
        "run_consultation", "view_results", "view_history",
        "import_export"
    ],
    "staff": [
        "run_consultation", "view_results", "view_history"
    ],
    "expert": [
        "run_consultation", "view_results", "view_history",
        "propose_rules", "manage_rules"
    ],
    "guest": [
        "view_results"
    ]
}

# ============================================================
# Fuzzy Engine Defaults
# ============================================================
FUZZY_DEFAULTS = {
    "defuzzify_method": "centroid",
    "resolution": 1000,  # Number of points for defuzzification
    "default_weight": 1.0
}

# ============================================================
# UI Settings
# ============================================================
UI_SETTINGS = {
    "window_width": 1400,
    "window_height": 850,
    "sidebar_width": 260,
    "font_family": "Segoe UI",
    "font_size": 10
}

# ============================================================
# Module Registry (auto-discovered from modules/ directory)
# ============================================================
AVAILABLE_MODULES = [
    "transfer",
    "compensation",
    "violation"
]
