# Borderlands 4 Firmware & Gear Research (Definitive)

## 1. Research Methodology: Signature Quintuple (sig_5)

To achieve maximum accuracy and eliminate the misclassification of standard weapons as gear, we use a strict **Signature Quintuple (sig_5)** matching system. Every item is analyzed using the following five identifiers:

`sig_5 = (Item Type Char, Manufacturer ID, Item Class ID, Prefix, Serial[6] Header Char)`

### Integrity of Reference Data
All `reference_vex_*.yaml`, `baseline_*.yaml`, and `vex_gear_snapshot_*.yaml` files are **historical snapshots**. These are treated as **Absolute Ground Truth** for the specific state they capture.

### Verified Baseline (Current)
- **File**: `baseline_bank.yaml`
- **SHA-256**: `9ee44a17c2f4864a78b60ec00579993fb454e710fff29e64ae2646f28b0ae897`
- **Verification Date**: 2026-02-22
- **Authoritative In-Game Counts vs. Detection Discrepancy**:

| Category | In-Game (Authoritative) | Detected (sig_5 Strict) | Status |
| :--- | :--- | :--- | :--- |
| **Weapon (Total)** | 63 | 198 | **Overcount (+135)** |
| **Grenade Ordnance** | 59 | 58 | **Near Match (-1)** |
| **Heavy Weapon Ord** | 19 | 18 | **Near Match (-1)** |
| **Shield (Consolidated)** | 102 | 69 | **Undercount (-33)** |
| **Class Mod** | 89 | 67 | **Undercount (-22)** |
| **Repkit** | 68 | 28 | **Undercount (-40)** |
| **Enhancement** | 91 | 53 | **Undercount (-38)** |

### Discrepancy Analysis (Incorrect Conclusions)
The current detection script undercounts gear because it relies on an **exclusive whitelist** derived from past reference files. 
1. **Precision vs. Recall**: The algorithm is tuned for 100% precision (ensuring no Weapon is ever counted as Gear). 
2. **Missing Signatures**: The ~135 "Weapon" items in the detection results include both the 63 standard firearms and **~72 gear variants** whose unique `sig_5` quintuples have not yet been mapped in the ground truth files.
3. **Future Research**: To resolve these discrepancies, future research must focus on capturing these unmapped variants from the "Weapon" pool and assigning them to their correct gear categories using verified character-state snapshots.

## 2. Classification Boundaries
- **Shield**: Consolidated Armor and Energy Shields.
- **Grenade Ordnance**: Standard throwable explosives.
- **Heavy Weapon Ordnance**: Specialized gear sharing the Grenade slot. NOT standard weapons.
- **Repkit**: Equipment used for repair/maintenance.
- **Enhancement**: Modifier gear.
- **Class Mod**: Character-specific capability modifiers.
- **Weapon**: Standard firearm categories. Items not matching verified gear signatures are classified here.

## 3. Firmware Research (Ongoing)
Firmware identification is based on bit sequences starting at bit 40. Current breakdown indicates a high prevalence of "Dead Eye" patterns across multiple categories, requiring further validation.
