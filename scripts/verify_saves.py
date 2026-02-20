import sys
import os
import yaml
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from discovery import find_save_directory
import blcrypt

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
            
            # Save the decrypted YAML
            with open(yaml_name, 'wb') as f:
                f.write(yaml_bytes)
            print(f"  Decrypted to: {yaml_name}")
            
            # Parse and summarize
            if isinstance(data, dict):
                if 'state' in data:
                    # Character File
                    state = data['state']
                    name = state.get('char_name', 'Unknown')
                    char_class = state.get('class', 'Unknown')
                    
                    exp_list = state.get('experience', [])
                    char_lv = "Unknown"
                    spec_lv = "Unknown"
                    
                    if isinstance(exp_list, list):
                        for entry in exp_list:
                            if isinstance(entry, dict):
                                if entry.get('type') == 'Character':
                                    char_lv = entry.get('level')
                                elif entry.get('type') == 'Specialization':
                                    spec_lv = entry.get('level')
                    
                    print(f"  Character: {name}")
                    print(f"  Class: {char_class}")
                    print(f"  Levels: Character {char_lv}, Specialization {spec_lv}")
                else:
                    # Profile File (likely)
                    print("  Profile Summary:")
                    
                    # Search for bank items
                    # Based on structure: shared -> inventory -> items -> bank
                    shared = data.get('shared', {})
                    if not shared:
                        # Fallback for nested domains structure if exists
                        shared = data.get('domains', {}).get('local', {}).get('shared', {})
                    
                    inventory = shared.get('inventory', {})
                    items = inventory.get('items', {})
                    bank = items.get('bank', {})
                    
                    if isinstance(bank, dict):
                        print(f"    Bank Items: {len(bank)}")
                    
                    # Search for Vault Card level
                    exp_list = shared.get('experience', [])
                    if isinstance(exp_list, list):
                        for entry in exp_list:
                            if isinstance(entry, dict) and 'VaultCard' in entry.get('type', ''):
                                vc_type = entry.get('type')
                                vc_lv = entry.get('level')
                                print(f"    {vc_type}: Level {vc_lv}")
            else:
                print("  Unknown file format")
                
        except Exception as e:
            print(f"  Error processing {sav_path.name}: {e}")
        print()

if __name__ == "__main__":
    verify_saves()
