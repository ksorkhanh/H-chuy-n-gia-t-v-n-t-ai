"""
Bộ điều khiển Tư vấn - Điều phối quy trình tư vấn.
Phối hợp giữa các module, động cơ mờ, động cơ pháp lý và lưu trữ bản ghi.
"""
import logging
from engines.fuzzy_engine import FuzzyEngine
from engines.legal_engine import LegalEngine
from models.rule import Rule
from models.case import Case
from modules.module_loader import ModuleLoader
from core.auth import AuthService

logger = logging.getLogger(__name__)


class ConsultationController:
    """Bộ điều khiển cho luồng tư vấn."""

    def __init__(self):
        self.module_loader = ModuleLoader()
        self.legal_engine = LegalEngine()
        self.auth_service = AuthService()

    def get_available_modules(self):
        """Lấy danh sách các module tư vấn khả dụng."""
        return self.module_loader.get_module_list()

    def get_module(self, module_name):
        """Lấy một module cụ thể."""
        return self.module_loader.get_module(module_name)

    def get_input_fields(self, module_name):
        """Lấy định nghĩa các trường nhập liệu cho một module."""
        module = self.module_loader.get_module(module_name)
        if module:
            return module.get_input_fields()
        return []

    def get_module_config(self, module_name):
        """Lấy toàn bộ cấu hình cho một module."""
        module = self.module_loader.get_module(module_name)
        if module:
            return module.get_config()
        return {}

    def run_consultation(self, module_name, inputs):
        """
        Chạy một phiên tư vấn đầy đủ.
        Tham số:
            module_name: Mã định danh module
            inputs: dict {tên_biến: giá_trị}
        Trả về:
            dict chứa score, conclusion, interpretation, legal_citations, explanation
        """
        module = self.module_loader.get_module(module_name)
        if not module:
            return {"error": f"Module không tìm thấy: {module_name}"}

        try:
            # 1. Khởi tạo động cơ mờ với cấu hình module
            fuzzy = FuzzyEngine()
            config = module.get_config()
            fuzzy.load_config(config)

            # 2. Nạp quy tắc từ cơ sở dữ liệu
            db_rules = Rule.get_by_module(module_name, active_only=True)
            if db_rules:
                fuzzy.load_rules_from_db(db_rules)
            # Nếu không có quy tắc từ DB, engine dùng quy tắc từ config (nếu có)

            # 3. Chạy suy diễn mờ
            result = fuzzy.run(inputs)

            # 4. Diễn giải kết quả bằng logic chuyên biệt của module
            interpretation = module.interpret_result(
                result["score"], result["conclusion"]
            )

            # 5. Lấy trích dẫn pháp lý cho các quy tắc khớp
            legal_citations = self.legal_engine.get_articles_for_rules(
                result["matched_rules"]
            )

            # 6. Xây dựng kết quả đầy đủ
            full_result = {
                "module_name": module.get_display_name(),
                "score": result["score"],
                "conclusion": result["conclusion"],
                "interpretation": interpretation,
                "explanation": result["explanation"],
                "matched_rules": result["matched_rules"],
                "legal_citations": legal_citations,
                "fuzzified_inputs": result.get("fuzzified_inputs", {}),
                "inputs": inputs
            }

            # 7. Lưu bản ghi vào lịch sử
            user = self.auth_service.get_current_user()
            if user:
                rule_ids = [r["rule_id"] for r in result["matched_rules"]]
                Case.save(
                    user_id=user["id"],
                    module=module_name,
                    input_data=inputs,
                    result_data={
                        "score": result["score"],
                        "conclusion": result["conclusion"],
                        "interpretation_title": interpretation["title"]
                    },
                    matched_rules=rule_ids,
                    score=result["score"],
                    conclusion=interpretation["title"]
                )

            return full_result

        except Exception as e:
            logger.error(f"Consultation error: {e}")
            return {"error": f"Lỗi trong quá trình tư vấn: {str(e)}"}
