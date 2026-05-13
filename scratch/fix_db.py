import sqlite3
import time

def fix_db():
    try:
        conn = sqlite3.connect('data/legal_expert.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password_hash='ca6bbfc6063ae623cbba4dc7c3ee5d866a51a5774ac98979964a8e8b594102ad' WHERE username='admin'")
        cursor.execute("UPDATE users SET password_hash='7cedeb1bb94fbfa8c9c0f9aadf7fd183c8793d46e1842aa711b080b0b7a7c3a1' WHERE username='staff01'")
        cursor.execute("UPDATE users SET password_hash='02351f85713eb01f1b148b76b14d0fc787cccf4bcd37f48d3abd9955b4791240' WHERE username='expert01'")
        conn.commit()
        conn.close()
        print('Updated live database successfully!')
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    # Add a little sleep to allow WAL to process if needed
    fix_db()
