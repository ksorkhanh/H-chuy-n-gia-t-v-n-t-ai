"""
Tax Module - Demonstration of system extensibility.
"""
import os
import json
from modules.base_module import BaseModule


class TaxModule(BaseModule):
    """Module for land tax assessment."""

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except Exception:
            self._config = {}

    def get_name(self):
        return self._config.get("module", "tax")

    def get_display_name(self):
        return self._config.get("display_name", "Thuế đất đai")

    def get_description(self):
        return self._config.get("description", "Tư vấn thuế")

    def get_icon(self):
        return self._config.get("icon", "💲")

    def get_config(self):
        return self._config

    def get_input_fields(self):
        return self._config.get("input_fields", [])

    def interpret_result(self, score, conclusion):
        """Interpret the fuzzy score into human-readable advice."""
        if score < 40:
            return {
                "level": "low",
                "title": "✅ THUẾ SUẤT ƯU ĐÃI",
                "color": "#27ae60",
                "description": f"Mức thuế/phí dự kiến ở mức thấp ({score:.1f}/100).",
                "recommendations": [
                    "Áp dụng cho đất nông nghiệp hoặc đất ở hạn mức.",
                    "Kiểm tra các diện đối tượng được miễn giảm thuế.",
                    "Chuẩn bị hồ sơ chứng minh mục đích sử dụng ưu đãi."
                ]
            }
        elif score < 70:
            return {
                "level": "medium",
                "title": "⚠️ THUẾ SUẤT PHỔ THÔNG",
                "color": "#f39c12",
                "description": f"Mức thuế/phí dự kiến ở mức trung bình ({score:.1f}/100).",
                "recommendations": [
                    "Áp dụng theo khung giá đất nhà nước hiện hành.",
                    "Lưu ý các khoản lệ phí trước bạ và phí cấp giấy chứng nhận.",
                    "Cân đối tài chính trước khi thực hiện giao dịch."
                ]
            }
        else:
            return {
                "level": "heavy",
                "title": "🔴 THUẾ SUẤT CAO",
                "color": "#e74c3c",
                "description": f"Mức thuế/phí dự kiến ở mức cao ({score:.1f}/100).",
                "recommendations": [
                    "Thường áp dụng cho đất thương mại dịch vụ hoặc vượt hạn mức.",
                    "Cần tư vấn chi tiết từ cơ quan thuế địa phương.",
                    "Xem xét các yếu tố vị trí sinh lợi cao ảnh hưởng đến giá thuế."
                ]
            }
