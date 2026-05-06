"""
User Model - CRUD operations for user management.
"""
import logging
from core.database import DatabaseManager
from core.auth import AuthService

logger = logging.getLogger(__name__)


class User:
    """User model for authentication and user management."""

    def __init__(self, id=None, username=None, role=None, full_name=None, email=None, is_active=True):
        self.id = id
        self.username = username
        self.role = role
        self.full_name = full_name
        self.email = email
        self.is_active = is_active

    @staticmethod
    def authenticate(username, password):
        """
        Authenticate user with username and password.
        Returns User object if successful, None otherwise.
        """
        db = DatabaseManager()
        row = db.fetch_one(
            "SELECT * FROM users WHERE username = ? AND is_active = 1",
            (username,)
        )
        if row and AuthService.verify_password(password, row["password_hash"], row["salt"]):
            auth = AuthService()
            auth.login(row)
            return User(
                id=row["id"],
                username=row["username"],
                role=row["role"],
                full_name=row["full_name"],
                email=row["email"]
            )
        return None

    @staticmethod
    def find_by_id(user_id):
        """Find user by ID."""
        db = DatabaseManager()
        row = db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        if row:
            return User(
                id=row["id"], username=row["username"],
                role=row["role"], full_name=row["full_name"],
                email=row["email"], is_active=bool(row["is_active"])
            )
        return None

    @staticmethod
    def find_by_username(username):
        """Find user by username."""
        db = DatabaseManager()
        row = db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))
        if row:
            return User(
                id=row["id"], username=row["username"],
                role=row["role"], full_name=row["full_name"],
                email=row["email"], is_active=bool(row["is_active"])
            )
        return None

    @staticmethod
    def get_all():
        """Get all users."""
        db = DatabaseManager()
        rows = db.fetch_all("SELECT * FROM users ORDER BY id")
        return [
            User(
                id=r["id"], username=r["username"],
                role=r["role"], full_name=r["full_name"],
                email=r["email"], is_active=bool(r["is_active"])
            ) for r in rows
        ]

    @staticmethod
    def create(username, password, role, full_name, email=None):
        """Create a new user."""
        db = DatabaseManager()
        password_hash, salt = AuthService.hash_password(password)
        try:
            cursor = db.execute(
                """INSERT INTO users (username, password_hash, salt, role, full_name, email)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (username, password_hash, salt, role, full_name, email)
            )
            logger.info(f"Created user: {username}")
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise

    @staticmethod
    def update(user_id, full_name=None, email=None, role=None, is_active=None):
        """Update user information."""
        db = DatabaseManager()
        updates = []
        params = []
        if full_name is not None:
            updates.append("full_name = ?")
            params.append(full_name)
        if email is not None:
            updates.append("email = ?")
            params.append(email)
        if role is not None:
            updates.append("role = ?")
            params.append(role)
        if is_active is not None:
            updates.append("is_active = ?")
            params.append(1 if is_active else 0)
        if not updates:
            return
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        db.execute(query, tuple(params))
        logger.info(f"Updated user ID: {user_id}")

    @staticmethod
    def change_password(user_id, new_password):
        """Change user password."""
        db = DatabaseManager()
        password_hash, salt = AuthService.hash_password(new_password)
        db.execute(
            "UPDATE users SET password_hash = ?, salt = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (password_hash, salt, user_id)
        )
        logger.info(f"Password changed for user ID: {user_id}")

    @staticmethod
    def delete(user_id):
        """Delete a user."""
        db = DatabaseManager()
        db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        logger.info(f"Deleted user ID: {user_id}")

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "full_name": self.full_name,
            "email": self.email,
            "is_active": self.is_active
        }
