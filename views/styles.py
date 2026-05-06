"""
QSS Stylesheet - Modern dark theme for the Legal Expert System.
Premium design with gradients, shadows, and smooth styling.
"""

MAIN_STYLESHEET = """
/* ============================================================
   Global Styles
   ============================================================ */
QWidget {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 10pt;
    color: #e0e0e0;
}

QMainWindow {
    background-color: #1a1d23;
}

/* ============================================================
   Sidebar
   ============================================================ */
#sidebar {
    background-color: #12151a;
    border-right: 1px solid #2a2d35;
    min-width: 260px;
    max-width: 260px;
}

#sidebar QPushButton {
    text-align: left;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    margin: 2px 10px;
    font-size: 10pt;
    color: #a0a4b0;
    background-color: transparent;
}

#sidebar QPushButton:hover {
    background-color: #1e2330;
    color: #ffffff;
}

#sidebar QPushButton:checked,
#sidebar QPushButton[active="true"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    color: #ffffff;
    font-weight: bold;
}

#sidebar_header {
    padding: 20px;
    border-bottom: 1px solid #2a2d35;
}

#sidebar_title {
    font-size: 14pt;
    font-weight: bold;
    color: #667eea;
}

#sidebar_subtitle {
    font-size: 8pt;
    color: #666;
    margin-top: 4px;
}

#user_info_label {
    color: #888;
    font-size: 9pt;
    padding: 10px 20px;
    border-top: 1px solid #2a2d35;
}

/* ============================================================
   Content Area
   ============================================================ */
#content_area {
    background-color: #1a1d23;
}

#page_title {
    font-size: 18pt;
    font-weight: bold;
    color: #ffffff;
    padding: 10px 0;
}

#page_subtitle {
    font-size: 10pt;
    color: #888;
    padding-bottom: 10px;
}

/* ============================================================
   Cards
   ============================================================ */
.card {
    background-color: #22252d;
    border: 1px solid #2a2d35;
    border-radius: 12px;
    padding: 20px;
}

.card:hover {
    border-color: #667eea;
}

.card_title {
    font-size: 13pt;
    font-weight: bold;
    color: #ffffff;
}

.card_subtitle {
    font-size: 9pt;
    color: #888;
    margin-top: 4px;
}

/* ============================================================
   Stat Cards (Dashboard)
   ============================================================ */
.stat_card {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #22252d, stop:1 #2a2d38);
    border: 1px solid #2a2d35;
    border-radius: 12px;
    padding: 20px;
}

.stat_value {
    font-size: 28pt;
    font-weight: bold;
    color: #667eea;
}

.stat_label {
    font-size: 9pt;
    color: #888;
    margin-top: 5px;
}

/* ============================================================
   Buttons
   ============================================================ */
QPushButton {
    padding: 8px 20px;
    border-radius: 8px;
    font-weight: 500;
    border: 1px solid #3a3d45;
    background-color: #2a2d35;
    color: #e0e0e0;
}

QPushButton:hover {
    background-color: #3a3d45;
    border-color: #667eea;
}

QPushButton:pressed {
    background-color: #1a1d23;
}

QPushButton:disabled {
    background-color: #1a1d23;
    color: #555;
    border-color: #2a2d35;
}

.btn_primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border: none;
    color: white;
    font-weight: bold;
    padding: 10px 30px;
}

.btn_primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7b8ef8, stop:1 #8b5fbf);
}

.btn_danger {
    background-color: #e74c3c;
    border: none;
    color: white;
}

.btn_danger:hover {
    background-color: #c0392b;
}

.btn_success {
    background-color: #27ae60;
    border: none;
    color: white;
}

.btn_success:hover {
    background-color: #219a52;
}

.btn_warning {
    background-color: #f39c12;
    border: none;
    color: white;
}

/* ============================================================
   Input Fields
   ============================================================ */
QLineEdit, QTextEdit, QPlainTextEdit {
    padding: 8px 12px;
    border: 1px solid #3a3d45;
    border-radius: 8px;
    background-color: #22252d;
    color: #e0e0e0;
    selection-background-color: #667eea;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #667eea;
}

QComboBox {
    padding: 8px 12px;
    border: 1px solid #3a3d45;
    border-radius: 8px;
    background-color: #22252d;
    color: #e0e0e0;
}

QComboBox:focus {
    border-color: #667eea;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox QAbstractItemView {
    background-color: #22252d;
    border: 1px solid #3a3d45;
    color: #e0e0e0;
    selection-background-color: #667eea;
}

QSpinBox, QDoubleSpinBox {
    padding: 8px 12px;
    border: 1px solid #3a3d45;
    border-radius: 8px;
    background-color: #22252d;
    color: #e0e0e0;
}

/* ============================================================
   Sliders
   ============================================================ */
QSlider::groove:horizontal {
    border: none;
    height: 6px;
    background-color: #3a3d45;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #667eea, stop:1 #764ba2);
    border: none;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border-radius: 3px;
}

/* ============================================================
   Tables
   ============================================================ */
QTableWidget {
    background-color: #22252d;
    border: 1px solid #2a2d35;
    border-radius: 8px;
    gridline-color: #2a2d35;
    color: #e0e0e0;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #2a2d35;
}

QTableWidget::item:selected {
    background-color: #667eea;
    color: white;
}

QHeaderView::section {
    background-color: #1a1d23;
    color: #a0a4b0;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #667eea;
    font-weight: bold;
}

/* ============================================================
   Scroll Bars
   ============================================================ */
QScrollBar:vertical {
    background-color: #1a1d23;
    width: 10px;
    border: none;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #3a3d45;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #667eea;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #1a1d23;
    height: 10px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #3a3d45;
    border-radius: 5px;
    min-width: 30px;
}

/* ============================================================
   Tab Widget
   ============================================================ */
QTabWidget::pane {
    border: 1px solid #2a2d35;
    border-radius: 8px;
    background-color: #22252d;
}

QTabBar::tab {
    padding: 10px 20px;
    background-color: #1a1d23;
    color: #888;
    border: none;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #22252d;
    color: #667eea;
    border-bottom: 2px solid #667eea;
}

/* ============================================================
   Labels
   ============================================================ */
QLabel {
    color: #e0e0e0;
}

.section_title {
    font-size: 14pt;
    font-weight: bold;
    color: #ffffff;
    padding: 10px 0 5px 0;
}

.field_label {
    font-size: 9pt;
    color: #a0a4b0;
    font-weight: bold;
    margin-bottom: 4px;
}

.description_label {
    font-size: 8pt;
    color: #666;
    font-style: italic;
}

/* ============================================================
   Group Box
   ============================================================ */
QGroupBox {
    border: 1px solid #2a2d35;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 15px;
    font-weight: bold;
    color: #a0a4b0;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
}

/* ============================================================
   Message Box / Dialog
   ============================================================ */
QMessageBox {
    background-color: #22252d;
}

QDialog {
    background-color: #1a1d23;
}

/* ============================================================
   Progress Bar
   ============================================================ */
QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #2a2d35;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    border-radius: 4px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
}

/* ============================================================
   Tool Tips
   ============================================================ */
QToolTip {
    background-color: #22252d;
    color: #e0e0e0;
    border: 1px solid #667eea;
    border-radius: 4px;
    padding: 6px;
}
"""

