#!/bin/bash
# scripts/verify_phase_3.sh

python -c "
import sys
import yaml
import glob
from pathlib import Path
sys.path.append(str(Path.cwd() / 'scripts'))

from bank_report import find_profile_save, decrypt_profile, extract_bank_serials, decode_serial

def map_serials_to_names():
    serial_to_name = {}
    # Find all verify_*.yaml files
    for yaml_file in glob.glob('verify_*.yaml'):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
                if not data: continue
                
                # Check for character save structure
                state = data.get('state', {})
                if state:
                    # Check backpack
                    backpack = state.get('inventory', {}).get('items', {}).get('backpack', {})
                    for slot, item in backpack.items():
                        if isinstance(item, dict) and 'serial' in item:
                            # We don't have name in YAML but maybe we can find it in another way or just report type
                            pass
                            
            except:
                continue
    return serial_to_name

path = find_profile_save()
if not path:
    print('Error: Profile save file not found.')
    sys.exit(1)

try:
    yaml_bytes = decrypt_profile(path)
    data = yaml.safe_load(yaml_bytes)
    bank = data['domains']['local']['shared']['inventory']['items']['bank']
    
    unique_types = {}
    
    for slot_id, item_data in bank.items():
        serial = item_data.get('serial')
        if serial:
            try:
                decoded = decode_serial(serial)
                type_id = decoded['item_type_id']
                if type_id not in unique_types:
                    unique_types[type_id] = serial
            except:
                continue

    print('Please provide the gear type for these sample serials:')
    for type_id, serial in sorted(unique_types.items()):
        print(f'Type {type_id} (Serial: {serial})')
        
except Exception as e:
    print(f'FAILURE: {e}')
"
