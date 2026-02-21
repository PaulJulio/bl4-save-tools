import yaml
import sys
import os
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bank_report import decrypt_profile, find_profile_save, get_user_info_from_path, find_save_directory
import blcrypt

def capture_baseline():
    print("--- Capturing Baseline State ---")
    
    # 1. Capture Bank Baseline
    path = find_profile_save()
    if not path:
        print("Error: profile.sav not found.")
        return
        
    yaml_bytes = decrypt_profile(path)
    profile_data = yaml.safe_load(yaml_bytes)
    bank = profile_data.get('domains', {}).get('local', {}).get('shared', {}).get('inventory', {}).get('items', {}).get('bank', {})
    bank_serials = [item.get('serial') for item in bank.values() if item.get('serial')]
    
    with open("baseline_bank.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"serials": bank_serials}, f)
    print(f"Captured {len(bank_serials)} bank serials to baseline_bank.yaml")

    # 2. Capture Vex Baseline (2.sav)
    save_dir = find_save_directory()
    if not save_dir:
        print("Error: Save directory not found.")
        return

    # Look for 2.sav recursively from the found root
    vex_save = next(save_dir.rglob("2.sav"), None)
        
    if vex_save:
        print(f"Found Vex save at: {vex_save}")
        user_id, platform = get_user_info_from_path(vex_save)
        vex_yaml_bytes = blcrypt.decrypt_sav_to_yaml(vex_save, user_id, platform)
        vex_data = yaml.safe_load(vex_yaml_bytes)
        
        equipped = vex_data.get('state', {}).get('inventory', {}).get('equipped_inventory', {}).get('equipped', {})
        vex_equipped_serials = {}
        for slot, items in equipped.items():
            if items:
                vex_equipped_serials[slot] = items[0].get('serial')
        
        with open("baseline_vex.yaml", "w", encoding="utf-8") as f:
            yaml.dump({"equipped": vex_equipped_serials}, f)
        print(f"Captured Vex equipped baseline to baseline_vex.yaml")
    else:
        print("Warning: Vex save (2.sav) not found.")

if __name__ == "__main__":
    capture_baseline()
