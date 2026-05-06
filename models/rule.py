"""
Rule Model - CRUD for fuzzy inference rules.
Supports JSON import/export for extensibility.
"""
import json
import logging
from core.database import DatabaseManager

logger = logging.getLogger(__name__)


class Rule:
    """Model for fuzzy inference rules."""

    def __init__(self, id=None, module=None, name=None, condition_json=None,
                 conclusion=None, weight=1.0, legal_article_id=None,
                 is_active=True, description=None):
        self.id = id
        self.module = module
        self.name = name
        self.condition_json = condition_json
        self.conclusion = conclusion
        self.weight = weight
        self.legal_article_id = legal_article_id
        self.is_active = is_active
        self.description = description

    @property
    def conditions(self):
        """Parse condition JSON to list of dicts."""
        if isinstance(self.condition_json, str):
            try:
                return json.loads(self.condition_json)
            except json.JSONDecodeError:
                return []
        return self.condition_json or []

    @staticmethod
    def get_by_module(module, active_only=True):
        db = DatabaseManager()
        if active_only:
            rows = db.fetch_all(
                "SELECT * FROM rules WHERE module = ? AND is_active = 1 ORDER BY name", (module,))
        else:
            rows = db.fetch_all(
                "SELECT * FROM rules WHERE module = ? ORDER BY name", (module,))
        return [Rule._from_row(r) for r in rows]

    @staticmethod
    def get_all(active_only=False):
        db = DatabaseManager()
        if active_only:
            rows = db.fetch_all("SELECT * FROM rules WHERE is_active = 1 ORDER BY module, name")
        else:
            rows = db.fetch_all("SELECT * FROM rules ORDER BY module, name")
        return [Rule._from_row(r) for r in rows]

    @staticmethod
    def find_by_id(rule_id):
        db = DatabaseManager()
        row = db.fetch_one("SELECT * FROM rules WHERE id = ?", (rule_id,))
        return Rule._from_row(row) if row else None

    @staticmethod
    def create(module, name, conditions, conclusion, weight=1.0,
               legal_article_id=None, description=None):
        db = DatabaseManager()
        cond_str = json.dumps(conditions, ensure_ascii=False)
        cursor = db.execute(
            """INSERT INTO rules (module, name, condition_json, conclusion,
               weight, legal_article_id, description) VALUES (?,?,?,?,?,?,?)""",
            (module, name, cond_str, conclusion, weight, legal_article_id, description))
        return cursor.lastrowid

    @staticmethod
    def update(rule_id, **kwargs):
        db = DatabaseManager()
        allowed = ['name', 'condition_json', 'conclusion', 'weight',
                    'legal_article_id', 'is_active', 'description']
        updates, params = [], []
        for k, v in kwargs.items():
            if k in allowed:
                if k == 'condition_json' and isinstance(v, list):
                    v = json.dumps(v, ensure_ascii=False)
                updates.append(f"{k} = ?")
                params.append(v)
        if updates:
            params.append(rule_id)
            db.execute(f"UPDATE rules SET {', '.join(updates)} WHERE id = ?", tuple(params))

    @staticmethod
    def delete(rule_id):
        db = DatabaseManager()
        db.execute("DELETE FROM rules WHERE id = ?", (rule_id,))

    @staticmethod
    def toggle_active(rule_id):
        db = DatabaseManager()
        db.execute("UPDATE rules SET is_active = CASE WHEN is_active=1 THEN 0 ELSE 1 END WHERE id=?", (rule_id,))

    @staticmethod
    def import_from_json(json_data):
        """Import rules from JSON. Returns (success_count, error_count)."""
        success, errors = 0, 0
        for rule_data in json_data.get("rules", []):
            try:
                legal_article_id = None
                if "legal_article_code" in rule_data and "legal_article_number" in rule_data:
                    db = DatabaseManager()
                    row = db.fetch_one(
                        """SELECT la.id FROM legal_articles la
                           JOIN legal_documents ld ON la.document_id = ld.id
                           WHERE ld.code = ? AND la.article_number = ?""",
                        (rule_data["legal_article_code"], rule_data["legal_article_number"]))
                    if row:
                        legal_article_id = row["id"]
                Rule.create(
                    module=json_data.get("metadata", {}).get("module", rule_data.get("module", "")),
                    name=rule_data["name"], conditions=rule_data["conditions"],
                    conclusion=rule_data["conclusion"], weight=rule_data.get("weight", 1.0),
                    legal_article_id=legal_article_id, description=rule_data.get("description"))
                success += 1
            except Exception as e:
                logger.error(f"Error importing rule: {e}")
                errors += 1
        return success, errors

    @staticmethod
    def export_to_dict(module=None):
        rules = Rule.get_by_module(module, active_only=False) if module else Rule.get_all()
        return {"metadata": {"module": module or "all"}, "rules": [r.to_dict() for r in rules]}

    @staticmethod
    def _from_row(row):
        if not row: return None
        return Rule(id=row["id"], module=row["module"], name=row["name"],
                    condition_json=row["condition_json"], conclusion=row["conclusion"],
                    weight=row["weight"], legal_article_id=row["legal_article_id"],
                    is_active=bool(row["is_active"]), description=row["description"])

    def to_dict(self):
        return {"id": self.id, "module": self.module, "name": self.name,
                "conditions": self.conditions, "conclusion": self.conclusion,
                "weight": self.weight, "legal_article_id": self.legal_article_id,
                "is_active": self.is_active, "description": self.description}
