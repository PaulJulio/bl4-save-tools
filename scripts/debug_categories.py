import yaml
import sys
from pathlib import Path
sys.path.append(str(Path.cwd() / 'scripts'))
from bank_report import decrypt_profile, find_profile_save

def debug():
    path = find_profile_save()
    yaml_bytes = decrypt_profile(path)
    data = yaml.safe_load(yaml_bytes)
    bank = data.get('domains', {}).get('local', {}).get('shared', {}).get('inventory', {}).get('items', {}).get('bank', {})
    
    print("--- Bank Sample (First 20 items) ---")
    for i, (slot, item) in enumerate(list(bank.items())[:20]):
        print(f"[{i}] {slot}: {item.get('serial')}")

if __name__ == "__main__":
    debug()
