# Specification - Bank Reporting

## Overview
A standalone Python script to analyze and report on items stored in the user's shared bank (profile save). The tool will categorize items by gear type and provide counts for specific "firmware" (components/modifiers) to help users manage their inventory and identify duplicates or surplus items.

## Functional Requirements
1. **Save Discovery:** Automatically locate the game's profile save file (`profile.sav`).
2. **Decryption:** Decrypt the `profile.sav` file to access item serials.
3. **Item Parsing:** Decode item serials to extract:
   - Gear Type (e.g., Shield, Pistol, Grenade).
   - Firmware/Components (e.g., "Jacked", "Hardened").
   - Item Name.
4. **Categorization:** Group items by their gear type.
5. **Firmware Reporting:** For each gear type, count the occurrences of unique firmware/component combinations.
6. **Console Output:**
   - Display a summary of firmware counts per gear type.
   - List the names of items in each category.
   - Clearly highlight if a user has "enough" of a certain combination (e.g., more than 3).

## Non-Functional Requirements
- **Performance:** Reporting should complete in under 5 seconds.
- **Reliability:** The script should handle missing or corrupted profile saves gracefully.

## Acceptance Criteria
- [ ] Script runs as `python scripts/bank_report.py`.
- [ ] Successfully reads and decrypts `profile.sav`.
- [ ] Correctly identifies and categorizes items from the shared bank.
- [ ] Displays counts for firmware/gear type combinations.
- [ ] Output is clearly formatted and easy to read.

## Out of Scope
- Reporting on character-specific inventory (only shared bank).
- Modifying save files (read-only for this track).
- Graphical User Interface (GUI).
