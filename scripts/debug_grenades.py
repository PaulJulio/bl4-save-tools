import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append('scripts')
from bank_report import get_item_info, bit_pack_decode
import yaml

def test():
    with open('reference_vex_grenades.yaml', 'r') as f:
        data = yaml.safe_load(f)
    items = data.get('items', [])
    
    report = {}
    for item in items:
        serial = item['serial']
        cat, fw = get_item_info(serial)
        if cat not in report: report[cat] = 0
        report[cat] += 1
        if cat == "Armor Shield":
            bits = bit_pack_decode(serial)
            db = bytearray()
            for i in range(0, (len(bits)//8)*8, 8):
                db.append(int(bits[i:i+8], 2))
            prefix = db[:2].hex().upper() if len(db) >= 2 else ""
            header_6 = serial[6] if len(serial) > 6 else ''
            print(f"DEBUG: Armor Shield found! Prefix={prefix}, Header6={header_6}, Serial={serial[:20]}...")

    print("\nSummary:")
    for cat, count in report.items():
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    test()
