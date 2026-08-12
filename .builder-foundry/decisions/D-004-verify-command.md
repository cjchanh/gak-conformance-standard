# D-004 — `verify` is the §5.4 tool; `digest` is not

- **Date:** 2026-08-12
- **Wave:** research → implementation
- **Status:** accepted
- **Author lane:** research-s02
- **Sources:** spec §5.4; SLSA verifying-artifacts v1.2; Sigstore threat model; doctrine Sequence C

## Decision

Ship:

```text
python3 -m gak_conformance verify --adapter module:Class --cert FILE
```

1. Load adapter (fail → exit 2, no receipt).
2. Run the in-repo harness.
3. Re-derive §5.3 digest.
4. Compare to the certification’s `clauses_digest`.
5. Exit **0** only if §3.4 conformant **and** digest matches.
6. Exit **1** if live score is not conformant **or** digest mismatches (including a now-conformant kernel vs a stale cert).
7. Exit **2** if the cert cannot be parsed or has no `clauses_digest`.

`digest --receipt` remains a file re-hash (no kernel). `--certify` remains “emit a new cert.” Neither is verification.

Keep CLI exits **0 / 1 / 2**. Do not require signatures.

## Rejected

- Declaring `score` + `digest` sufficient for §5.4.
- Architecture’s CLI table that omitted `verify`.
- Cosign/DSSE as a v0 gate.
- Research’s 3/4 exit split (doctrine 0/1/2 wins).

## Follow-through

FEAT-0039, FEAT-0040 (`--help` names `verify`).
