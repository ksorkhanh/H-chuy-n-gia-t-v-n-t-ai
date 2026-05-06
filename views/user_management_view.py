"""
User Management View - Admin panel for managing users.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QHeaderView, QDialog, QFormLayout, QLineEdit,
                              QComboBox, QMessageBox, QAbstractItemView)
from PyQt6.QtCore import Qt


class UserManagementView(QWidget):
    def __init__(self, user_controller):
        super().__init__()
        self.controller = user_controller
        self._setup_ui()
        self._load_users()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("👥  Quản Lý Người Dùng")
        title.setObjectName("page_title")
        layout.addWidget(title)

        toolbar = QHBoxLayout()
        toolbar.addStretch()
        btn_add = QPushButton("➕ Thêm Người Dùng")
        btn_add.setProperty("class", "btn_primary")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._add_user)
        toolbar.addWidget(btn_add)
        btn_refresh = QPushButton("🔄 Làm Mới")
        btn_refresh.clicked.connect(self._load_users)
        toolbar.addWidget(btn_refresh)
        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Họ tên", "Email", "Vai trò", "Trạng thái"])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        actions = QHBoxLayout()
        btn_edit = QPushButton("✏️ Sửa")
        btn_edit.clicked.connect(self._edit_user)
        btn_reset = QPushButton("🔑 Reset MK")
        btn_reset.setProperty("class", "btn_warning")
        btn_reset.clicked.connect(self._reset_password)
        btn_del = QPushButton("🗑️ Xóa")
        btn_del.setProperty("class", "btn_danger")
        btn_del.clicked.connect(self._delete_user)
        actions.addStretch()
        actions.addWidget(btn_edit)
        actions.addWidget(btn_reset)
        actions.addWidget(btn_del)
        layout.addLayout(actions)

    def _load_users(self):
        try:
            users = self.controller.get_all_users()
        except PermissionError:
            QMessageBox.warning(self, "Lỗi", "Không có quyền")
            return
        role_map = {"admin": "Quản trị viên", "staff": "Nhân viên", "expert": "Chuyên gia", "guest": "Khách"}
        self.table.setRowCount(len(users))
        for i, u in enumerate(users):
            self.table.setItem(i, 0, QTableWidgetItem(str(u["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(u["username"]))
            self.table.setItem(i, 2, QTableWidgetItem(u["full_name"]))
            self.table.setItem(i, 3, QTableWidgetItem(u.get("email") or ""))
            self.table.setItem(i, 4, QTableWidgetItem(role_map.get(u["role"], u["role"])))
            self.table.setItem(i, 5, QTableWidgetItem("✅" if u["is_active"] else "❌"))

    def _add_user(self):
        d = UserDialog(self)
        if d.exec() == QDialog.DialogCode.Accepted:
            data = d.get_data()
            try:
                self.controller.create_user(**data)
                self._load_users()
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    def _edit_user(self):
        row = self.table.currentRow()
        if row < 0: return
        uid = int(self.table.item(row, 0).text())
        user = self.controller.get_user(uid)
        if user:
            d = UserDialog(self, user.to_dict(), True)
            if d.exec() == QDialog.DialogCode.Accepted:
                data = d.get_data()
                try:
                    self.controller.update_user(uid, full_name=data["full_name"],
                        email=data.get("email"), role=data["role"])
                    self._load_users()
                except Exception as e:
                    QMessageBox.warning(self, "Lỗi", str(e))

    def _reset_password(self):
        row = self.table.currentRow()
        if row < 0: return
        uid = int(self.table.item(row, 0).text())
        if QMessageBox.question(self, "Xác nhận", "Reset mật khẩu về '123456'?") == QMessageBox.StandardButton.Yes:
            try:
                self.controller.reset_password(uid)
                QMessageBox.information(self, "OK", "Đã reset mật khẩu")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    def _delete_user(self):
        row = self.table.currentRow()
        if row < 0: return
        uid = int(self.table.item(row, 0).text())
        if QMessageBox.question(self, "Xác nhận", "Xóa người dùng này?") == QMessageBox.StandardButton.Yes:
            try:
                self.controller.delete_user(uid)
                self._load_users()
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))


class UserDialog(QDialog):
    def __init__(self, parent=None, data=None, edit_mode=False):
        super().__init__(parent)
        self.edit_mode = edit_mode
        self.setWindowTitle("Sửa" if edit_mode else "Thêm Người Dùng")
        self.setMinimumWidth(400)
        self.setStyleSheet("QDialog { background-color: #1a1d23; }")
        layout = QFormLayout(self)
        self.username_input = QLineEdit(data.get("username", "") if data else "")
        if edit_mode: self.username_input.setEnabled(False)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.fullname_input = QLineEdit(data.get("full_name", "") if data else "")
        self.email_input = QLineEdit(data.get("email", "") if data else "")
        self.role_input = QComboBox()
        for label, val in [("Quản trị viên","admin"),("Nhân viên","staff"),("Chuyên gia","expert"),("Khách","guest")]:
            self.role_input.addItem(label, val)
        if data and data.get("role"):
            for i in range(self.role_input.count()):
                if self.role_input.itemData(i) == data["role"]:
                    self.role_input.setCurrentIndex(i); break
        layout.addRow("Username:", self.username_input)
        if not edit_mode: layout.addRow("Mật khẩu:", self.password_input)
        layout.addRow("Họ tên:", self.fullname_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Vai trò:", self.role_input)
        bl = QHBoxLayout()
        bs = QPushButton("💾 Lưu"); bs.setProperty("class","btn_primary"); bs.clicked.connect(self.accept)
        bc = QPushButton("Hủy"); bc.clicked.connect(self.reject)
        bl.addStretch(); bl.addWidget(bs); bl.addWidget(bc)
        layout.addRow(bl)

    def get_data(self):
        d = {"username": self.username_input.text(), "full_name": self.fullname_input.text(),
             "email": self.email_input.text() or None, "role": self.role_input.currentData()}
        if not self.edit_mode: d["password"] = self.password_input.text()
        return d
