import yaml
import sys
from collections import Counter

def main():
    with open('reference_bank.yaml', 'r') as f:
        bank_data = yaml.safe_load(f)
    bank_items = bank_data.get('items', [])
    
    with open('reference_vex_grenades.yaml', 'r') as f:
        vex_data = yaml.safe_load(f)
    vex_items = vex_data.get('items', [])
    
    bank_flags = Counter([i['flags'] for i in bank_items])
    vex_flags = Counter([i['flags'] for i in vex_items])
    
    print("Vex Flags (Known Grenades):")
    for f, count in vex_flags.items():
        print(f"  Flag {f}: {count} items")
        
    print("\nBank Flags (Should be 0 grenades):")
    for f, count in bank_flags.items():
        print(f"  Flag {f}: {count} items")

if __name__ == "__main__":
    main()
