import os
import yaml
from pathlib import Path
from discovery import find_save_directory
from blcrypt import decrypt_sav_to_yaml

CUSTOM_B85_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~"

def custom_base85_decode(data: str) -> bytes:
    """
    Decodes a custom base85-encoded serial string into bytes.
    """
    if data.startswith('@U'):
        data = data[2:]
    data = data.replace('/', '|')
    
    pad_len = (5 - (len(data) % 5)) % 5
    data += CUSTOM_B85_ALPHABET[-1] * pad_len
    
    out = bytearray()
    for i in range(0, len(data), 5):
        chunk = data[i:i+5]
        acc = 0
        for c in chunk:
            acc = acc * 85 + CUSTOM_B85_ALPHABET.index(c)
        
        for j in range(3, -1, -1):
            out.append((acc >> (8 * j)) & 0xff)
            
    if pad_len:
        out = out[:-pad_len]
    return bytes(out)

def reverse_bits_in_byte(b: int) -> int:
    """
    Reverses the bit order in a single byte.
    """
    rev = 0
    for _ in range(8):
        rev = (rev << 1) | (b & 1)
        b >>= 1
    return rev

def bytes_to_binary_string(data: bytes) -> str:
    """
    Converts bytes to a binary string after reversing bits in each byte.
    """
    reversed_bytes = [reverse_bits_in_byte(b) for b in data]
    return "".join(bin(b)[2:].zfill(8) for b in reversed_bytes)

class BitReader:
    def __init__(self, binary_str: str):
        self.bits = binary_str
        self.pos = 0

    def read_bits(self, n: int) -> str:
        res = self.bits[self.pos : self.pos + n]
        self.pos += n
        return res

    def read_int(self, n: int) -> int:
        bits = self.read_bits(n)
        if not bits:
            return 0
        return int(bits[::-1], 2)

    def read_varint(self) -> int:
        res_bits = ""
        while True:
            chunk = self.read_bits(5)
            if len(chunk) < 5:
                break
            res_bits += chunk[:4]
            if chunk[4] == '0':
                break
        if not res_bits:
            return 0
        return int(res_bits[::-1], 2)

    def peek_bits(self, n: int) -> str:
        return self.bits[self.pos : self.pos + n]

def find_profile_save():
    """
    Locates the profile.sav file.
    """
    save_dir = find_save_directory()
    if not save_dir:
        return None
        
    for root, dirs, files in os.walk(save_dir):
        if "profile.sav" in files:
            return Path(root) / "profile.sav"
            
    return None

def get_user_info_from_path(sav_path: Path):
    """
    Extracts User ID and Platform from the save path.
    Expected structure: .../SaveGames/<user_id>/Profiles/client/profile.sav
    """
    user_id = sav_path.parent.parent.parent.name
    if user_id.isdigit() and len(user_id) >= 16:
        return user_id, "steam"
    else:
        return user_id, "epic"

def decrypt_profile(sav_path: Path):
    """
    Decrypts the profile save and returns the YAML bytes.
    """
    user_id, platform = get_user_info_from_path(sav_path)
    return decrypt_sav_to_yaml(sav_path, user_id, platform)

def extract_bank_serials(yaml_bytes: bytes):
    """
    Extracts item serials from the bank.
    """
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

def decode_serial(serial: str):
    """
    Decodes a serial and extracts item information.
    """
    decoded = custom_base85_decode(serial)
    binary_str = bytes_to_binary_string(decoded)
    reader = BitReader(binary_str)
    
    # Header 5 bits
    header = reader.read_int(5)
    # hard separator (00)
    reader.read_bits(2)
    # itemtype ID (varint)
    item_type_id = reader.read_varint()
    # soft separator (01)
    reader.read_bits(2)
    # padding 0 (varint)
    padding_zero = reader.read_varint()
    # soft separator (01)
    reader.read_bits(2)
    
    level = None
    # Key-value pairs until double hard separator (00 00)
    while True:
        if reader.peek_bits(2) == "00":
            reader.read_bits(2)
            if reader.peek_bits(2) == "00":
                reader.read_bits(2)
                break
            continue
            
        key = reader.read_varint()
        reader.read_bits(2) # soft separator
        value = reader.read_varint()
        
        if key == 1:
            level = value
            
        if reader.peek_bits(2) == "01":
            reader.read_bits(2)
        elif reader.peek_bits(2) == "00":
            reader.read_bits(2)

    parts = []
    while reader.pos < len(binary_str) - 5:
        part = reader.read_varint()
        if part == 0 and reader.pos >= len(binary_str) - 8:
            break
        parts.append(part)
        
    return {
        "item_type_id": item_type_id,
        "level": level,
        "parts": parts
    }

def generate_bank_report(serials: list):
    """
    Groups items by gear type and counts firmware combinations.
    Returns a nested dictionary structure.
    """
    report = {}
    
    for serial in serials:
        try:
            gear_type, firmware = get_item_info(serial)
            
            if gear_type not in report:
                report[gear_type] = {
                    "count": 0,
                    "firmware_counts": {}
                }
                
            report[gear_type]["count"] += 1
            
            # Use tuple for immutable key
            firmware_key = tuple(sorted(firmware))
            if firmware_key not in report[gear_type]["firmware_counts"]:
                report[gear_type]["firmware_counts"][firmware_key] = 0
            
            report[gear_type]["firmware_counts"][firmware_key] += 1
            
        except Exception as e:
            # Skip invalid serials for the report
            continue
            
    return report

def main():
    pass

if __name__ == "__main__":
    main()
