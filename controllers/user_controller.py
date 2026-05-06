"""
User Controller - Manages users and roles.
"""
import logging
from models.user import User
from core.auth import AuthService

logger = logging.getLogger(__name__)


class UserController:
    """Controller for user management (admin only)."""

    def __init__(self):
        self.auth = AuthService()

    def get_all_users(self):
        self.auth.require_permission("manage_users")
        return [u.to_dict() for u in User.get_all()]

    def get_user(self, user_id):
        user = User.find_by_id(user_id)
        return user.to_dict() if user else None

    def create_user(self, username, password, role, full_name, email=None):
        self.auth.require_permission("manage_users")
        return User.create(username, password, role, full_name, email)

    def update_user(self, user_id, **kwargs):
        self.auth.require_permission("manage_users")
        User.update(user_id, **kwargs)

    def delete_user(self, user_id):
        self.auth.require_permission("manage_users")
        # Prevent deleting self
        current = self.auth.get_current_user()
        if current and current["id"] == user_id:
            raise ValueError("Không thể xóa tài khoản đang đăng nhập")
        User.delete(user_id)

    def change_password(self, user_id, new_password):
        self.auth.require_permission("manage_users")
        User.change_password(user_id, new_password)

    def reset_password(self, user_id, new_password="123456"):
        """Reset user password to default."""
        self.auth.require_permission("manage_users")
        User.change_password(user_id, new_password)
