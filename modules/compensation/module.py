"""
Compensation Module - Bồi thường khi Nhà nước thu hồi đất.
Evaluates compensation levels for state land acquisition.
"""
import os
import json
from modules.base_module import BaseModule


class CompensationModule(BaseModule):
    """Module tư vấn bồi thường khi Nhà nước thu hồi đất."""

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = json.load(f)

    def get_name(self):
        return "compensation"

    def get_display_name(self):
        return self._config.get("display_name", "Bồi thường thu hồi đất")

    def get_description(self):
        return self._config.get("description", "")

    def get_icon(self):
        return self._config.get("icon", "")

    def get_config(self):
        return self._config

    def get_input_fields(self):
        return self._config.get("input_fields", [])

    def interpret_result(self, score, conclusion):
        """Interpret compensation assessment result."""
        if score >= 70:
            return {
                "level": "high",
                "title": "BỒI THƯỜNG MỨC CAO",
                "color": "#27ae60",
                "description": (
                    f"Điểm đánh giá: {score:.1f}/100\n\n"
                    "Trường hợp được đánh giá ở mức bồi thường cao. "
                    "Người bị thu hồi đất có quyền được bồi thường theo giá đất "
                    "cụ thể phù hợp giá thị trường, đồng thời được hỗ trợ tái định cư "
                    "theo Nghị định 88/2024/NĐ-CP."
                ),
                "recommendations": [
                    "Yêu cầu bồi thường theo giá đất cụ thể tại thời điểm thu hồi",
                    "Đề nghị hỗ trợ tái định cư nếu phải di chuyển chỗ ở",
                    "Yêu cầu hỗ trợ đào tạo, chuyển đổi nghề nghiệp",
                    "Kiểm tra phương án bồi thường được niêm yết công khai",
                    "Nộp đơn khiếu nại nếu mức bồi thường chưa thỏa đáng"
                ]
            }
        elif score >= 40:
            return {
                "level": "medium",
                "title": "BỒI THƯỜNG MỨC TRUNG BÌNH",
                "color": "#f39c12",
                "description": (
                    f"Điểm đánh giá: {score:.1f}/100\n\n"
                    "Mức bồi thường ở mức trung bình. Cần xem xét kỹ các yếu tố "
                    "ảnh hưởng đến mức bồi thường và đối chiếu với bảng giá đất "
                    "của địa phương."
                ),
                "recommendations": [
                    "Đối chiếu mức bồi thường với bảng giá đất địa phương",
                    "Xem xét hệ số điều chỉnh K theo vị trí thực tế",
                    "Kiểm tra các khoản hỗ trợ bổ sung theo quy định",
                    "Tham khảo ý kiến tổ chức tư vấn định giá đất"
                ]
            }
        else:
            return {
                "level": "low",
                "title": "BỒI THƯỜNG MỨC THẤP",
                "color": "#e74c3c",
                "description": (
                    f"Điểm đánh giá: {score:.1f}/100\n\n"
                    "Mức bồi thường được đánh giá thấp do các yếu tố về loại đất, "
                    "thời gian sử dụng hoặc diện tích. Tuy nhiên, người bị thu hồi đất "
                    "vẫn có quyền được bồi thường theo quy định."
                ),
                "recommendations": [
                    "Kiểm tra lại điều kiện được bồi thường theo Điều 95 Luật Đất đai",
                    "Bổ sung giấy tờ chứng minh quyền sử dụng đất",
                    "Xem xét các khoản hỗ trợ khác ngoài bồi thường đất",
                    "Liên hệ Hội đồng bồi thường để được tư vấn cụ thể"
                ]
            }
