# D-007 — Spec §7 / appendix command retarget

**Status:** binding  
**Date:** 2026-08-12  
**Author lane:** product-director  
**Authority:** `.builder-foundry/decisions/ARCHITECTURE.md` — "Spec text: v1 clauses frozen; §7 docs retarget is allowed."

## Problem

`v1/spec.md` §7.1 still tells authors:

```python
from deponent.conformance import run_conformance
```

Appendix A still documents `python3 -m deponent.badge verify --kernel deponent` as the fail-closed verification command. Appendix B still lists `python3 -m deponent.conform --list-clauses`.

A stranger who follows the **normative spec** (not just the README) is sent to Deponent internals. That contradicts the mission and Sequence B.

## Cut vs edit

| Surface | Action |
|---|---|
| §4 clause text, profiles, capability gates | **KEEP** — frozen |
| §5.1 / §5.2 / §5.3 schema and digest `de6b7089…` | **KEEP** — frozen |
| §3.4 verdict math | **KEEP** — frozen |
| §1 sentence "The reference harness ships with Deponent" | **KEEP** — ratified 2026-07-03 term. Historical. Do not pretend the ratification never said it. |
| §7.1 step 4 code sample | **RETARGET** to `from gak_conformance import run_conformance` plus the CLI one-liner |
| Appendix A verify command | **RETARGET** to `python3 -m gak_conformance verify --adapter … --cert …` |
| Appendix B list-clauses | **RETARGET** to `python3 -m gak_conformance list-clauses` |
| Historical Deponent commands | One-line footnote: kernel-local, not the category entrypoint |

## Non-goals

- Do not change the published evidence JSON.
- Do not change `check_consistency.py` frozen-digest assertion.
- Do not add v1.1 as the default face.
- Do not claim the spec was always vendor-hosted.

## Verification

- Frozen digest string still in spec.md
- `python3 scripts/check_consistency.py` exit 0
- First Python fence after `### 7.1` imports `gak_conformance`, not `deponent.conformance`
- Appendix A primary fence is `gak_conformance verify`
