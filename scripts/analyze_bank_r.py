import sys
import yaml
from pathlib import Path
from collections import Counter

sys.path.append('scripts')
from bank_report import bit_pack_decode

def main():
    with open('reference_bank.yaml', 'r') as f:
        data = yaml.safe_load(f)
    serials = data.get('serials', [])
    
    res = []
    for s in serials:
        if s[3] == 'r':
            b = bit_pack_decode(s)
            db = bytearray()
            for i in range(0, (len(b)//8)*8, 8):
                db.append(int(b[i:i+8], 2))
            mid = db[4] if len(db) > 4 else None
            cid = db[8] if len(db) > 8 else None
            res.append((mid, cid))
            
    counts = Counter(res)
    print("MID | CID | Total")
    print("-" * 15)
    for (mid, cid), count in sorted(counts.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        print(f"{str(mid):<3} | {str(cid):<3} | {count}")

if __name__ == "__main__":
    main()
