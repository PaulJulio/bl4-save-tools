import sys
import yaml
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append('scripts')
from bank_report import get_item_info, bit_pack_decode

def main():
    with open('baseline_bank.yaml', 'r') as f:
        data = yaml.safe_load(f)
    
    serials = data.get('serials', [])
    
    report = {}
    for serial in serials:
        cat, has_fw = get_item_info(serial)
        if cat not in report:
            report[cat] = {"total": 0, "fw": 0}
        report[cat]["total"] += 1
        if has_fw:
            report[cat]["fw"] += 1
            
    print(f"{'Category':<30} | {'Total':<6} | {'FW'}")
    print("-" * 45)
    for cat in sorted(report.keys()):
        d = report[cat]
        print(f"{cat:<30} | {d['total']:<6} | {d['fw']}")
        
    print("\n--- Detailed 'r' type Analysis ---")
    for serial in serials:
        if serial[3] == 'r':
            b = bit_pack_decode(serial)
            db = bytearray()
            for i in range(0, (len(b)//8)*8, 8):
                db.append(int(b[i:i+8], 2))
            mid = db[4] if len(db) > 4 else None
            cid = db[8] if len(db) > 8 else None
            cat, fw = get_item_info(serial)
            if cat in ["Grenade Ordnance", "Heavy Weapon Ordnance", "Weapon", "Armor Shield"]:
                print(f"{cat:<25} | mid={str(mid):<4} | cid={str(cid):<4} | fw={str(fw):<5} | {serial}")

if __name__ == "__main__":
    main()
