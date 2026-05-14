"""
Bộ điều khiển Quy tắc - Quản lý các quy tắc suy diễn mờ.
"""
import json
import logging
from models.rule import Rule
from core.auth import AuthService
from utils.helpers import load_json_file

logger = logging.getLogger(__name__)


class RuleController:
    """Bộ điều khiển cho quản lý quy tắc."""

    def __init__(self):
        self.auth = AuthService()

    def get_all_rules(self, module=None):
        if module:
            return [r.to_dict() for r in Rule.get_by_module(module, active_only=False)]
        return [r.to_dict() for r in Rule.get_all()]

    def get_rule(self, rule_id):
        rule = Rule.find_by_id(rule_id)
        return rule.to_dict() if rule else None

    def create_rule(self, module, name, conditions, conclusion,
                    weight=1.0, legal_article_id=None, description=None):
        self.auth.require_permission("manage_rules")
        return Rule.create(module, name, conditions, conclusion,
                           weight, legal_article_id, description)

    def update_rule(self, rule_id, **kwargs):
        self.auth.require_permission("manage_rules")
        Rule.update(rule_id, **kwargs)

    def delete_rule(self, rule_id):
        self.auth.require_permission("manage_rules")
        Rule.delete(rule_id)

    def toggle_rule(self, rule_id):
        self.auth.require_permission("manage_rules")
        Rule.toggle_active(rule_id)

    def import_rules_from_file(self, filepath):
        """Nhập quy tắc từ file JSON."""
        self.auth.require_permission("import_export")
        json_data = load_json_file(filepath)
        if json_data is None:
            return 0, 1  # 0 success, 1 error
        return Rule.import_from_json(json_data)

    def import_rules_from_json(self, json_str):
        """Nhập quy tắc từ chuỗi JSON."""
        self.auth.require_permission("import_export")
        try:
            json_data = json.loads(json_str)
            return Rule.import_from_json(json_data)
        except json.JSONDecodeError:
            return 0, 1

    def export_rules(self, module=None):
        """Xuất quy tắc ra dict."""
        return Rule.export_to_dict(module)
