# Tech Stack - Borderlands 4 Save Automation Tools

## Core Technologies
- **Python:** Primary programming language for local automation, reporting, and save file processing.
- **JavaScript:** Secondary programming language, supporting existing web-based features.
- **YAML:** Human-readable format for representing save data and configuration files.
- **CSV:** Tabular format for managing game data like missions, challenges, and item lists.

## Key Python Libraries
- **PyCryptodome:** For cryptographic operations, including save decryption and encryption.
- **PyYAML:** For parsing and generating YAML representations of save data.

## Infrastructure & Environment
- **Local Execution:** Scripts are designed for local, terminal-based interaction on the user's machine.
- **Direct File System Access:** Interaction with local game save directories (e.g., `%USERPROFILE%\Documents\My Games\Borderlands 4\Saved\SaveGames`).
- **Personal Utility:** No remote server dependency; the tool is intended for personal, local use.
