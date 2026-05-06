"""
Reset passwords for default accounts to '123456'.
"""
import sys
sys.path.insert(0, '.')
from models.user import User
from core.database import DatabaseManager

def reset_passwords():
    db = DatabaseManager()
    db.initialize_database()
    
    accounts = ['admin', 'staff01', 'expert01']
    for username in accounts:
        user = User.find_by_username(username)
        if user:
            User.change_password(user.id, '123456')
            print(f"Password for '{username}' reset to '123456'")
        else:
            print(f"User '{username}' not found.")

if __name__ == "__main__":
    reset_passwords()
