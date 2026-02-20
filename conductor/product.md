# Product Guide - Borderlands 4 Save Editor & Automation Tools

## Initial Concept
A web-based tool for modifying Borderlands 4 (PC) save files, allowing players to decrypt, edit via YAML, and re-encrypt their character and profile data. The project aims to provide a fast and reliable way to customize the gaming experience through preset modifications and manual editing.

## Vision & Goals
The Borderlands 4 Save Editor & Automation Tools aim to simplify the management and modification of save data for casual players. 
- **Automated Reporting:** Transitioning to local Python scripts that can automatically gather and report on save file contents, particularly shared bank items.
- **Local Autonomy:** Shifting focus from remote web deployments to a local-first approach that interacts directly with the user's computer.
- **Reliability:** Providing robust tools for safe save processing and metadata extraction.

## Target Audience
- **Casual Players:** Gamers who want a quick summary of their items or want to skip repetitive tasks.
- **Modders/Researchers:** Users interested in the underlying save structure and automated data extraction.

## Key Features (Current Phase)
- **Local Automation Script:** A new Python-based script for automated information gathering and bank item reporting.
- **Bank Item Summary:** Automated reporting of items stored in the shared `profile.sav` bank.
- **Direct Local Access:** Reading save files directly from the game's local storage path.
- **Save Decryption/Encryption:** Core processing capabilities for `.sav` files using platform-specific keys.

## Future Roadmap
- **Comprehensive Reporting:** Expanding the automated reports to include mission progress and character stats.
- **Local Tool Suite:** Further development of the Python script into a full-featured local utility.
- **UI/UX Polish:** Improving the user interface for both the web tool and local scripts.

## User Experience
- **Utility-First:** A minimalistic and efficient experience, prioritizing speed and local automation over remote accessibility.
- **Direct Interaction:** A more seamless experience for users running the tools on their own machines.
