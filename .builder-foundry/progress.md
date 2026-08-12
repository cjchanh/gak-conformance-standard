# Builder Foundry Progress

- Campaign: `mission-gak-v0-standard-20260812`
- Profile: `standard`
- Branch: `foundry/gak-v0-standard`
- Initialized: 2026-08-12T17:53:08Z
- Session 3 (this file): product director — journeys, doctrine, acceptance, cuts

## Wave 0 — baseline (done)

- HEAD `e55b068` preserved; dirty untracked foundry install recorded, not destroyed.
- Contract lock `2bab65ac…` matches; amendments none.

## Wave 1 — research (session 1 + session 2)

- Session 1: receipt/clause/packaging (SLSA, Scorecard, PEP 621, json.dumps separators).
- Session 2: four grok-fleet tasks + six native lanes + official page reads.
- Material session-2 changes: ship `verify`; lazy Deponent adapter; zip excludes; loader `..` reject; path redaction; keep exits 0/1/2; no REUSE gate; no official agent-gate suite.

## Wave 2–3 — doctrine / architecture (done, amended in session 3)

- D-003 optional adapter; D-004 verify; D-005 release hygiene.
- D-006 v0 cuts; D-007 spec §7/appendix command retarget.
- USER_JOURNEYS.md (A–D) binding.
- Doctrine §13 re-audited against the shipped face; §16 session-3 addendum.

## Wave 4 — implementation (session 3 product-face)

- README doctrine order; repository-root contract.
- `selfcheck` → `HARNESS_OK` (not a kernel certification).
- CLI refuses `--certify` on `fixture-*` kernels (exit 2).
- `examples/adapter_skeleton.py` (raises; not a mark).
- spec §7.1 / Appendix A/B retargeted to `gak_conformance`. Frozen digest untouched.
- pytest **65 passed**, 1 skipped (live Deponent).

## Wave 5 — verification (in progress this session)

- `tests/test_journeys.py` locks Sequence A, spec §7.1, clone-to-run, skeleton FAIL, v1 table.
- Independent QA of ITER-0003–0006 pending at write time.

## Wave 8 — local release (rebuilt)

- `.builder-foundry/release/artifact.zip`
- SHA-256 `2091e6aaac4676380418e96bf2e1819764dafa8bce8d99db91921065a86af0fc`
- `forbidden_scan=pass`; smoke help+selfcheck+fixture score; zip contains `examples/adapter_skeleton.py`.

## Guard

Expected FAIL until min sessions (4), holdout, red-team loop file, independent iteration review, remaining waves.

## Remote mutation

None. No push, PR, publish, or deploy.
