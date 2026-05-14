"""
Động cơ Logic Mờ - Hệ thống suy diễn mờ Mamdani tổng quát.
Độc lập với miền ứng dụng: tất cả các biến, hàm liên thuộc và quy tắc
được nạp từ cấu hình (JSON/dict), không mã hóa cứng.

Quy trình: Mờ hóa → Đánh giá quy tắc → Tổng hợp → Giải mờ (Trọng tâm)
"""
import numpy as np
import json
import logging

logger = logging.getLogger(__name__)


class MembershipFunction:
    """
    Biểu diễn một hàm liên thuộc mờ.
    Hỗ trợ dạng tam giác và hình thang.
    """

    def __init__(self, name, mf_type, params, label=None):
        """
        Tham số:
            name: Tên tập mờ (ví dụ: 'thấp', 'trung_bình', 'cao')
            mf_type: 'triangular' hoặc 'trapezoidal'
            params: [a, b, c] cho tam giác, [a, b, c, d] cho hình thang
            label: Nhãn hiển thị tiếng Việt
        """
        self.name = name
        self.mf_type = mf_type
        self.params = params
        self.label = label or name

    def evaluate(self, x):
        """Tính độ liên thuộc cho giá trị đầu vào x."""
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
    Biểu diễn một biến mờ (đầu vào hoặc đầu ra).
    Chứa miền giá trị và các hàm liên thuộc.
    """

    def __init__(self, name, var_range, membership_functions, label=None, unit=None):
        """
        Tham số:
            name: Mã định danh biến
            var_range: [min, max] miền giá trị
            membership_functions: danh sách các đối tượng MembershipFunction
            label: Nhãn hiển thị
            unit: Đơn vị đo
        """
        self.name = name
        self.range = var_range
        self.membership_functions = {mf.name: mf for mf in membership_functions}
        self.label = label or name
        self.unit = unit or ""

    def fuzzify(self, crisp_value):
        """
        Chuyển đổi giá trị rõ thành các độ liên thuộc mờ.
        Trả về dict: {tên_tập_mờ: độ_liên_thuộc}
        """
        result = {}
        for name, mf in self.membership_functions.items():
            result[name] = mf.evaluate(crisp_value)
        return result

    def get_mf_names(self):
        """Lấy danh sách tên các hàm liên thuộc."""
        return list(self.membership_functions.keys())


class FuzzyRule:
    """
    Biểu diễn một quy tắc mờ IF-THEN.
    Các điều kiện được nối bằng AND (toán tử min).
    """

    def __init__(self, rule_id, conditions, conclusion, weight=1.0,
                 legal_article_id=None, description=None):
        """
        Tham số:
            rule_id: Mã định danh quy tắc
            conditions: danh sách {'variable': tên, 'term': tên_tập}
            conclusion: tên tập mờ đầu ra
            weight: trọng số quy tắc (0-1)
            legal_article_id: điều khoản pháp lý liên kết
            description: mô tả quy tắc
        """
        self.rule_id = rule_id
        self.conditions = conditions
        self.conclusion = conclusion
        self.weight = weight
        self.legal_article_id = legal_article_id
        self.description = description


class FuzzyEngine:
    """
    Động cơ Suy diễn Mờ Mamdani tổng quát.
    Hoàn toàn độc lập với miền ứng dụng - tất cả cấu hình được nạp từ bên ngoài.
    """

    def __init__(self, resolution=1000):
        """
        Tham số:
            resolution: Số điểm cho quá trình giải mờ
        """
        self.input_variables = {}   # {name: FuzzyVariable}
        self.output_variable = None  # FuzzyVariable
        self.rules = []             # list of FuzzyRule
        self.resolution = resolution

    def load_config(self, config):
        """
        Nạp toàn bộ cấu hình hệ thống mờ từ dict.

        Định dạng cấu hình mong đợi:
        {
            "input_variables": [...],
            "output_variable": {...},
            "rules": [...]  // tuỳ chọn, có thể nạp từ CSDL
        }
        """
        # Nạp các biến đầu vào
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

        # Nạp biến đầu ra
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

        # Nạp quy tắc nếu có trong cấu hình
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
        Nạp quy tắc từ các đối tượng mô hình Rule (từ cơ sở dữ liệu).
        Tham số:
            rule_models: danh sách các instance của mô hình Rule
        """
        self.rules = []
        for rm in rule_models:
            conditions = rm.conditions  # Đã được phân tích từ JSON
            self.rules.append(FuzzyRule(
                rule_id=rm.id,
                conditions=conditions,
                conclusion=rm.conclusion,
                weight=rm.weight,
                legal_article_id=rm.legal_article_id,
                description=rm.description
            ))

    def add_rule(self, rule):
        """Thêm một quy tắc vào động cơ."""
        self.rules.append(rule)

    def fuzzify(self, inputs):
        """
        Mờ hóa tất cả các giá trị đầu vào.
        Tham số:
            inputs: dict {tên_biến: giá_trị_rõ}
        Trả về:
            dict {tên_biến: {tập_mờ: độ_liên_thuộc}}
        """
        fuzzified = {}
        for var_name, value in inputs.items():
            if var_name in self.input_variables:
                fuzzified[var_name] = self.input_variables[var_name].fuzzify(value)
        return fuzzified

    def evaluate_rules(self, fuzzified_inputs):
        """
        Đánh giá tất cả quy tắc sử dụng đầu vào đã mờ hóa.
        Sử dụng toán tử AND (min) cho các điều kiện.
        Trả về danh sách các bộ (quy_tắc, độ_kích_hoạt).
        """
        results = []
        for rule in self.rules:
            # Tính độ kích hoạt (AND = min của tất cả điều kiện)
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
        Tổng hợp tất cả kết quả quy tắc sử dụng toán tử MAX.
        Trả về hàm liên thuộc đầu ra tổng hợp dưới dạng mảng.
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
                    # Cắt ngọn hàm liên thuộc tại độ kích hoạt (Mamdani)
                    clipped = min(mf_value, strength)
                    # Tổng hợp bằng MAX
                    aggregated[i] = max(aggregated[i], clipped)

        return x, aggregated

    def defuzzify(self, x, aggregated):
        """
        Giải mờ bằng phương pháp trọng tâm.
        Trả về giá trị rõ đầu ra.
        """
        total_area = np.sum(aggregated)
        if total_area == 0:
            # Trả về điểm giữa nếu không có quy tắc nào kích hoạt
            return (x[0] + x[-1]) / 2

        centroid = np.sum(x * aggregated) / total_area
        return float(centroid)

    def run(self, inputs):
        """
        Chạy toàn bộ quy trình suy diễn mờ.
        Tham số:
            inputs: dict {tên_biến: giá_trị_rõ}
        Trả về:
            dict chứa score, conclusion, explanation, matched_rules
        """
        # Bước 1: Mờ hóa
        fuzzified = self.fuzzify(inputs)
        logger.debug(f"Fuzzified: {fuzzified}")

        # Bước 2: Đánh giá quy tắc
        rule_results = self.evaluate_rules(fuzzified)
        logger.debug(f"Rule results: {len(rule_results)} rules fired")

        # Bước 3: Tổng hợp
        x, aggregated = self.aggregate(rule_results)

        # Bước 4: Giải mờ
        score = self.defuzzify(x, aggregated)

        # Xác định kết luận dựa trên hàm liên thuộc đầu ra
        conclusion = self._determine_conclusion(score)

        # Xây dựng giải thích
        matched_rules_info = []
        for rule, strength in rule_results:
            matched_rules_info.append({
                "rule_id": rule.rule_id,
                "description": rule.description,
                "firing_strength": round(strength, 3),
                "conclusion": rule.conclusion,
                "legal_article_id": rule.legal_article_id
            })

        # Sắp xếp theo độ kích hoạt giảm dần
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
        """Xác định tập mờ đầu ra phù hợp nhất với điểm số."""
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
        """Xây dựng giải thích dễ đọc cho người dùng."""
        lines = []
        lines.append("=" * 50)
        lines.append("KẾT QUẢ PHÂN TÍCH FUZZY")
        lines.append("=" * 50)

        # Tóm tắt đầu vào
        lines.append("\n📥 DỮ LIỆU ĐẦU VÀO:")
        for var_name, value in inputs.items():
            var = self.input_variables.get(var_name)
            label = var.label if var else var_name
            unit = var.unit if var else ""
            lines.append(f"  • {label}: {value} {unit}")

        # Kết quả mờ hóa
        lines.append("\n🔄 KẾT QUẢ FUZZIFICATION:")
        for var_name, memberships in fuzzified.items():
            var = self.input_variables.get(var_name)
            label = var.label if var else var_name
            active = {k: v for k, v in memberships.items() if v > 0}
            if active:
                parts = [f"{k}={v:.3f}" for k, v in active.items()]
                lines.append(f"  • {label}: {', '.join(parts)}")

        # Các quy tắc đã kích hoạt
        lines.append(f"\n📋 SỐ LUẬT KÍCH HOẠT: {len(matched_rules)}")
        for i, rule in enumerate(matched_rules[:5], 1):  # 5 quy tắc hàng đầu
            rule_desc = rule['description'] or f"Rule #{rule['rule_id']}"
            lines.append(f"  {i}. {rule_desc}")
            lines.append(f"     Độ kích hoạt: {rule['firing_strength']:.3f}")

        # Kết quả cuối cùng
        lines.append(f"\n📊 ĐIỂM ĐÁNH GIÁ: {score:.2f}")

        # Nhãn đầu ra
        if self.output_variable:
            out_mf = self.output_variable.membership_functions.get(conclusion)
            conclusion_label = out_mf.label if out_mf else conclusion
            lines.append(f"📌 KẾT LUẬN: {conclusion_label}")

        lines.append("=" * 50)
        return "\n".join(lines)

    def get_variable_info(self):
        """Lấy thông tin về tất cả các biến cho giao diện."""
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
