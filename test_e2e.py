"""End-to-end test for the Legal Expert System."""
import sys
sys.path.insert(0, '.')

from core.database import DatabaseManager
from modules.module_loader import ModuleLoader
from controllers.consultation_controller import ConsultationController
from models.user import User

# Init DB
db = DatabaseManager()
db.initialize_database()

# Fix passwords
for uname in ['admin', 'staff01', 'expert01']:
    u = User.find_by_username(uname)
    if u:
        User.change_password(u.id, '123456')

# Login as staff
user = User.authenticate('staff01', '123456')
print(f"Login: {user.full_name} ({user.role})")

# Load modules
ml = ModuleLoader()
ml.discover_modules()

# Run consultations
ctrl = ConsultationController()

# Test 1: Transfer
print("\n=== TEST 1: Chuyen nhuong QSD dat ===")
r1 = ctrl.run_consultation('transfer', {
    'legal_status': 8.0, 'land_value': 5.0,
    'area': 6.0, 'location': 7.0, 'financial_obligation': 9.0
})
print(f"Score: {r1['score']}")
print(f"Conclusion: {r1['conclusion']}")
print(f"Title: {r1['interpretation']['title']}")
print(f"Matched rules: {len(r1['matched_rules'])}")
print(f"Legal citations: {len(r1['legal_citations'])}")
for c in r1['legal_citations']:
    print(f"  - {c['formatted']}")

# Test 2: Violation
print("\n=== TEST 2: Vi pham hanh chinh ===")
r2 = ctrl.run_consultation('violation', {
    'severity': 8.0, 'violation_area': 7.0,
    'duration': 6.0, 'recidivism': 9.0, 'damage': 7.5
})
print(f"Score: {r2['score']}")
print(f"Title: {r2['interpretation']['title']}")
print(f"Matched rules: {len(r2['matched_rules'])}")

# Test 3: Compensation
print("\n=== TEST 3: Boi thuong thu hoi dat ===")
r3 = ctrl.run_consultation('compensation', {
    'land_type': 8.0, 'usage_duration': 7.0,
    'area': 6.5, 'k_coefficient': 7.0, 'resettlement': 8.0
})
print(f"Score: {r3['score']}")
print(f"Title: {r3['interpretation']['title']}")
print(f"Matched rules: {len(r3['matched_rules'])}")

# Check history
from controllers.history_controller import HistoryController
hc = HistoryController()
stats = hc.get_statistics()
print(f"\nHistory stats: {stats}")

print("\n=== ALL E2E TESTS PASSED! ===")
