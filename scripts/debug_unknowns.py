import yaml
import sys
from pathlib import Path
sys.path.append(str(Path.cwd() / 'scripts'))

from bank_report import bit_pack_decode, decrypt_profile, find_profile_save, FIRMWARE_FAMILIES, to_bits

class CustomLoader(yaml.SafeLoader):
    def construct_python_tuple(self, node):
        return tuple(self.construct_sequence(node))

CustomLoader.add_constructor('tag:yaml.org,2002:python/tuple', CustomLoader.construct_python_tuple)

def debug_unknowns():
    path = find_profile_save()
    yaml_bytes = decrypt_profile(path)
    data = yaml.safe_load(yaml_bytes)
    bank = data.get('domains', {}).get('local', {}).get('shared', {}).get('inventory', {}).get('items', {}).get('bank', {})
    
    family_b_header = FIRMWARE_FAMILIES["Family B"]
    unknown_b_bits = {}

    print("--- Debugging Unknown Family B (Top 10 patterns) ---")
    for item in bank.values():
        serial = item.get('serial')
        if not serial: continue
        bits = to_bits(bit_pack_decode(serial))
        
        pos = bits.find(family_b_header, 40)
        if pos != -1:
            remainder = bits[pos + len(family_b_header) : pos + len(family_b_header) + 10]
            if remainder not in unknown_b_bits:
                unknown_b_bits[remainder] = 0
            unknown_b_bits[remainder] += 1

    for bits, count in sorted(unknown_b_bits.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"Bits: {bits} | Count: {count}")

if __name__ == "__main__":
    debug_unknowns()
