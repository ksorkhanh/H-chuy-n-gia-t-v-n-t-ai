"""
Login View - Beautiful login screen with gradient background.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QPushButton, QFrame, QSpacerItem,
                              QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from views.styles import LOGIN_STYLESHEET


class LoginView(QWidget):
    """Login screen with modern dark theme."""

    # Signal emitted when login is successful
    login_success = pyqtSignal(dict)

    def __init__(self, auth_controller):
        super().__init__()
        self.auth_controller = auth_controller
        self.setStyleSheet(LOGIN_STYLESHEET)
        self.setObjectName("login_container")
        self._setup_ui()

    def _setup_ui(self):
        """Build the login UI."""
        # Main centered layout
        main_layout = QHBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Login card
        card = QFrame()
        card.setObjectName("login_card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icon
        icon_label = QLabel("⚖️")
        icon_label.setObjectName("login_icon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)

        # Title
        title = QLabel("Hệ Thống Chuyên Gia")
        title.setObjectName("login_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Tư Vấn Pháp Lý Thông Minh")
        subtitle.setObjectName("login_subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(10)

        # Username
        user_label = QLabel("Tên đăng nhập")
        user_label.setProperty("class", "field_label")
        card_layout.addWidget(user_label)

        self.username_input = QLineEdit()
        self.username_input.setObjectName("login_input")
        self.username_input.setPlaceholderText("Nhập tên đăng nhập...")
        self.username_input.setMinimumHeight(45)
        card_layout.addWidget(self.username_input)

        # Password
        pass_label = QLabel("Mật khẩu")
        pass_label.setProperty("class", "field_label")
        card_layout.addWidget(pass_label)

        self.password_input = QLineEdit()
        self.password_input.setObjectName("login_input")
        self.password_input.setPlaceholderText("Nhập mật khẩu...")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.returnPressed.connect(self._on_login)
        card_layout.addWidget(self.password_input)

        # Error message
        self.error_label = QLabel("")
        self.error_label.setObjectName("login_error")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        card_layout.addWidget(self.error_label)

        card_layout.addSpacing(5)

        # Login button
        self.login_btn = QPushButton("🔐  Đăng Nhập")
        self.login_btn.setObjectName("login_btn")
        self.login_btn.setMinimumHeight(48)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.clicked.connect(self._on_login)
        card_layout.addWidget(self.login_btn)

        card_layout.addSpacing(10)

        # Footer
        footer = QLabel("Phiên bản 1.0 • Fuzzy Logic Expert System")
        footer.setObjectName("login_footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(footer)

        # Default credentials hint
        hint = QLabel("Tài khoản mặc định: admin / 123456")
        hint.setObjectName("login_footer")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(hint)

        main_layout.addWidget(card)

    def _on_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        success, message, user_data = self.auth_controller.login(username, password)

        if success:
            self.error_label.setVisible(False)
            self.login_success.emit(user_data)
        else:
            self.error_label.setText(f"❌ {message}")
            self.error_label.setVisible(True)

    def reset(self):
        """Reset form fields."""
        self.username_input.clear()
        self.password_input.clear()
        self.error_label.setVisible(False)
        self.username_input.setFocus()
