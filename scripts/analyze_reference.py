import sys
import yaml
from pathlib import Path

sys.path.append('scripts')
from bank_report import bit_pack_decode

def main():
    fname = sys.argv[1] if len(sys.argv) > 1 else 'reference_vex_heavy.yaml'
    with open(fname, 'r') as f:
        data = yaml.safe_load(f)
    items = data.get('items', [])
    
    FIRMWARE_PATTERNS = {
        "Family A": "0111100101110010111000001",
        "Family B": "111100101110010111000001",
        "Family C": "00111100101110010111000001",
        "Family D": "001101100010000010001100"
    }

    for item in items:
        s = item['serial']
        b = bit_pack_decode(s)
        db = bytearray()
        for i in range(0, (len(b)//8)*8, 8):
            db.append(int(b[i:i+8], 2))
        tc = s[3]
        cid = (db[8] if tc=='r' and len(db)>8 else (db[3] if tc=='e' and len(db)>3 else None))
        mid = (db[4] if tc=='r' and len(db)>4 else (db[1] if tc=='e' and len(db)>1 else None))
        pre = db[:2].hex().upper() if len(db) >= 2 else ""
        
        has_fw = any(p in b for p in FIRMWARE_PATTERNS.values())
        print(f"tc={tc} mid={str(mid):<4} cid={str(cid):<4} pre={pre} fw={str(has_fw):<5} | {s}")

if __name__ == "__main__":
    main()
