import yaml
import sys
import os

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
    return type_char, class_id, manuf_id, bits, len(decoded_bytes)

def main():
    with open('baseline_bank.yaml', 'r') as f:
        data = yaml.safe_load(f)
    serials = data.get('serials', [])
    
    families = {
        "A": "0111100101110010111000001",
        "B": "111100101110010111000001",
        "C": "00111100101110010111000001",
        "D": "001101100010000010001100"
    }

    print(f"{'TC':<3} | {'MID':<5} | {'CID':<5} | {'DLEN':<5} | {'Total':<6} | {'With FW':<8}")
    print("-" * 50)
    
    groups = {}
    for serial in serials:
        tc, cid, mid, bits, dlen = get_stats(serial)
        key = (tc, mid, cid, dlen)
        if key not in groups:
            groups[key] = {"total": 0, "with_fw": 0}
        groups[key]["total"] += 1
        
        has_fw = False
        for pattern in families.values():
            if pattern in bits:
                has_fw = True
                break
        if has_fw:
            groups[key]["with_fw"] += 1
            
    for (tc, mid, cid, dlen), d in sorted(groups.items(), key=lambda x: (x[0][0], str(x[0][1]), str(x[0][2]), x[0][3])):
        print(f"{tc:<3} | {str(mid):<5} | {str(cid):<5} | {str(dlen):<5} | {d['total']:<6} | {d['with_fw']:<8}")

if __name__ == "__main__":
    main()
