import yaml
import sys
import os
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bank_report import decrypt_profile, find_profile_save, get_user_info_from_path, find_save_directory
import blcrypt

def capture_reference(category_name):
    print(f"--- Capturing Reference State for {category_name} ---")
    
    # 1. Capture Bank
    path = find_profile_save()
    if not path:
        print("Error: profile.sav not found.")
        return
        
    yaml_bytes = decrypt_profile(path)
    profile_data = yaml.safe_load(yaml_bytes)
    bank = profile_data.get('domains', {}).get('local', {}).get('shared', {}).get('inventory', {}).get('items', {}).get('bank', {})
    
    bank_items = []
    for slot, item in bank.items():
        if isinstance(item, dict) and item.get('serial'):
            bank_items.append({
                "serial": item.get('serial'),
                "flags": item.get('state_flags', 0)
            })
    
    bank_filename = f"reference_bank_{category_name}.yaml"
    with open(bank_filename, "w", encoding="utf-8") as f:
        yaml.dump({"items": bank_items, "description": f"Bank state while {category_name} is in Vex inventory"}, f)
    print(f"Captured {len(bank_items)} bank items to {bank_filename}")

    # 2. Capture Vex Inventory (2.sav)
    save_dir = find_save_directory()
    if not save_dir:
        print("Error: Save directory not found.")
        return

    vex_save = next(save_dir.rglob("2.sav"), None)
        
    if vex_save:
        print(f"Found Vex save at: {vex_save}")
        user_id, platform = get_user_info_from_path(vex_save)
        vex_yaml_bytes = blcrypt.decrypt_sav_to_yaml(vex_save, user_id, platform)
        vex_data = yaml.safe_load(vex_yaml_bytes)
        
        inventory = vex_data.get('state', {}).get('inventory', {})
        vex_items = []
        
        # Capture Equipped
        equipped_inventory = inventory.get('equipped_inventory', {})
        if equipped_inventory is None: equipped_inventory = {}
        equipped = equipped_inventory.get('equipped', {})
        if equipped is None: equipped = {}
        
        for slot, item_list in equipped.items():
            if isinstance(item_list, list) and len(item_list) > 0:
                s = item_list[0].get('serial')
                f = item_list[0].get('state_flags', 0)
                if s: vex_items.append({"serial": s, "flags": f})
        
        # Capture Backpack
        items = inventory.get('items', {})
        if isinstance(items, dict):
            backpack = items.get('backpack', {})
            if isinstance(backpack, dict):
                for slot, item in backpack.items():
                    if isinstance(item, dict) and item.get('serial'):
                        vex_items.append({
                            "serial": item.get('serial'),
                            "flags": item.get('state_flags', 0)
                        })
        
        vex_filename = f"reference_vex_{category_name}.yaml"
        with open(vex_filename, "w", encoding="utf-8") as f:
            yaml.dump({"items": vex_items, "description": f"Vex inventory containing {category_name}"}, f)
        print(f"Captured {len(vex_items)} items from Vex to {vex_filename}")
    else:
        print("Warning: Vex save (2.sav) not found.")

if __name__ == "__main__":
    cat = sys.argv[1] if len(sys.argv) > 1 else "misc"
    capture_reference(cat)
