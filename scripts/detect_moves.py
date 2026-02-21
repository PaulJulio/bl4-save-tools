import yaml
import sys
import os
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bank_report import decrypt_profile, find_profile_save, get_user_info_from_path, find_save_directory, bit_pack_decode, to_bits, get_stats
import blcrypt

class CustomLoader(yaml.SafeLoader):
    def construct_python_tuple(self, node):
        return tuple(self.construct_sequence(node))

CustomLoader.add_constructor('tag:yaml.org,2002:python/tuple', CustomLoader.construct_python_tuple)

def detect_moves():
    path = find_profile_save()
    yaml_bytes = decrypt_profile(path)
    profile_data = yaml.safe_load(yaml_bytes)
    bank = profile_data.get('domains', {}).get('local', {}).get('shared', {}).get('inventory', {}).get('items', {}).get('bank', {})
    
    save_dir = find_save_directory()
    vex_save = next(save_dir.rglob("2.sav"), None)
    user_id, platform = get_user_info_from_path(vex_save)
    vex_yaml_bytes = blcrypt.decrypt_sav_to_yaml(vex_save, user_id, platform)
    vex_data = yaml.safe_load(vex_yaml_bytes)
    backpack = vex_data.get('state', {}).get('inventory', {}).get('items', {}).get('backpack', {})

    bank_cid_155 = []
    for item in bank.values():
        serial = item.get('serial', '')
        tc, cid, bits = get_stats(serial)
        if cid == 155:
            bank_cid_155.append(bits)
    
    vex_cid_155 = []
    for item in backpack.values():
        if isinstance(item, dict):
            serial = item.get('serial', '')
            tc, cid, bits = get_stats(serial)
            if cid == 155:
                vex_cid_155.append(bits)

    print(f"--- Bits 64-128 for No Firmware Enhancements ({len(vex_cid_155)}) ---")
    for b in vex_cid_155:
        print(b[64:128])

    print(f"\n--- Bits 64-128 for With Firmware Enhancements (First 10 of {len(bank_cid_155)}) ---")
    for b in bank_cid_155[:10]:
        print(b[64:128])

if __name__ == "__main__":
    detect_moves()
