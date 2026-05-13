import sqlite3
import json

def add_tax_rules():
    conn = sqlite3.connect('data/legal_expert.db')
    cursor = conn.cursor()
    
    # Check if tax rules exist
    cursor.execute("SELECT COUNT(*) FROM rules WHERE module='tax'")
    if cursor.fetchone()[0] == 0:
        rules = [
            ('tax', 'R1_Tax_LowRes', json.dumps([{"variable":"land_value","term":"low"},{"variable":"usage_purpose","term":"residential"}]), 'preferential', 1.0, 1, 'Đất ở khu vực giá thấp -> Ưu đãi'),
            ('tax', 'R2_Tax_MedRes', json.dumps([{"variable":"land_value","term":"medium"},{"variable":"usage_purpose","term":"residential"}]), 'standard', 1.0, 1, 'Đất ở khu vực giá trung bình -> Tiêu chuẩn'),
            ('tax', 'R3_Tax_HighRes', json.dumps([{"variable":"land_value","term":"high"},{"variable":"usage_purpose","term":"residential"}]), 'standard', 0.8, 1, 'Đất ở trung tâm -> Tiêu chuẩn'),
            ('tax', 'R4_Tax_LowCom', json.dumps([{"variable":"land_value","term":"low"},{"variable":"usage_purpose","term":"commercial"}]), 'standard', 0.9, 1, 'Đất thương mại ở quê -> Tiêu chuẩn'),
            ('tax', 'R5_Tax_MedCom', json.dumps([{"variable":"land_value","term":"medium"},{"variable":"usage_purpose","term":"commercial"}]), 'high_tax', 0.9, 1, 'Đất thương mại vừa -> Thuế cao'),
            ('tax', 'R6_Tax_HighCom', json.dumps([{"variable":"land_value","term":"high"},{"variable":"usage_purpose","term":"commercial"}]), 'high_tax', 1.0, 1, 'Đất thương mại trung tâm -> Rất cao')
        ]
        cursor.executemany("INSERT INTO rules (module, name, condition_json, conclusion, weight, legal_article_id, description) VALUES (?,?,?,?,?,?,?)", rules)
        conn.commit()
        print('Added tax rules to live DB')
    else:
        print('Tax rules already exist')
    
    conn.close()

if __name__ == '__main__':
    add_tax_rules()
