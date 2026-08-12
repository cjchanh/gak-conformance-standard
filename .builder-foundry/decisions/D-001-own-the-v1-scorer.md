# D-001 — Own the frozen v1 scorer in this repository

- **Date:** 2026-08-12
- **Wave:** baseline / architecture
- **Status:** accepted
- **Author lane:** lead (session 1)

## Decision

Implement `gak_conformance` in this repo as the mechanical harness for
`gak-conformance/v1` (exactly the 13 §4 clauses). Do **not** import
`deponent.conformance` or `deponent.badge` as the harness.

## Why

1. Mission: a third party scores a kernel without Deponent internals.
2. Measured: `python3 -m gak_conformance` does not exist; `check_consistency.py`
   exits 3 without `deponent`.
3. Measured: live Deponent `CLAUSES` has 16 entries including
   `GAK-REDIRECT-DENIED` and `GAK-NEWLINE-CHAINED`, which are **not** in
   `v1/spec.md`. Using Deponent as the harness would silently expand the
   category.

## Rejected alternatives

- Wrap `deponent.conformance.run_conformance` — couples the standard to a
  kernel and inherits extras.
- Ship spec-only and tell people to install Deponent — status quo; third-party
  scores stay 0.
- Adopt Deponent's 16 clauses as "v1.2" this campaign — out of mission scope;
  would require a spec amendment.

## Follow-through

- FEAT-0001, FEAT-0009, FEAT-0025, FEAT-0032
- Optional later: Deponent adapter (FEAT-0026) that *drives* Deponent, scored
  by *this* harness.
