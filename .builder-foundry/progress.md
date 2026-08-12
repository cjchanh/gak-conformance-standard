# Builder Foundry Progress

- Campaign: `mission-gak-v0-standard-20260812`
- Profile: `standard`
- Branch: `foundry/gak-v0-standard`
- Initialized: 2026-08-12T17:53:08Z
- Session 2 (this file): primary-source research fan-out + evidence-backed product changes

## Wave 0 — baseline (done)

- HEAD `e55b068` preserved; dirty untracked foundry install recorded, not destroyed.
- Contract lock `2bab65ac…` matches; amendments none.

## Wave 1 — research (session 1 + session 2)

- Session 1: receipt/clause/packaging (SLSA, Scorecard, PEP 621, json.dumps separators).
- Session 2: four grok-fleet tasks + six native lanes + official page reads.
- Material session-2 changes: ship `verify`; lazy Deponent adapter; zip excludes; loader `..` reject; path redaction; keep exits 0/1/2; no REUSE gate; no official agent-gate suite.

## Wave 2–3 — doctrine / architecture (done, amended)

- D-003 optional adapter; D-004 verify; D-005 release hygiene.
- Doctrine Sequence A token aligned to shipped `PassingActionAdapter`.

## Wave 4 — implementation (session 2 closed remaining critical/high)

- `verify`, `list-clauses`, `DeponentKernelAdapter`, loader grammar, CWE-209 redaction.
- pytest **44 passed**, 1 skipped (live Deponent).
- Features 44/44 pass in the ledger (live Deponent score is the skip path).

## Wave 8 — local release (artifact built)

- `.builder-foundry/release/artifact.zip`
- SHA-256 `81d92f14168096dc2cb11dbd484da208387df4b91b087556eb2807f2957eeda2`
- `forbidden_scan=pass`; smoke help+selfcheck+fixture score pass.

## Guard

Expected FAIL until min sessions (4), holdout, red-team, remaining iteration quota, independent review.

## Remote mutation

None. No push, PR, publish, or deploy.
