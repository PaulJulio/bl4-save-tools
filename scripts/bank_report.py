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

# Definitive Ground Truth Signatures (tc, mid, cid, prefix, header_6)
GT_CLASSMOD = {('!', 72, 109, '8348', 'G'), ('!', 72, 110, '8348', 'G'), ('!', 72, 111, '8348', 'G'), ('#', 179, 109, 'A5B3', 'K'), ('#', 179, 111, 'A5B3', 'K'), ('e', 192, 155, '7BC0', 'm')}
GT_REPKIT = {('e', 196, 155, '7BC4', 'r'), ('e', 199, 155, '7BC7', 'v'), ('e', 202, 230, '7BCA', '%')}
GT_ENHANCEMENT = {('e', 195, 155, '7BC3', 'q'), ('e', 197, 155, '7BC5', 's'), ('e', 200, 38, '7BC8', '&'), ('e', 202, 230, '7BCA', ')'), ('e', 203, 77, '7BCB', '#'), ('e', 203, 205, '7BCB', '!'), ('e', 223, 77, '7BDF', '>'), ('e', 49, 11, '7A31', '0'), ('b', 89, 139, '6D59', 'r'), ('f', 136, 22, '7C88', '4')}
GT_SHIELD = {('e', 201, 77, '7BC9', '+'), ('e', 208, 205, '7BD0', '?'), ('e', 221, 205, '7BDD', '<'), ('r', 18, 6, 'AE11', 'O'), ('r', 30, 7, 'AE11', 'O'), ('r', 30, 29, 'AE11', 'O'), ('r', 30, 75, 'AE11', 'O'), ('r', 30, 153, 'AE11', 'O'), ('r', 252, 2, 'AE15', 'H'), ('r', 252, 83, 'AE15', 'H'), ('r', 252, 83, 'AE1A', 'c'), ('r', 252, 114, 'AE15', 'H'), ('r', 252, 141, 'AE15', 'H'), ('r', 252, 146, 'AE1A', 'c'), ('r', 252, 158, 'AE15', 'J'), ('r', 252, 175, 'AE1A', 'c'), ('r', 252, 182, 'AE1A', 'c'), ('r', 252, 183, 'AE15', 'H'), ('r', 252, 183, 'AE1A', 'c'), ('r', 252, 184, 'AE15', 'J'), ('r', 252, 185, 'AE15', 'H'), ('r', 252, 186, 'AE15', 'H'), ('r', 252, 186, 'AE1A', 'c'), ('r', 252, 187, 'AE15', 'H'), ('r', 252, 189, 'AE15', 'J'), ('r', 252, 190, 'AE15', 'J'), ('r', 252, 191, 'AE15', 'J'), ('r', 252, 192, 'AE1A', 'c'), ('r', 252, 193, 'AE1A', 'c'), ('r', 252, 203, 'AE15', 'H'), ('r', 252, 203, 'AE15', 'J'), ('r', 252, 203, 'AE1A', 'c'), ('r', 252, 208, 'AE15', 'J'), ('r', 252, 209, 'AE15', 'J'), ('r', 252, 209, 'AE1A', 'c'), ('r', 252, 210, 'AE15', 'H'), ('r', 252, 210, 'AE15', 'J'), ('r', 252, 210, 'AE1A', 'c'), ('r', 252, 211, 'AE15', 'J'), ('r', 252, 213, 'AE1A', 'c'), ('r', 252, 214, 'AE1A', 'c'), ('r', 252, 219, 'AE1A', 'c'), ('r', 252, 220, 'AE15', 'J'), ('r', 252, 221, 'AE1A', 'c'), ('r', 254, 75, 'AE14', 'L'), ('r', 254, 91, 'AE14', 'L'), ('r', 254, 92, 'AE14', 'L'), ('r', 254, 95, 'AE14', 'L'), ('r', 254, 97, 'AE14', 'L'), ('r', 254, 104, 'AE14', 'L'), ('r', 254, 105, 'AE14', 'L'), ('r', 254, 106, 'AE14', 'L'), ('r', 254, 107, 'AE14', 'L'), ('r', 252, 219, 'AE15', 'H'), ('r', 252, 215, 'AE15', 'H')}
GT_GRENADE = {('e', 197, 155, '7BC5', 't'), ('e', 198, 155, '7BC6', 'u'), ('e', 200, 155, '7BC8', 'x'), ('e', 202, 102, '7BCA', '*'), ('r', 252, 114, 'AE18', 'X'), ('r', 252, 165, 'AE18', 'X'), ('r', 252, 175, 'AE12', '9'), ('r', 252, 182, 'AE12', '9'), ('r', 252, 183, 'AE12', '9'), ('r', 252, 183, 'AE18', 'X'), ('r', 252, 185, 'AE12', '9'), ('r', 252, 187, 'AE18', 'X'), ('r', 252, 189, 'AE18', 'X'), ('r', 252, 192, 'AE18', 'X'), ('r', 252, 193, 'AE12', '9'), ('r', 252, 195, 'AE12', '9'), ('r', 252, 208, 'AE12', '9'), ('r', 252, 210, 'AE12', '9'), ('r', 252, 213, 'AE12', '9'), ('r', 252, 214, 'AE12', '9'), ('r', 252, 215, 'AE12', '9'), ('r', 252, 216, 'AE12', 'B'), ('r', 252, 219, 'AE12', 'B'), ('r', 252, 221, 'AE12', '9'), ('r', 252, 221, 'AE12', 'B'), ('r', 254, 90, 'AE14', 'N'), ('r', 254, 91, 'AE14', 'N'), ('r', 254, 92, 'AE14', 'N'), ('r', 254, 93, 'AE14', 'N'), ('r', 254, 94, 'AE14', 'N'), ('r', 254, 95, 'AE14', 'N'), ('r', 254, 101, 'AE14', 'N'), ('r', 254, 106, 'AE14', 'N'), ('r', 254, 107, 'AE14', 'N'), ('r', 254, 108, 'AE14', 'N'), ('r', 254, 110, 'AE14', 'N'), ('r', 254, 166, 'AE14', 'N'), ('r', 254, 169, 'AE14', 'N'), ('r', 254, 204, 'AE14', 'N')}
GT_HEAVY = {('e', 202, 155, '7BCA', 'z'), ('r', 252, 110, 'AE13', 'E'), ('r', 252, 173, 'AE13', 'E'), ('r', 252, 185, 'AE13', 'E'), ('r', 252, 186, 'AE13', 'E'), ('r', 252, 192, 'AE14', 'F'), ('r', 252, 203, 'AE13', 'E'), ('r', 252, 203, 'AE14', 'F'), ('r', 252, 213, 'AE14', 'F'), ('r', 252, 214, 'AE14', 'F'), ('r', 252, 215, 'AE14', 'F'), ('r', 252, 219, 'AE13', 'E'), ('r', 254, 91, 'AE14', 'M'), ('r', 254, 93, 'AE14', 'M'), ('r', 254, 114, 'AE14', 'M')}

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

