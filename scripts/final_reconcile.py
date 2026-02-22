import sys
import yaml
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append('scripts')
from bank_report import get_item_info

def main():
    with open('baseline_bank.yaml', 'r') as f:
        data = yaml.safe_load(f)
    
    serials = data.get('serials', [])
    report = {}
    for s in serials:
        cat, fw = get_item_info(s)
        if cat not in report:
            report[cat] = {"total": 0, "fw": 0}
        report[cat]["total"] += 1
        if fw:
            report[cat]["fw"] += 1
            
    for k, v in sorted(report.items()):
        print(f"{k}: {v['total']} / {v['fw']}")

if __name__ == "__main__":
    main()
