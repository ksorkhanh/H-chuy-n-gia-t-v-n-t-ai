"""
History Controller - Manages consultation history.
"""
import json
import logging
from models.case import Case
from core.auth import AuthService

logger = logging.getLogger(__name__)


class HistoryController:
    """Controller for consultation history."""

    def __init__(self):
        self.auth = AuthService()

    def get_history(self, limit=100):
        """Get consultation history based on user role."""
        user = self.auth.get_current_user()
        if not user:
            return []
        if user["role"] == "admin":
            rows = Case.get_all(limit)
        else:
            rows = Case.get_by_user(user["id"], limit)
        return [dict(r) for r in rows]

    def get_case_detail(self, case_id):
        """Get detailed case information."""
        row = Case.find_by_id(case_id)
        if row:
            result = dict(row)
            # Parse JSON fields
            if result.get("input_data"):
                result["input_data"] = json.loads(result["input_data"])
            if result.get("result_data"):
                result["result_data"] = json.loads(result["result_data"])
            if result.get("matched_rules"):
                result["matched_rules"] = json.loads(result["matched_rules"])
            return result
        return None

    def search_history(self, module=None, date_from=None, date_to=None):
        """Search history with filters."""
        user = self.auth.get_current_user()
        user_id = None if user and user["role"] == "admin" else (user["id"] if user else None)
        rows = Case.search(module, date_from, date_to, user_id)
        return [dict(r) for r in rows]

    def delete_case(self, case_id):
        """Delete a case. Admins can delete any, users can delete their own."""
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
        """Delete all history cases."""
        user = self.auth.get_current_user()
        if not user:
            return False
            
        if user["role"] == "admin":
            Case.delete_all()
        else:
            Case.delete_all(user_id=user["id"])
        return True

    def get_statistics(self):
        """Get consultation statistics."""
        return Case.get_statistics()
