import sys
import os
import yaml
import struct
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from discovery import find_save_directory
import blcrypt
from bank_report import decode_item_serial

def find_and_decode_serials_in_yaml(yaml_data: dict) -> dict:
    """
    Recursively searches for @U serials and decodes them.
    Returns a dictionary mapping path to decoded info.
    """
    decoded_serials = {}

    def search_dict(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, str) and value.startswith('@U'):
                    decoded = decode_item_serial(value)
                    if decoded.confidence != "none":
                        # Convert dataclass to dict for YAML serialization
                        info = asdict(decoded)
                        # Remove raw_fields to keep YAML readable, or keep if requested
                        # info.pop('raw_fields', None) 
                        decoded_serials[new_path] = info
                elif isinstance(value, (dict, list)):
                    search_dict(value, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                if isinstance(item, str) and item.startswith('@U'):
                    decoded = decode_item_serial(item)
                    if decoded.confidence != "none":
                        decoded_serials[new_path] = asdict(decoded)
                elif isinstance(item, (dict, list)):
                    search_dict(item, new_path)

    search_dict(yaml_data)
    return decoded_serials

def verify_saves():
    save_dir = find_save_directory()
    if not save_dir:
        print("Error: Could not locate Borderlands 4 save directory.")
        return

    # Use the identified Steam ID from our research
    steam_id = "76561197967455859"
    print(f"Using Steam ID: {steam_id}")
    print(f"Source Directory: {save_dir}\n")

    sav_files = sorted(list(save_dir.rglob("*.sav")))
    
    for sav_path in sav_files:
        yaml_name = f"verify_{sav_path.stem}.yaml"
        print(f"--- Processing {sav_path.name} ---")
        
        try:
            # Decrypt
            yaml_bytes = blcrypt.decrypt_sav_to_yaml(sav_path, steam_id, platform="steam")
            
            # Use a slightly more robust YAML loader that handles custom tags
            data = yaml.load(yaml_bytes, Loader=yaml.SafeLoader)
            
            if isinstance(data, dict):
                # Perform deep serial decoding
                decoded_info = find_and_decode_serials_in_yaml(data)
                if decoded_info:
                    data['_DECODED_ITEMS_SUMMARY'] = decoded_info
                    print(f"  Decoded {len(decoded_info)} item serials.")

                # Save the enriched YAML
                with open(yaml_name, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                print(f"  Decrypted and enriched to: {yaml_name}")
            
            # Print brief summary to console
            if isinstance(data, dict):
                if 'state' in data:
                    state = data['state']
                    name = state.get('char_name', 'Unknown')
                    print(f"  Character: {name}")
                else:
                    shared = data.get('shared', {}) or data.get('domains', {}).get('local', {}).get('shared', {})
                    bank = shared.get('inventory', {}).get('items', {}).get('bank', {})
                    if isinstance(bank, dict):
                        print(f"    Bank Items: {len(bank)}")
                
        except Exception as e:
            print(f"  Error processing {sav_path.name}: {e}")
            import traceback
            traceback.print_exc()
        print()

if __name__ == "__main__":
    verify_saves()
