import yaml
import sys
from pathlib import Path

# Custom loader to handle python/tuple if it leaked into the YAML
class CustomLoader(yaml.SafeLoader):
    def construct_python_tuple(self, node):
        return tuple(self.construct_sequence(node))

CustomLoader.add_constructor('tag:yaml.org,2002:python/tuple', CustomLoader.construct_python_tuple)

def take_snapshot(output_name):
    verify_file = Path("verify_2.yaml")
    if not verify_file.exists():
        print("Error: verify_2.yaml not found. Please run scripts/verify_saves.py first.")
        return

    with open(verify_file, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=CustomLoader)

    equipped = data.get('state', {}).get('inventory', {}).get('equipped_inventory', {}).get('equipped', {})
    decoded_summary = data.get('_DECODED_ITEMS_SUMMARY', {})

    snapshot = {
        "character": data.get('state', {}).get('char_name', 'Unknown'),
        "equipped_slots": {}
    }

    for slot_name, items in equipped.items():
        if not items: continue
        item = items[0]
        serial = item.get('serial')
        
        path = f"state.inventory.equipped_inventory.equipped.{slot_name}[0].serial"
        decoded_info = decoded_summary.get(path, {})

        snapshot["equipped_slots"][slot_name] = {
            "serial": serial,
            "decoded_info": decoded_info
        }

    with open(output_name, "w", encoding="utf-8") as f:
        yaml.dump(snapshot, f, default_flow_style=False, sort_keys=True)
    
    print(f"Snapshot saved to {output_name} for {snapshot['character']}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "vex_gear_snapshot.yaml"
    take_snapshot(out)
