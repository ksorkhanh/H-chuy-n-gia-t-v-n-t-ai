"""
History View - Consultation history with search and detail view.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QHeaderView, QComboBox, QDialog, QTextEdit,
                              QAbstractItemView, QFrame, QScrollArea,
                              QMessageBox)
from PyQt6.QtCore import Qt
import json


class HistoryView(QWidget):
    def __init__(self, history_controller):
        super().__init__()
        self.controller = history_controller
        self._setup_ui()
        self._load_history()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("Lịch Sử Tư Vấn")
        title.setObjectName("page_title")
        layout.addWidget(title)

        # Filters
        toolbar = QHBoxLayout()
        self.module_filter = QComboBox()
        self.module_filter.setMinimumHeight(38)
        self.module_filter.addItem("Tất cả", "")
        self.module_filter.addItem("Chuyển nhượng", "transfer")
        self.module_filter.addItem("Bồi thường", "compensation")
        self.module_filter.addItem("Vi phạm", "violation")
        self.module_filter.currentIndexChanged.connect(self._load_history)
        toolbar.addWidget(self.module_filter)
        toolbar.addStretch()

        btn_refresh = QPushButton("Làm Mới")
        btn_refresh.clicked.connect(self._load_history)
        toolbar.addWidget(btn_refresh)
        layout.addLayout(toolbar)

        # History table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Thời gian", "Module", "Người dùng", "Điểm", "Kết luận"])
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self._view_detail)
        layout.addWidget(self.table)

        # Actions
        actions = QHBoxLayout()
        btn_view = QPushButton("Xem Chi Tiết")
        btn_view.setProperty("class", "btn_primary")
        btn_view.clicked.connect(self._view_detail)
        
        btn_delete = QPushButton("Xóa Chọn")
        btn_delete.setStyleSheet("background-color: #e74c3c; color: white;")
        btn_delete.clicked.connect(self._delete_selected)
        
        btn_delete_all = QPushButton("Xóa Tất Cả")
        btn_delete_all.setStyleSheet("background-color: #c0392b; color: white;")
        btn_delete_all.clicked.connect(self._delete_all)
        
        actions.addWidget(btn_delete_all)
        actions.addWidget(btn_delete)
        actions.addStretch()
        actions.addWidget(btn_view)
        layout.addLayout(actions)

    def _delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một lịch sử để xóa.")
            return
            
        case_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, 'Xác nhận xóa', 
                                     f"Bạn có chắc chắn muốn xóa lịch sử #{case_id} không?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
                                     
        if reply == QMessageBox.StandardButton.Yes:
            if self.controller.delete_case(case_id):
                QMessageBox.information(self, "Thành công", "Đã xóa lịch sử.")
                self._load_history()
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể xóa lịch sử này.")

    def _delete_all(self):
        reply = QMessageBox.question(self, 'Xác nhận xóa tất cả', 
                                     "Bạn có chắc chắn muốn xóa TẤT CẢ lịch sử tư vấn không?\nHành động này không thể hoàn tác!",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
                                     
        if reply == QMessageBox.StandardButton.Yes:
            if hasattr(self.controller, 'delete_all_cases') and self.controller.delete_all_cases():
                QMessageBox.information(self, "Thành công", "Đã xóa tất cả lịch sử.")
                self._load_history()
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể xóa lịch sử.")

    def _load_history(self):
        module = self.module_filter.currentData()
        if module:
            cases = self.controller.search_history(module=module)
        else:
            cases = self.controller.get_history()

        module_names = {"transfer": "Chuyển nhượng", "compensation": "Bồi thường", "violation": "Vi phạm", "tax": "Thuế đất"}
        self.table.setRowCount(len(cases))
        for i, c in enumerate(cases):
            self.table.setItem(i, 0, QTableWidgetItem(str(c["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(str(c["created_at"])))
            self.table.setItem(i, 2, QTableWidgetItem(
                module_names.get(c["module"], c["module"])))
            self.table.setItem(i, 3, QTableWidgetItem(c.get("user_name", "")))
            score = c.get("score")
            score_item = QTableWidgetItem(f"{score:.1f}" if score else "—")
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Apply color based on score
            if score is not None:
                score_item.setForeground(Qt.GlobalColor.black)
                if score >= 70:
                    score_item.setBackground(Qt.GlobalColor.green)
                elif score >= 40:
                    score_item.setBackground(Qt.GlobalColor.yellow)
                else:
                    score_item.setBackground(Qt.GlobalColor.red)
            
            self.table.setItem(i, 4, score_item)
            self.table.setItem(i, 5, QTableWidgetItem(c.get("conclusion") or ""))

    def _view_detail(self):
        row = self.table.currentRow()
        if row < 0:
            return
        case_id = int(self.table.item(row, 0).text())
        case = self.controller.get_case_detail(case_id)
        if case:
            dialog = CaseDetailDialog(self, case)
            dialog.exec()


class CaseDetailDialog(QDialog):
    def __init__(self, parent, case_data):
        super().__init__(parent)
        self.setWindowTitle(f"Chi Tiết Bản Ghi #{case_data['id']}")
        self.setMinimumSize(600, 500)
        self.setStyleSheet("""
            QDialog { background-color: #ffffff; }
            QLabel { color: #333; }
            QPushButton { color: #333; background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px; }
        """)

        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        content_layout = QVBoxLayout(content)

        # Header
        header = QLabel(f"Bản Ghi #{case_data['id']}")
        header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #667eea;")
        content_layout.addWidget(header)

        info_text = (
            f"📅 Thời gian: {case_data.get('created_at', '')}\n"
            f"Người dùng: {case_data.get('user_name', '')}\n"
            f"Module: {case_data.get('module', '')}\n"
            f"Điểm: {case_data.get('score', 'K/A')}\n"
            f"Kết luận: {case_data.get('conclusion', '')}"
        )
        info = QLabel(info_text)
        info.setStyleSheet("color: #222; font-size: 10pt; padding: 10px; "
                          "background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px;")
        content_layout.addWidget(info)

        # Input data
        input_data = case_data.get("input_data", {})
        if input_data:
            inp_title = QLabel("📥 Dữ Liệu Đầu Vào")
            inp_title.setStyleSheet("font-size: 12pt; font-weight: bold; color: #1a1a1a; margin-top: 10px;")
            content_layout.addWidget(inp_title)

            if isinstance(input_data, dict):
                for k, v in input_data.items():
                    content_layout.addWidget(QLabel(f"  • {k}: {v}"))

        # Result data
        result_data = case_data.get("result_data", {})
        if result_data:
            res_title = QLabel("Kết Quả")
            res_title.setStyleSheet("font-size: 12pt; font-weight: bold; color: #1a1a1a; margin-top: 10px;")
            content_layout.addWidget(res_title)

            if isinstance(result_data, dict):
                for k, v in result_data.items():
                    content_layout.addWidget(QLabel(f"  • {k}: {v}"))

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)
