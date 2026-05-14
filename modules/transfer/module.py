"""
Transfer Module - Chuyển nhượng quyền sử dụng đất.
Evaluates feasibility of land use right transfers.
"""
import os
import json
from modules.base_module import BaseModule


class TransferModule(BaseModule):
    """Module tư vấn chuyển nhượng quyền sử dụng đất."""

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = json.load(f)

    def get_name(self):
        return "transfer"

    def get_display_name(self):
        return self._config.get("display_name", "Chuyển nhượng QSD đất")

    def get_description(self):
        return self._config.get("description", "")

    def get_icon(self):
        return self._config.get("icon", "")

    def get_config(self):
        return self._config

    def get_input_fields(self):
        return self._config.get("input_fields", [])

    def interpret_result(self, score, conclusion):
        """Interpret transfer feasibility result."""
        if score >= 70:
            return {
                "level": "high",
                "title": "KHẢ THI CAO",
                "color": "#27ae60",
                "description": (
                    f"Điểm đánh giá: {score:.1f}/100\n\n"
                    "Việc chuyển nhượng quyền sử dụng đất có tính khả thi cao. "
                    "Hồ sơ pháp lý cơ bản đáp ứng yêu cầu theo Luật Đất đai 2024. "
                    "Nên tiến hành các thủ tục công chứng và đăng ký biến động."
                ),
                "recommendations": [
                    "Hoàn tất hợp đồng chuyển nhượng có công chứng/chứng thực",
                    "Nộp hồ sơ đăng ký biến động tại Văn phòng đăng ký đất đai",
                    "Thực hiện nghĩa vụ tài chính (thuế TNCN, lệ phí trước bạ)",
                    "Nhận Giấy chứng nhận mới trong 10 ngày làm việc"
                ]
            }
        elif score >= 40:
            return {
                "level": "medium",
                "title": "CẦN XEM XÉT THÊM",
                "color": "#f39c12",
                "description": (
                    f"Điểm đánh giá: {score:.1f}/100\n\n"
                    "Việc chuyển nhượng có thể thực hiện được nhưng cần bổ sung "
                    "hoặc hoàn thiện một số điều kiện. Nên tham khảo thêm ý kiến "
                    "chuyên gia pháp lý trước khi tiến hành."
                ),
                "recommendations": [
                    "Kiểm tra và bổ sung giấy tờ pháp lý còn thiếu",
                    "Xác minh tình trạng quy hoạch khu vực",
                    "Đánh giá lại giá chuyển nhượng theo thị trường",
                    "Tham khảo ý kiến luật sư hoặc công chứng viên"
                ]
            }
        else:
            return {
                "level": "low",
                "title": "KHẢ THI THẤP",
                "color": "#e74c3c",
                "description": (
                    f"Điểm đánh giá: {score:.1f}/100\n\n"
                    "Việc chuyển nhượng gặp nhiều rào cản pháp lý nghiêm trọng. "
                    "Không đủ điều kiện theo Điều 45 Luật Đất đai 2024. "
                    "Cần giải quyết các vấn đề pháp lý trước khi tiến hành."
                ),
                "recommendations": [
                    "Hoàn thiện thủ tục cấp Giấy chứng nhận QSD đất",
                    "Giải quyết tranh chấp (nếu có)",
                    "Hoàn thành nghĩa vụ tài chính với Nhà nước",
                    "Kiểm tra đất không bị kê biên thi hành án",
                    "Liên hệ cơ quan đăng ký đất đai để được hướng dẫn"
                ]
            }
