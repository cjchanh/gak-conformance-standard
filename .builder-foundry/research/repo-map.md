# GAK repo map (read-only archaeology)

Campaign `mission-gak-v0-standard-20260812`. Head `e55b068` (`main`).
Writable root: this repo only. Siblings Deponent / Sworn were read, not copied.

## 1. Tracked tree vs untracked foundry install

**Tracked product (published standard; no Python package):**

| Path | Role |
|---|---|
| [`v1/spec.md`](../../v1/spec.md) | Normative standard |
| [`v1/evidence/`](../../v1/evidence/) | Author self-score pack (12 files) |
| [`scripts/check_consistency.py`](../../scripts/check_consistency.py) | Spec ↔ live-Deponent checker |
| [`README.md`](../../README.md) | User journeys (Deponent-hosted) |
| [`LICENSE`](../../LICENSE), [`NOTICE`](../../NOTICE) | Apache-2.0 |

**Absent from tree:** `gak_conformance/`, `pyproject.toml`, `tests/`, fixture adapter, in-repo score CLI.

**Untracked foundry install** (baseline porcelain 2026-08-12T17:53:07Z):
`.builder-foundry/`, `.builder-foundry-kit/`, `.agents/skills/builder-foundry/`,
`.claude/skills/builder-foundry/`, `.grok/skills/builder-foundry/`,
`AGENTS.builder-foundry.md`, `MISSION_FOUNDRY_GAK_V0.md`.

## 2. Frozen v1 spec (cite [`v1/spec.md`](../../v1/spec.md))

**IDs:** `gak-conformance/v1`, certification schema `gak-certification/v1`.

**Profiles:** kernel declares exactly one of `action-gate` | `commit-gate`.
Clauses also use `universal`.

**Capabilities:** optional `reconcile`, `attest`. v1.1 adds optional `content-blind-audit`.

**13 frozen v1 clauses**

| ID | Profile | Requires |
|---|---|---|
| `GAK-CHAIN-INTACT` | universal | — |
| `GAK-TAMPER-EVIDENT` | universal | — |
| `GAK-ATTEST-HONEST` | universal | `attest` |
| `GAK-DENY-DEFAULT` | action-gate | — |
| `GAK-ALLOW-INBOUNDS` | action-gate | — |
| `GAK-PATH-CONTAINMENT` | action-gate | — |
| `GAK-DESTRUCTIVE-FLOOR` | action-gate | — |
| `GAK-PROGRAM-ALLOWLIST` | action-gate | — |
| `GAK-JAIL-FAILS-CLOSED` | action-gate | — |
| `GAK-RECONCILE-UNDECLARED` | action-gate | `reconcile` |
| `GAK-COMMIT-DENY-SECURITY` | commit-gate | — |
| `GAK-COMMIT-ALLOW-CLEAN` | commit-gate | — |
| `GAK-COMMIT-TESTIFIES` | commit-gate | — |

**v1.1 optional 14th:** `GAK-AUDIT-CONTENT-BLIND` — universal, requires `content-blind-audit`, method `audit_is_content_blind()`. Harness id `gak-conformance/v1.1`. **v0 ships frozen v1 (13), not 14.**

**§3.4 verdict:** conformant iff no FAIL and ≥1 PASS. Erroring check = FAIL. Out-of-profile / unclaimed capability = NA.

**§5.1 receipt fields:** `kernel`, `profile`, `conformant`, `counts` `{pass,fail,na}`, `clauses[]` `{id,profile,status,detail}`. **No timestamp.** 13 clause rows for v1.

**§5.3 digest:** sort `(id,status)` lex; JSON `{"clauses":[[id,status],...],"harness":"gak-conformance/v1","kernel":"<name>"}` via `json.dumps(..., sort_keys=True)`; SHA-256 UTF-8 hex lowercase. Worked v1: `de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406`. v1.1: `cf26befe5ad50a18afb427e7257f9272142873ac11879cf2ab81b90eaedbf664`.

**§6 adapter**

