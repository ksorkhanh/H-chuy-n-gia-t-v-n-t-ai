"""
Fuzzy Logic Engine - Generic Mamdani fuzzy inference system.
Domain-independent: all variables, membership functions, and rules
are loaded from configuration (JSON/dict), not hardcoded.

Process: Fuzzification → Rule Evaluation → Aggregation → Defuzzification (Centroid)
"""
import numpy as np
import json
import logging

logger = logging.getLogger(__name__)


class MembershipFunction:
    """
    Represents a fuzzy membership function.
    Supports triangular and trapezoidal shapes.
    """

    def __init__(self, name, mf_type, params, label=None):
        """
        Args:
            name: Term name (e.g., 'low', 'medium', 'high')
            mf_type: 'triangular' or 'trapezoidal'
            params: [a, b, c] for triangular, [a, b, c, d] for trapezoidal
            label: Display label in Vietnamese
        """
        self.name = name
        self.mf_type = mf_type
        self.params = params
        self.label = label or name

    def evaluate(self, x):
        """Calculate membership degree for input value x."""
        if self.mf_type == "triangular":
            a, b, c = self.params
            if x < a or x > c:
                return 0.0
            elif x == b:
                return 1.0
            elif x < b:
                return (x - a) / (b - a)
            else:
                return (c - x) / (c - b)

        elif self.mf_type == "trapezoidal":
            a, b, c, d = self.params
            if x < a or x > d:
                return 0.0
            elif x >= b and x <= c:
                return 1.0
            elif x < b:
                return (x - a) / (b - a)
            else:
                return (d - x) / (d - c)
        return 0.0


class FuzzyVariable:
    """
    Represents a fuzzy input or output variable.
    Contains range and membership functions.
    """

    def __init__(self, name, var_range, membership_functions, label=None, unit=None):
        """
        Args:
            name: Variable identifier
            var_range: [min, max] universe of discourse
            membership_functions: list of MembershipFunction objects
            label: Display label
            unit: Unit of measurement
        """
        self.name = name
        self.range = var_range
        self.membership_functions = {mf.name: mf for mf in membership_functions}
        self.label = label or name
        self.unit = unit or ""

    def fuzzify(self, crisp_value):
        """
        Convert crisp value to fuzzy membership degrees.
        Returns dict: {term_name: degree}
        """
        result = {}
        for name, mf in self.membership_functions.items():
            result[name] = mf.evaluate(crisp_value)
        return result

    def get_mf_names(self):
        """Get list of membership function names."""
        return list(self.membership_functions.keys())


class FuzzyRule:
    """
    Represents a fuzzy IF-THEN rule.
    Conditions are AND-connected (min operator).
    """

    def __init__(self, rule_id, conditions, conclusion, weight=1.0,
                 legal_article_id=None, description=None):
        """
        Args:
            rule_id: Unique rule identifier
            conditions: list of {'variable': name, 'term': term_name}
            conclusion: output term name
            weight: rule weight (0-1)
            legal_article_id: linked legal article
            description: rule description
        """
        self.rule_id = rule_id
        self.conditions = conditions
        self.conclusion = conclusion
        self.weight = weight
        self.legal_article_id = legal_article_id
        self.description = description


