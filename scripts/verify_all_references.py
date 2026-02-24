import yaml
import sys
import os
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append('scripts')
from bank_report import get_item_info, bit_pack_decode

def main():
    reference_files = [
        'reference_vex_armor_shield.yaml',
        'reference_vex_classmod_p1.yaml',
        'reference_vex_classmod_p2.yaml',
        'reference_vex_energy_shield.yaml',
        'reference_vex_enhancement_p1.yaml',
        'reference_vex_enhancement_p2.yaml',
        'reference_vex_grenades.yaml',
        'reference_vex_heavy.yaml',
        'reference_vex_repkit.yaml'
    ]

    print(f"{'Source File':<35} | {'Category':<25} | {'Total':<6} | {'FW'}")
    print("-" * 80)

    for fname in reference_files:
        if not Path(fname).exists():
            print(f"Skipping {fname} (not found)")
            continue
            
        with open(fname, 'r') as f:
            data = yaml.safe_load(f)
        
        items = data.get('items', [])
        report = {}
        for item in items:
            serial = item['serial']
            cat, has_fw = get_item_info(serial)
            if cat not in report:
                report[cat] = {"total": 0, "fw": 0}
            report[cat]["total"] += 1
            if has_fw:
                report[cat]["fw"] += 1
        
        # Determine the expected category from filename
        expected = fname.replace('reference_vex_', '').replace('_p1', '').replace('_p2', '').replace('.yaml', '').replace('_', ' ')
        
        for cat in sorted(report.keys()):
            d = report[cat]
            mark = "!" if expected.lower() not in cat.lower() else " "
            print(f"{mark}{fname:<34} | {cat:<25} | {d['total']:<6} | {d['fw']}")

if __name__ == "__main__":
    main()
