"""
Hệ Thống Chuyên Gia Tư Vấn Pháp Lý - Điểm Vào Chính
Hệ thống chuyên gia tư vấn pháp lý sử dụng Fuzzy Logic

Đây là điểm vào chính của ứng dụng.
Khởi tạo CSDL, nạp các module và khởi động giao diện PyQt6.
"""
import sys
import os
import logging

# Thêm thư mục gốc dự án vào đường dẫn
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from config.settings import APP_NAME, DEBUG
from core.database import DatabaseManager
from core.auth import AuthService
from modules.module_loader import ModuleLoader
from controllers.auth_controller import AuthController
from views.login_view import LoginView
from views.main_window import MainWindow

# Cấu hình logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LegalExpertApp:
    """
    Lớp ứng dụng chính.
    Quản lý vòng đời của ứng dụng:
    đăng nhập -> cửa sổ chính -> đăng xuất -> đăng nhập.
    """

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)

        # Áp dụng stylesheet toàn cục
        from views.styles import GLOBAL_STYLESHEET
        self.app.setStyleSheet(GLOBAL_STYLESHEET)

        # Khởi tạo cơ sở dữ liệu
        logger.info("Initializing database...")
        self.db = DatabaseManager()
        is_new = self.db.initialize_database()
        if is_new:
            logger.info("Database created with seed data.")
            self._fix_seed_passwords()
        else:
            logger.info("Database already exists.")

        # Phát hiện và nạp các module
        logger.info("Loading modules...")
        self.module_loader = ModuleLoader()
        self.module_loader.discover_modules()
        logger.info(f"Loaded {len(self.module_loader.get_module_names())} modules: "
                     f"{self.module_loader.get_module_names()}")

        # Khởi tạo bộ điều khiển xác thực
        self.auth_ctrl = AuthController()

        # Các cửa sổ
        self.login_view = None
        self.main_window = None

    def _fix_seed_passwords(self):
        """
        Sửa mật khẩu của người dùng mẫu để sử dụng băm đúng.
        File SQL mẫu dùng mã băm tạm, nên cần cập nhật lại tại đây.
        """
        from models.user import User
        users_to_fix = [
            ("admin", "123456"),
            ("staff01", "123456"),
            ("expert01", "123456")
        ]
        for username, password in users_to_fix:
            user = User.find_by_username(username)
            if user:
                User.change_password(user.id, password)
                logger.info(f"Fixed password for user: {username}")

    def show_login(self):
        """Hiển thị cửa sổ đăng nhập."""
        self.login_view = LoginView(self.auth_ctrl)
        self.login_view.login_success.connect(self._on_login_success)
        self.login_view.setMinimumSize(800, 600)
        self.login_view.setWindowTitle(APP_NAME)
        self.login_view.show()

    def _on_login_success(self, user_data):
        """Xử lý đăng nhập thành công - hiển thị cửa sổ chính."""
        logger.info(f"Login successful: {user_data['username']} ({user_data['role']})")

        # Ẩn cửa sổ đăng nhập
        if self.login_view:
            self.login_view.close()

        # Hiển thị cửa sổ chính
        self.main_window = MainWindow(user_data, self.auth_ctrl)
        self.main_window.on_logout_callback = self._on_logout
        self.main_window.showMaximized()

    def _on_logout(self):
        """Xử lý đăng xuất - hiển thị lại màn hình đăng nhập."""
        logger.info("User logged out, showing login screen")
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        self.show_login()

    def run(self):
        """Khởi động ứng dụng."""
        logger.info(f"Starting {APP_NAME}...")
        self.show_login()
        return self.app.exec()


def main():
    """Điểm vào chính của ứng dụng."""
    try:
        app = LegalExpertApp()
        sys.exit(app.run())
    except Exception as e:
        logger.error(f"Lỗi ứng dụng: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
