import yaml
import sys
import os
from pathlib import Path

sys.path.append('scripts')
from bank_report import get_user_info_from_path, find_save_directory
import blcrypt

def main():
    save_dir = find_save_directory()
    vex_save = next(save_dir.rglob("2.sav"), None)
    if not vex_save:
        print("2.sav not found")
        return
        
    user_id, platform = get_user_info_from_path(vex_save)
    yaml_bytes = blcrypt.decrypt_sav_to_yaml(vex_save, user_id, platform)
    data = yaml.safe_load(yaml_bytes)
    
    inv = data.get('state', {}).get('inventory', {})
    items = inv.get('items', {})
    backpack = items.get('backpack', {})
    print(f"Backpack type: {type(backpack)}")
    if isinstance(backpack, dict):
        print(f"Backpack slots: {len(backpack)}")
        if 'slot_0' in backpack:
            s0 = backpack['slot_0']
            print(f"Slot 0 type: {type(s0)}")
            print(f"Slot 0 value: {s0}")
            if isinstance(s0, dict):
                print(f"Slot 0 serial: {s0.get('serial')}")
            
if __name__ == "__main__":
    main()
