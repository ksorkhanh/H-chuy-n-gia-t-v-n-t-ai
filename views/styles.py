"""
QSS Stylesheet - Enterprise Flat Theme.
Loads colors and fonts from config/theme.json dynamically.
"""
import json
import os

# Load theme variables
THEME_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'theme.json')
try:
    with open(THEME_FILE, 'r', encoding='utf-8') as f:
        THEME = json.load(f)
except Exception:
    # Fallback to Enterprise Dark Theme
    THEME = {
        "font_family": "'Segoe UI', 'Inter', 'Roboto', 'Arial', sans-serif",
        "font_size": "10pt",
        "bg_primary": "#1E1E1E",
        "bg_secondary": "#252526",
        "bg_tertiary": "#2D2D2D",
        "input_bg": "#333333",
        "border_color": "#3E3E42",
        "accent_color": "#0078D4",
        "accent_hover": "#106EBE",
        "text_primary": "#CCCCCC",
        "text_highlight": "#FFFFFF",
        "text_muted": "#FFFFFF",
        "success_color": "#107C10",
        "warning_color": "#D83B01",
        "danger_color": "#D13438"
    }

_GLOBAL_STYLESHEET_TEMPLATE = """
/* ============================================================
   Global Styles
   ============================================================ */
QWidget {
    font-family: @font_family@;
    font-size: @font_size@;
    color: @text_primary@;
}

QMainWindow {
    background-color: @bg_primary@;
}

/* ============================================================
   Sidebar
   ============================================================ */
#sidebar {
    background-color: @bg_secondary@;
    border-right: 1px solid @border_color@;
    min-width: 260px;
    max-width: 260px;
}

#sidebar QPushButton {
    text-align: left;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    margin: 2px 10px;
    font-size: @font_size@;
    font-weight: bold;
    color: @text_primary@;
    background-color: transparent;
}

#sidebar QPushButton:hover {
    background-color: @bg_tertiary@;
    color: @text_highlight@;
}

#sidebar QPushButton:checked,
#sidebar QPushButton[active="true"] {
    background-color: @accent_color@;
    color: @text_highlight@;
}

#sidebar_header {
    padding: 20px;
    border-bottom: 1px solid @border_color@;
}

#sidebar_title {
    font-size: 14pt;
    font-weight: bold;
    color: @text_highlight@;
}

#sidebar_subtitle {
    font-size: 8pt;
    color: @text_muted@;
    margin-top: 4px;
}

#user_info_label {
    color: @text_muted@;
    font-size: 9pt;
    padding: 10px 20px;
    border-top: 1px solid @border_color@;
}

/* ============================================================
   Content Area
   ============================================================ */
#content_area {
    background-color: @bg_primary@;
}

#page_title {
    font-size: 18pt;
    font-weight: bold;
    color: @text_highlight@;
    padding: 10px 0;
}

#page_subtitle {
    font-size: 10pt;
    color: @text_muted@;
    padding-bottom: 10px;
}

/* ============================================================
   Cards
   ============================================================ */
*[class="card"] {
    background-color: @bg_tertiary@;
    border: 1px solid @border_color@;
    border-radius: 4px;
    padding: 20px;
}

*[class="card"]:hover {
    border-color: @accent_color@;
}

*[class="card_title"] {
    font-size: 12pt;
    font-weight: bold;
    color: @text_highlight@;
}

*[class="card_subtitle"] {
    font-size: 9pt;
    color: @text_muted@;
    margin-top: 4px;
}

/* ============================================================
   Stat Cards (Dashboard)
   ============================================================ */
*[class="stat_card"] {
    background-color: @bg_secondary@;
    border: 1px solid @border_color@;
    border-left: 4px solid @accent_color@;
    border-radius: 4px;
    padding: 20px;
}

*[class="stat_value"] {
    font-size: 24pt;
    font-weight: bold;
    color: @text_highlight@;
}

*[class="stat_label"] {
    font-size: 9pt;
    color: @text_muted@;
    margin-top: 5px;
    text-transform: uppercase;
}

/* ============================================================
   Buttons
   ============================================================ */
QPushButton {
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    border: 1px solid @border_color@;
    background-color: @input_bg@;
    color: @text_primary@;
}

QPushButton:hover {
    background-color: @border_color@;
    color: @text_highlight@;
}

QPushButton:pressed {
    background-color: @bg_secondary@;
}

QPushButton:disabled {
    background-color: @bg_primary@;
    color: @text_muted@;
    border-color: @bg_tertiary@;
}

*[class="btn_primary"] {
    background-color: @accent_color@;
    border: 1px solid @accent_color@;
    color: #FFFFFF;
    padding: 8px 24px;
}

*[class="btn_primary"]:hover {
    background-color: @accent_hover@;
    border-color: @accent_hover@;
}

*[class="btn_danger"] {
    background-color: @danger_color@;
    border: 1px solid @danger_color@;
    color: #FFFFFF;
}

*[class="btn_danger"]:hover {
    background-color: #A4262C;
    border-color: #A4262C;
}

*[class="btn_success"] {
    background-color: @success_color@;
    border: 1px solid @success_color@;
    color: #FFFFFF;
}

*[class="btn_success"]:hover {
    background-color: #0B5A0B;
    border-color: #0B5A0B;
}

*[class="btn_warning"] {
    background-color: @warning_color@;
    border: 1px solid @warning_color@;
    color: #FFFFFF;
}

/* ============================================================
   Input Fields
   ============================================================ */
QLineEdit, QTextEdit, QPlainTextEdit {
    padding: 8px 12px;
    border: 1px solid @border_color@;
    border-radius: 4px;
    background-color: @input_bg@;
    color: @text_highlight@;
    selection-background-color: @accent_color@;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: @accent_color@;
    background-color: @bg_secondary@;
}

QComboBox {
    padding: 8px 12px;
    border: 1px solid @border_color@;
    border-radius: 4px;
    background-color: @input_bg@;
    color: @text_highlight@;
}

QComboBox:focus {
    border-color: @accent_color@;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
    background-color: transparent;
}

QComboBox QAbstractItemView {
    background-color: @bg_tertiary@;
    border: 1px solid @border_color@;
    color: @text_highlight@;
    selection-background-color: @accent_color@;
    selection-color: #FFFFFF;
}

QSpinBox, QDoubleSpinBox {
    padding: 8px 12px;
    border: 1px solid @border_color@;
    border-radius: 4px;
    background-color: @input_bg@;
    color: @text_highlight@;
}

/* ============================================================
   Sliders
   ============================================================ */
QSlider::groove:horizontal {
    border: none;
    height: 4px;
    background-color: @border_color@;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background-color: @accent_color@;
    border: none;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}

QSlider::sub-page:horizontal {
    background-color: @accent_color@;
    border-radius: 2px;
}

/* ============================================================
   Tables
   ============================================================ */
QTableWidget {
    background-color: @bg_secondary@;
    border: 1px solid @border_color@;
    border-radius: 4px;
    gridline-color: @border_color@;
    color: @text_primary@;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid @border_color@;
}

QTableWidget::item:selected {
    background-color: @accent_hover@;
    color: #FFFFFF;
}

QHeaderView::section {
    background-color: @bg_tertiary@;
    color: @text_primary@;
    padding: 10px;
    border: none;
    border-right: 1px solid @border_color@;
    border-bottom: 1px solid @border_color@;
    font-weight: bold;
    text-transform: uppercase;
}

/* ============================================================
   Scroll Bars
   ============================================================ */
QScrollBar:vertical {
    background-color: @bg_primary@;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: @border_color@;
    border-radius: 0px;
    min-height: 30px;
    margin: 0px 2px 0px 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: @text_muted@;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: @bg_primary@;
    height: 12px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: @border_color@;
    border-radius: 0px;
    min-width: 30px;
    margin: 2px 0px 2px 0px;
}

/* ============================================================
   Tab Widget
   ============================================================ */
QTabWidget::pane {
    border: 1px solid @border_color@;
    border-top: none;
    background-color: @bg_secondary@;
}

QTabBar::tab {
    padding: 10px 20px;
    background-color: @bg_tertiary@;
    color: @text_muted@;
    border: 1px solid @border_color@;
    border-bottom: none;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: @bg_secondary@;
    color: @accent_color@;
    font-weight: bold;
    border-top: 2px solid @accent_color@;
}

/* ============================================================
   Labels
   ============================================================ */
QLabel {
    color: @text_primary@;
}

*[class="section_title"] {
    font-size: 14pt;
    font-weight: bold;
    color: @text_highlight@;
    padding: 10px 0 5px 0;
    text-transform: uppercase;
}

*[class="field_label"] {
    font-size: 9pt;
    color: @text_muted@;
    font-weight: bold;
    margin-bottom: 4px;
}

*[class="description_label"] {
    font-size: 8pt;
    color: @text_muted@;
}

/* ============================================================
   Group Box
   ============================================================ */
QGroupBox {
    border: 1px solid @border_color@;
    border-radius: 4px;
    margin-top: 15px;
    padding-top: 15px;
    font-weight: bold;
    color: @text_muted@;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: @accent_color@;
}

/* ============================================================
   Message Box / Dialog
   ============================================================ */
QMessageBox {
    background-color: @bg_secondary@;
}

QDialog {
    background-color: @bg_primary@;
}

/* ============================================================
   Progress Bar
   ============================================================ */
QProgressBar {
    border: 1px solid @border_color@;
    border-radius: 2px;
    background-color: @bg_tertiary@;
    height: 12px;
    text-align: center;
    color: @text_highlight@;
}

QProgressBar::chunk {
    background-color: @accent_color@;
}

/* ============================================================
   Tool Tips
   ============================================================ */
QToolTip {
    background-color: @bg_secondary@;
    color: @text_primary@;
    border: 1px solid @border_color@;
    padding: 6px;
}

/* ============================================================
   LOGIN STYLES
   ============================================================ */
#login_container {
    background-color: @bg_primary@;
}

#login_card {
    background-color: @bg_secondary@;
    border: 1px solid @border_color@;
    border-radius: 4px;
    padding: 40px;
    min-width: 380px;
}

#login_title {
    font-size: 20pt;
    font-weight: bold;
    color: @text_highlight@;
    text-transform: uppercase;
    letter-spacing: 1px;
}

#login_subtitle {
    font-size: 10pt;
    color: @text_muted@;
    margin-bottom: 25px;
}

#login_icon {
    font-size: 32pt;
    color: @accent_color@;
}

#login_input {
    padding: 12px 16px;
    border: 1px solid @border_color@;
    border-radius: 4px;
    background-color: @input_bg@;
    color: @text_highlight@;
    font-size: 10pt;
}

#login_input:focus {
    border-color: @accent_color@;
    background-color: @bg_tertiary@;
}

#login_btn {
    padding: 12px;
    border-radius: 4px;
    font-size: 11pt;
    font-weight: bold;
    background-color: @accent_color@;
    border: none;
    color: white;
}

#login_btn:hover {
    background-color: @accent_hover@;
}

#login_error {
    color: @danger_color@;
    font-size: 9pt;
}

#login_footer {
    color: @text_muted@;
    font-size: 8pt;
}
"""

# Apply variables to stylesheet strings
GLOBAL_STYLESHEET = _GLOBAL_STYLESHEET_TEMPLATE

for k, v in THEME.items():
    GLOBAL_STYLESHEET = GLOBAL_STYLESHEET.replace(f"@{k}@", str(v))

# Export colors directly for views that might need them
RESULT_COLORS = {
    "high": THEME["success_color"],
    "medium": THEME["warning_color"],
    "low": THEME["danger_color"],
    "heavy": THEME["danger_color"],
    "light": THEME["success_color"]
}
