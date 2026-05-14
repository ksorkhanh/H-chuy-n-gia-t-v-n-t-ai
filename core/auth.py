"""
Dịch vụ Xác thực - Xử lý đăng nhập, đăng xuất, băm mật khẩu,
và kiểm tra quyền cho Hệ Thống Chuyên Gia Tư Vấn Pháp Lý.
"""
import hashlib
import os
import time
import logging
from config.settings import ROLE_PERMISSIONS, SESSION_TIMEOUT_MINUTES

logger = logging.getLogger(__name__)


class AuthService:
    """
    Dịch vụ xác thực và phân quyền.
    Quản lý phiên đăng nhập của người dùng và kiểm tra quyền hạn.
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
        Băm mật khẩu sử dụng SHA-256 kèm salt.
        Trả về tuple (password_hash, salt).
        """
        if salt is None:
            salt = os.urandom(32).hex()
        password_hash = hashlib.sha256(
            (password + salt).encode('utf-8')
        ).hexdigest()
        return password_hash, salt

    @staticmethod
    def verify_password(password, password_hash, salt):
        """Xác minh mật khẩu với mã băm và salt đã lưu."""
        computed_hash = hashlib.sha256(
            (password + salt).encode('utf-8')
        ).hexdigest()
        return computed_hash == password_hash

    def login(self, user_row):
        """
        Thiết lập người dùng đang đăng nhập hiện tại.
        user_row phải là một đối tượng dạng dict chứa dữ liệu người dùng.
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
        """Xóa phiên đăng nhập hiện tại."""
        if self._current_user:
            logger.info(f"User '{self._current_user['username']}' logged out")
        self._current_user = None
        self._login_time = None

    def get_current_user(self):
        """Lấy người dùng hiện tại hoặc None nếu chưa đăng nhập."""
        if self._current_user and self._login_time:
            # Kiểm tra hết hạn phiên đăng nhập
            elapsed = (time.time() - self._login_time) / 60
            if elapsed > SESSION_TIMEOUT_MINUTES:
                logger.warning("Session timed out")
                self.logout()
                return None
        return self._current_user

    def is_authenticated(self):
        """Kiểm tra xem người dùng đã đăng nhập chưa."""
        return self.get_current_user() is not None

    def has_permission(self, permission):
        """Kiểm tra người dùng hiện tại có quyền cụ thể không."""
        user = self.get_current_user()
        if not user:
            return False
        role = user["role"]
        return permission in ROLE_PERMISSIONS.get(role, [])

    def get_user_permissions(self):
        """Lấy tất cả các quyền của người dùng hiện tại."""
        user = self.get_current_user()
        if not user:
            return []
        return ROLE_PERMISSIONS.get(user["role"], [])

    def require_permission(self, permission):
        """
        Kiểm tra quyền và báo lỗi nếu không được phép.
        Sử dụng như một bộ lọc bảo vệ trong các controller.
        """
        if not self.has_permission(permission):
            raise PermissionError(
                f"Không có quyền thực hiện: {permission}"
            )