# Detailed firmware signatures from docs/firmware_research.md
FIRMWARE_SIGNATURES = {
    "Action Fist": "0111100101110010111000001" + "000001" + "1011101100",
    "Atlas Infinum": "0111100101110010111000001" + "000001" + "1000001100",
    "Gadget Ahoy": "0111100101110010111000001" + "000001" + "01111010100110001100",
    "Heating Up": "0111100101110010111000001" + "000001" + "1101010100",
    "Jacked": "0111100101110010111000001" + "000001" + "1011101001",
    "Oscar Mike": "0111100101110010111000001" + "000001" + "01110010100011010000",
    "Risky Boots": "0111100101110010111000001" + "000001" + "1001011000",
    "Trickshot": "0111100101110010111000001" + "000001" + "1011101011",
    "Dead Eye": "01111001011100101110000",
    "Get Throwin'": "111100101110010111000001" + "000001" + "0110101100",
    "Reel Big Fist": "111100101110010111000001" + "000001" + "0110110001",
    "Rubberband Man": "111100101110010111000001" + "000001" + "0111110110",
    "Daed-dy O'": "111100101110010111000001" + "000001" + "0111111010",
    "Bullets to Spare": "111100101110010111000001",
    "Atlas E.X.": "00111100101110010111000001" + "000001" + "1010100011",
    "God Killer": "00111100101110010111000001" + "000001" + "1010110101",
    "Lifeblood": "00111100101110010111000001" + "000001" + "0101011110",
    "Baker": "001101100010000010001100" + "1100" + "1010101000",
    "GooJFC": "001101100010000010001100" + "1100" + "1010101111",
    "High Caliber": "001101100010000010001100" + "1100" + "0100000110"
}

