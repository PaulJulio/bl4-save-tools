import sys
import yaml
from pathlib import Path

sys.path.append('scripts')
from bank_report import bit_pack_decode

def main():
    with open('reference_vex_grenades.yaml', 'r') as f:
        data = yaml.safe_load(f)
    serials = data.get('serials', [])
    
    print(f"Analyzing {len(serials)} grenades...")
    
    for s in serials:
        b = bit_pack_decode(s)
        # Convert bits to bytes for easier inspection
        db = bytearray()
        for i in range(0, (len(b)//8)*8, 8):
            db.append(int(b[i:i+8], 2))
            
        # Inspect first few bytes
        # Byte 0: Header/Type info?
        # Byte 1: Manufacturer?
        # Byte 2: ??
        # Byte 3: Class? (for e-type)
        # ...
        
        tc = s[3]
        # Let's print the first 12 bytes
        bytes_str = " ".join([f"{x:02X}" for x in db[:12]])
        print(f"tc={tc} | bytes={bytes_str} | {s[:20]}...")

if __name__ == "__main__":
    main()
