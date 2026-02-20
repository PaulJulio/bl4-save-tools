# Implementation Plan - Save File Location and Decryption

## Phase 1: Research and Discovery [checkpoint: 3fb907a]
- [x] Task: Research standard Borderlands 4 save file paths for Steam and Epic on Windows. 62ae668
- [x] Task: Verify the existing decryption logic in the codebase and identify any necessary updates. 62ae668
- [x] Task: Conductor - User Manual Verification 'Phase 1: Research and Discovery' (Protocol in workflow.md)

## Phase 2: Implementation - Discovery and Decryption
- [ ] Task: Create a Python module for automatically locating the save directory.
    - [ ] Write Tests: Create unit tests for directory discovery across different platform IDs.
    - [ ] Implement Feature: Implement the `find_save_directory` function.
- [ ] Task: Integrate the decryption logic into the new Python script.
    - [ ] Write Tests: Create tests for decrypting sample save files with valid/invalid keys.
    - [ ] Implement Feature: Implement the `decrypt_save_file` function (TODO: Implement Epic support).
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Implementation - Discovery and Decryption' (Protocol in workflow.md)

## Phase 3: Validation and Integration
- [ ] Task: Implement basic validation for the decrypted data.
    - [ ] Write Tests: Verify that decrypted YAML contains expected keys (e.g., `state`, `experience`).
    - [ ] Implement Feature: Add validation checks to the decryption process.
- [ ] Task: Create a simple CLI entry point for testing the discovery and decryption.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Validation and Integration' (Protocol in workflow.md)
