import sys
import yaml
from pathlib import Path

sys.path.append('scripts')
from bank_report import bit_pack_decode, get_item_info

def main():
    with open('baseline_bank.yaml', 'r') as f:
        data = yaml.safe_load(f)
    
    serials = data.get('serials', [])
    for s in serials:
        if s[3] == 'r':
            b = bit_pack_decode(s)
            db = bytearray()
            for i in range(0, (len(b)//8)*8, 8):
                db.append(int(b[i:i+8], 2))
            mid = db[4] if len(db) > 4 else None
            cid = db[8] if len(db) > 8 else None
            cat, fw = get_item_info(s)
            print(f"mid={mid}, cid={cid}, fw={fw}, serial={s}")

if __name__ == "__main__":
    main()
