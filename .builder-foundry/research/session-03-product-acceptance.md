# Session 3 — product acceptance (measured)

**Date:** 2026-08-12  
**Role:** product director  
**Independent QA:** AUTOMATED_WORTH_TESTING (not quality proven)

## What a stranger can now do

From the repository root, no Deponent, no pip:

```
python3 -m gak_conformance --help          # exit 0
python3 -m gak_conformance selfcheck       # HARNESS_OK on stderr
python3 -m gak_conformance score --adapter gak_conformance.fixtures.action_gate:PassingActionAdapter --out receipt.json
```

Empty cwd: `No module named gak_conformance` (documented).

## Cuts that changed the product (D-006)

- No second CLI / required PYTHONPATH
- No selfcheck `GAK-conformant` banner
- No fixture `--certify`
- No v1.1 sworn rows in the primary table
- No receipt-schema fork (`harness_fixture` field)

## Spec (D-007)

§7.1 and Appendix A/B commands retargeted to `gak_conformance`.  
Frozen digest `de6b7089…` still in spec. `check_consistency` exit 0.

## Worth-testing (independent-qa-s03-post)

| Dimension | Score |
|---|---|
| First-use | PASS |
| Trust | PASS |
| Reuse | PASS |

Call: **AUTOMATED_WORTH_TESTING**.

## Not closed

- Live Deponent 13-clause re-score in this environment
- Third-party verdicts: zero
- Fabricated adapters (spec §6.3)
- Final audit wave / foundry_guard session quota
