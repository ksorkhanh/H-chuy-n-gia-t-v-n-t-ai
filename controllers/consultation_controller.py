"""
Consultation Controller - Orchestrates the consultation process.
Coordinates between modules, fuzzy engine, legal engine, and case storage.
"""
import logging
from engines.fuzzy_engine import FuzzyEngine
from engines.legal_engine import LegalEngine
from models.rule import Rule
from models.case import Case
from modules.module_loader import ModuleLoader
from core.auth import AuthService

logger = logging.getLogger(__name__)


class ConsultationController:
    """Controller for consultation workflow."""

    def __init__(self):
        self.module_loader = ModuleLoader()
        self.legal_engine = LegalEngine()
        self.auth_service = AuthService()

    def get_available_modules(self):
        """Get list of available consultation modules."""
        return self.module_loader.get_module_list()

    def get_module(self, module_name):
        """Get a specific module."""
        return self.module_loader.get_module(module_name)

    def get_input_fields(self, module_name):
        """Get input field definitions for a module."""
        module = self.module_loader.get_module(module_name)
        if module:
            return module.get_input_fields()
        return []

    def run_consultation(self, module_name, inputs):
        """
        Run a full consultation.
        Args:
            module_name: Module identifier
            inputs: dict of {variable_name: value}
        Returns:
            dict with score, conclusion, interpretation, legal_citations, explanation
        """
        module = self.module_loader.get_module(module_name)
        if not module:
            return {"error": f"Module không tìm thấy: {module_name}"}

        try:
            # 1. Initialize fuzzy engine with module config
            fuzzy = FuzzyEngine()
            config = module.get_config()
            fuzzy.load_config(config)

            # 2. Load rules from database
            db_rules = Rule.get_by_module(module_name, active_only=True)
            if db_rules:
                fuzzy.load_rules_from_db(db_rules)
            # If no DB rules, engine uses config rules (if any)

            # 3. Run fuzzy inference
            result = fuzzy.run(inputs)

            # 4. Interpret result using module-specific logic
            interpretation = module.interpret_result(
                result["score"], result["conclusion"]
            )

            # 5. Get legal citations for matched rules
            legal_citations = self.legal_engine.get_articles_for_rules(
                result["matched_rules"]
            )

            # 6. Build complete result
            full_result = {
                "module_name": module.get_display_name(),
                "score": result["score"],
                "conclusion": result["conclusion"],
                "interpretation": interpretation,
                "explanation": result["explanation"],
                "matched_rules": result["matched_rules"],
                "legal_citations": legal_citations,
                "fuzzified_inputs": result.get("fuzzified_inputs", {}),
                "inputs": inputs
            }

            # 7. Save case to history
            user = self.auth_service.get_current_user()
            if user:
                rule_ids = [r["rule_id"] for r in result["matched_rules"]]
                Case.save(
                    user_id=user["id"],
                    module=module_name,
                    input_data=inputs,
                    result_data={
                        "score": result["score"],
                        "conclusion": result["conclusion"],
                        "interpretation_title": interpretation["title"]
                    },
                    matched_rules=rule_ids,
                    score=result["score"],
                    conclusion=interpretation["title"]
                )

            return full_result

        except Exception as e:
            logger.error(f"Consultation error: {e}")
            return {"error": f"Lỗi trong quá trình tư vấn: {str(e)}"}
