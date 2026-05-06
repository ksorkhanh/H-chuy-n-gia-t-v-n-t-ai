"""
Violation Module - Vi phạm hành chính đất đai.
Evaluates penalty levels for land-related administrative violations.
"""
import os
import json
from modules.base_module import BaseModule


class ViolationModule(BaseModule):
    """Module tư vấn xử phạt vi phạm hành chính đất đai."""

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = json.load(f)

    def get_name(self):
        return "violation"

    def get_display_name(self):
        return self._config.get("display_name", "Vi phạm hành chính đất đai")

    def get_description(self):
        return self._config.get("description", "")

    def get_icon(self):
        return self._config.get("icon", "⚖️")

    def get_config(self):
        return self._config

    def get_input_fields(self):
        return self._config.get("input_fields", [])

    def interpret_result(self, score, conclusion):
        """Interpret violation penalty result."""
        if score >= 70:
            return {
                "level": "heavy",
                "title": "🔴 MỨC PHẠT NẶNG",
                "color": "#e74c3c",
                "description": (
                    f"Điểm đánh giá: {score:.1f}/100\n\n"
                    "Vi phạm ở mức nghiêm trọng, áp dụng mức phạt cao theo "
                    "Nghị định 91/2019/NĐ-CP. Ngoài phạt tiền, có thể áp dụng "
                    "biện pháp khắc phục hậu quả bắt buộc."
                ),
                "recommendations": [
                    "Phạt tiền ở mức cao theo khung quy định",
                    "Buộc khôi phục tình trạng đất ban đầu",
                    "Buộc nộp lại số lợi bất hợp pháp",
                    "Xem xét truy cứu trách nhiệm hình sự nếu đủ yếu tố",
                    "Tước quyền sử dụng giấy phép (nếu có)"
                ]
            }
        elif score >= 40:
            return {
                "level": "medium",
                "title": "🟡 MỨC PHẠT TRUNG BÌNH",
                "color": "#f39c12",
                "description": (
                    f"Điểm đánh giá: {score:.1f}/100\n\n"
                    "Vi phạm ở mức trung bình. Áp dụng phạt tiền theo khung "
                    "quy định tại Nghị định 91/2019/NĐ-CP, kèm biện pháp "
                    "khắc phục hậu quả."
                ),
                "recommendations": [
                    "Phạt tiền theo khung trung bình của hành vi vi phạm",
                    "Buộc thực hiện đúng quy định về sử dụng đất",
                    "Hoàn thiện thủ tục pháp lý còn thiếu",
                    "Tự nguyện khắc phục hậu quả để được giảm nhẹ"
                ]
            }
        else:
            return {
                "level": "light",
                "title": "🟢 MỨC PHẠT NHẸ / CẢNH CÁO",
                "color": "#27ae60",
                "description": (
                    f"Điểm đánh giá: {score:.1f}/100\n\n"
                    "Vi phạm ở mức nhẹ, có thể áp dụng hình thức cảnh cáo "
                    "hoặc phạt tiền ở mức thấp nhất. Khuyến khích tự nguyện "
                    "khắc phục vi phạm."
                ),
                "recommendations": [
                    "Cảnh cáo hoặc phạt tiền mức thấp nhất",
                    "Tự nguyện khắc phục vi phạm trong thời hạn",
                    "Hoàn thiện thủ tục sử dụng đất theo quy định",
                    "Lưu ý không tái phạm để tránh tình tiết tăng nặng"
                ]
            }
