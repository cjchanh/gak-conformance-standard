# D-003 — Optional Deponent adapter is a lazy wrap, not a harness import

- **Date:** 2026-08-12
- **Wave:** research → implementation
- **Status:** accepted
- **Author lane:** research-s02
- **Sources:** CPython importlib 3.14.7; PEP 621; ARCHITECTURE.md §9; F-28–F-30

## Decision

Ship `gak_conformance.adapters.deponent:DeponentKernelAdapter`.

- Module import does **not** import Deponent.
- `__init__` probes `importlib.util.find_spec("deponent")` then
  `importlib.import_module("deponent.adapters.deponent")` (string form).
- Wrap `DeponentAdapter` only. Intersect `supports` with `{reconcile, attest}`.
- Do not forward `audit_is_content_blind`. Do not import `deponent.conformance` / `deponent.badge`.
- Absent Deponent → `ImportError` → CLI exit 2 with a skip message.
- No `[project.optional-dependencies] deponent`.
- Do not edit `tests/test_import_boundary.py` to allow `import deponent`.

## Rejected

- Top-level `import deponent` (fails AST isolation; loads vendor at `import gak_conformance.adapters.deponent`).
- Narrowing the AST scan so a real import is allowed.
- `deponent` extra (vendor-named install path).
- Subprocess isolation (runpy is not a sandbox; overbuild).
- Treating live 16-clause Deponent `CLAUSES` as the GAK table.

## Follow-through

FEAT-0026. Tests always cover the absent path. Live score is `importorskip`.
