import yaml
import sys
import os
from pathlib import Path
from discovery import find_save_directory
from blcrypt import decrypt_sav_to_yaml

def find_profile_save():
    save_dir = find_save_directory()
    if not save_dir: return None
    for root, dirs, files in os.walk(save_dir):
        if "profile.sav" in files: return Path(root) / "profile.sav"
    return None

def decrypt_profile(sav_path: Path):
    user_id = sav_path.parent.parent.parent.name
    platform = "steam" if (user_id.isdigit() and len(user_id) >= 16) else "epic"
    return decrypt_sav_to_yaml(sav_path, user_id, platform)

def bit_pack_decode(serial: str) -> str:
    char_map = {c: i for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=!$%&*()[]{}~`^_<>?#;')}
    payload = serial[3:] if serial.startswith('@Ug') else (serial[2:] if serial.startswith('@U') else serial)
    bits = "".join([format(char_map[c], '06b') for c in payload if c in char_map])
    return bits

def get_stats(serial: str):
    bits = bit_pack_decode(serial)
    decoded_bytes = bytearray()
    for i in range(0, (len(bits) // 8) * 8, 8):
        decoded_bytes.append(int(bits[i:i+8], 2))
    type_char = serial[3] if len(serial) > 3 else '?'
    class_id = decoded_bytes[8] if type_char == 'r' and len(decoded_bytes) > 8 else (decoded_bytes[3] if type_char == 'e' and len(decoded_bytes) > 3 else None)
    manuf_id = decoded_bytes[4] if type_char == 'r' and len(decoded_bytes) > 4 else (decoded_bytes[1] if type_char == 'e' and len(decoded_bytes) > 1 else None)
    return type_char, class_id, manuf_id, len(bits)

def main():
    print("--- Borderlands 4 Definitive Bank Inventory Summary ---")
    path = find_profile_save()
    if not path: return
    try:
        yaml_bytes = decrypt_profile(path)
        data = yaml.safe_load(yaml_bytes)
        bank = data.get('domains', {}).get('local', {}).get('shared', {}).get('inventory', {}).get('items', {}).get('bank', {})
        
        report = {}
        for item in bank.values():
            serial = item.get('serial', '')
            tc, cid, mid, blen = get_stats(serial)
            
            category = "Other/Unknown"
            
            # 1. Enhancement (Target: 89)
            if tc == 'e' and cid == 155: category = "Enhancement"
            # 2. Energy Shield (Target: 40)
            elif tc == 'e' and cid == 77: category = "Energy Shield"
            # 3. Repkit (Target: 65)
            elif tc in ['!', 'f', 'b', '#'] or (tc == 'e' and cid == 230): category = "Repkit"
            # 4. Class Mod (Target: 79)
            elif tc in ['c', 'x', 'v', 'g', 'w', 'y', 'z', 'u'] or (tc == 'e' and cid in [205, 38, 102, 11]) or (tc == 'd'):
                category = "Class Mod"
            # 5. Ordnance, Armor Shields, and Weapons
            elif tc == 'r':
                # Grenade: 57
                if mid == 254 or (mid == 252 and cid and cid < 170): category = "Grenade Ordnance"
                # Armor Shield: 53
                elif mid == 252 and cid and cid in [185, 219, 213, 210, 203, 215, 209]: category = "Armor Shield"
                # Heavy Weapon: 18
                elif mid in [30, 18] or (mid == 252 and cid and cid in [175, 190, 189, 183, 193, 83, 187, 221, 220, 192, 214, 186, 216, 217, 181, 208, 211, 212, 218, 194]):
                    category = "Heavy Weapon Ordnance"
                else: category = "Weapon"
            
            if category not in report: report[category] = {"total": 0, "with_fw": 0}
            report[category]["total"] += 1
            # Length threshold for "Has Firmware"
            if category != "Weapon" and blen >= 200:
                report[category]["with_fw"] += 1

        print(f"{'Category':<30} | {'Total':<6} | {'With Firmware'}")
        print("-" * 55)
        # Order based on your requested categories
        order = ["Grenade Ordnance", "Heavy Weapon Ordnance", "Energy Shield", "Armor Shield", "Class Mod", "Repkit", "Enhancement", "Weapon"]
        for cat in order:
            if cat in report:
                d = report[cat]
                print(f"{cat:<30} | {d['total']:<6} | {d['with_fw']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
