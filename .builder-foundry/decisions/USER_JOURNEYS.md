# USER_JOURNEYS — GAK v0 (binding)

**Date:** 2026-08-12  
**Owner:** product-director  
**Paired with:** DESIGN_DOCTRINE.md, D-006, D-007

A journey is user-observable. If a test cannot fail it, it is not a journey.

## Journey A — stranger, no Deponent (first-run)

**Who:** category skeptic. CPython + this clone. No pip. No Deponent.

**Steps (repository root):**

```text
python3 -m gak_conformance --help
python3 -m gak_conformance selfcheck
python3 -m gak_conformance score \
  --adapter gak_conformance.fixtures.action_gate:PassingActionAdapter \
  --out receipt.json
```

**Pass when:**

- `--help` exit 0; names score, selfcheck, verify, list-clauses, digest
- `selfcheck` exit 0; stderr contains `HARNESS_OK` and `not a kernel certification`
- `selfcheck` does not print `GAK-conformant`
- `receipt.json` is §5.1; `kernel` starts with `fixture-`; 13 clauses; no timestamp
- README first 40 lines contain the bound (research prototype / not secure / not audited / not endorsed) and "repository root"
- First fenced block does not mention `deponent.badge`

**Fail when:** command requires Deponent, pip, or a hidden `PYTHONPATH` from the repo root.

**Wrong-cwd contract:** from an empty directory, `python3 -m gak_conformance` exits nonzero with `No module named gak_conformance`. That is expected, not a crash.

## Journey B — score your kernel (the job)

**Who:** kernel author with a real gate.

**Steps:**

1. Copy `examples/adapter_skeleton.py`.
2. Drive the real kernel. Methods that still raise score FAIL.
3. `python3 -m gak_conformance score --adapter your_pkg.adapter:YourAdapter --out receipt.json --certify`
4. Exit 0 / 1 / 2 per the table.

**Pass when:** switching `--adapter` needs no new conceptual model; skeleton cannot earn a fabricated PASS.

## Journey C — verify a published claim

```text
python3 -m gak_conformance verify \
  --adapter your_pkg.adapter:YourAdapter \
  --cert certification.json
```

**Pass when:** matching digest + live conformant → 0; stale digest → 1 even if live kernel is conformant; unloadable adapter → 2.

`digest --receipt FILE` is **not** Journey C. It does not re-run the kernel.

## Journey D — Deponent if present (not first-run)

```text
python3 -m gak_conformance score \
  --adapter gak_conformance.adapters.deponent:DeponentKernelAdapter \
  --out deponent-receipt.json
```

**Pass when:** labeled optional; absent Deponent → exit 2, not a harness crash; README places this below A/B/C; third-party count stays zero.

## Recovery journeys (must stay visible)

| Situation | User sees | Exit |
|---|---|---|
| Not in repository root | `No module named gak_conformance` | ≠0 |
| Bad `--adapter` | `BLOCKED:` + reason | 2 |
| Brick / all-NA / any FAIL | receipt with `conformant: false` | 1 |
| Fixture used as a public mark | HARNESS_OK + README void language | 0 on selfcheck only |

## Out of v0 journeys

Install from PyPI. Badge gallery. Language-neutral CLI. Sandboxed adapters. Scoring v1.1 by default.
