# D-008 — Inbound artifact contract (receipt ≠ certification)

- **Date:** 2026-08-12
- **Wave:** architecture
- **Status:** accepted
- **Author lane:** architecture-s04
- **Sources:** spec §5.1 / §5.2 / §5.4; measured type-confusion (`EVID-ARCH-TYPE`); SLSA v1.2 verifying-artifacts (predicateType check); D-004; CUT-04

## Decision

CLI inbound JSON is typed.

1. `digest --receipt` accepts a **§5.1 receipt** only. A certification, a timestamped object, or a clause census that does not match `--harness` is exit **2**. No hash is printed.
2. `verify --cert` accepts a **§5.2 certification** only. A receipt is exit **2** with a type name, not `BLOCKED: 'clauses_digest'`.
3. `verify` **inherits** `harness_version` from the certification. `--harness` is optional. A conflicting flag is exit **2** (usage), not exit **1** (kernel drift).
4. A certification whose `clauses_digest` does not match its own clause pairs is exit **2** **before** the adapter is imported.
5. A self-consistent certification for a different kernel that does not match the live re-score remains exit **1** (D-004 / §5.4).
6. `clauses_digest()` stays a pure function. The contract is a CLI / `artifacts.py` gate. No `explain-receipt` command (CUT-04).
7. Stdlib only. `v1/receipt.schema.json` and `v1/certification.schema.json` document the shapes; runtime does not depend on jsonschema.

## Why now

Measured 2026-08-12 (HEAD `5dfbe5f`):

- `digest --receipt` of a v1.1 receipt or certification under default v1 printed `d35b3247…` and exited 0. Published v1.1 identity is `cf26befe…`.
- `verify --cert` of a receipt exited 2 with `BLOCKED: 'clauses_digest'`.
- `verify` of a v1.1 fixture certification without `--harness` exited 1 mismatch (false kernel drift).

## Rejected

- Auto-detect harness from clause count (hides the error).
- Allow digest of either object (fake verifier).
- New inspect/explain subcommand (CUT-04).
- Signatures, DSSE, TSA, network (mission: offline SHA-256).
- Exit 1 on type confusion (that is "could not hash/score").
- Weakening D-004: published digest is still not a waiver when the cert is self-consistent.

## Follow-through

FEAT-0052–0057. Tests in `tests/test_artifacts.py`. Oracle: published v1 receipt still digests to `de6b7089…`.
