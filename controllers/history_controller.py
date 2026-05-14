"""
Bộ điều khiển Lịch sử - Quản lý lịch sử tư vấn.
"""
import json
import logging
from models.case import Case
from core.auth import AuthService

logger = logging.getLogger(__name__)


class HistoryController:
    """Bộ điều khiển cho lịch sử tư vấn."""

    def __init__(self):
        self.auth = AuthService()

    def get_history(self, limit=100):
        """Lấy lịch sử tư vấn theo vai trò người dùng."""
        user = self.auth.get_current_user()
        if not user:
            return []
        if user["role"] == "admin":
            rows = Case.get_all(limit)
        else:
            rows = Case.get_by_user(user["id"], limit)
        return [dict(r) for r in rows]

    def get_case_detail(self, case_id):
        """Lấy thông tin chi tiết của một bản ghi."""
        row = Case.find_by_id(case_id)
        if row:
            result = dict(row)
            # Phân tích các trường JSON
            if result.get("input_data"):
                result["input_data"] = json.loads(result["input_data"])
            if result.get("result_data"):
                result["result_data"] = json.loads(result["result_data"])
            if result.get("matched_rules"):
                result["matched_rules"] = json.loads(result["matched_rules"])
            return result
        return None

    def search_history(self, module=None, date_from=None, date_to=None):
        """Tìm kiếm lịch sử với các bộ lọc."""
        user = self.auth.get_current_user()
        user_id = None if user and user["role"] == "admin" else (user["id"] if user else None)
        rows = Case.search(module, date_from, date_to, user_id)
        return [dict(r) for r in rows]

    def delete_case(self, case_id):
        """Xóa một bản ghi. Quản trị viên xóa bất kỳ, người dùng chỉ xóa của mình."""
        user = self.auth.get_current_user()
        if not user:
            return False
            
        case = Case.find_by_id(case_id)
        if not case:
            return False
            
        if user["role"] == "admin" or case["user_id"] == user["id"]:
            Case.delete(case_id)
            return True
        return False

    def delete_all_cases(self):
        """Xóa toàn bộ lịch sử tư vấn."""
        user = self.auth.get_current_user()
        if not user:
            return False
            
        if user["role"] == "admin":
            Case.delete_all()
        else:
            Case.delete_all(user_id=user["id"])
        return True

    def get_statistics(self):
        """Lấy thống kê tư vấn."""
        return Case.get_statistics()
