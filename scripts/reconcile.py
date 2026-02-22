import sys
import yaml
from pathlib import Path

sys.path.append('scripts')
from bank_report import get_item_info, bit_pack_decode

def main():
    fname = 'reference_bank_heavy.yaml'
    with open(fname, 'r') as f:
        data = yaml.safe_load(f)
    items = data.get('items', [])
    
    for item in items:
        s = item['serial']
        cat, fw = get_item_info(s)
        if cat == "Grenade Ordnance":
            b = bit_pack_decode(s)
            db = bytearray()
            for i in range(0, (len(b)//8)*8, 8):
                db.append(int(b[i:i+8], 2))
            tc = s[3]
            mid = db[4] if len(db) > 4 else None
            cid = db[8] if len(db) > 8 else None
            pre = db[:2].hex().upper() if len(db) >= 2 else ""
            print(f"cat={cat} tc={tc} mid={mid} cid={cid} pre={pre} serial={s}")

if __name__ == "__main__":
    main()
