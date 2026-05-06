"""
Seed rules for the Tax module.
"""
import sys
sys.path.insert(0, '.')
import json
from models.rule import Rule
from core.database import DatabaseManager

def seed_tax_rules():
    db = DatabaseManager()
    
    # Check if tax rules already exist
    existing = Rule.get_by_module('tax')
    if existing:
        print("Tax rules already exist. Skipping.")
        return

    tax_rules = [
        {
            "module": "tax",
            "name": "Tax Rule 1 - Low Value Residential",
            "conditions": [
                {"variable": "land_value", "term": "low"},
                {"variable": "usage_purpose", "term": "residential"}
            ],
            "conclusion": "preferential",
            "weight": 1.0,
            "description": "Giá trị thấp và sử dụng để ở thường hưởng thuế suất ưu đãi."
        },
        {
            "module": "tax",
            "name": "Tax Rule 2 - High Value Commercial",
            "conditions": [
                {"variable": "land_value", "term": "high"},
                {"variable": "usage_purpose", "term": "commercial"}
            ],
            "conclusion": "high_tax",
            "weight": 1.0,
            "description": "Giá trị cao và mục đích thương mại chịu thuế suất cao."
        },
        {
            "module": "tax",
            "name": "Tax Rule 3 - Medium Value",
            "conditions": [
                {"variable": "land_value", "term": "medium"}
            ],
            "conclusion": "standard",
            "weight": 0.8,
            "description": "Giá trị trung bình áp dụng mức thuế phổ thông."
        }
    ]

    for r in tax_rules:
        Rule.create(
            module=r["module"],
            name=r["name"],
            conditions=r["conditions"],
            conclusion=r["conclusion"],
            weight=r["weight"],
            description=r["description"]
        )
    
    print(f"Successfully seeded {len(tax_rules)} tax rules.")

if __name__ == "__main__":
    seed_tax_rules()