- Attrs: `name:str`, `profile:str`, `supports:frozenset[str]`
- Universal: `clean_chain_verifies() -> bool`, `tamper_is_detected() -> bool`
- Action-gate: `verdict(tool, params) -> "ALLOW"|"BLOCK"`, `jail_fails_closed() -> bool`
- Optional: `reconcile_catches_undeclared()`, `attest_abstains_when_unproven()`
- Commit-gate: `commit_verdict(files) -> "ALLOW"|"BLOCK"`, `commit_testifies(files) -> bool`
- Raise → clause FAIL.

Anchor tools (literal): `definitely_not_a_real_tool`; `write_file` `ok.txt` / `../escape.py`; `run_cmd` `rm -rf /` / `ftp some.host`; commit `["crypto/vault.py"]` / `["README.md"]`.

## 3. `scripts/check_consistency.py` ↔ Deponent

Exact imports:

```
from deponent.badge import HARNESS_VERSION, certify
from deponent.conformance import CLAUSES
import sworn   # optional; NOTICE if evidence exists but import fails
```

Uses `certify("deponent")` (twice) and, if sworn importable, `certify("sworn")`.
Compares live `CLAUSES` ids/profiles/`requires` to `**GAK-…**` headings in spec.
Picks evidence `deponent-certification.json` or `deponent-certification-v1.1.json` from live `HARNESS_VERSION`.

**Exit 3** (fail-closed, cannot check): spec missing, or `ImportError` on `deponent.badge` / `deponent.conformance`. Exit 1 = inconsistency. Exit 0 = consistent.

This coupling **is the mission defect.** Scorer must not live behind those imports.

## 4. README journeys vs mission

README tells a stranger to:

1. Install **Deponent**, then `python3 -m deponent.badge verify --kernel deponent`
2. Implement §6 and run **Deponent’s** harness (`from deponent.conformance import run_conformance` in spec §7.1)

Mission requires: `python3 -m gak_conformance score --adapter <module:Class> [--out receipt.json]` plus offline `--help` / fixture selfcheck **with no Deponent install**.

Gap: user-facing score path is still the reference kernel’s package.

## 5. Evidence pack (`v1/evidence/`)

| File | Version | Content |
|---|---|---|
| `deponent-conformance-receipt.json` | v1 | 10P/0F/3NA, 13 clauses, action-gate |
| `deponent-certification.json` | v1 | digest `de6b7089…`, harness `gak-conformance/v1` |
| `deponent-verify-output.txt` | v1 | EARNED, exit 0 |
| `determinism-proof.txt` | v1 | two runs same digest; deponent `@ e7e8fe6` |
| `harness-clause-list.txt` | v1 | 13 clauses (matches spec §4) |
| `deponent-conformance-receipt-v1.1.json` | v1.1 | 11P/0F/3NA, **14** clauses |
| `deponent-certification-v1.1.json` | v1.1 | digest `cf26befe…` |
| `deponent-verify-output-v1.1.txt` | v1.1 | EARNED 11/3 |
| `determinism-proof-v1.1.txt` | v1.1 | identical `cf26befe…` |
| `harness-clause-list-v1.1.txt` | v1.1 | 14 clauses (+ `GAK-AUDIT-CONTENT-BLIND`) |
| `sworn-conformance-receipt-v1.1.json` | v1.1 | sworncode commit-gate, 5P/0F/9NA |
| `sworn-certification-v1.1.json` | v1.1 | digest `e65dd28b…` |

No sworn **v1** (13-clause) receipt. Author self-scores ≠ third-party verdict.

## 6. Sibling Deponent — public score surface only

Repo: `/Users/cj/Workspace/active/deponent`. Do **not** copy private files.

**Public (use later to *score* Deponent, not to *be* the harness):**

| Module | Symbols |
|---|---|
| `deponent/adapters/contract.py` | `KernelAdapter` (Protocol) |
| `deponent/adapters/deponent.py` | `DeponentAdapter` (`name="deponent"`, `profile="action-gate"`, `supports` `{attest, content-blind-audit}` + `reconcile` if `deponent.reconcile` importable) |
| `deponent/adapters/sworn.py` | `SwornAdapter` (`name="sworncode"`, `profile="commit-gate"`, `supports=frozenset()`) |
| `deponent/adapters/__init__.py` | `BUILTIN_ADAPTERS = {"deponent": DeponentAdapter, "sworn": SwornAdapter}` (+ optional `provenant-rs`) |
| `deponent/conformance.py` | `Clause`, `ClauseResult`, `ConformanceReceipt`, `CLAUSES`, `run_conformance(kernel, clauses=CLAUSES) -> ConformanceReceipt` |
| `deponent/conform.py` | CLI `--kernel` / `--list-clauses` / `--out` |
| `deponent/badge.py` | `HARNESS_VERSION="gak-conformance/v1.1"`, `certify`, `verify`, CLI exit 0/1/2 |
| `deponent/sworn_adapter.py` | re-exports `SwornAdapter`; runs `run_conformance` |

