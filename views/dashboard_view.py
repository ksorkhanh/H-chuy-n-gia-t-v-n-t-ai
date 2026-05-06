"""
Dashboard View - Statistics overview and quick access to modules.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QFrame, QGridLayout, QPushButton, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor, QFont, QPen


class BarChart(QWidget):
    """A simple custom bar chart widget."""
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data or {} # {"label": value}
        self.setMinimumHeight(200)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        if not self.data: return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height() - 40 # space for labels
        margin = 40
        
        max_val = max(self.data.values()) if self.data.values() else 1
        if max_val == 0: max_val = 1
        
        bar_width = (width - 2 * margin) / len(self.data)
        
        # Colors
        bar_color = QColor("#667eea")
        text_color = QColor("#888")
        
        for i, (label, val) in enumerate(self.data.items()):
            # Calculate rect
            bar_height = (val / max_val) * (height - margin)
            x = margin + i * bar_width + 10
            y = height - bar_height
            
            # Draw bar
            painter.setBrush(bar_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(int(x), int(y), int(bar_width - 20), int(bar_height), 5, 5)
            
            # Draw label
            painter.setPen(text_color)
            painter.setFont(QFont("Arial", 8))
            painter.drawText(QRect(int(x - 10), int(height + 5), int(bar_width), 20), 
                             Qt.AlignmentFlag.AlignCenter, label)
            
            # Draw value
            painter.drawText(QRect(int(x - 10), int(y - 20), int(bar_width), 20), 
                             Qt.AlignmentFlag.AlignCenter, str(val))


class DashboardView(QWidget):
    """Dashboard with statistics and module quick access."""

    module_selected = pyqtSignal(str)  # Emitted when a module card is clicked

    def __init__(self, consultation_controller, history_controller):
        super().__init__()
        self.consultation_ctrl = consultation_controller
        self.history_ctrl = history_controller
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        # Page title
        title = QLabel("📊  Dashboard")
        title.setObjectName("page_title")
        layout.addWidget(title)

        subtitle = QLabel("Tổng quan hệ thống tư vấn pháp lý")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(subtitle)

        # Statistics cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        self.stat_total = self._create_stat_card("0", "Tổng số tư vấn", "📋")
        self.stat_transfer = self._create_stat_card("0", "Chuyển nhượng", "🔄")
        self.stat_compensation = self._create_stat_card("0", "Bồi thường", "💰")
        self.stat_violation = self._create_stat_card("0", "Vi phạm", "⚖️")
        self.stat_tax = self._create_stat_card("0", "Thuế đất", "💲")

        stats_layout.addWidget(self.stat_total)
        stats_layout.addWidget(self.stat_transfer)
        stats_layout.addWidget(self.stat_compensation)
        stats_layout.addWidget(self.stat_violation)
        stats_layout.addWidget(self.stat_tax)
        layout.addLayout(stats_layout)

        # Module section title
        section_label = QLabel("🚀  Chọn Module Tư Vấn")
        section_label.setProperty("class", "section_title")
        layout.addWidget(section_label)

        # Module cards
        modules_layout = QHBoxLayout()
        modules_layout.setSpacing(15)

        modules = self.consultation_ctrl.get_available_modules()
        for mod in modules:
            card = self._create_module_card(
                mod["icon"], mod["display_name"], mod["description"], mod["name"]
            )
            modules_layout.addWidget(card)

        # Fill remaining space if fewer than 3 modules
        while modules_layout.count() < 3:
            spacer = QWidget()
            modules_layout.addWidget(spacer)

        layout.addLayout(modules_layout)

        # Info section
        info_frame = QFrame()
        info_frame.setProperty("class", "card")
        info_frame.setStyleSheet("""
            QFrame { background-color: #22252d; border: 1px solid #2a2d35;
                     border-radius: 12px; padding: 20px; }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_title = QLabel("ℹ️  Về Hệ Thống")
        info_title.setProperty("class", "card_title")
        info_layout.addWidget(info_title)

        info_text = QLabel(
            "Hệ thống chuyên gia tư vấn pháp lý sử dụng Fuzzy Logic (Mamdani) "
            "để đánh giá và tư vấn các vấn đề liên quan đến Luật Đất đai 2024.\n\n"
            "• Cơ sở pháp lý: Luật Đất đai 2024, NĐ 88/2024, NĐ 91/2019\n"
            "• Phương pháp: Suy diễn mờ Mamdani với defuzzification Centroid\n"
            "• Thiết kế: MVC, plugin-based, có khả năng mở rộng"
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: #888; line-height: 1.6;")
        info_layout.addWidget(info_text)
        layout.addWidget(info_frame)

        # Recent Activity / Chart Section
        chart_section = QHBoxLayout()
        
        # Left: Chart
        self.chart_card = QFrame()
        self.chart_card.setProperty("class", "card")
        self.chart_card.setMinimumWidth(400)
        chart_layout = QVBoxLayout(self.chart_card)
        chart_layout.addWidget(QLabel("📈 Thống kê theo nghiệp vụ"))
        self.bar_chart = BarChart()
        chart_layout.addWidget(self.bar_chart)
        chart_section.addWidget(self.chart_card)
        
        layout.addLayout(chart_section)
        layout.addStretch()

    def _create_stat_card(self, value, label, icon):
        """Create a statistics card."""
        card = QFrame()
        card.setProperty("class", "stat_card")
        card.setStyleSheet("""
            QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #22252d, stop:1 #2a2d38);
                border: 1px solid #2a2d35; border-radius: 12px; padding: 20px; }
        """)
        card_layout = QVBoxLayout(card)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24pt;")
        card_layout.addWidget(icon_label)

        value_label = QLabel(value)
        value_label.setObjectName(f"stat_value_{label}")
        value_label.setProperty("class", "stat_value")
        value_label.setStyleSheet("font-size: 28pt; font-weight: bold; color: #667eea;")
        card_layout.addWidget(value_label)

        text_label = QLabel(label)
        text_label.setProperty("class", "stat_label")
        text_label.setStyleSheet("font-size: 9pt; color: #888;")
        card_layout.addWidget(text_label)

        # Store reference for updating
        card.value_label = value_label
        return card

    def _create_module_card(self, icon, title, description, module_name):
        """Create a clickable module card."""
        card = QPushButton()
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setStyleSheet("""
            QPushButton {
                background-color: #22252d; border: 1px solid #2a2d35;
                border-radius: 12px; padding: 25px; text-align: left;
            }
            QPushButton:hover {
                border-color: #667eea;
                background-color: #262a33;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32pt;")
        card_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13pt; font-weight: bold; color: #fff;")
        title_label.setWordWrap(True)
        card_layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 9pt; color: #888;")
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)

        card_layout.addStretch()

        card.clicked.connect(lambda: self.module_selected.emit(module_name))
        return card

    def refresh_stats(self):
        """Refresh dashboard statistics."""
        try:
            stats = self.history_ctrl.get_statistics()
            self.stat_total.value_label.setText(str(stats.get("total", 0)))
            by_module = stats.get("by_module", {})
            self.stat_transfer.value_label.setText(str(by_module.get("transfer", 0)))
            self.stat_compensation.value_label.setText(str(by_module.get("compensation", 0)))
            self.stat_violation.value_label.setText(str(by_module.get("violation", 0)))
            self.stat_tax.value_label.setText(str(by_module.get("tax", 0)))
            
            # Update chart
            chart_data = {
                "Chuyển nhượng": by_module.get("transfer", 0),
                "Bồi thường": by_module.get("compensation", 0),
                "Vi phạm": by_module.get("violation", 0),
                "Thuế": by_module.get("tax", 0)
            }
            self.bar_chart.set_data(chart_data)
        except Exception:
            pass
