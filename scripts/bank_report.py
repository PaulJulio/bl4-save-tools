import yaml
import sys
import os
from pathlib import Path
from discovery import find_save_directory
from blcrypt import decrypt_sav_to_yaml

# Firmware families from docs/firmware_research.md
FIRMWARE_PATTERNS = {
    "Family A": "0111100101110010111000001",
    "Family B": "111100101110010111000001",
    "Family C": "00111100101110010111000001",
    "Family D": "001101100010000010001100"
}

HEAVY_SIGNATURES = [
    ('e', 202, 155, '7BCA'), ('r', 252, 110, 'AE13'), ('r', 252, 155, 'AE13'),
    ('r', 252, 185, 'AE13'), ('r', 252, 186, 'AE13'), ('r', 252, 192, 'AE14'),
    ('r', 252, 203, 'AE13'), ('r', 252, 203, 'AE14'), ('r', 252, 213, 'AE14'),
    ('r', 252, 214, 'AE14'), ('r', 252, 215, 'AE14'), ('r', 252, 219, 'AE13'),
    ('r', 254, 91, 'AE14'), ('r', 254, 93, 'AE14'), ('r', 254, 114, 'AE14')
]

def bit_pack_decode(serial: str) -> str:
    char_map = {c: i for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=!$%&*()[]{}~`^_<>?#;')}
    payload = serial[3:] if serial.startswith('@Ug') else (serial[2:] if serial.startswith('@U') else serial)
    bits = "".join([format(char_map[c], '06b') for c in payload if c in char_map])
    return bits

def get_user_info_from_path(path: Path):
    user_id = path.parent.parent.parent.name
    platform = "steam" if (user_id.isdigit() and len(user_id) >= 16) else "epic"
    return user_id, platform

def find_profile_save():
    save_dir = find_save_directory()
    if not save_dir: return None
    for root, dirs, files in os.walk(save_dir):
        if "profile.sav" in files: return Path(root) / "profile.sav"
    return None

def decrypt_profile(sav_path: Path):
    user_id, platform = get_user_info_from_path(sav_path)
    return decrypt_sav_to_yaml(sav_path, user_id, platform)

def extract_bank_serials(decrypted_yaml: bytes):
    data = yaml.safe_load(decrypted_yaml)
    bank = data.get('domains', {}).get('local', {}).get('shared', {}).get('inventory', {}).get('items', {}).get('bank', {})
    return [item.get('serial', '') for item in bank.values() if isinstance(item, dict) and item.get('serial')]

def get_item_info(serial: str):
    bits = bit_pack_decode(serial)
    db = bytearray()
    for i in range(0, (len(bits) // 8) * 8, 8):
        db.append(int(bits[i:i+8], 2))
    
    type_char = serial[3] if len(serial) > 3 else '?'
    class_id = db[8] if type_char == 'r' and len(db) > 8 else (db[3] if type_char == 'e' and len(db) > 3 else None)
    manuf_id = db[4] if type_char == 'r' and len(db) > 4 else (db[1] if type_char == 'e' and len(db) > 1 else None)
    prefix = db[:2].hex().upper() if len(db) >= 2 else ""
    sig = (type_char, manuf_id, class_id, prefix)
    
    category = "Weapon"
    has_fw = any(p in bits for p in FIRMWARE_PATTERNS.values())
    
    # Specific fix for Repkit/ClassMod firmware reporting
    if has_fw:
        pass # Standard pattern match is good
    elif len(db) > 1 and (db[1] & 0x0F) >= 13:
        has_fw = True # Heuristic for unlocked firmware
    
    if sig in HEAVY_SIGNATURES:
        category = "Heavy Weapon Ordnance"
    elif type_char == 'r':
        if manuf_id == 30: category = "Heavy Weapon Ordnance"
        elif prefix == 'AE14' and manuf_id == 254:
            if len(bits) > 17 and bits[17] == '1': category = "Grenade Ordnance"
            else: category = "Heavy Weapon Ordnance"
        elif prefix in ['AE12', 'AE18']: category = "Grenade Ordnance"
        elif prefix in ['AE13', 'AE15', 'AE16', 'AE1A', 'AE1E', 'AE11']:
            if class_id in [185, 203, 209, 210, 213, 215, 219]: category = "Armor Shield"; has_fw = True
            elif class_id in [175, 181, 183, 83]: category = "Heavy Weapon Ordnance"
            else: category = "Weapon"
        else: category = "Weapon"
            
    elif type_char == 'e':
        if class_id == 77: category = "Energy Shield"; has_fw = True
        elif class_id == 155:
            if prefix in ['7BC5', '7BC6', '7BC8']: category = "Grenade Ordnance"
            else: category = "Enhancement"; has_fw = True
        elif class_id == 230: category = "Repkit"; has_fw = True
        elif class_id == 102:
            if prefix == '7BCA': category = "Grenade Ordnance"
            else: category = "Class Mod"; has_fw = True
        elif class_id in [205, 38, 11]: category = "Class Mod"; has_fw = True
            
    elif type_char in ['!', '#', 'b', 'f']:
        category = "Repkit"; has_fw = True
        
    elif type_char in ['c', 'd', 'g', 'v', 'w', 'x', 'y', 'z', 'u']:
        category = "Class Mod"; has_fw = True
            
    return category, has_fw

def main():
    print("--- Borderlands 4 Definitive Bank Inventory Summary ---")
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if path.suffix == '.yaml':
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
            items = data.get('items', [])
            if items: serials = [i['serial'] for i in items if i.get('serial')]
            else: serials = data.get('serials', [])
        else:
            yaml_bytes = decrypt_profile(path)
            serials = extract_bank_serials(yaml_bytes)
    else:
        path = find_profile_save()
        if not path: return
        yaml_bytes = decrypt_profile(path)
        serials = extract_bank_serials(yaml_bytes)
    
    try:
        report = {}
        for serial in serials:
            category, has_fw = get_item_info(serial)
            if category not in report: report[category] = {"total": 0, "with_fw": 0}
            report[category]["total"] += 1
            if has_fw: report[category]["with_fw"] += 1

        print(f"{'Category':<30} | {'Total':<6} | {'With Firmware'}")
        print("-" * 55)
        order = ["Grenade Ordnance", "Heavy Weapon Ordnance", "Energy Shield", "Armor Shield", "Class Mod", "Repkit", "Enhancement", "Weapon"]
        for cat in order:
            if cat in report:
                d = report[cat]
                print(f"{cat:<30} | {d['total']:<6} | {d['with_fw']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
