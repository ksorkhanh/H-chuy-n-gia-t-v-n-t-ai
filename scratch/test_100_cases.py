import sys
import os
import random
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import DatabaseManager
from core.auth import AuthService
from controllers.consultation_controller import ConsultationController
from models.user import User

def run_test_suite():
    print("Starting automated test suite (100 cases)...")
    
    # Initialize DB
    db = DatabaseManager()
    db.reset_database()
    
    # Mock login as admin
    auth = AuthService()
    admin_user = User.find_by_username("admin")
    if admin_user:
        auth.login(admin_user.to_dict())
    
    controller = ConsultationController()
    controller.module_loader.discover_modules()
    modules = controller.get_available_modules()
    
    if not modules:
        print("No modules found!")
        return

    results_file = "test_results_100.txt"
    with open(results_file, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"BÁO CÁO KIỂM THỬ HỆ THỐNG CHUYÊN GIA (100 TRƯỜNG HỢP)\n")
        f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        total_cases = 100
        cases_per_module = total_cases // len(modules)
        
        case_count = 0
        for mod_info in modules:
            mod_name = mod_info['name']
            mod_display = mod_info['display_name']
            f.write(f"\n>>> MODULE: {mod_display.upper()} ({mod_name})\n")
            f.write("-" * 50 + "\n")
            
            fields = controller.get_input_fields(mod_name)
            
            for i in range(cases_per_module):
                case_count += 1
                # Generate random inputs
                inputs = {}
                for field in fields:
                    # Generate values in range [min, max] with step
                    min_val = field.get('min', 0)
                    max_val = field.get('max', 10)
                    step = field.get('step', 0.5)
                    
                    # Number of steps
                    num_steps = int((max_val - min_val) / step)
                    random_step = random.randint(0, num_steps)
                    val = min_val + (random_step * step)
                    inputs[field['name']] = val
                
                # Run consultation
                result = controller.run_consultation(mod_name, inputs)
                
                if "error" in result:
                    f.write(f"CASE {case_count}: LỖI - {result['error']}\n")
                    continue
                
                interp = result.get('interpretation', {})
                f.write(f"CASE {case_count:03d}:\n")
                f.write(f"  Inputs: {json.dumps(inputs, ensure_ascii=False)}\n")
                f.write(f"  Score:  {result['score']:.1f} / 100\n")
                f.write(f"  Result: {interp.get('title', 'N/A')}\n")
                f.write(f"  Rules:  {len(result.get('matched_rules', []))} rules fired\n")
                f.write("-" * 30 + "\n")
                
                if case_count % 10 == 0:
                    print(f"Processed {case_count}/{total_cases} cases...")

        f.write("\n" + "=" * 80 + "\n")
        f.write("KẾT THÚC KIỂM THỬ\n")
        f.write("=" * 80 + "\n")

    print(f"Test completed. Results saved to {results_file}")

if __name__ == "__main__":
    run_test_suite()
