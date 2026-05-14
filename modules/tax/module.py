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
        return self._config.get("icon", "")

    def get_config(self):
        return self._config

    def get_input_fields(self):
        return self._config.get("input_fields", [])

    def interpret_result(self, score, conclusion):
        """Interpret the fuzzy score into human-readable advice."""
        if score < 40:
            return {
                "level": "low",
                "title": "THUẾ SUẤT ƯU ĐÃI / MIỄN GIẢM",
                "color": "#27ae60",
                "description": f"Dự báo nghĩa vụ tài chính ở mức RẤT THẤP ({score:.1f}/100). Có khả năng thuộc diện được hưởng chính sách ưu đãi của Nhà nước.",
                "recommendations": [
                    "Khu vực đất có giá trị thấp, vị trí vùng sâu vùng xa, ven đô hoặc thuộc vùng có điều kiện kinh tế khó khăn.",
                    "Áp dụng cho đất nông nghiệp, đất trồng rừng, hoặc diện tích đất ở hoàn toàn nằm trong hạn mức giao đất của địa phương.",
                    "Hành động: Kiểm tra kỹ Điều 157 Luật Đất đai 2024 về các trường hợp được miễn, giảm tiền sử dụng đất, tiền thuê đất.",
                    "Chuẩn bị các giấy tờ chứng minh nguồn gốc đất, hoàn cảnh gia đình hoặc chính sách người có công để cơ quan thuế xét duyệt ưu đãi."
                ]
            }
        elif score < 70:
            return {
                "level": "medium",
                "title": "THUẾ SUẤT TIÊU CHUẨN",
                "color": "#f39c12",
                "description": f"Dự báo nghĩa vụ tài chính ở mức TRUNG BÌNH ({score:.1f}/100). Đất sẽ chịu mức thuế/phí theo khung giá thông thường của địa phương.",
                "recommendations": [
                    "Thường áp dụng cho đất ở tại các khu dân cư tiêu chuẩn, nông thôn hoặc đô thị nhưng không có lợi thế thương mại đặc biệt.",
                    "Diện tích đất nằm trong hạn mức hoặc vượt hạn mức không đáng kể.",
                    "Thuế sẽ áp dụng bảng giá đất mới nhất do UBND cấp tỉnh ban hành (theo nguyên tắc thị trường của Luật Đất đai 2024).",
                    "Hành động: Dự trù thêm lệ phí trước bạ (thường là 0.5% giá trị đất) và các loại phí thẩm định hồ sơ, phí cấp Giấy chứng nhận.",
                    "Khuyến nghị: Truy cập cổng thông tin điện tử của Sở TN&MT địa phương để tra cứu chính xác bảng giá đất tại vị trí tuyến đường đang xét."
                ]
            }
        else:
            return {
                "level": "heavy",
                "title": "THUẾ SUẤT CAO",
                "color": "#e74c3c",
                "description": f"Dự báo nghĩa vụ tài chính ở mức CAO ({score:.1f}/100). Tài sản thuộc nhóm bị áp dụng biểu thuế suất lớn hoặc có hệ số điều chỉnh K cao.",
                "recommendations": [
                    "Thường áp dụng cho đất thương mại, dịch vụ, đất mặt tiền trung tâm đô thị hoặc phần diện tích đất ở vượt quá hạn mức quy định (đánh thuế lũy tiến).",
                    "Theo định hướng mới, Nhà nước đánh thuế cao đối với người sử dụng nhiều diện tích đất, vị trí sinh lời cao, nhiều nhà ở, hoặc chậm đưa đất vào sử dụng.",
                    "Hành động: Cần có kế hoạch tài chính vững vàng. Chi phí thực hiện nghĩa vụ tài chính có thể chiếm tỷ trọng lớn trong tổng vốn đầu tư.",
                    "Khuyến nghị: Nên tìm kiếm dịch vụ tư vấn thuế chuyên nghiệp để tối ưu hóa chi phí hoặc lập dự án đầu tư để được hưởng chính sách thuê đất trả tiền hàng năm."
                ]
            }
