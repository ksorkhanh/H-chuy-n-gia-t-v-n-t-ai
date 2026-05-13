"""
Consultation View - Dynamic form and result display for consultation.
Builds UI dynamically from module config.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QFrame, QScrollArea, QSlider,
                              QComboBox, QGroupBox, QGridLayout, QTextEdit,
                              QSplitter, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
import json


class ConsultationView(QWidget):
    """Consultation view with module selection, input form, and result display."""

    def __init__(self, consultation_controller):
        super().__init__()
        self.controller = consultation_controller
        self.current_module = None
        self.input_widgets = {}
        self.value_labels = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(30, 10, 30, 20)

        # Header Row: Title + Module Selector
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        title = QLabel("🔍  Tư Vấn Pháp Lý")
        title.setObjectName("page_title")
        header_layout.addWidget(title)
        
        header_layout.addSpacing(40)
        
        header_layout.addWidget(QLabel("Lĩnh vực:"))
        self.module_combo = QComboBox()
        self.module_combo.setMinimumWidth(280)
        self.module_combo.setMinimumHeight(34)
        self._populate_modules()
        self.module_combo.currentIndexChanged.connect(self._on_module_changed)
        header_layout.addWidget(self.module_combo)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Splitter: left=form, right=result
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # === LEFT: Input Form ===
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 10, 0)

        form_title = QLabel("📝 Nhập Dữ Liệu")
        form_title.setProperty("class", "section_title")
        form_layout.addWidget(form_title)

        # Scrollable form area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self.form_widget = QWidget()
        self.form_layout_inner = QVBoxLayout(self.form_widget)
        self.form_layout_inner.setSpacing(8)
        scroll.setWidget(self.form_widget)
        form_layout.addWidget(scroll)

        # Run button
        self.run_btn = QPushButton("🚀  Chạy Phân Tích")
        self.run_btn.setProperty("class", "btn_primary")
        self.run_btn.setMinimumHeight(48)
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self._on_run)
        form_layout.addWidget(self.run_btn)

        splitter.addWidget(form_container)

        # === RIGHT: Result Display ===
        result_container = QWidget()
        result_layout = QVBoxLayout(result_container)
        result_layout.setContentsMargins(10, 0, 0, 0)

        result_title = QLabel("📊 Kết Quả Tư Vấn")
        result_title.setProperty("class", "section_title")
        result_layout.addWidget(result_title)

        self.result_scroll = QScrollArea()
        self.result_scroll.setWidgetResizable(True)
        self.result_scroll.setStyleSheet("QScrollArea { border: none; }")

        self.result_widget = QWidget()
        self.result_inner = QVBoxLayout(self.result_widget)

        # Placeholder
        self.placeholder = QLabel(
            "⬅️ Chọn module, nhập dữ liệu và nhấn 'Chạy Phân Tích'\nđể xem kết quả tư vấn."
        )
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color: #666; font-size: 11pt; padding: 40px;")
        self.result_inner.addWidget(self.placeholder)
        self.result_inner.addStretch()

        self.result_scroll.setWidget(self.result_widget)
        result_layout.addWidget(self.result_scroll)

        splitter.addWidget(result_container)
        splitter.setSizes([450, 550])

        layout.addWidget(splitter)

        # Load first module
        if self.module_combo.count() > 0:
            self._on_module_changed(0)

    def _populate_modules(self):
        """Populate module combo box."""
        modules = self.controller.get_available_modules()
        for mod in modules:
            self.module_combo.addItem(
                f"{mod['icon']}  {mod['display_name']}", mod['name']
            )

    def _on_module_changed(self, index):
        """Handle module selection change."""
        if index < 0:
            return
        module_name = self.module_combo.currentData()
        self.current_module = module_name
        self._build_form(module_name)

    def _build_form(self, module_name):
        """Build dynamic input form using dropdowns from module config."""
        # Clear existing form
        self.input_widgets = {}
        self.value_labels = {}
        while self.form_layout_inner.count():
            item = self.form_layout_inner.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get full config for membership functions
        config = self.controller.get_module_config(module_name)
        input_vars = {v["name"]: v for v in config.get("input_variables", [])}
        fields = self.controller.get_input_fields(module_name)

        for field in fields:
            group = QFrame()
            group.setStyleSheet("""
                QFrame { background-color: #22252d; border: 1px solid #2a2d35;
                         border-radius: 8px; padding: 10px; }
            """)
            group_layout = QVBoxLayout(group)
            group_layout.setSpacing(6)

            # Field label and value
            header = QHBoxLayout()
            label = QLabel(f"📌 {field['label']}")
            label.setStyleSheet("font-weight: bold; font-size: 10pt; color: #fff;")
            header.addWidget(label)

            value_label = QLabel("0.0")
            value_label.setStyleSheet(
                "font-size: 14pt; font-weight: bold; color: #667eea; min-width: 50px;"
            )
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            header.addWidget(value_label)
            group_layout.addLayout(header)

            # Description
            desc = QLabel(field.get("description", ""))
            desc.setStyleSheet("color: #666; font-size: 8pt; font-style: italic;")
            desc.setWordWrap(True)
            group_layout.addWidget(desc)

            # Dropdown (ComboBox)
            combo = QComboBox()
            combo.setMinimumHeight(42)
            combo.setCursor(Qt.CursorShape.PointingHandCursor)
            combo.setStyleSheet("""
                QComboBox {
                    background-color: #1a1d23;
                    border: 1px solid #3a3d45;
                    border-radius: 5px;
                    padding: 5px 15px;
                    color: #eee;
                    font-size: 10pt;
                }
                QComboBox::drop-down { border: none; }
                QComboBox QAbstractItemView {
                    background-color: #1a1d23;
                    color: #eee;
                    selection-background-color: #667eea;
                    border: 1px solid #3a3d45;
                }
            """)

            # Find membership functions for this variable
            var_cfg = input_vars.get(field["name"], {})
            mfs = var_cfg.get("membership_functions", [])

            if not mfs:
                # Fallback if no MFs (unlikely)
                combo.addItem("Mặc định", 5.0)
            else:
                for mf in mfs:
                    # Calculate peak/midpoint as representative value
                    params = mf["params"]
                    if mf["type"] == "triangular":
                        rep_val = params[1]
                    else:  # trapezoidal
                        rep_val = (params[1] + params[2]) / 2

                    label_text = mf.get("label", mf["name"])
                    combo.addItem(f"🔹 {label_text}", rep_val)

            # Set default selection based on field['default']
            default_val = field.get("default", 5.0)
            best_idx = 0
            min_diff = 999
            for i in range(combo.count()):
                diff = abs(combo.itemData(i) - default_val)
                if diff < min_diff:
                    min_diff = diff
                    best_idx = i
            combo.setCurrentIndex(best_idx)

            # Update value label initially and on change
            value_label.setText(f"{combo.itemData(best_idx):.1f}")
            combo.currentIndexChanged.connect(
                lambda idx, c=combo, lbl=value_label: lbl.setText(f"{c.itemData(idx):.1f}")
            )

            group_layout.addWidget(combo)
            self.input_widgets[field["name"]] = combo
            self.value_labels[field["name"]] = value_label

            self.form_layout_inner.addWidget(group)

        self.form_layout_inner.addStretch()

    def _on_run(self):
        """Run consultation with current inputs."""
        if not self.current_module:
            return

        # Collect input values
        inputs = {}
        for name, widget in self.input_widgets.items():
            if isinstance(widget, QComboBox):
                inputs[name] = widget.currentData()
            elif hasattr(widget, "value"):
                inputs[name] = widget.value() / getattr(widget, "multiplier", 1)

        # Run consultation
        self.run_btn.setEnabled(False)
        self.run_btn.setText("⏳  Đang phân tích...")

        result = self.controller.run_consultation(self.current_module, inputs)

        self.run_btn.setEnabled(True)
        self.run_btn.setText("🚀  Chạy Phân Tích")

        if "error" in result:
            self._show_error(result["error"])
        else:
            self._display_result(result)

    def _display_result(self, result):
        """Display consultation result."""
        self.last_result = result # Store for export
        # Clear previous results
        while self.result_inner.count():
            item = self.result_inner.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        interp = result.get("interpretation", {})
        color = interp.get("color", "#667eea")

        # Score card
        score_card = QFrame()
        score_card.setStyleSheet(f"""
            QFrame {{ background-color: #22252d; border: 2px solid {color};
                     border-radius: 8px; padding: 12px; }}
        """)
        score_layout = QVBoxLayout(score_card)

        # Title
        title_label = QLabel(interp.get("title", "Kết quả"))
        title_label.setStyleSheet(f"font-size: 16pt; font-weight: bold; color: {color};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addWidget(title_label)

        # Score
        score_val = QLabel(f"{result['score']:.1f}")
        score_val.setStyleSheet(f"font-size: 36pt; font-weight: bold; color: {color};")
        score_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addWidget(score_val)

        score_unit = QLabel("/ 100 điểm")
        score_unit.setStyleSheet("font-size: 10pt; color: #888;")
        score_unit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addWidget(score_unit)

        self.result_inner.addWidget(score_card)

        # Description
        desc_card = QFrame()
        desc_card.setStyleSheet("""
            QFrame { background-color: #22252d; border: 1px solid #2a2d35;
                     border-radius: 8px; padding: 12px; }
        """)
        desc_layout = QVBoxLayout(desc_card)
        desc_title = QLabel("📋 Nhận Xét")
        desc_title.setStyleSheet("font-size: 12pt; font-weight: bold; color: #fff;")
        desc_layout.addWidget(desc_title)

        desc_text = QLabel(interp.get("description", ""))
        desc_text.setWordWrap(True)
        desc_text.setStyleSheet("color: #ccc; line-height: 1.6; padding: 5px 0;")
        desc_layout.addWidget(desc_text)
        self.result_inner.addWidget(desc_card)

        # Recommendations
        recs = interp.get("recommendations", [])
        if recs:
            rec_card = QFrame()
            rec_card.setStyleSheet("""
                QFrame { background-color: #22252d; border: 1px solid #2a2d35;
                         border-radius: 8px; padding: 12px; }
            """)
            rec_layout = QVBoxLayout(rec_card)
            rec_title = QLabel("💡 Khuyến Nghị")
            rec_title.setStyleSheet("font-size: 12pt; font-weight: bold; color: #fff;")
            rec_layout.addWidget(rec_title)

            for i, rec in enumerate(recs, 1):
                rec_label = QLabel(f"  {i}. {rec}")
                rec_label.setWordWrap(True)
                rec_label.setStyleSheet("color: #ccc; padding: 3px 0;")
                rec_layout.addWidget(rec_label)
            self.result_inner.addWidget(rec_card)

        # Legal Citations
        citations = result.get("legal_citations", [])
        if citations:
            law_card = QFrame()
            law_card.setStyleSheet("""
                QFrame { background-color: #22252d; border: 1px solid #2a2d35;
                         border-radius: 8px; padding: 12px; }
            """)
            law_layout = QVBoxLayout(law_card)
            law_title = QLabel("📜 Căn Cứ Pháp Lý")
            law_title.setStyleSheet("font-size: 12pt; font-weight: bold; color: #fff;")
            law_layout.addWidget(law_title)

            for cite in citations:
                cite_frame = QFrame()
                cite_frame.setStyleSheet("""
                    QFrame { background-color: #1a1d23; border-left: 3px solid #667eea;
                             border-radius: 4px; padding: 10px; margin: 5px 0; }
                """)
                cite_layout = QVBoxLayout(cite_frame)

                cite_header = QLabel(f"📌 {cite['formatted']}")
                cite_header.setStyleSheet("font-weight: bold; color: #667eea;")
                cite_layout.addWidget(cite_header)

                cite_content = QLabel(cite['content'])
                cite_content.setWordWrap(True)
                cite_content.setStyleSheet("color: #aaa; font-size: 9pt;")
                cite_layout.addWidget(cite_content)

                law_layout.addWidget(cite_frame)
            self.result_inner.addWidget(law_card)

        # Matched Rules
        matched = result.get("matched_rules", [])
        if matched:
            rules_card = QFrame()
            rules_card.setStyleSheet("""
                QFrame { background-color: #22252d; border: 1px solid #2a2d35;
                         border-radius: 8px; padding: 12px; }
            """)
            rules_layout = QVBoxLayout(rules_card)
            rules_title = QLabel(f"⚙️ Luật Kích Hoạt ({len(matched)})")
            rules_title.setStyleSheet("font-size: 12pt; font-weight: bold; color: #fff;")
            rules_layout.addWidget(rules_title)

            for rule in matched[:10]:
                rdesc = rule.get('description') or f"Rule #{rule['rule_id']}"
                rule_label = QLabel(
                    f"  • {rdesc}  "
                    f"[Độ kích hoạt: {rule['firing_strength']:.3f}]"
                )
                rule_label.setWordWrap(True)
                rule_label.setStyleSheet("color: #aaa; font-size: 9pt; padding: 2px 0;")
                rules_layout.addWidget(rule_label)
            self.result_inner.addWidget(rules_card)

        self.result_inner.addStretch()

        # Add Export Button
        export_btn = QPushButton("📄 Xuất Báo Cáo (Text)")
        export_btn.setMinimumHeight(40)
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.clicked.connect(self._on_export_report)
        self.result_inner.addWidget(export_btn)

    def _on_export_report(self):
        """Export current result to a text file."""
        if not hasattr(self, 'last_result'):
            return
            
        from PyQt6.QtWidgets import QFileDialog
        import datetime
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Lưu báo cáo", f"BaoCao_{self.current_module}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "Text Files (*.txt)"
        )
        
        if filename:
            try:
                res = self.last_result
                interp = res.get("interpretation", {})
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("="*60 + "\n")
                    f.write("            BÁO CÁO TƯ VẤN PHÁP LÝ ĐẤT ĐAI\n")
                    f.write("="*60 + "\n\n")
                    f.write(f"Module: {self.current_module.upper()}\n")
                    f.write(f"Thời gian: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    f.write("-" * 20 + " KẾT QUẢ " + "-" * 20 + "\n")
                    f.write(f"ĐIỂM ĐÁNH GIÁ: {res['score']:.1f} / 100\n")
                    f.write(f"KẾT LUẬN: {interp.get('title', 'N/A')}\n\n")
                    f.write(f"NHẬN XÉT: {interp.get('description', '')}\n\n")
                    
                    if interp.get("recommendations"):
                        f.write("-" * 20 + " KHUYẾN NGHỊ " + "-" * 20 + "\n")
                        for i, rec in enumerate(interp["recommendations"], 1):
                            f.write(f"{i}. {rec}\n")
                        f.write("\n")
                        
                    if res.get("legal_citations"):
                        f.write("-" * 20 + " CĂN CỨ PHÁP LÝ " + "-" * 20 + "\n")
                        for cite in res["legal_citations"]:
                            f.write(f"📌 {cite['formatted']}\n")
                            f.write(f"   Nội dung: {cite['content'][:200]}...\n\n")
                            
                    f.write("\n" + "="*60 + "\n")
                    f.write("Hệ thống chuyên gia tư vấn pháp lý thông minh - Version 1.0\n")
                
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Thành công", f"Báo cáo đã được lưu tại:\n{filename}")
            except Exception as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Lỗi", f"Không thể lưu báo cáo: {str(e)}")

    def _show_error(self, message):
        """Display error message."""
        while self.result_inner.count():
            item = self.result_inner.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        error_label = QLabel(f"❌ {message}")
        error_label.setStyleSheet("color: #e74c3c; font-size: 12pt; padding: 20px;")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_inner.addWidget(error_label)
        self.result_inner.addStretch()

    def set_module(self, module_name):
        """Set the active module from external navigation."""
        for i in range(self.module_combo.count()):
            if self.module_combo.itemData(i) == module_name:
                self.module_combo.setCurrentIndex(i)
                break
