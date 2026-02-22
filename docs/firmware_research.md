# Borderlands 4 Firmware & Gear Research (Definitive)

This document synthesizes the research conducted on item serials, gear categories, and firmware identification for Borderlands 4.

## 1. Gear Category Identification (Verified)

Through bitwise analysis and save movement tracking, we identified that gear categories are defined by a combination of the **Item Type Character** (at index 3 of the serial), **Manufacturer ID**, and **Item Class ID**.

### Category Mapping Key
| Category | Type Char | Class ID | Manufacturer ID | Logic / Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Enhancement** | `e` | `155` | Various | Direct Match (89 items) |
| **Energy Shield** | `e` | `77` | `208, 221, 201` | Direct Match (40 items) |
| **Armor Shield** | `r` | `185, 219, 213, 210, 203, 215, 209` | `252` | Verified via movement |
| **Grenade Ordnance** | `r` | `< 170` | `254, 252` | Shared slot with Heavy |
| **Heavy Weapon Ord** | `r` | `175, 190, 189, 183...` | `30, 18, 252` | Shared slot with Grenade |
| **Repkit** | `!, f, b, #` | `230` (if `e`) | Various | Mixed item types |
| **Class Mod** | `c, x, v, g, w...` | `205, 38, 102, 11` (if `e`) | Various | Mixed item types |
| **Weapon** | `r` | Various | Various | Non-gear items |

---

## 2. Firmware Bit Fingerprints

Firmware is encoded as bit sequences typically starting at bit 40 (post-header). We have categorized them into "Families" based on shared header patterns.

### Family A (Header: `0111100101110010111000001`)
- **Action Fist**: `...000001` + `1011101100`
- **Atlas Infinum**: `...000001` + `1000001100`
- **Gadget Ahoy**: `...000001` + `01111010100110001100`
- **Heating Up**: `...000001` + `1101010100`
- **Jacked**: `...000001` + `1011101001`
- **Oscar Mike**: `...000001` + `01110010100011010000`
- **Risky Boots**: `...000001` + `1001011000`
- **Trickshot**: `...000001` + `1011101011`
- **Dead Eye**: `01111001011100101110000` (Variant)

### Family B (Header: `111100101110010111000001`)
- **Get Throwin'**: `...000001` + `0110101100`
- **Reel Big Fist**: `...000001` + `0110110001`
- **Rubberband Man**: `...000001` + `0111110110`
- **Daed-dy O'**: `...000001` + `0111111010`
- **Bullets to Spare**: Identified by the header itself.

### Family C (Header: `00111100101110010111000001`)
- **Atlas E.X.**: `...000001` + `1010100011`
- **God Killer**: `...000001` + `1010110101`
- **Lifeblood**: `...000001` + `0101011110`

### Family D (Header: `001101100010000010001100`)
- **Baker**: `...1100` + `1010101000`
- **GooJFC**: `...1100` + `1010101111`
- **High Caliber**: `...1100` + `0100000110`

---

## 3. Firmware Lock/Status Analysis

Analysis of "Locked" vs "Unlocked" variants indicated that lock status is typically controlled by bits in the **second byte** (bits 8-15) of the bitstream, though this can vary by category:
- `13` (00010011): Unlocked
- `14` (00010100): Locked
- `15` (00010101): Locked (Alternative)

---

## 4. Unmapped / Missing Data
- **Skillcraft**: No fingerprint established.
- **Boxer**: No fingerprint established.
- **Weapon Firmware**: Weapons do not have firmware, only gear

---

## 5. Reference Data Snapshots (Gold Standard)

To achieve 100% accuracy, we are capturing isolated snapshots where Vex's inventory contains only one specific gear type.

| Snapshot File | Category | Total Items | With Firmware | Date | Significance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `reference_vex_grenades.yaml` | Grenade Ordnance | 67 | 41 (User reported) | 2026-02-21 | Established definitive `r` vs `e` grenade signatures. |
| `reference_vex_heavy.yaml` | Heavy Ordnance | 19 | 16 | 2026-02-21 | Captured signatures for all Heavy Weapons. |
| `reference_vex_energy_shield.yaml` | Energy Shield | 47 | 38 | 2026-02-21 | Definitive signatures for Energy Shields. |
| `reference_vex_armor_shield.yaml` | Armor Shield | 57 | 50 | 2026-02-21 | Definitive signatures for Armor Shields. |
| `reference_vex_repkit.yaml` | Repkit | 70 | 62 | 2026-02-21 | Definitive signatures for Repkits. |
| `reference_vex_enhancement_p1.yaml` | Enhancement (P1) | 48 | 35 | 2026-02-21 | Phase 1 of Enhancements (Legendary/Epic). |
| `reference_vex_enhancement_p2.yaml` | Enhancement (P2) | 45 | 41 | 2026-02-21 | Phase 2 of Enhancements (Rare/Uncommon). |
| `reference_vex_classmod_p1.yaml` | Class Mod (P1) | 47 | 33 | 2026-02-21 | Phase 1 of Class Mods (Legendary/Epic). |
| `reference_vex_classmod_p2.yaml` | Class Mod (P2) | 43 | 43 | 2026-02-21 | Phase 2 of Class Mods (Rare/Uncommon/Common). |

---

## 6. Tooling Reference
- `scripts/bank_report.py`: Definitive reporting tool using the verified mappings.
- `scripts/detect_moves.py`: Research utility for tracking item movement between Bank and Inventory.
- `scripts/analyze_firmware.py`: Low-level bitstream comparison utility.
