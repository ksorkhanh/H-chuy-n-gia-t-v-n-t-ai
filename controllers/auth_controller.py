"""
Bộ điều khiển Xác thực - Xử lý đăng nhập/đăng xuất và kiểm tra quyền.
"""
import logging
from models.user import User
from core.auth import AuthService

logger = logging.getLogger(__name__)


class AuthController:
    """Bộ điều khiển cho các thao tác xác thực."""

    def __init__(self):
        self.auth_service = AuthService()

    def login(self, username, password):
        """
        Thử đăng nhập bằng thông tin xác thực.
        Trả về (thành_công, thông_báo, dict_người_dùng).
        """
        if not username or not password:
            return False, "Vui lòng nhập tên đăng nhập và mật khẩu", None

        user = User.authenticate(username, password)
        if user:
            return True, f"Đăng nhập thành công! Xin chào {user.full_name}", user.to_dict()
        else:
            return False, "Tên đăng nhập hoặc mật khẩu không đúng", None

    def logout(self):
        """Đăng xuất người dùng hiện tại."""
        self.auth_service.logout()

    def get_current_user(self):
        """Lấy thông tin người dùng đang đăng nhập."""
        return self.auth_service.get_current_user()

    def has_permission(self, permission):
        """Kiểm tra người dùng hiện tại có quyền không."""
        return self.auth_service.has_permission(permission)

    def get_user_permissions(self):
        """Lấy tất cả quyền của người dùng hiện tại."""
        return self.auth_service.get_user_permissions()
