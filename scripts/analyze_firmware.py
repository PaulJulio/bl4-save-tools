import yaml
import sys
from pathlib import Path
sys.path.append(str(Path.cwd() / 'scripts'))

from bank_report import bit_pack_decode

class CustomLoader(yaml.SafeLoader):
    def construct_python_tuple(self, node):
        return tuple(self.construct_sequence(node))

CustomLoader.add_constructor('tag:yaml.org,2002:python/tuple', CustomLoader.construct_python_tuple)

def to_bits(data):
    return "".join(bin(b)[2:].zfill(8) for b in data)

def analyze_headers():
    identified = [
        ("Baker", "vex_gear_snapshot_batch1.yaml", "slot_8"),
        ("Action Fist", "vex_gear_snapshot_batch1.yaml", "slot_4"),
        ("Airstrike", "vex_gear_snapshot_batch1.yaml", "slot_5"),
        ("Jacked", "vex_gear_snapshot_batch4.yaml", "slot_4"),
        ("Heating Up", "vex_gear_snapshot_batch3.yaml", "slot_6"),
        ("High Caliber", "vex_gear_snapshot_batch5.yaml", "slot_8"),
        ("GooJFC", "vex_gear_snapshot_batch13.yaml", "slot_8")
    ]

    print(f"{'Firmware':<15} | {'Bits 40-80'}")
    print("-" * 60)

    for name, filename, slot in identified:
        if not Path(filename).exists(): continue
        with open(filename, 'r', encoding='utf-8') as f:
            snap = yaml.load(f, Loader=CustomLoader)
        serial = snap['equipped_slots'][slot]['serial']
        bits = to_bits(bit_pack_decode(serial))
        print(f"{name:<15} | {bits[40:80]}")

if __name__ == "__main__":
    analyze_headers()
