"""
Giao diện Tổng quan - Thống kê, truy cập nhanh và hoạt động gần đây.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QFrame, QGridLayout, QPushButton, QScrollArea,
                              QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPoint, QTimer
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QLinearGradient
from datetime import datetime

class BarChart(QWidget):
    """Widget biểu đồ cột tùy chỉnh đẹp mắt."""
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data or {} # {"label": value}
        self.setMinimumHeight(220)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        if not self.data: return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height() - 40 # khoảng trống cho nhãn
        margin = 40
        
        max_val = max(self.data.values()) if self.data.values() else 1
        if max_val == 0: max_val = 1
        
        bar_width = (width - 2 * margin) / len(self.data)
        
        # Màu sắc
        text_color = QColor("#a0aec0")
        
        for i, (label, val) in enumerate(self.data.items()):
            bar_height = (val / max_val) * (height - margin)
            x = margin + i * bar_width + 15
            y = height - bar_height
            
            # Gradient cho cột
            gradient = QLinearGradient(0, y, 0, height)
            gradient.setColorAt(0.0, QColor("#667eea"))
            gradient.setColorAt(1.0, QColor("#764ba2"))
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            # Vẽ cột với góc trên bo tròn
            painter.drawRoundedRect(int(x), int(y), int(bar_width - 30), int(bar_height), 6, 6)
            
            # Vẽ nhãn
            painter.setPen(text_color)
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(QRect(int(x - 15), int(height + 10), int(bar_width), 20), 
                             Qt.AlignmentFlag.AlignCenter, label)
            
            # Vẽ giá trị
            painter.setPen(QColor("#ffffff"))
            painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            painter.drawText(QRect(int(x - 15), int(y - 25), int(bar_width), 20), 
                             Qt.AlignmentFlag.AlignCenter, str(val))


class DashboardView(QWidget):
    """Tổng quan với thống kê, truy cập nhanh và hoạt động gần đây."""

    module_selected = pyqtSignal(str)
    action_requested = pyqtSignal(str)  # users, rules, history

    def __init__(self, consultation_controller, history_controller):
        super().__init__()
        self.consultation_ctrl = consultation_controller
        self.history_ctrl = history_controller
        self.user = self.history_ctrl.auth.get_current_user()
        self._setup_ui()
        # Bộ hẹn giờ tự động làm mới
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(30000) # Làm mới mỗi 30 giây

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        # Tiêu đề
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        greeting = f"👋 Xin chào, {self.user['full_name']}!" if self.user else "Dashboard"
        title = QLabel(greeting)
        title.setObjectName("page_title")
        title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #fff;")
        header_layout.addWidget(title)

        subtitle = QLabel("Tổng quan tình hình tư vấn pháp lý và trạng thái hệ thống")
        subtitle.setObjectName("page_subtitle")
        subtitle.setStyleSheet("font-size: 11pt; color: #a0aec0;")
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)

        # Thẻ thống kê (Hàng trên)
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        self.stat_total = self._create_stat_card("0", "Tổng tư vấn", "", "#3182ce")
        self.stat_transfer = self._create_stat_card("0", "Chuyển nhượng", "", "#38a169")
        self.stat_compensation = self._create_stat_card("0", "Bồi thường", "", "#d69e2e")
        self.stat_violation = self._create_stat_card("0", "Vi phạm", "", "#e53e3e")
        self.stat_tax = self._create_stat_card("0", "Thuế đất", "", "#805ad5")

        stats_layout.addWidget(self.stat_total)
        stats_layout.addWidget(self.stat_transfer)
        stats_layout.addWidget(self.stat_compensation)
        stats_layout.addWidget(self.stat_violation)
        stats_layout.addWidget(self.stat_tax)
        layout.addLayout(stats_layout)

        # Hàng giữa: Module & Thao tác nhanh
        mid_layout = QHBoxLayout()
        mid_layout.setSpacing(20)

        # Trái: Các Module
        modules_frame = QFrame()
        modules_layout = QVBoxLayout(modules_frame)
        modules_layout.setContentsMargins(0, 0, 0, 0)
        
        section_label = QLabel("Chọn Module Tư Vấn")
        section_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #e2e8f0; margin-bottom: 10px;")
        modules_layout.addWidget(section_label)

        mod_grid = QGridLayout()
        mod_grid.setSpacing(15)
        modules = self.consultation_ctrl.get_available_modules()
        for i, mod in enumerate(modules):
            card = self._create_module_card(mod["icon"], mod["display_name"], mod["description"], mod["name"])
            mod_grid.addWidget(card, i // 2, i % 2) # 2 columns
            
        modules_layout.addLayout(mod_grid)
        modules_layout.addStretch()
        mid_layout.addWidget(modules_frame, stretch=2)

        # Phải: Thao tác nhanh (Chỉ admin hoặc có quyền)
        if self.user and self.user.get('role') == 'admin':
            actions_frame = QFrame()
            actions_layout = QVBoxLayout(actions_frame)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            action_label = QLabel("⚡ Thao tác nhanh")
            action_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #e2e8f0; margin-bottom: 10px;")
            actions_layout.addWidget(action_label)
            
            btn_users = self._create_action_btn("Quản lý người dùng", "#4299e1")
            btn_users.clicked.connect(lambda: self.action_requested.emit("users"))
            
            btn_rules = self._create_action_btn("Quản lý luật mờ", "#48bb78")
            btn_rules.clicked.connect(lambda: self.action_requested.emit("rules"))
            
            btn_history = self._create_action_btn("Xem toàn bộ lịch sử", "#ed8936")
            btn_history.clicked.connect(lambda: self.action_requested.emit("history"))
            
            actions_layout.addWidget(btn_users)
            actions_layout.addWidget(btn_rules)
            actions_layout.addWidget(btn_history)
            actions_layout.addStretch()
            
            mid_layout.addWidget(actions_frame, stretch=1)
            
        layout.addLayout(mid_layout)

        # Hàng dưới: Biểu đồ & Hoạt động gần đây
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Trái: Biểu đồ
        chart_card = self._create_panel("Thống kê theo nghiệp vụ")
        chart_layout = QVBoxLayout(chart_card)
        self.bar_chart = BarChart()
        chart_layout.addWidget(self.bar_chart)
        bottom_layout.addWidget(chart_card, stretch=1)
        
        # Phải: Hoạt động gần đây
        recent_card = self._create_panel("🕒 Hoạt động gần đây")
        recent_layout = QVBoxLayout(recent_card)
        
        self.recent_table = QTableWidget(0, 4)
        self.recent_table.setHorizontalHeaderLabels(["Thời gian", "Người dùng", "Nghiệp vụ", "Kết quả"])
        self.recent_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.recent_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.recent_table.verticalHeader().setVisible(False)
        self.recent_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.recent_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.recent_table.setAlternatingRowColors(True)
        self.recent_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                color: #e2e8f0;
                gridline-color: #2d3748;
            }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #2d3748; }
            QHeaderView::section {
                background-color: #1a202c;
                color: #a0aec0;
                font-weight: bold;
                border: none;
                padding: 10px;
                text-align: left;
            }
        """)
        recent_layout.addWidget(self.recent_table)
        bottom_layout.addWidget(recent_card, stretch=1)

        layout.addLayout(bottom_layout)
        layout.addStretch()

    def _create_panel(self, title_text):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel(title_text)
        title.setStyleSheet("font-size: 13pt; font-weight: bold; color: #fff; border: none; background: transparent;")
        layout.addWidget(title)
        return panel

    def _create_action_btn(self, text, hover_color):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 15px;
                font-size: 11pt;
                font-weight: bold;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                color: white;
                border-color: {hover_color};
            }}
        """)
        return btn

    def _create_stat_card(self, value, label, icon, highlight_color):
        """Tạo thẻ thống kê với giao diện đẹp."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }}
            QFrame:hover {{
                border-color: {highlight_color};
            }}
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Bên trái: Văn bản
        text_layout = QVBoxLayout()
        val_label = QLabel(value)
        val_label.setStyleSheet(f"font-size: 24pt; font-weight: bold; color: {highlight_color}; border: none;")
        card.value_label = val_label # Lưu tham chiếu
        
        name_label = QLabel(label)
        name_label.setStyleSheet("font-size: 10pt; color: #94a3b8; border: none;")
        
        text_layout.addWidget(val_label)
        text_layout.addWidget(name_label)
        
        # Bên phải: Biểu tượng
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 28pt; border: none; background: transparent;")
        
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(icon_label)
        
        return card

    def _create_module_card(self, icon, title, description, module_name):
        """Tạo thẻ module có thể nhấp được."""
        card = QPushButton()
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        card.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 20px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2d3748;
                border-color: #667eea;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24pt; background: transparent; border: none;")
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #fff; background: transparent; border: none;")
        title_label.setWordWrap(True)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label, stretch=1)
        card_layout.addLayout(header_layout)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 9pt; color: #94a3b8; background: transparent; border: none;")
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)

        card.clicked.connect(lambda: self.module_selected.emit(module_name))
        return card

    def refresh_data(self):
        """Làm mới thống kê và lịch sử gần đây trên tổng quan."""
        self.refresh_stats()
        self.refresh_recent_activity()

    def refresh_stats(self):
        """Làm mới thống kê tổng quan."""
        try:
            stats = self.history_ctrl.get_statistics()
            self.stat_total.value_label.setText(str(stats.get("total", 0)))
            by_module = stats.get("by_module", {})
            self.stat_transfer.value_label.setText(str(by_module.get("transfer", 0)))
            self.stat_compensation.value_label.setText(str(by_module.get("compensation", 0)))
            self.stat_violation.value_label.setText(str(by_module.get("violation", 0)))
            self.stat_tax.value_label.setText(str(by_module.get("tax", 0)))
            
            # Cập nhật biểu đồ
            chart_data = {
                "Chuyển nhượng": by_module.get("transfer", 0),
                "Bồi thường": by_module.get("compensation", 0),
                "Vi phạm": by_module.get("violation", 0),
                "Thuế": by_module.get("tax", 0)
            }
            self.bar_chart.set_data(chart_data)
        except Exception as e:
            print(f"Error refreshing stats: {e}")

    def refresh_recent_activity(self):
        """Lấy và hiển thị các bản ghi gần đây."""
        try:
            # Lấy các bản ghi toàn cục cho admin, hoặc cá nhân cho người dùng
            recent_cases = self.history_ctrl.get_history(limit=5)
            self.recent_table.setRowCount(0)
            
            for row_idx, case in enumerate(recent_cases):
                self.recent_table.insertRow(row_idx)
                
                # Định dạng thời gian
                created_at = case.get("created_at", "")
                if created_at:
                    try:
                        dt = datetime.fromisoformat(created_at)
                        time_str = dt.strftime("%H:%M %d/%m")
                    except:
                        time_str = created_at[:16]
                else:
                    time_str = "K/A"
                    
                user_name = case.get("user_name", "Ẩn danh")
                module = case.get("module", "")
                
                # Định dạng kết luận
                score = case.get("score", 0)
                conclusion = case.get("conclusion", "")
                result_str = f"{score:.1f} - {conclusion}"
                
                item_time = QTableWidgetItem(time_str)
                item_user = QTableWidgetItem(user_name)
                item_mod = QTableWidgetItem(module)
                item_res = QTableWidgetItem(result_str)
                
                self.recent_table.setItem(row_idx, 0, item_time)
                self.recent_table.setItem(row_idx, 1, item_user)
                self.recent_table.setItem(row_idx, 2, item_mod)
                self.recent_table.setItem(row_idx, 3, item_res)
                
        except Exception as e:
            print(f"Error refreshing recent activity: {e}")

    def showEvent(self, event):
        """Được gọi khi giao diện trở nên hiển thị."""
        super().showEvent(event)
        self.refresh_data()
