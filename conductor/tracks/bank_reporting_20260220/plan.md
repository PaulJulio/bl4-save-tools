# Implementation Plan - Bank Reporting

## Phase 1: Foundation & Discovery
- [ ] Task: Create `tests/test_bank_report.py` and `scripts/bank_report.py` boilerplate
- [ ] Task: Implement profile save discovery logic in `bank_report.py`
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Discovery' (Protocol in workflow.md)

## Phase 2: Decryption & Parsing
- [ ] Task: Implement decryption for `profile.sav` using existing `blcrypt` logic
- [ ] Task: Implement item serial extraction from decrypted profile data
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Decryption & Parsing' (Protocol in workflow.md)

## Phase 3: Categorization & Firmware Logic
- [ ] Task: Implement item decoding to extract gear type and firmware/components
- [ ] Task: Implement categorization and counting logic for firmware/gear combinations
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Categorization & Firmware Logic' (Protocol in workflow.md)

## Phase 4: Reporting & Output
- [ ] Task: Implement formatted console output for bank inventory summary
- [ ] Task: Implement highlighting/alerting for items exceeding the count threshold (>3)
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Reporting & Output' (Protocol in workflow.md)
