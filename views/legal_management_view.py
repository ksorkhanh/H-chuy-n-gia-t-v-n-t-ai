"""
Giao diện Quản lý Pháp lý - CRUD cho văn bản và điều khoản pháp lý.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QHeaderView, QLineEdit, QDialog, QFormLayout,
                              QTextEdit, QComboBox, QSpinBox, QMessageBox,
                              QFrame, QSplitter, QAbstractItemView)
from PyQt6.QtCore import Qt


class LegalManagementView(QWidget):
    """Giao diện quản lý văn bản và điều khoản pháp lý."""

    def __init__(self, legal_controller):
        super().__init__()
        self.controller = legal_controller
        self._setup_ui()
        self._load_documents()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("Quản Lý Văn Bản Pháp Lý")
        title.setObjectName("page_title")
        layout.addWidget(title)

        # Toolbar
        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm văn bản...")
        self.search_input.setMinimumHeight(38)
        self.search_input.textChanged.connect(self._on_search)
        toolbar.addWidget(self.search_input)

        btn_add = QPushButton("➕ Thêm Văn Bản")
        btn_add.setProperty("class", "btn_primary")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._add_document)
        toolbar.addWidget(btn_add)

        btn_refresh = QPushButton("Làm Mới")
        btn_refresh.clicked.connect(self._load_documents)
        toolbar.addWidget(btn_refresh)
        layout.addLayout(toolbar)

        # Splitter: documents table | articles table
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Documents table
        doc_frame = QFrame()
        doc_layout = QVBoxLayout(doc_frame)
        doc_layout.setContentsMargins(0, 0, 0, 0)
        doc_label = QLabel("📄 Văn Bản Pháp Luật")
        doc_label.setProperty("class", "section_title")
        doc_layout.addWidget(doc_label)

        self.doc_table = QTableWidget()
        self.doc_table.setColumnCount(6)
        self.doc_table.setHorizontalHeaderLabels(
            ["ID", "Tên văn bản", "Mã", "Năm", "Lĩnh vực", "Trạng thái"])
        self.doc_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.doc_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.doc_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.doc_table.currentCellChanged.connect(self._on_doc_selected)
        doc_layout.addWidget(self.doc_table)

        # Document actions
        doc_actions = QHBoxLayout()
        btn_edit_doc = QPushButton("✏️ Sửa")
        btn_edit_doc.clicked.connect(self._edit_document)
        btn_del_doc = QPushButton("️ Xóa")
        btn_del_doc.setProperty("class", "btn_danger")
        btn_del_doc.clicked.connect(self._delete_document)
        doc_actions.addStretch()
        doc_actions.addWidget(btn_edit_doc)
        doc_actions.addWidget(btn_del_doc)
        doc_layout.addLayout(doc_actions)

        splitter.addWidget(doc_frame)

        # Articles table
        art_frame = QFrame()
        art_layout = QVBoxLayout(art_frame)
        art_layout.setContentsMargins(0, 0, 0, 0)
        art_label = QLabel("Điều Khoản")
        art_label.setProperty("class", "section_title")
        art_layout.addWidget(art_label)

        self.art_table = QTableWidget()
        self.art_table.setColumnCount(5)
        self.art_table.setHorizontalHeaderLabels(
            ["ID", "Điều", "Khoản", "Nội dung", "Từ khóa"])
        self.art_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.art_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.art_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        art_layout.addWidget(self.art_table)

        art_actions = QHBoxLayout()
        btn_add_art = QPushButton("➕ Thêm Điều")
        btn_add_art.setProperty("class", "btn_primary")
        btn_add_art.clicked.connect(self._add_article)
        btn_edit_art = QPushButton("✏️ Sửa")
        btn_edit_art.clicked.connect(self._edit_article)
        btn_del_art = QPushButton("️ Xóa")
        btn_del_art.setProperty("class", "btn_danger")
        btn_del_art.clicked.connect(self._delete_article)
        art_actions.addStretch()
        art_actions.addWidget(btn_add_art)
        art_actions.addWidget(btn_edit_art)
        art_actions.addWidget(btn_del_art)
        art_layout.addLayout(art_actions)

        splitter.addWidget(art_frame)
        layout.addWidget(splitter)

    def _load_documents(self):
        """Load all documents into table."""
        docs = self.controller.get_all_documents()
        self.doc_table.setRowCount(len(docs))
        for i, doc in enumerate(docs):
            self.doc_table.setItem(i, 0, QTableWidgetItem(str(doc["id"])))
            self.doc_table.setItem(i, 1, QTableWidgetItem(doc["title"]))
            self.doc_table.setItem(i, 2, QTableWidgetItem(doc["code"]))
            self.doc_table.setItem(i, 3, QTableWidgetItem(str(doc["year"])))
            self.doc_table.setItem(i, 4, QTableWidgetItem(doc["domain"]))
            status = "Hoạt động" if doc["is_active"] else "Tắt"
            self.doc_table.setItem(i, 5, QTableWidgetItem(status))

    def _on_doc_selected(self, row, col, prev_row, prev_col):
        """Load articles for selected document."""
        if row < 0:
            return
        doc_id_item = self.doc_table.item(row, 0)
        if doc_id_item:
            doc_id = int(doc_id_item.text())
            articles = self.controller.get_articles_by_document(doc_id)
            self.art_table.setRowCount(len(articles))
            for i, art in enumerate(articles):
                self.art_table.setItem(i, 0, QTableWidgetItem(str(art["id"])))
                self.art_table.setItem(i, 1, QTableWidgetItem(art["article_number"]))
                self.art_table.setItem(i, 2, QTableWidgetItem(art.get("clause") or ""))
                self.art_table.setItem(i, 3, QTableWidgetItem(art["content"][:100]))
                self.art_table.setItem(i, 4, QTableWidgetItem(art.get("keywords") or ""))

    def _on_search(self, text):
        if text:
            docs = self.controller.search_documents(text)
        else:
            docs = self.controller.get_all_documents()
        self.doc_table.setRowCount(len(docs))
        for i, doc in enumerate(docs):
            self.doc_table.setItem(i, 0, QTableWidgetItem(str(doc["id"])))
            self.doc_table.setItem(i, 1, QTableWidgetItem(doc["title"]))
            self.doc_table.setItem(i, 2, QTableWidgetItem(doc["code"]))
            self.doc_table.setItem(i, 3, QTableWidgetItem(str(doc["year"])))
            self.doc_table.setItem(i, 4, QTableWidgetItem(doc["domain"]))
            status = "" if doc["is_active"] else ""
            self.doc_table.setItem(i, 5, QTableWidgetItem(status))

    def _add_document(self):
        dialog = DocumentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                self.controller.create_document(**data)
                self._load_documents()
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    def _edit_document(self):
        row = self.doc_table.currentRow()
        if row < 0:
            return
        doc_id = int(self.doc_table.item(row, 0).text())
        doc = self.controller.get_document(doc_id)
        if doc:
            dialog = DocumentDialog(self, doc)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                try:
                    self.controller.update_document(doc_id, **data)
                    self._load_documents()
                except Exception as e:
                    QMessageBox.warning(self, "Lỗi", str(e))

    def _delete_document(self):
        row = self.doc_table.currentRow()
        if row < 0:
            return
        doc_id = int(self.doc_table.item(row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận",
            "Xóa văn bản này sẽ xóa tất cả điều khoản liên quan. Tiếp tục?")
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.delete_document(doc_id)
                self._load_documents()
                self.art_table.setRowCount(0)
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    def _add_article(self):
        row = self.doc_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Thông báo", "Chọn văn bản trước")
            return
        doc_id = int(self.doc_table.item(row, 0).text())
        dialog = ArticleDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                self.controller.create_article(doc_id, **data)
                self._on_doc_selected(row, 0, -1, -1)
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    def _edit_article(self):
        row = self.art_table.currentRow()
        if row < 0:
            return
        art_id = int(self.art_table.item(row, 0).text())
        from models.legal import LegalArticle
        art = LegalArticle.find_by_id(art_id)
        if art:
            dialog = ArticleDialog(self, art.to_dict())
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                try:
                    self.controller.update_article(art_id, **data)
                    doc_row = self.doc_table.currentRow()
                    self._on_doc_selected(doc_row, 0, -1, -1)
                except Exception as e:
                    QMessageBox.warning(self, "Lỗi", str(e))

    def _delete_article(self):
        row = self.art_table.currentRow()
        if row < 0:
            return
        art_id = int(self.art_table.item(row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Xóa điều khoản này?")
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.delete_article(art_id)
                doc_row = self.doc_table.currentRow()
                self._on_doc_selected(doc_row, 0, -1, -1)
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", str(e))


class DocumentDialog(QDialog):
    """Dialog for adding/editing legal documents."""
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm/Sửa Văn Bản Pháp Lý")
        self.setMinimumWidth(500)
        self.setStyleSheet("QDialog { background-color: #1a1d23; }")
        layout = QFormLayout(self)
        layout.setSpacing(12)

        self.title_input = QLineEdit(data.get("title", "") if data else "")
        self.code_input = QLineEdit(data.get("code", "") if data else "")
        self.year_input = QSpinBox()
        self.year_input.setRange(1945, 2030)
        self.year_input.setValue(data.get("year", 2024) if data else 2024)
        self.domain_input = QComboBox()
        for label, val in [("Đất đai", "dat_dai"), ("Dân sự", "dan_su"), 
                          ("Hình sự", "hinh_su"), ("Lao động", "lao_dong"), ("Thuế", "thue")]:
            self.domain_input.addItem(label, val)
            
        if data and data.get("domain"):
            idx = self.domain_input.findData(data["domain"])
            if idx >= 0: self.domain_input.setCurrentIndex(idx)
        self.desc_input = QTextEdit(data.get("description", "") if data else "")
        self.desc_input.setMaximumHeight(100)

        layout.addRow("Tên văn bản:", self.title_input)
        layout.addRow("Mã:", self.code_input)
        layout.addRow("Năm:", self.year_input)
        layout.addRow("Lĩnh vực:", self.domain_input)
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
        return {
            "title": self.title_input.text(),
            "code": self.code_input.text(),
            "year": self.year_input.value(),
            "domain": self.domain_input.currentData(),
            "description": self.desc_input.toPlainText()
        }


class ArticleDialog(QDialog):
    """Dialog for adding/editing legal articles."""
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm/Sửa Điều Khoản")
        self.setMinimumWidth(500)
        self.setStyleSheet("QDialog { background-color: #1a1d23; }")
        layout = QFormLayout(self)
        layout.setSpacing(12)

        self.article_input = QLineEdit(data.get("article_number", "") if data else "")
        self.clause_input = QLineEdit(data.get("clause", "") if data else "")
        self.content_input = QTextEdit(data.get("content", "") if data else "")
        self.content_input.setMinimumHeight(150)
        self.keywords_input = QLineEdit(data.get("keywords", "") if data else "")

        layout.addRow("Số điều:", self.article_input)
        layout.addRow("Khoản:", self.clause_input)
        layout.addRow("Nội dung:", self.content_input)
        layout.addRow("Từ khóa:", self.keywords_input)

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
        return {
            "article_number": self.article_input.text(),
            "clause": self.clause_input.text() or None,
            "content": self.content_input.toPlainText(),
            "keywords": self.keywords_input.text() or None
        }