# Login page specific styles
LOGIN_STYLESHEET = """
#login_container {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0f0c29, stop:0.5 #302b63, stop:1 #24243e);
}

#login_card {
    background-color: rgba(34, 37, 45, 240);
    border: 1px solid #3a3d45;
    border-radius: 16px;
    padding: 40px;
    min-width: 380px;
}

#login_title {
    font-size: 22pt;
    font-weight: bold;
    color: #ffffff;
}

#login_subtitle {
    font-size: 10pt;
    color: #888;
    margin-bottom: 20px;
}

#login_icon {
    font-size: 48pt;
}

#login_input {
    padding: 12px 16px;
    border: 1px solid #3a3d45;
    border-radius: 10px;
    background-color: #1a1d23;
    color: #e0e0e0;
    font-size: 11pt;
}

#login_input:focus {
    border-color: #667eea;
}

#login_btn {
    padding: 12px;
    border-radius: 10px;
    font-size: 12pt;
    font-weight: bold;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #667eea, stop:1 #764ba2);
    border: none;
    color: white;
}

#login_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7b8ef8, stop:1 #8b5fbf);
}

#login_error {
    color: #e74c3c;
    font-size: 9pt;
}

#login_footer {
    color: #555;
    font-size: 8pt;
}
"""

# Result display colors
RESULT_COLORS = {
    "high": "#27ae60",
    "medium": "#f39c12",
    "low": "#e74c3c",
    "heavy": "#e74c3c",
    "light": "#27ae60"
}
