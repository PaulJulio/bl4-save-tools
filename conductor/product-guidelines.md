# Product Guidelines - Borderlands 4 Save Automation Tools

## Prose & Tone
- **Developer-Focused:** Documentation and comments should be written for a technical audience, assuming familiarity with Python and basic data structures.
- **Direct & Technical:** Explanations should be concise and focused on the underlying logic and implementation details.
- **Internal Consistency:** Maintain consistent naming conventions and structures throughout the codebase for ease of maintenance.

## User Experience (CLI/Terminal)
- **In-Terminal Access:** The primary interaction model is through the terminal using Python scripts.
- **Robust Feedback:** Scripts must provide clear and detailed output for all operations, including successes, warnings, and errors.
- **Safe Operations:** Prioritize read-only operations for reporting; any write operations must be handled with extreme care and include automatic backups.
- **Personal Utility:** Design the tools for local, personal use, focusing on efficiency and direct file system interaction.

## Design Principles
- **Local-First:** All operations occur locally on the user's machine, with no dependency on remote servers or web interfaces.
- **Modular Design:** Organize scripts into modular components (e.g., decryption, reporting, data extraction) to allow for easy expansion.
- **Reliability:** Ensure that all save file interactions are thoroughly validated to maintain data integrity.

## Documentation
- **Technical Readme:** The documentation should focus on how to run the scripts, their dependencies, and how the data is processed.
- **Code Comments:** Use clear and informative comments within the Python scripts to explain complex logic and data structures.