def get_item_info(serial: str):
    bits = bit_pack_decode(serial)
    db = bytearray()
    for i in range(0, (len(bits) // 8) * 8, 8):
        db.append(int(bits[i:i+8], 2))
    
    type_char = serial[3] if len(serial) > 3 else '?'
    header_6 = serial[6] if len(serial) > 6 else ''
    mid_idx = 4 if type_char == 'r' else 1
    manuf_id = db[mid_idx] if len(db) > mid_idx else None
    cid_idx = 8 if type_char == 'r' else 3
    class_id = db[cid_idx] if len(db) > cid_idx else None
    prefix = db[:2].hex().upper() if len(db) >= 2 else ""
    
    # Signature (Type, MID, CID, Prefix, Header_6)
    sig_5 = (type_char, manuf_id, class_id, prefix, header_6)
    
    category = "Weapon"
    fw_name = None
    has_fw = False

    # 1. Definitive Ground Truth Match
    if sig_5 in GT_CLASSMOD: category = "Class Mod"; has_fw = True
    elif sig_5 in GT_REPKIT: category = "Repkit"; has_fw = True
    elif sig_5 in GT_ENHANCEMENT: category = "Enhancement"; has_fw = True
    elif sig_5 in GT_SHIELD: category = "Shield"; has_fw = True
    elif sig_5 in GT_GRENADE: category = "Grenade Ordnance"
    elif sig_5 in GT_HEAVY: category = "Heavy Weapon Ordnance"
    
    # 2. NO FALLBACKS ALLOWED. Everything else is a Weapon.

    # Firmware Logic
    if category != "Weapon":
        for name, pattern in FIRMWARE_SIGNATURES.items():
            if pattern in bits:
                fw_name = name
                has_fw = True
                break
                
        if not fw_name:
            for family, pattern in FIRMWARE_PATTERNS.items():
                if pattern in bits:
                    fw_name = family
                    has_fw = True
                    break
        
        if not has_fw and len(db) > 1 and (db[1] & 0x0F) >= 13:
            has_fw = True

    return category, fw_name if fw_name else (has_fw)

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
            category, fw_info = get_item_info(serial)
            if category not in report: report[category] = {"total": 0, "fw": {}}
            report[category]["total"] += 1
            if fw_info:
                fw_name = fw_info if isinstance(fw_info, str) else "Generic Firmware"
                if fw_name not in report[category]["fw"]:
                    report[category]["fw"][fw_name] = 0
                report[category]["fw"][fw_name] += 1

        print(f"{'Category':<30} | {'Total':<6} | {'Firmware Breakdown'}")
        print("-" * 80)
        order = ["Grenade Ordnance", "Heavy Weapon Ordnance", "Shield", "Class Mod", "Repkit", "Enhancement", "Weapon"]
        for cat in order:
            if cat in report:
                d = report[cat]
                fw_summary = ", ".join([f"{name}: {count}" for name, count in sorted(d["fw"].items())])
                if not fw_summary: fw_summary = "None"
                print(f"{cat:<30} | {d['total']:<6} | {fw_summary}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
