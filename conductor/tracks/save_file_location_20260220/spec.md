# Specification - Save File Location and Decryption

## Overview
This track focuses on implementing the core functionality for automatically locating Borderlands 4 save files on the user's machine and providing a robust decryption mechanism. This is a critical first step for the local automation tools.

## Requirements
- **Save File Discovery:** Automatically identify the game's save directory on Windows.
- **Platform Key Management:** Handle Steam and Epic ID keys for save decryption.
- **Save Decryption:** Implement the logic to decrypt `.sav` files into a human-readable format (YAML).
- **Validation:** Ensure that the discovered files are valid Borderlands 4 save files.

## Technical Details
- **Language:** Python
- **Libraries:** `pycryptodome` for cryptographic operations.
- **Target OS:** Windows
- **Save Paths:**
    - Steam: `%USERPROFILE%\Documents\My Games\Borderlands 4\Saved\SaveGames\<STEAM_ID>\Profiles\client`
    - Epic: Similar path structure under `EpicGames` or platform-specific subfolders.
