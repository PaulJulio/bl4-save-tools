# Implementation Plan - Bank Reporting

## Phase 1: Foundation & Discovery [checkpoint: 0a5679f]
- [x] Task: Create `tests/test_bank_report.py` and `scripts/bank_report.py` boilerplate (2e94f4f)
- [x] Task: Implement profile save discovery logic in `bank_report.py` (bbd3106)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Discovery' (Protocol in workflow.md) (0a5679f)

## Phase 2: Decryption & Parsing [checkpoint: 9ef6c22]
- [x] Task: Implement decryption for `profile.sav` using existing `blcrypt` logic (ea8735a)
- [x] Task: Implement item serial extraction from decrypted profile data (57200b3)
- [x] Task: Conductor - User Manual Verification 'Phase 2: Decryption & Parsing' (Protocol in workflow.md) (9ef6c22)

## Phase 3: Categorization & Firmware Logic
- [x] Task: Implement item decoding to extract gear type and firmware/components (ea8735a)
- [x] Task: Implement categorization and counting logic for firmware/gear combinations (4b6b1c7)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Categorization & Firmware Logic' (Protocol in workflow.md)

## Phase 4: Reporting & Output
- [ ] Task: Implement formatted console output for bank inventory summary
- [ ] Task: Implement highlighting/alerting for items exceeding the count threshold (>3)
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Reporting & Output' (Protocol in workflow.md)
