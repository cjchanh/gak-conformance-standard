# D-006 — GAK v0 cut list (session 3)

**Status:** binding  
**Date:** 2026-08-12  
**Author lane:** product-director  
**Why now:** Session-2 shipped a working scorer. Session-3 is acceptance and cut. The ledger marked 44/44 pass; first-use still failed doctrine §4 / §10 on reading load, repo-root contract, fixture-as-mark, and spec §7.1 still pointing at Deponent.

Cuts are refusals, not backlog. Do not implement these in v0.

## CUT (will not ship)

| ID | Cut | Why | What we ship instead |
|---|---|---|---|
| CUT-01 | Second CLI (`scripts/gak.py`, `gak` wrapper as a competing face) | Doctrine: one primary command. Two names split the product. | `python3 -m gak_conformance` from the **repository root** |
| CUT-02 | Hidden `PYTHONPATH=.` as a required first-run step | Hidden env is a first-use failure. Measured: repo-root works; `/tmp` cwd fails with `No module named gak_conformance`. | Document repository-root. Optional PYTHONPATH only if invoking from another directory. |
| CUT-03 | `selfcheck` printing `CONFORMANT` / `GAK-conformant` as a banner | Fixture selfcheck is a harness probe, not a public mark (spec §6.3 / §8). | stderr: `HARNESS_OK … (not a kernel certification)`. stdout stays §5.1 JSON. |
| CUT-04 | `explain-receipt` subcommand | Reading-load. Receipt fields fit in one README table. | README "How to read a receipt" |
| CUT-05 | Badge gallery / kernel directory / leaderboard | Mission non-goal. Inflates adoption. | Third-party count stays **zero** |
| CUT-06 | `[project.optional-dependencies] deponent` | Makes the kernel look like it owns the standard (HYP-0012). | `find_spec` + exit 2 |
| CUT-07 | v1.1 sworn evidence in the primary artifact table | v0 face is frozen 13-clause v1. Table was teaching the amendment. | v1 Deponent pack in the table; v1.1 / sworn in Status only |
| CUT-08 | Duplicate "score your kernel" command fence above the fold | First 40 lines must be Sequence A + bound, not Sequence B + digest trivia. | Sequence B once, after how-to-read |
| CUT-09 | Language-neutral CLI claim | `--adapter module:Class` is Python. | Honest Python-v0 sentence |
| CUT-10 | Adapter sandbox / pickle / plugin directory | Residual import-exec is documented, not hidden. | Grammar reject (`..`, paths) already shipped |
| CUT-11 | Full REUSE 3.3 as a v0 gate | D-005. | LICENSE + NOTICE + PEP 639 |
| CUT-12 | Editing frozen clause text, §3.4 math, or digest `de6b7089…` | Would fork the standard. | §7.1 / Appendix A/B **command** retarget only (D-007) |
| CUT-13 | Publishing fixture receipts as certifications | Void mark (spec §6.3). | Kernel name `fixture-*` + README + HARNESS_OK |
| CUT-14 | Rewriting Deponent / flipping visibility / PyPI | Mission exclusion. | Optional adapter when present |
| CUT-15 | Web UI, Assurance UI, attest/compliance maps | Leave-behind must stay public-safe. | Spec + harness + adapter + one evidence pack |

## KEEP (already decided; do not reopen)

- Frozen `gak-conformance/v1` default (13 clauses)
- Exit table 0 / 1 / 2
- Digest default separators (not compact)
- Stdlib-only runtime
- Optional Deponent adapter, no extra
- Third-party verdicts: zero
- Bounded mark language (spec §8)
- `verify --adapter --cert` is the §5.4 tool; `digest --receipt` is file re-hash only

## Acceptance consequence

A feature that implements a CUT is a defect. Journey tests must lock CUT-01, CUT-02, CUT-03, CUT-07, CUT-08, CUT-13.
