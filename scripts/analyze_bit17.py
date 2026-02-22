import sys
import yaml
from pathlib import Path
from collections import Counter

sys.path.append('scripts')
from bank_report import bit_pack_decode

def main():
    with open('reference_bank_heavy.yaml', 'r') as f:
        data = yaml.safe_load(f)
    items = data.get('items', [])
    
    mids = []
    for item in items:
        s = item['serial']
        if s[3] == 'r':
            b = bit_pack_decode(s)
            if b[17] == '0':
                db = bytearray()
                for i in range(0, (len(b)//8)*8, 8):
                    db.append(int(b[i:i+8], 2))
                mid = db[4] if len(db) > 4 else None
                mids.append(mid)
                
    counts = Counter(mids)
    print("Manufacturers for bit17=0 in Bank:")
    for mid, count in counts.most_common():
        print(f"  MID {mid}: {count} items")

if __name__ == "__main__":
    main()
