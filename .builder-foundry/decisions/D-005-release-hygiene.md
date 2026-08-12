# D-005 — Leave-behind is product+zip, not the campaign tree

- **Date:** 2026-08-12
- **Wave:** research → implementation
- **Status:** accepted
- **Author lane:** research-s02
- **Sources:** Apache-2.0 §4d; PEP 639; git-archive export-ignore; kit `safe_release_zip.py`

## Decision

1. **Product scan** (FEAT-0007): `gak_conformance/`, `scripts/`, `tests/`, `v1/`, `README.md`, `LICENSE`, `NOTICE`, `pyproject.toml`. Needles: `deponent/attest.py`, `00Agent`, `cds-compliance`, `CMMC-RMF`, `ATO-in-a-Box`, `per-control map`, `/Users/cj`, `marathon.pid`, `BEGIN PRIVATE KEY`. Do **not** fail the product scan because `.builder-foundry/` names those tokens.
2. **Zip** (FEAT-0027/0028): kit `create_release.py` plus excludes for `MISSION_FOUNDRY_GAK_V0.md`, `AGENTS.builder-foundry.md`, `.agents/*`, `.claude/*`, `.grok/*`. Smoke with `PYTHONPATH=.`.
3. **Git:** add `export-ignore` for campaign/kit/agent dirs. Do **not** gitignore all of `.builder-foundry/` (campaign state is the ledger). Ignore untracked mission/kit face files so `git add -A` cannot stage them.
4. **License metadata:** PEP 639 `license = "Apache-2.0"` + `license-files`.
5. **REUSE 3.3:** optional hygiene, not a v0 gate.

## Rejected

- Treating zipper-clean as `git add -A`-safe.
- Shipping mission/campaign host paths in the public zip.
- Full REUSE annotation of every file this wave.
