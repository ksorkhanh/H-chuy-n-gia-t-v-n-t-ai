import sqlite3
import json
import os

db_path = r'd:\STUDY\23AI VKU 2023-2028\Semester 6 VKU\Hệ Chuyên Gia\JOB_01\data\legal_expert.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("DELETE FROM rules WHERE module = 'tax'")
    
    new_rules = [
        ('tax', 'R1_Tax_Preferential', json.dumps([{"variable":"location_type","term":"remote"},{"variable":"area_size","term":"within_limit"}]), 'preferential', 1.0, 1, 'Đất vùng sâu vùng xa, trong hạn mức -> Thuế ưu đãi'),
        ('tax', 'R2_Tax_Standard_Res', json.dumps([{"variable":"usage_purpose","term":"residential"},{"variable":"location_type","term":"rural"}]), 'standard', 0.9, 1, 'Đất ở nông thôn -> Tiêu chuẩn'),
        ('tax', 'R3_Tax_Standard_Urb', json.dumps([{"variable":"usage_purpose","term":"residential"},{"variable":"location_type","term":"urban"},{"variable":"area_size","term":"within_limit"}]), 'standard', 0.8, 1, 'Đất ở đô thị trong hạn mức -> Tiêu chuẩn'),
        ('tax', 'R4_Tax_High_OverLimit', json.dumps([{"variable":"usage_purpose","term":"residential"},{"variable":"area_size","term":"over_limit"}]), 'high_tax', 0.9, 1, 'Đất ở vượt hạn mức -> Thuế cao lũy tiến'),
        ('tax', 'R5_Tax_High_Com_Urb', json.dumps([{"variable":"usage_purpose","term":"commercial"},{"variable":"location_type","term":"urban"}]), 'high_tax', 1.0, 1, 'Đất thương mại đô thị -> Rất cao'),
        ('tax', 'R6_Tax_Med_Com_Rur', json.dumps([{"variable":"usage_purpose","term":"commercial"},{"variable":"location_type","term":"rural"}]), 'standard', 0.9, 1, 'Đất thương mại nông thôn -> Tiêu chuẩn (tương đối cao)'),
        ('tax', 'R7_Tax_High_Value_Urban', json.dumps([{"variable":"land_value","term":"high"},{"variable":"location_type","term":"urban"}]), 'high_tax', 1.0, 1, 'Đất giá trị cao ở đô thị -> Thuế cao'),
        ('tax', 'R8_Tax_Low_Value_Remote', json.dumps([{"variable":"land_value","term":"low"},{"variable":"location_type","term":"remote"}]), 'preferential', 0.9, 1, 'Đất giá trị thấp ở vùng sâu -> Ưu đãi')
    ]

    for rule in new_rules:
        cursor.execute("INSERT INTO rules (module, name, condition_json, conclusion, weight, legal_article_id, description) VALUES (?, ?, ?, ?, ?, ?, ?)", rule)

    conn.commit()
    print("Updated tax rules successfully in rules table.")
except Exception as e:
    print(f"Failed to update rules table: {e}")

conn.close()
