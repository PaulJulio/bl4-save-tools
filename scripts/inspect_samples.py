import sys
import yaml
from pathlib import Path
sys.path.append(str(Path.cwd() / 'scripts'))

from bank_report import find_profile_save, decrypt_profile, extract_bank_serials, decode_item_serial

def inspect_samples():
    path = find_profile_save()
    if not path:
        print("Profile not found.")
        return

    yaml_bytes = decrypt_profile(path)
    serials = extract_bank_serials(yaml_bytes)
    
    samples = {} # category -> list of items
    
    for serial in serials:
        decoded = decode_item_serial(serial)
        cat = decoded.item_category
        if cat not in samples:
            samples[cat] = []
        if len(samples[cat]) < 2: # Get 2 samples per category
            samples[cat].append(decoded)

    for cat, items in samples.items():
        print(f"\n=== Category: {cat} ===")
        for i, item in enumerate(items):
            print(f"\nSample {i+1}:")
            print(f"  Serial: {item.serial}")
            print(f"  Item Type Char: {item.item_type}")
            print(f"  Confidence: {item.confidence}")
            print(f"  Stats: {item.stats}")
            print(f"  Raw Fields (first 10):")
            for k, v in list(item.raw_fields.items())[:10]:
                print(f"    {k}: {v}")

if __name__ == "__main__":
    inspect_samples()
