"""
Authentication Service - Handles login, logout, password hashing,
and permission checking for the Legal Expert System.
"""
import hashlib
import os
import time
import logging
from config.settings import ROLE_PERMISSIONS, SESSION_TIMEOUT_MINUTES

logger = logging.getLogger(__name__)


class AuthService:
    """
    Authentication and authorization service.
    Manages user sessions and permission checks.
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
        self._current_user = None
        self._login_time = None

    @staticmethod
    def hash_password(password, salt=None):
        """
        Hash password using SHA-256 with salt.
        Returns (password_hash, salt) tuple.
        """
        if salt is None:
            salt = os.urandom(32).hex()
        password_hash = hashlib.sha256(
            (password + salt).encode('utf-8')
        ).hexdigest()
        return password_hash, salt

    @staticmethod
    def verify_password(password, password_hash, salt):
        """Verify password against stored hash and salt."""
        computed_hash = hashlib.sha256(
            (password + salt).encode('utf-8')
        ).hexdigest()
        return computed_hash == password_hash

    def login(self, user_row):
        """
        Set the current authenticated user.
        user_row should be a dict-like object with user data.
        """
        self._current_user = {
            "id": user_row["id"],
            "username": user_row["username"],
            "role": user_row["role"],
            "full_name": user_row["full_name"]
        }
        self._login_time = time.time()
        logger.info(f"User '{user_row['username']}' logged in with role '{user_row['role']}'")

    def logout(self):
        """Clear current user session."""
        if self._current_user:
            logger.info(f"User '{self._current_user['username']}' logged out")
        self._current_user = None
        self._login_time = None

    def get_current_user(self):
        """Get current authenticated user or None if not logged in."""
        if self._current_user and self._login_time:
            # Check session timeout
            elapsed = (time.time() - self._login_time) / 60
            if elapsed > SESSION_TIMEOUT_MINUTES:
                logger.warning("Session timed out")
                self.logout()
                return None
        return self._current_user

    def is_authenticated(self):
        """Check if a user is currently authenticated."""
        return self.get_current_user() is not None

    def has_permission(self, permission):
        """Check if current user has a specific permission."""
        user = self.get_current_user()
        if not user:
            return False
        role = user["role"]
        return permission in ROLE_PERMISSIONS.get(role, [])

    def get_user_permissions(self):
        """Get all permissions for the current user."""
        user = self.get_current_user()
        if not user:
            return []
        return ROLE_PERMISSIONS.get(user["role"], [])

    def require_permission(self, permission):
        """
        Check permission and raise error if not authorized.
        Use as a guard in controllers.
        """
        if not self.has_permission(permission):
            raise PermissionError(
                f"Không có quyền thực hiện: {permission}"
            )
