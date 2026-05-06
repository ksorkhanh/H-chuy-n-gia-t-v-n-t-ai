"""
Case Model - Save and retrieve consultation history.
"""
import json
import logging
from core.database import DatabaseManager

logger = logging.getLogger(__name__)


class Case:
    """Model for consultation cases and history."""

    def __init__(self, id=None, user_id=None, module=None, input_data=None,
                 result_data=None, matched_rules=None, score=None,
                 conclusion=None, created_at=None, notes=None):
        self.id = id
        self.user_id = user_id
        self.module = module
        self.input_data = input_data
        self.result_data = result_data
        self.matched_rules = matched_rules
        self.score = score
        self.conclusion = conclusion
        self.created_at = created_at
        self.notes = notes

    @staticmethod
    def save(user_id, module, input_data, result_data, matched_rules=None,
             score=None, conclusion=None, notes=None):
        """Save a consultation case."""
        db = DatabaseManager()
        input_str = json.dumps(input_data, ensure_ascii=False)
        result_str = json.dumps(result_data, ensure_ascii=False)
        rules_str = json.dumps(matched_rules, ensure_ascii=False) if matched_rules else None
        cursor = db.execute(
            """INSERT INTO cases (user_id, module, input_data, result_data,
               matched_rules, score, conclusion, notes) VALUES (?,?,?,?,?,?,?,?)""",
            (user_id, module, input_str, result_str, rules_str, score, conclusion, notes))
        return cursor.lastrowid

    @staticmethod
    def get_by_user(user_id, limit=50):
        """Get consultation history for a user."""
        db = DatabaseManager()
        rows = db.fetch_all(
            """SELECT c.*, u.full_name as user_name
               FROM cases c JOIN users u ON c.user_id = u.id
               WHERE c.user_id = ? ORDER BY c.created_at DESC LIMIT ?""",
            (user_id, limit))
        return rows

    @staticmethod
    def get_all(limit=100):
        """Get all consultation history."""
        db = DatabaseManager()
        rows = db.fetch_all(
            """SELECT c.*, u.full_name as user_name
               FROM cases c JOIN users u ON c.user_id = u.id
               ORDER BY c.created_at DESC LIMIT ?""", (limit,))
        return rows

    @staticmethod
    def find_by_id(case_id):
        """Find case by ID with full details."""
        db = DatabaseManager()
        row = db.fetch_one(
            """SELECT c.*, u.full_name as user_name
               FROM cases c JOIN users u ON c.user_id = u.id WHERE c.id = ?""",
            (case_id,))
        return row

    @staticmethod
    def search(module=None, date_from=None, date_to=None, user_id=None):
        """Search cases with filters."""
        db = DatabaseManager()
        query = """SELECT c.*, u.full_name as user_name
                   FROM cases c JOIN users u ON c.user_id = u.id WHERE 1=1"""
        params = []
        if module:
            query += " AND c.module = ?"
            params.append(module)
        if date_from:
            query += " AND c.created_at >= ?"
            params.append(date_from)
        if date_to:
            query += " AND c.created_at <= ?"
            params.append(date_to)
        if user_id:
            query += " AND c.user_id = ?"
            params.append(user_id)
        query += " ORDER BY c.created_at DESC"
        return db.fetch_all(query, tuple(params))

    @staticmethod
    def delete(case_id):
        db = DatabaseManager()
        db.execute("DELETE FROM cases WHERE id = ?", (case_id,))

    @staticmethod
    def get_statistics():
        """Get consultation statistics."""
        db = DatabaseManager()
        total = db.fetch_one("SELECT COUNT(*) as count FROM cases")
        by_module = db.fetch_all(
            "SELECT module, COUNT(*) as count FROM cases GROUP BY module")
        return {"total": total["count"] if total else 0,
                "by_module": {r["module"]: r["count"] for r in by_module}}
