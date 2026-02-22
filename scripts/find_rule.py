import yaml
import sys
from collections import Counter

sys.path.append('scripts')
from bank_report import bit_pack_decode

def main():
    with open('reference_vex_grenades.yaml', 'r') as f:
        vex_data = yaml.safe_load(f)
    vex_bits = [bit_pack_decode(i['serial']) for i in vex_data.get('items', [])]
    
    # We want a pattern that is in exactly 41 of 67 items
    targets = [41] # The user said 41/57, but I have 67 items. 
    # Maybe the proportion is similar? 41/57 approx 72%. 
    # 72% of 67 is 48.
    # Let's look for ANY pattern that appears in 40-50 items.
    
    patterns = Counter()
    for b in vex_bits:
        # Only look at bits 40 onwards (as per docs)
        b_fw = b[40:]
        # Use a sliding window
        window = 16
        seen_in_this_item = set()
        for i in range(len(b_fw) - window):
            seen_in_this_item.add(b_fw[i:i+window])
        for p in seen_in_this_item:
            patterns[p] += 1
            
    p = "0111100101110010"
    with open('reference_bank.yaml', 'r') as f:
        bank_data = yaml.safe_load(f)
    bank_bits = [bit_pack_decode(i['serial']) for i in bank_data.get('items', [])]
    bank_count = sum(1 for b in bank_bits if p in b)
    print(f"Pattern {p} matches {bank_count} bank items.")

if __name__ == "__main__":
    main()
