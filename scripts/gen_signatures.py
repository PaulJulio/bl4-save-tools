import yaml
import sys
from pathlib import Path

sys.path.append('scripts')
from bank_report import bit_pack_decode

def gs(s):
    b = bit_pack_decode(s)
    db = bytearray()
    for i in range(0, (len(b)//8)*8, 8):
        db.append(int(b[i:i+8], 2))
    tc = s[3]
    cid = (db[8] if tc=='r' and len(db)>8 else (db[3] if tc=='e' and len(db)>3 else None))
    mid = (db[4] if tc=='r' and len(db)>4 else (db[1] if tc=='e' and len(db)>1 else None))
    prefix = db[:2].hex().upper() if len(db) >= 2 else ""
    return (tc, mid, cid, prefix)

def main():
    fname = sys.argv[1] if len(sys.argv) > 1 else 'reference_vex_grenades.yaml'
    with open(fname, 'r') as f:
        data = yaml.safe_load(f)
    items = data.get('items', [])
    
    sigs = set()
    for i in items:
        sigs.add(gs(i['serial']))
        
    label = fname.split('_')[-1].split('.')[0].upper()
    print(f"{label}_SIGNATURES = [")
    for sig in sorted(list(sigs)):
        print(f"    {sig},")
    print("]")

if __name__ == "__main__":
    main()
