"""
Legal Expert System - Main Entry Point
Hệ thống chuyên gia tư vấn pháp lý sử dụng Fuzzy Logic

This is the main entry point for the application.
It initializes the database, loads modules, and starts the PyQt6 GUI.
"""
import sys
import os
import logging

# Add project root to path
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

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LegalExpertApp:
    """
    Main application class.
    Manages the lifecycle of the application:
    login -> main window -> logout -> login cycle.
    """

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)

        # Initialize database
        logger.info("Initializing database...")
        self.db = DatabaseManager()
        is_new = self.db.initialize_database()
        if is_new:
            logger.info("Database created with seed data.")
            self._fix_seed_passwords()
        else:
            logger.info("Database already exists.")

        # Discover and load modules
        logger.info("Loading modules...")
        self.module_loader = ModuleLoader()
        self.module_loader.discover_modules()
        logger.info(f"Loaded {len(self.module_loader.get_module_names())} modules: "
                     f"{self.module_loader.get_module_names()}")

        # Initialize auth controller
        self.auth_ctrl = AuthController()

        # Windows
        self.login_view = None
        self.main_window = None

    def _fix_seed_passwords(self):
        """
        Fix seed user passwords to use proper hashing.
        The seed SQL uses placeholder hashes, so we update them here.
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
        """Show the login window."""
        self.login_view = LoginView(self.auth_ctrl)
        self.login_view.login_success.connect(self._on_login_success)
        self.login_view.setMinimumSize(800, 600)
        self.login_view.setWindowTitle(APP_NAME)
        self.login_view.show()

    def _on_login_success(self, user_data):
        """Handle successful login - show main window."""
        logger.info(f"Login successful: {user_data['username']} ({user_data['role']})")

        # Hide login
        if self.login_view:
            self.login_view.close()

        # Show main window
        self.main_window = MainWindow(user_data, self.auth_ctrl)
        self.main_window.on_logout_callback = self._on_logout
        self.main_window.showMaximized()

    def _on_logout(self):
        """Handle logout - show login again."""
        logger.info("User logged out, showing login screen")
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        self.show_login()

    def run(self):
        """Start the application."""
        logger.info(f"Starting {APP_NAME}...")
        self.show_login()
        return self.app.exec()


def main():
    """Application entry point."""
    try:
        app = LegalExpertApp()
        sys.exit(app.run())
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