class FuzzyEngine:
    """
    Generic Mamdani Fuzzy Inference Engine.
    Completely domain-independent - all configuration loaded externally.
    """

    def __init__(self, resolution=1000):
        """
        Args:
            resolution: Number of points for defuzzification
        """
        self.input_variables = {}   # {name: FuzzyVariable}
        self.output_variable = None  # FuzzyVariable
        self.rules = []             # list of FuzzyRule
        self.resolution = resolution

    def load_config(self, config):
        """
        Load complete fuzzy system configuration from dict.

        Expected config format:
        {
            "input_variables": [...],
            "output_variable": {...},
            "rules": [...]  // optional, can be loaded from DB
        }
        """
        # Load input variables
        for var_cfg in config.get("input_variables", []):
            mfs = []
            for mf_cfg in var_cfg.get("membership_functions", []):
                mfs.append(MembershipFunction(
                    name=mf_cfg["name"],
                    mf_type=mf_cfg.get("type", "triangular"),
                    params=mf_cfg["params"],
                    label=mf_cfg.get("label")
                ))
            var = FuzzyVariable(
                name=var_cfg["name"],
                var_range=var_cfg["range"],
                membership_functions=mfs,
                label=var_cfg.get("label"),
                unit=var_cfg.get("unit")
            )
            self.input_variables[var.name] = var

        # Load output variable
        out_cfg = config.get("output_variable", {})
        if out_cfg:
            mfs = []
            for mf_cfg in out_cfg.get("membership_functions", []):
                mfs.append(MembershipFunction(
                    name=mf_cfg["name"],
                    mf_type=mf_cfg.get("type", "triangular"),
                    params=mf_cfg["params"],
                    label=mf_cfg.get("label")
                ))
            self.output_variable = FuzzyVariable(
                name=out_cfg["name"],
                var_range=out_cfg["range"],
                membership_functions=mfs,
                label=out_cfg.get("label"),
                unit=out_cfg.get("unit")
            )

        # Load rules if provided in config
        for rule_cfg in config.get("rules", []):
            self.add_rule(FuzzyRule(
                rule_id=rule_cfg.get("id"),
                conditions=rule_cfg["conditions"],
                conclusion=rule_cfg["conclusion"],
                weight=rule_cfg.get("weight", 1.0),
                description=rule_cfg.get("description")
            ))

    def load_rules_from_db(self, rule_models):
        """
        Load rules from Rule model objects (from database).
        Args:
            rule_models: list of Rule model instances
        """
        self.rules = []
        for rm in rule_models:
            conditions = rm.conditions  # Already parsed from JSON
            self.rules.append(FuzzyRule(
                rule_id=rm.id,
                conditions=conditions,
                conclusion=rm.conclusion,
                weight=rm.weight,
                legal_article_id=rm.legal_article_id,
                description=rm.description
            ))

    def add_rule(self, rule):
        """Add a single rule to the engine."""
        self.rules.append(rule)

    def fuzzify(self, inputs):
        """
        Fuzzify all input values.
        Args:
            inputs: dict {variable_name: crisp_value}
        Returns:
            dict {variable_name: {term: degree}}
        """
        fuzzified = {}
        for var_name, value in inputs.items():
            if var_name in self.input_variables:
                fuzzified[var_name] = self.input_variables[var_name].fuzzify(value)
        return fuzzified

    def evaluate_rules(self, fuzzified_inputs):
        """
        Evaluate all rules using fuzzified inputs.
        Uses AND (min) operator for conditions.
        Returns list of (rule, firing_strength) tuples.
        """
        results = []
        for rule in self.rules:
            # Calculate firing strength (AND = min of all conditions)
            strengths = []
            all_conditions_met = True

            for condition in rule.conditions:
                var_name = condition["variable"]
                term = condition["term"]

                if var_name in fuzzified_inputs:
                    degree = fuzzified_inputs[var_name].get(term, 0.0)
                    strengths.append(degree)
                else:
                    all_conditions_met = False
                    break

            if all_conditions_met and strengths:
                firing_strength = min(strengths) * rule.weight
                if firing_strength > 0:
                    results.append((rule, firing_strength))

        return results

    def aggregate(self, rule_results):
        """
        Aggregate all rule outputs using MAX operator.
        Returns the aggregated output membership function as array.
        """
        if not self.output_variable:
            raise ValueError("Output variable not configured")

        out_range = self.output_variable.range
        x = np.linspace(out_range[0], out_range[1], self.resolution)
        aggregated = np.zeros(self.resolution)

        for rule, strength in rule_results:
            conclusion_term = rule.conclusion
            if conclusion_term in self.output_variable.membership_functions:
                mf = self.output_variable.membership_functions[conclusion_term]
                for i, xi in enumerate(x):
                    mf_value = mf.evaluate(xi)
                    # Clip the MF at firing strength (Mamdani implication)
                    clipped = min(mf_value, strength)
                    # Aggregate using MAX
                    aggregated[i] = max(aggregated[i], clipped)

        return x, aggregated

    def defuzzify(self, x, aggregated):
        """
        Defuzzify using centroid method.
        Returns crisp output value.
        """
        total_area = np.sum(aggregated)
        if total_area == 0:
            # Return midpoint if no rules fired
            return (x[0] + x[-1]) / 2

        centroid = np.sum(x * aggregated) / total_area
        return float(centroid)

    def run(self, inputs):
        """
        Run complete fuzzy inference.
        Args:
            inputs: dict {variable_name: crisp_value}
        Returns:
            dict with score, conclusion, explanation, matched_rules
        """
        # Step 1: Fuzzification
        fuzzified = self.fuzzify(inputs)
        logger.debug(f"Fuzzified: {fuzzified}")

        # Step 2: Rule evaluation
        rule_results = self.evaluate_rules(fuzzified)
        logger.debug(f"Rule results: {len(rule_results)} rules fired")

        # Step 3: Aggregation
        x, aggregated = self.aggregate(rule_results)

        # Step 4: Defuzzification
        score = self.defuzzify(x, aggregated)

        # Determine conclusion based on output MFs
        conclusion = self._determine_conclusion(score)

        # Build explanation
        matched_rules_info = []
        for rule, strength in rule_results:
            matched_rules_info.append({
                "rule_id": rule.rule_id,
                "description": rule.description,
                "firing_strength": round(strength, 3),
                "conclusion": rule.conclusion,
                "legal_article_id": rule.legal_article_id
            })

        # Sort by firing strength descending
        matched_rules_info.sort(key=lambda x: x["firing_strength"], reverse=True)

        explanation = self._build_explanation(inputs, fuzzified, matched_rules_info, score, conclusion)

        return {
            "score": round(score, 2),
            "conclusion": conclusion,
            "explanation": explanation,
            "matched_rules": matched_rules_info,
            "fuzzified_inputs": {k: {t: round(d, 3) for t, d in v.items() if d > 0}
                                 for k, v in fuzzified.items()},
            "aggregation_data": {"x": x.tolist(), "y": aggregated.tolist()}
        }

    def _determine_conclusion(self, score):
        """Determine which output term best matches the score."""
        if not self.output_variable:
            return "unknown"

        best_term = None
        best_degree = 0
        for name, mf in self.output_variable.membership_functions.items():
            degree = mf.evaluate(score)
            if degree > best_degree:
                best_degree = degree
                best_term = name

        return best_term or "unknown"

    def _build_explanation(self, inputs, fuzzified, matched_rules, score, conclusion):
        """Build human-readable explanation."""
        lines = []
        lines.append("=" * 50)
        lines.append("KẾT QUẢ PHÂN TÍCH FUZZY")
        lines.append("=" * 50)

        # Input summary
        lines.append("\n📥 DỮ LIỆU ĐẦU VÀO:")
        for var_name, value in inputs.items():
            var = self.input_variables.get(var_name)
            label = var.label if var else var_name
            unit = var.unit if var else ""
            lines.append(f"  • {label}: {value} {unit}")

        # Fuzzification results
        lines.append("\n🔄 KẾT QUẢ FUZZIFICATION:")
        for var_name, memberships in fuzzified.items():
            var = self.input_variables.get(var_name)
            label = var.label if var else var_name
            active = {k: v for k, v in memberships.items() if v > 0}
            if active:
                parts = [f"{k}={v:.3f}" for k, v in active.items()]
                lines.append(f"  • {label}: {', '.join(parts)}")

        # Rules fired
        lines.append(f"\n📋 SỐ LUẬT KÍCH HOẠT: {len(matched_rules)}")
        for i, rule in enumerate(matched_rules[:5], 1):  # Top 5 rules
            rule_desc = rule['description'] or f"Rule #{rule['rule_id']}"
            lines.append(f"  {i}. {rule_desc}")
            lines.append(f"     Độ kích hoạt: {rule['firing_strength']:.3f}")

        # Final result
        lines.append(f"\n📊 ĐIỂM ĐÁNH GIÁ: {score:.2f}")

        # Output label
        if self.output_variable:
            out_mf = self.output_variable.membership_functions.get(conclusion)
            conclusion_label = out_mf.label if out_mf else conclusion
            lines.append(f"📌 KẾT LUẬN: {conclusion_label}")

        lines.append("=" * 50)
        return "\n".join(lines)

    def get_variable_info(self):
        """Get information about all variables for UI."""
        info = {"inputs": [], "output": None}
        for name, var in self.input_variables.items():
            info["inputs"].append({
                "name": var.name, "label": var.label,
                "range": var.range, "unit": var.unit,
                "terms": [{"name": mf.name, "label": mf.label}
                          for mf in var.membership_functions.values()]
            })
        if self.output_variable:
            info["output"] = {
                "name": self.output_variable.name,
                "label": self.output_variable.label,
                "range": self.output_variable.range,
                "terms": [{"name": mf.name, "label": mf.label}
                          for mf in self.output_variable.membership_functions.values()]
            }
        return info