**`run_conformance`:** for each clause: if profile ∉ {`universal`, `kernel.profile`} → NA; if `requires` not in `kernel.supports` → NA; else `bool(check(kernel))`; exception → FAIL. `conformant` = no FAIL and ≥1 PASS. `to_dict()` matches §5.1.

**Registration:** drop a class in `deponent/adapters/` and add it to `BUILTIN_ADAPTERS` (Deponent-owned). GAK v0 must accept `module:Class` instead.

**Do not copy (path names only):** `deponent/attest.py`, `deponent/operator_attest.py`, `deponent/selfgate.py`, `00Agent`, `cds-compliance`, CMMC/RMF maps. Wheel already excludes `deponent/attest.py`.

**Adapter private coupling (names only; DeponentAdapter drives real kernel):** `deponent.gate.Gate`, `deponent.cell.Cell`, `deponent.ledger.Ledger`, `deponent.cell.jail_available` (patched), `deponent.reconcile`, `Cell.attest()`.

**Drift vs frozen v1:** live `CLAUSES` has **16** rows — spec 13 + `GAK-AUDIT-CONTENT-BLIND` + **`GAK-REDIRECT-DENIED`** + **`GAK-NEWLINE-CHAINED`** (not in `v1/spec.md`). Do **not** copy live `CLAUSES` into GAK v0.

## 7. Sibling Sworn — no in-tree GAK adapter

Repo: `/Users/cj/Workspace/active/sworn`. Package `sworn` (`src/sworn/`), version 0.4.0. `__init__.py` exports only `__version__`.

**Public kernel surface the existing adapter already uses:**

| Path | Symbol |
|---|---|
| `sworn/config.py` | `load_config(repo_root) -> SwornConfig` |
| `sworn/pipeline.py` | `run_pipeline(repo_root, files, config) -> PipelineResult` (`decision` `PASS`\|`BLOCKED`) |
| `sworn/evidence/log.py` | `verify_chain(log_path) -> (bool, str)`, `read_entries(log_path)` |

Adapter lives **only** in Deponent (`SwornAdapter`). Mapping: `PASS`→`ALLOW`, else `BLOCK`.

**Do not copy:** `sworn/kernels/cmmc/*`, `sworn/evidence/cmmc_report.py`.

## 8. Known measured failures

- No `gak_conformance` module.
- Default Python cannot import `deponent` or `sworn`.
- `scripts/check_consistency.py` takes **exit 3** on that ImportError.

## 9. Writer leases (recommended)

| Lease | Paths | Bound |
|---|---|---|
| **scorer** | `gak_conformance/` (new), `pyproject.toml` | v1 13 clauses, §5.1 receipt, §5.3 digest, `python3 -m gak_conformance score --adapter …`, fixture `--help`/selfcheck. **Do not import `deponent.*` as the harness.** |
| **checker** | `scripts/check_consistency.py` | Point at in-repo scorer + frozen evidence; keep exit 3 = cannot check. |
| **docs** | `README.md` | Stranger journey = in-repo score command, not `deponent.badge`. |
| **fixtures** | `gak_conformance/fixtures/` or `fixtures/` | Fake adapter; no sibling install. |
| **tests** | `tests/` | Census=13, digest algo, NA/FAIL/§3.4, determinism, no-deponent import. |
| **spec** | `v1/spec.md` | **Frozen.** No clause add/rename. v1.1 stays optional. |
| **evidence** | `v1/evidence/` | Refresh only after a live **v1** (13-clause) score. Keep v1.1 files; do not treat as v0 acceptance. |

**Out of lease:** sibling repos; `.builder-foundry/{contract,claim,feature,hypothesis}*`; private Deponent/Sworn paths above; push/PyPI/visibility.
