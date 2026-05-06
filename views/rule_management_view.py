"""
Rule Management View - CRUD for fuzzy inference rules with import/export.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QHeaderView, QLineEdit, QDialog, QFormLayout,
                              QTextEdit, QComboBox, QDoubleSpinBox, QMessageBox,
                              QFileDialog, QCheckBox, QAbstractItemView)
from PyQt6.QtCore import Qt
import json


class RuleManagementView(QWidget):
    """View for managing fuzzy inference rules."""

    def __init__(self, rule_controller, legal_controller):
        super().__init__()
        self.rule_ctrl = rule_controller
        self.legal_ctrl = legal_controller
        self._setup_ui()
        self._load_rules()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("⚙️  Quản Lý Luật Suy Diễn (Rules)")
        title.setObjectName("page_title")
        layout.addWidget(title)

        # Toolbar
        toolbar = QHBoxLayout()

        self.module_filter = QComboBox()
        self.module_filter.setMinimumWidth(200)
        self.module_filter.setMinimumHeight(38)
        self.module_filter.addItem("📋 Tất cả module", "")
        self.module_filter.addItem("🔄 Chuyển nhượng", "transfer")
        self.module_filter.addItem("💰 Bồi thường", "compensation")
        self.module_filter.addItem("⚖️ Vi phạm", "violation")
        self.module_filter.currentIndexChanged.connect(self._load_rules)
        toolbar.addWidget(self.module_filter)

        toolbar.addStretch()

        btn_add = QPushButton("➕ Thêm Rule")
        btn_add.setProperty("class", "btn_primary")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._add_rule)
        toolbar.addWidget(btn_add)

        btn_import = QPushButton("📥 Import JSON")
        btn_import.clicked.connect(self._import_rules)
        toolbar.addWidget(btn_import)

        btn_export = QPushButton("📤 Export JSON")
        btn_export.clicked.connect(self._export_rules)
        toolbar.addWidget(btn_export)

        btn_refresh = QPushButton("🔄")
        btn_refresh.clicked.connect(self._load_rules)
        toolbar.addWidget(btn_refresh)

        layout.addLayout(toolbar)

        # Rules table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Module", "Tên", "Điều kiện", "Kết luận",
            "Trọng số", "Điều luật", "Trạng thái"
        ])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Actions
        actions = QHBoxLayout()
        btn_edit = QPushButton("✏️ Sửa")
        btn_edit.clicked.connect(self._edit_rule)
        btn_toggle = QPushButton("🔀 Bật/Tắt")
        btn_toggle.setProperty("class", "btn_warning")
        btn_toggle.clicked.connect(self._toggle_rule)
        btn_delete = QPushButton("🗑️ Xóa")
        btn_delete.setProperty("class", "btn_danger")
        btn_delete.clicked.connect(self._delete_rule)

        actions.addStretch()
        actions.addWidget(btn_edit)
        actions.addWidget(btn_toggle)
        actions.addWidget(btn_delete)
        layout.addLayout(actions)

    def _load_rules(self):
        """Load rules into table."""
        module = self.module_filter.currentData()
        rules = self.rule_ctrl.get_all_rules(module if module else None)
        self.table.setRowCount(len(rules))

        for i, rule in enumerate(rules):
            self.table.setItem(i, 0, QTableWidgetItem(str(rule["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(rule["module"]))
            self.table.setItem(i, 2, QTableWidgetItem(rule["name"]))

            # Format conditions
            conds = rule.get("conditions", [])
            cond_str = ", ".join([f"{c['variable']}={c['term']}" for c in conds])
            self.table.setItem(i, 3, QTableWidgetItem(cond_str))

            self.table.setItem(i, 4, QTableWidgetItem(rule["conclusion"]))
            self.table.setItem(i, 5, QTableWidgetItem(f"{rule['weight']:.2f}"))
            self.table.setItem(i, 6, QTableWidgetItem(
                str(rule.get("legal_article_id") or "—")))

            status = "✅ Bật" if rule["is_active"] else "❌ Tắt"
            item = QTableWidgetItem(status)
            if not rule["is_active"]:
                item.setForeground(Qt.GlobalColor.gray)
            self.table.setItem(i, 7, item)

    def _add_rule(self):
        dialog = RuleDialog(self, self.legal_ctrl)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                self.rule_ctrl.create_rule(**data)
                self._load_rules()
                QMessageBox.information(self, "Thành công", "Đã thêm rule mới")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    def _edit_rule(self):
        row = self.table.currentRow()
        if row < 0:
            return
        rule_id = int(self.table.item(row, 0).text())
        rule = self.rule_ctrl.get_rule(rule_id)
        if rule:
            dialog = RuleDialog(self, self.legal_ctrl, rule)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                try:
                    self.rule_ctrl.update_rule(rule_id,
                        name=data["name"],
                        condition_json=data["conditions"],
                        conclusion=data["conclusion"],
                        weight=data["weight"],
                        legal_article_id=data.get("legal_article_id"),
                        description=data.get("description"))
                    self._load_rules()
                except Exception as e:
                    QMessageBox.warning(self, "Lỗi", str(e))

    def _toggle_rule(self):
        row = self.table.currentRow()
        if row < 0:
            return
        rule_id = int(self.table.item(row, 0).text())
        try:
            self.rule_ctrl.toggle_rule(rule_id)
            self._load_rules()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def _delete_rule(self):
        row = self.table.currentRow()
        if row < 0:
            return
        rule_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Xóa rule này?")
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.rule_ctrl.delete_rule(rule_id)
                self._load_rules()
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    def _import_rules(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Import Rules", "", "JSON Files (*.json)")
        if filepath:
            try:
                success, errors = self.rule_ctrl.import_rules_from_file(filepath)
                self._load_rules()
                QMessageBox.information(self, "Import",
                    f"Thành công: {success}\nLỗi: {errors}")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    def _export_rules(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export Rules", "rules_export.json", "JSON Files (*.json)")
        if filepath:
            module = self.module_filter.currentData()
            data = self.rule_ctrl.export_rules(module if module else None)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "Export", "Xuất file thành công!")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))


class RuleDialog(QDialog):
    """Dialog for adding/editing rules."""

    def __init__(self, parent=None, legal_ctrl=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm/Sửa Rule")
        self.setMinimumWidth(550)
        self.setStyleSheet("QDialog { background-color: #1a1d23; }")
        layout = QFormLayout(self)
        layout.setSpacing(12)

        self.module_input = QComboBox()
        self.module_input.addItems(["transfer", "compensation", "violation"])
        if data:
            idx = self.module_input.findText(data.get("module", ""))
            if idx >= 0:
                self.module_input.setCurrentIndex(idx)

        self.name_input = QLineEdit(data.get("name", "") if data else "")

        self.conditions_input = QTextEdit()
        self.conditions_input.setMaximumHeight(120)
        if data and data.get("conditions"):
            conds = data["conditions"]
            if isinstance(conds, str):
                self.conditions_input.setPlainText(conds)
            else:
                self.conditions_input.setPlainText(json.dumps(conds, ensure_ascii=False, indent=2))

        self.conclusion_input = QLineEdit(data.get("conclusion", "") if data else "")

        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(0.0, 1.0)
        self.weight_input.setSingleStep(0.1)
        self.weight_input.setDecimals(2)
        self.weight_input.setValue(data.get("weight", 1.0) if data else 1.0)

        self.article_input = QComboBox()
        self.article_input.addItem("— Không gán —", None)
        if legal_ctrl:
            articles = legal_ctrl.get_all_articles()
            for art in articles:
                label = f"{art['article_number']} - {art['document_title'][:40]}"
                self.article_input.addItem(label, art["id"])
        if data and data.get("legal_article_id"):
            for i in range(self.article_input.count()):
                if self.article_input.itemData(i) == data["legal_article_id"]:
                    self.article_input.setCurrentIndex(i)
                    break

        self.desc_input = QLineEdit(data.get("description", "") if data else "")

        layout.addRow("Module:", self.module_input)
        layout.addRow("Tên rule:", self.name_input)
        layout.addRow("Điều kiện (JSON):", self.conditions_input)

        hint = QLabel('Ví dụ: [{"variable":"severity","term":"serious"}]')
        hint.setStyleSheet("color: #666; font-size: 8pt;")
        layout.addRow("", hint)

        layout.addRow("Kết luận:", self.conclusion_input)
        layout.addRow("Trọng số:", self.weight_input)
        layout.addRow("Điều luật:", self.article_input)
        layout.addRow("Mô tả:", self.desc_input)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("💾 Lưu")
        btn_save.setProperty("class", "btn_primary")
        btn_save.clicked.connect(self.accept)
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)

    def get_data(self):
        cond_text = self.conditions_input.toPlainText()
        try:
            conditions = json.loads(cond_text)
        except json.JSONDecodeError:
            conditions = []

        return {
            "module": self.module_input.currentText(),
            "name": self.name_input.text(),
            "conditions": conditions,
            "conclusion": self.conclusion_input.text(),
            "weight": self.weight_input.value(),
            "legal_article_id": self.article_input.currentData(),
            "description": self.desc_input.text()
        }
