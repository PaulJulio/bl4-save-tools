import os
import yaml
import struct
import zlib
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from discovery import find_save_directory
from blcrypt import decrypt_sav_to_yaml

@dataclass
class ItemStats:
    primary_stat: Optional[int] = None
    secondary_stat: Optional[int] = None
    level: Optional[int] = None
    rarity: Optional[int] = None
    manufacturer: Optional[int] = None
    item_class: Optional[int] = None
    flags: Optional[List[int]] = None

@dataclass
class DecodedItem:
    serial: str
    item_type: str
    item_category: str
    length: int
    stats: ItemStats
    raw_fields: Dict[str, Union[int, List[int]]]
    confidence: str

def bit_pack_decode(serial: str) -> bytes:
    """
    Decodes the 6-bit packed serial format used in BL4.
    """
    if serial.startswith('@Ug'):
        payload = serial[3:]
    elif serial.startswith('@U'):
        payload = serial[2:]
    else:
        payload = serial

    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=!$%&*()[]{}~`^_<>?#;'
    char_map = {c: i for i, c in enumerate(chars)}

    bits = []
    for c in payload:
        if c in char_map:
            val = char_map[c]
            bits.extend(format(val, '06b'))

    bit_string = ''.join(bits)
    # Ensure bit string length is multiple of 8
    bit_string = bit_string[:(len(bit_string) // 8) * 8]

    byte_data = bytearray()
    for i in range(0, len(bit_string), 8):
        byte_val = int(bit_string[i:i+8], 2)
        byte_data.append(byte_val)

    return bytes(byte_data)

def extract_fields(data: bytes) -> Dict[str, Union[int, List[int]]]:
    fields = {}

    if len(data) >= 4:
        fields['header_le'] = struct.unpack('<I', data[:4])[0]
        fields['header_be'] = struct.unpack('>I', data[:4])[0]

    stats_16 = []
    for i in range(0, min(len(data)-1, 20), 2):
        val16 = struct.unpack('<H', data[i:i+2])[0]
        fields[f'val16_at_{i}'] = val16
        if 100 <= val16 <= 10000:
            stats_16.append((i, val16))

    fields['potential_stats'] = stats_16

    flags = []
    for i in range(min(len(data), 20)):
        byte_val = data[i]
        fields[f'byte_{i}'] = byte_val
        if byte_val < 100:
            flags.append((i, byte_val))

    fields['potential_flags'] = flags

    return fields

def decode_weapon(data: bytes, serial: str) -> DecodedItem:
    fields = extract_fields(data)
    stats = ItemStats()

    if 'val16_at_0' in fields:
        stats.primary_stat = fields['val16_at_0']
    if 'val16_at_12' in fields:
        stats.secondary_stat = fields['val16_at_12']
    if 'byte_4' in fields:
        stats.manufacturer = fields['byte_4']
    if 'byte_8' in fields:
        stats.item_class = fields['byte_8']
    if 'byte_1' in fields:
        stats.rarity = fields['byte_1']
    if 'byte_13' in fields:
        stats.level = fields['byte_13']

    return DecodedItem(
        serial=serial,
        item_type='r',
        item_category='Weapon',
        length=len(data),
        stats=stats,
        raw_fields=fields,
        confidence="high" if len(data) in [24, 26] else "medium"
    )

def decode_equipment_e(data: bytes, serial: str) -> DecodedItem:
    fields = extract_fields(data)
    stats = ItemStats()

    if 'val16_at_2' in fields:
        stats.primary_stat = fields['val16_at_2']
    if 'val16_at_8' in fields:
        stats.secondary_stat = fields['val16_at_8']
    if 'val16_at_10' in fields and len(data) > 38:
        stats.level = fields['val16_at_10']
    if 'byte_1' in fields:
        stats.manufacturer = fields['byte_1']
    if 'byte_3' in fields:
        stats.item_class = fields['byte_3']
    if 'byte_9' in fields:
        stats.rarity = fields['byte_9']

    return DecodedItem(
        serial=serial,
        item_type='e',
        item_category='Equipment',
        length=len(data),
        stats=stats,
        raw_fields=fields,
        confidence="high" if 'byte_1' in fields and fields['byte_1'] == 49 else "medium"
    )

def decode_equipment_d(data: bytes, serial: str) -> DecodedItem:
    fields = extract_fields(data)
    stats = ItemStats()

    if 'val16_at_4' in fields:
        stats.primary_stat = fields['val16_at_4']
    if 'val16_at_8' in fields:
        stats.secondary_stat = fields['val16_at_8']
    if 'val16_at_10' in fields:
        stats.level = fields['val16_at_10']
    if 'byte_5' in fields:
        stats.manufacturer = fields['byte_5']
    if 'byte_6' in fields:
        stats.item_class = fields['byte_6']
    if 'byte_14' in fields:
        stats.rarity = fields['byte_14']

    return DecodedItem(
        serial=serial,
        item_type='d',
        item_category='Equipment (Alt)',
        length=len(data),
        stats=stats,
        raw_fields=fields,
        confidence="high" if 'byte_5' in fields and fields['byte_5'] == 15 else "medium"
    )

def decode_item_serial(serial: str) -> DecodedItem:
    try:
        data = bit_pack_decode(serial)

        if len(serial) >= 4 and serial.startswith('@Ug'):
            item_type = serial[3]
        else:
            item_type = '?'

        if item_type == 'r':
            return decode_weapon(data, serial)
        elif item_type == 'e':
            return decode_equipment_e(data, serial)
        elif item_type == 'd':
            return decode_equipment_d(data, serial)
        else:
            fields = extract_fields(data)
            category_map = {
                'w': 'Weapon (Special)',
                'u': 'Utility',
                'f': 'Consumable',
                '!': 'Special'
            }
            return DecodedItem(
                serial=serial,
                item_type=item_type,
                item_category=category_map.get(item_type, 'Unknown'),
                length=len(data),
                stats=ItemStats(),
                raw_fields=fields,
                confidence="low"
            )
    except Exception as e:
        return DecodedItem(serial=serial, item_type='error', item_category='Error', length=0, stats=ItemStats(), raw_fields={}, confidence="none")

def find_profile_save():
    save_dir = find_save_directory()
    if not save_dir:
        return None
    for root, dirs, files in os.walk(save_dir):
        if "profile.sav" in files:
            return Path(root) / "profile.sav"
    return None

def get_user_info_from_path(sav_path: Path):
    user_id = sav_path.parent.parent.parent.name
    if user_id.isdigit() and len(user_id) >= 16:
        return user_id, "steam"
    else:
        return user_id, "epic"

def decrypt_profile(sav_path: Path):
    user_id, platform = get_user_info_from_path(sav_path)
    return decrypt_sav_to_yaml(sav_path, user_id, platform)

def extract_bank_serials(yaml_bytes: bytes):
    data = yaml.safe_load(yaml_bytes)
    if not data:
        return []
    try:
        bank = data['domains']['local']['shared']['inventory']['items']['bank']
        if not bank:
            return []
        return [item['serial'] for item in bank.values() if isinstance(item, dict) and 'serial' in item]
    except (KeyError, TypeError):
        return []

def generate_bank_report(serials: list):
    report = {}
    for serial in serials:
        decoded = decode_item_serial(serial)
        cat = decoded.item_category
        if cat not in report:
            report[cat] = {"count": 0, "firmware_counts": {}}
        report[cat]["count"] += 1
        
        # Use primary_stat/manufacturer/rarity as a pseudo-firmware fingerprint
        stats = decoded.stats
        firmware_key = (stats.manufacturer, stats.rarity, stats.item_class)
        if firmware_key not in report[cat]["firmware_counts"]:
            report[cat]["firmware_counts"][firmware_key] = 0
        report[cat]["firmware_counts"][firmware_key] += 1
    return report

def main():
    print("--- Borderlands 4 Bank Reporter ---")
    path = find_profile_save()
    if not path:
        print("Error: Could not locate profile.sav.")
        return
    print(f"Loading profile from: {path}\n")
    try:
        yaml_bytes = decrypt_profile(path)
        serials = extract_bank_serials(yaml_bytes)
        if not serials:
            print("The shared bank is empty.")
            return
        report = generate_bank_report(serials)
        print(f"{'Gear Type':<20} | {'Count':<6} | {'Unique Combos':<15} | {'Notes'}")
        print("-" * 75)
        for cat in sorted(report.keys()):
            data = report[cat]
            count = data["count"]
            unique = len(data["firmware_counts"])
            excessive = [f"{v}x duplicates!" for v in data["firmware_counts"].values() if v > 3]
            notes = ", ".join(excessive)
            print(f"{cat:<20} | {count:<6} | {unique:<15} | {notes}")
    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    main()
