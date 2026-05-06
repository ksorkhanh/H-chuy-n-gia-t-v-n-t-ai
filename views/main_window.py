"""
Main Window - Primary application window with sidebar navigation.
Manages view switching and role-based menu visibility.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                              QPushButton, QLabel, QStackedWidget, QFrame,
                              QSpacerItem, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from views.styles import MAIN_STYLESHEET
from views.dashboard_view import DashboardView
from views.consultation_view import ConsultationView
from views.legal_management_view import LegalManagementView
from views.rule_management_view import RuleManagementView
from views.user_management_view import UserManagementView
from views.history_view import HistoryView

from controllers.auth_controller import AuthController
from controllers.consultation_controller import ConsultationController
from controllers.legal_controller import LegalController
from controllers.rule_controller import RuleController
from controllers.user_controller import UserController
from controllers.history_controller import HistoryController

from config.settings import UI_SETTINGS


class MainWindow(QMainWindow):
    """Main application window with sidebar and stacked content."""

    def __init__(self, user_data, auth_controller):
        super().__init__()
        self.user_data = user_data
        self.auth_ctrl = auth_controller

        # Initialize controllers
        self.consultation_ctrl = ConsultationController()
        self.legal_ctrl = LegalController()
        self.rule_ctrl = RuleController()
        self.user_ctrl = UserController()
        self.history_ctrl = HistoryController()

        self.setWindowTitle("Hệ Thống Chuyên Gia Tư Vấn Pháp Lý")
        self.setMinimumSize(
            UI_SETTINGS["window_width"],
            UI_SETTINGS["window_height"]
        )
        self.setStyleSheet(MAIN_STYLESHEET)

        self.sidebar_buttons = {}
        self._setup_ui()
        self._setup_views()
        self._apply_permissions()

        # Show dashboard by default
        self._switch_view("dashboard")

    def _setup_ui(self):
        """Build main layout: sidebar + content area."""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === SIDEBAR ===
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(4)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar header
        header = QFrame()
        header.setObjectName("sidebar_header")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 15)

        app_title = QLabel("⚖️ Tư Vấn Pháp Lý")
        app_title.setObjectName("sidebar_title")
        header_layout.addWidget(app_title)

        app_sub = QLabel("Expert System v1.0")
        app_sub.setObjectName("sidebar_subtitle")
        header_layout.addWidget(app_sub)

        sidebar_layout.addWidget(header)
        sidebar_layout.addSpacing(10)

        # Navigation buttons
        nav_items = [
            ("dashboard", "📊  Dashboard"),
            ("consultation", "🔍  Tư Vấn"),
            ("legal", "📜  Văn Bản Pháp Lý"),
            ("rules", "⚙️  Quản Lý Rules"),
            ("users", "👥  Người Dùng"),
            ("history", "📜  Lịch Sử"),
        ]

        for key, label in nav_items:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, k=key: self._switch_view(k))
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons[key] = btn

        sidebar_layout.addStretch()

        # User info at bottom
        user_frame = QFrame()
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(15, 10, 15, 10)

        role_names = {
            "admin": "Quản trị viên",
            "staff": "Nhân viên",
            "expert": "Chuyên gia",
            "guest": "Khách"
        }

        user_info = QLabel(
            f"👤 {self.user_data['full_name']}\n"
            f"🔑 {role_names.get(self.user_data['role'], self.user_data['role'])}"
        )
        user_info.setObjectName("user_info_label")
        user_layout.addWidget(user_info)

        logout_btn = QPushButton("🚪  Đăng Xuất")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent; color: #e74c3c;
                border: 1px solid #e74c3c; border-radius: 8px;
                padding: 8px; margin: 5px 10px;
            }
            QPushButton:hover { background-color: #e74c3c; color: white; }
        """)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self._on_logout)
        user_layout.addWidget(logout_btn)

        sidebar_layout.addWidget(user_frame)
        main_layout.addWidget(sidebar)

        # === CONTENT AREA ===
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")
        main_layout.addWidget(self.content_stack)

    def _setup_views(self):
        """Initialize all views and add to stack."""
        self.views = {}

        # Dashboard
        self.dashboard_view = DashboardView(
            self.consultation_ctrl, self.history_ctrl)
        self.dashboard_view.module_selected.connect(
            lambda m: self._open_consultation(m))
        self.content_stack.addWidget(self.dashboard_view)
        self.views["dashboard"] = self.dashboard_view

        # Consultation
        self.consultation_view = ConsultationView(self.consultation_ctrl)
        self.content_stack.addWidget(self.consultation_view)
        self.views["consultation"] = self.consultation_view

        # Legal Management
        self.legal_view = LegalManagementView(self.legal_ctrl)
        self.content_stack.addWidget(self.legal_view)
        self.views["legal"] = self.legal_view

        # Rule Management
        self.rule_view = RuleManagementView(self.rule_ctrl, self.legal_ctrl)
        self.content_stack.addWidget(self.rule_view)
        self.views["rules"] = self.rule_view

        # User Management
        self.user_view = UserManagementView(self.user_ctrl)
        self.content_stack.addWidget(self.user_view)
        self.views["users"] = self.user_view

        # History
        self.history_view = HistoryView(self.history_ctrl)
        self.content_stack.addWidget(self.history_view)
        self.views["history"] = self.history_view

    def _apply_permissions(self):
        """Show/hide sidebar items based on user role."""
        permissions = self.auth_ctrl.get_user_permissions()

        # Legal management - admin only
        if "manage_legal" not in permissions:
            self.sidebar_buttons["legal"].setVisible(False)

        # Rule management - admin & expert
        if "manage_rules" not in permissions:
            self.sidebar_buttons["rules"].setVisible(False)

        # User management - admin only
        if "manage_users" not in permissions:
            self.sidebar_buttons["users"].setVisible(False)

    def _switch_view(self, view_key):
        """Switch to a specific view."""
        if view_key in self.views:
            self.content_stack.setCurrentWidget(self.views[view_key])

            # Update sidebar button states
            for key, btn in self.sidebar_buttons.items():
                btn.setChecked(key == view_key)

            # Refresh data on view switch
            if view_key == "dashboard":
                self.dashboard_view.refresh_stats()
            elif view_key == "history":
                self.history_view._load_history()

    def _open_consultation(self, module_name):
        """Open consultation view with specific module."""
        self.consultation_view.set_module(module_name)
        self._switch_view("consultation")

    def _on_logout(self):
        """Handle logout."""
        reply = QMessageBox.question(
            self, "Đăng xuất",
            "Bạn có chắc muốn đăng xuất?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.auth_ctrl.logout()
            self.close()
            # Signal to show login again is handled in main.py
            if hasattr(self, 'on_logout_callback'):
                self.on_logout_callback()
