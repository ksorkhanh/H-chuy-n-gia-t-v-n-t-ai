"""
Auth Controller - Handles login/logout and permission checks.
"""
import logging
from models.user import User
from core.auth import AuthService

logger = logging.getLogger(__name__)


class AuthController:
    """Controller for authentication operations."""

    def __init__(self):
        self.auth_service = AuthService()

    def login(self, username, password):
        """
        Attempt to login with credentials.
        Returns (success, message, user_dict).
        """
        if not username or not password:
            return False, "Vui lòng nhập tên đăng nhập và mật khẩu", None

        user = User.authenticate(username, password)
        if user:
            return True, f"Đăng nhập thành công! Xin chào {user.full_name}", user.to_dict()
        else:
            return False, "Tên đăng nhập hoặc mật khẩu không đúng", None

    def logout(self):
        """Logout current user."""
        self.auth_service.logout()

    def get_current_user(self):
        """Get current logged in user."""
        return self.auth_service.get_current_user()

    def has_permission(self, permission):
        """Check if current user has permission."""
        return self.auth_service.has_permission(permission)

    def get_user_permissions(self):
        """Get all permissions for current user."""
        return self.auth_service.get_user_permissions()
