import yaml
import sys
from pathlib import Path

class CustomLoader(yaml.SafeLoader):
    def construct_python_tuple(self, node):
        return tuple(self.construct_sequence(node))

CustomLoader.add_constructor('tag:yaml.org,2002:python/tuple', CustomLoader.construct_python_tuple)

def compare_snapshots():
    files = [
        "vex_gear_snapshot.yaml",
        "vex_gear_snapshot_unequipped.yaml",
        "vex_gear_snapshot_batch1.yaml"
    ]
    
    data = []
    for f in files:
        if not Path(f).exists():
            continue
        with open(f, 'r') as stream:
            data.append(yaml.load(stream, Loader=CustomLoader))

    all_slots = set()
    for d in data:
        all_slots.update(d['equipped_slots'].keys())

    # Header
    cols = ["Slot"] + [f"Snap {i+1}" for i in range(len(data))]
    header = " | ".join(f"{c:<15}" for c in cols)
    print(header)
    print("-" * len(header))
    
    for slot in sorted(list(all_slots)):
        row = [slot]
        for d in data:
            s = d['equipped_slots'].get(slot, {}).get('serial', 'EMPTY')
            short = (s[:12] + "...") if len(s) > 12 else s
            row.append(short)
        
        print(" | ".join(f"{c:<15}" for c in row))

if __name__ == "__main__":
    compare_snapshots()
