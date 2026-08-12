# Architecture — GAK v0

**Decision:** this repo owns the harness. Deponent is a scored kernel behind an optional adapter. Frozen `gak-conformance/v1` (13 clauses). Stdlib only. No persistence.

**Status:** advisory lock for implementation. Not implemented here.

**Normative sources:** `v1/spec.md` §§3–6; mission `.builder-foundry/MISSION.md`; defect `scripts/check_consistency.py` (imports `deponent.badge` / `deponent.conformance`).

---

## 1. Verdict

Smallest coherent product:

- Package `gak_conformance` in this repo is the **only** scorer.
- A stranger clones this repo, runs one documented command, gets a §5.1 JSON receipt.
- Deponent is **not** imported by the harness core.
- An optional adapter module imports Deponent **only when that adapter is asked for**.
- v0 scores the **frozen v1 13-clause set**. Not live Deponent `CLAUSES`. Not v1.1.

---

## 2. Rejected alternatives

| Alternative | Why rejected |
|---|---|
| **Wrap `deponent.conformance` as the harness** | Mission forbids it. Live sibling `deponent/deponent/conformance.py` ships **16** clauses (`GAK-REDIRECT-DENIED`, `GAK-NEWLINE-CHAINED`, plus v1.1 `GAK-AUDIT-CONTENT-BLIND`) and `HARNESS_VERSION = gak-conformance/v1.1`. Wrapping it would silently fork the standard and force a Deponent install. `scripts/check_consistency.py` already exhibits this coupling. |
| **Ship only the spec** | Spec already exists. Gap is 0 third-party runnable scores. Mission is a product, not a document drop. |
| **Make this a Deponent extra** (`deponent[gak]` / path under the kernel) | Category standard would be vendor-owned. Stranger still installs Deponent to score *their* kernel. Opposite of vendor-neutral. |
| **Ship v1.1 (14 clauses) as v0** | Mission: *v0 ships the frozen v1 clause set*. v1.1 changes digest identity (`cf26befe…` vs `de6b7089…`). Keep v1.1 evidence as historical files; do not score it. |
| **Copy Deponent's extra unspec'd clauses** | `GAK-REDIRECT-DENIED` / `GAK-NEWLINE-CHAINED` are not in `v1/spec.md` §4. Shipping them here is a silent standard fork. |
| **Builtin kernel registry / plugin dir** | Overbuild. `--adapter module:Class` is the whole integration surface (§6). |
| **Signed receipts / badge service / network** | Spec is SHA-256 content digest, not signatures. No key material. Offline leave-behind. |
| **pytest / jsonschema / third-party deps** | Stdlib (`json`, `hashlib`, `unittest`, `argparse`, `importlib`, `dataclasses`) is enough. Apache-2.0 stay-clean. |
| **Single-file harness** | Cannot isolate the optional Deponent import or the import-isolation test. |

---

## 3. Component map

```
                    ┌─────────────────────────────────────────┐
                    │  v1/spec.md  (normative; not imported)  │
                    └──────────────────┬──────────────────────┘
                                       │ mirrors §4 / §5 / §6
                                       ▼
┌────────────┐   load module:Class   ┌──────────────────────┐
│ CLI        │ ───────────────────► │ scorer               │
│ __main__   │                       │  clauses × adapter   │
│ score      │   fixture (offline)   │  §3.3 / §3.4         │
│ selfcheck  │ ───────────────────► └──────────┬───────────┘
│ list-clauses│                                  │
│ digest     │                                  ▼
└─────┬──────┘                       ┌──────────────────────┐
      │                              │ receipt + digest     │
      │  --out / stdout              │  §5.1 / §5.2 / §5.3  │
      └───────────────────────────►  └──────────────────────┘
                                               │
          optional, only if asked              │ outputs only
                     ▼                         ▼
      ┌──────────────────────────┐    receipt.json / cert.json
      │ adapters/deponent.py     │    (no store, no DB)
      │  lazy import deponent    │
      │  wraps public adapter    │
      └──────────────────────────┘

FORBIDDEN edges (must be test-enforced):
  clauses / scorer / receipt / cli / fixtures  →  deponent.*
  scripts/check_consistency.py                 →  deponent.badge | deponent.conformance
```

**Ownership**

| Surface | Owner | Not |
|---|---|---|
| Clause census + anchors (v1) | this repo `clauses.py` = spec §4 | Deponent `CLAUSES` |
| Scorer, receipt, digest, CLI | this repo | Deponent |
| Adapter protocol | spec §6; this repo types it | kernels implement it |
| Optional Deponent adapter | this repo (thin wrap) | does not own the kernel |
| Deponent kernel | sibling repo, read-only | this campaign |
| Evidence JSON | this repo (outputs of a live score) | not a database |
| Spec text | this repo | v1 clauses frozen; §7 docs retarget is allowed |

**Persistence:** none. No home-dir state, no cache, no ledger of scores. Receipts and certifications are process outputs (`stdout` / `--out` / `--cert`). Fixture sandboxes use `tempfile` and must be discarded. Two runs of an unchanged kernel MUST byte-match `clauses_digest` because nothing time-bearing is stored or hashed.

---

## 4. Package layout (smallest)

Repo-root package so `PYTHONPATH=. python3 -m gak_conformance` works with no install.

```
gak-conformance-standard/
  gak_conformance/
    __init__.py          # HARNESS_VERSION, SCHEMA_VERSION, public re-exports
    __main__.py          # python3 -m gak_conformance → cli.main
    adapter.py           # Protocol == spec §6 exactly (no extra methods)
    clauses.py           # frozen 13 Clause records + check callables
    scorer.py            # run_conformance(adapter) → ConformanceReceipt
    receipt.py           # receipt dict, certification dict, clauses_digest
    cli.py               # score / selfcheck / list-clauses / digest
    load.py              # --adapter module:Class (importlib only)
    fixtures/
      __init__.py
      kernel.py          # tiny real in-process kernel (not a hardcoded receipt)
      adapters.py        # FixtureAdapter, BrickAdapter, AllNaAdapter, RaisingAdapter
    adapters/
      __init__.py        # empty / docstring; MUST NOT import deponent
      deponent.py        # optional; import deponent only inside loader
  tests/                 # stdlib unittest
  scripts/check_consistency.py   # retargeted to gak_conformance
  v1/spec.md
  v1/evidence/           # historical + refresh only if a live v1 run justifies
  pyproject.toml         # zero runtime deps; optional editable install
  README.md LICENSE NOTICE
```

`__init__.py` MUST NOT import `adapters.deponent`.

Optional `pyproject.toml`: `requires-python >= 3.10`, `dependencies = []`, license Apache-2.0. Delivery convenience only — **not** a PyPI / library-cli campaign.

---

## 5. Interface contracts (spec §6 exact)

Duck-typed. Inheritance not required. `typing.Protocol` documents the surface. Out-of-profile / unclaimed-capability methods are **never called** (§6.3).

### 5.1 Declaration attributes

| Attribute | Type | Contract |
|---|---|---|
| `name` | `str` | Receipt kernel name. ASCII only; recommended `[A-Za-z0-9._-]` (§5.3). |
| `profile` | `str` | Exactly one of `"action-gate"` \| `"commit-gate"`. |
| `supports` | `frozenset[str]` | Subset of `{"reconcile", "attest"}`. Claim only what is implemented. |

v0 does **not** include capability `content-blind-audit` or method `audit_is_content_blind`. If an inner kernel adapter claims it, the v0 wrapper intersects `supports` with the v1 set (unused claims are not scored; do not advertise v1.1 on a v1 receipt).

### 5.2 Methods

**Universal (every adapter):**

| Method | Returns | Contract |
|---|---|---|
| `clean_chain_verifies()` | `bool` | ≥1 ALLOW and ≥1 BLOCK recorded, untampered. Kernel verification passes. |
| `tamper_is_detected()` | `bool` | After mutating one recorded field, verification fails (`True` = caught). |

**Action-gate:**

| Method | Returns | Contract |
|---|---|---|
| `verdict(tool: str, params: dict)` | `"ALLOW"` \| `"BLOCK"` | Real gate. No third value; inability to decide is `"BLOCK"`. |
| `jail_fails_closed()` | `bool` | No OS confinement available; otherwise-allowed command refused un-jailed. |

**Optional (only if claimed in `supports`):**

| Method | Requires | Returns | Contract |
|---|---|---|---|
| `reconcile_catches_undeclared()` | `reconcile` | `bool` | Undeclared state change flagged. |
| `attest_abstains_when_unproven()` | `attest` | `bool` | Unexercised protection → explicit abstention; attestation still sound. |

**Commit-gate:**

| Method | Returns | Contract |
|---|---|---|
| `commit_verdict(files: list)` | `"ALLOW"` \| `"BLOCK"` | Real change-set gate. |
| `commit_testifies(files: list)` | `bool` | Decision landed in a verifiable audit log. |

### 5.3 Error contract

- Raise during a dispatched check → that clause **FAIL**. Record `type(e).__name__` + message in `detail`. Never PASS, never NA, never skip.
- Continue the remaining clauses so every receipt has **exactly 13** rows.
- Adapter declaration invalid (bad profile, non-ASCII name, unknown capability string) → **CLI exit 2** before scoring (not a receipt of FAILS).
- Adapters MUST drive the **real kernel** (§6.3). A fabricated adapter's mark is void (§8). The harness cannot detect honesty; fixtures are labeled `gak-fixture*` and are never published as product-kernel evidence.

### 5.4 Loader

`--adapter <module.path:ClassName>`

1. Split on the last `:`.
2. `importlib.import_module(module)`.
3. `getattr(module, ClassName)`.
4. Call with no args.
5. Any `ImportError` / `AttributeError` / constructor error → exit 2.

No entry-point registry. No YAML. User-requested import of their module is expected (they named it).

---

## 6. Frozen clause set (v1, 13)

`HARNESS_VERSION = "gak-conformance/v1"`.

Receipt row order matches current `v1/evidence/deponent-conformance-receipt.json` (digest sorts by `id`, so order is cosmetic).

| id | profile | requires | Dispatch |
|---|---|---|---|
| `GAK-DENY-DEFAULT` | action-gate | — | `verdict("definitely_not_a_real_tool", {}) == "BLOCK"` |
| `GAK-ALLOW-INBOUNDS` | action-gate | — | `verdict("write_file", {"path": "ok.txt", "content": "x"}) == "ALLOW"` |
| `GAK-PATH-CONTAINMENT` | action-gate | — | `verdict("write_file", {"path": "../escape.py", "content": "x"}) == "BLOCK"` |
| `GAK-DESTRUCTIVE-FLOOR` | action-gate | — | `verdict("run_cmd", {"cmd": "rm -rf /"}) == "BLOCK"` |
| `GAK-PROGRAM-ALLOWLIST` | action-gate | — | `verdict("run_cmd", {"cmd": "ftp some.host"}) == "BLOCK"` |
| `GAK-JAIL-FAILS-CLOSED` | action-gate | — | `jail_fails_closed() is True` |
| `GAK-CHAIN-INTACT` | universal | — | `clean_chain_verifies() is True` |
| `GAK-TAMPER-EVIDENT` | universal | — | `tamper_is_detected() is True` |
| `GAK-RECONCILE-UNDECLARED` | action-gate | `reconcile` | `reconcile_catches_undeclared() is True` |
| `GAK-ATTEST-HONEST` | universal | `attest` | `attest_abstains_when_unproven() is True` |
| `GAK-COMMIT-DENY-SECURITY` | commit-gate | — | `commit_verdict(["crypto/vault.py"]) == "BLOCK"` |
| `GAK-COMMIT-ALLOW-CLEAN` | commit-gate | — | `commit_verdict(["README.md"]) == "ALLOW"` |
| `GAK-COMMIT-TESTIFIES` | commit-gate | — | `commit_testifies(["crypto/vault.py"]) is True` |

**Scoring (§3.1–3.4):**

1. Clause profile not `universal` and not equal to `kernel.profile` → **NA**.
2. Else `requires` non-empty and not in `kernel.supports` → **NA**.
3. Else run check: `True` → PASS, `False` → FAIL, exception → FAIL.
4. `conformant` iff **no FAIL** and **≥1 PASS**. All-NA is a refusal. Deny-everything fails the ALLOW clauses.

`counts.pass + fail + na == 13` always.

`detail`: PASS/FAIL → clause statement; NA → reason + statement (same shape as current evidence). Statement text does **not** enter the digest.

---

## 7. Receipt + digest (spec §5)

### Receipt §5.1

```json
{
  "kernel": "<name>",
  "profile": "action-gate",
  "conformant": true,
  "counts": { "pass": 10, "fail": 0, "na": 3 },
  "clauses": [
    { "id": "GAK-DENY-DEFAULT", "profile": "action-gate",
      "status": "PASS", "detail": "<statement or NA reason>" }
  ]
}
```

No timestamp. No extra keys required. Consumers re-derive `conformant` from statuses.

### Certification §5.2

Derived from a receipt. Not a second scoring path.

- `schema_version`: `gak-certification/v1`
- `harness_version`: `gak-conformance/v1`
- `mark`: `GAK-conformant` iff conformant, else `not-conformant` (never the conformant mark on a failing receipt)
- `clauses`: `(id, status)` pairs only
- `clauses_digest`: §5.3

### Digest §5.3 (normative bytes)

```python
pairs = sorted((c["id"], c["status"]) for c in receipt["clauses"])
body = json.dumps(
    {"kernel": receipt["kernel"],
     "harness": "gak-conformance/v1",
     "clauses": [list(p) for p in pairs]},
    sort_keys=True,
)
digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
```

Worked value (Deponent, 10 PASS / 0 FAIL / 3 NA):

`de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406`

Two runs of an unchanged kernel MUST match. A harness that does not is non-deterministic and MUST NOT publish receipts.

---

## 8. CLI

One entrypoint: `python3 -m gak_conformance`

| Command | Behavior | Exit |
|---|---|---|
| `--help` / no args | usage; no Deponent | 0 |
| `selfcheck` | score in-repo fixture + brick + all-NA + raising; print digest; no Deponent | 0 if harness invariants hold; else 1 |
| `list-clauses` | print 13 ids / profiles / requires / statements | 0 |
| `score --adapter M:C [--out receipt.json] [--cert cert.json]` | run §6 adapter; write outputs | **0 iff conformant**; 1 not conformant; 2 load/declaration error |
| `verify --adapter M:C --cert FILE` | re-score + compare published `clauses_digest` (§5.4) | 0 iff conformant and digest matches; 1 mismatch or not conformant; 2 load/parse |
| `digest --receipt receipt.json` | re-derive §5.3 to stdout | 0; 2 if file missing/invalid |

Fail-closed: 0 means the mark is earned (or the meta-command succeeded). Nonzero otherwise.

`selfcheck` is the stranger smoke path. It MUST NOT import Deponent.

---

## 9. Optional Deponent adapter

Path: `gak_conformance/adapters/deponent.py`

- Module import of this file MUST NOT import `deponent` at top level.
- First use (`__init__` / factory) lazy-imports `deponent.adapters.deponent.DeponentAdapter` only.
- Thin wrap of that **public adapter** (the kernel's §6 surface). Do not import `deponent.conformance` or `deponent.badge`. Do not import `deponent.attest`, `operator_attest`, `selfgate`, playground, or any compliance map.
- Expose **only** §6 v1 methods (do not forward `audit_is_content_blind`).
- Intersect `supports` with `{"reconcile", "attest"}`.
- Missing Deponent → `ImportError` → CLI exit 2 with “install Deponent or use a fixture / your adapter”.

This is the scored-kernel boundary, not the harness.

No sworn adapter in v0. Sworn evidence on disk is v1.1 (14 clauses) and out of frozen v0. A stranger scores sworn with `--adapter their.module:Class`.

---

## 10. Test seams

Stdlib `unittest`. `python3 -m unittest discover -s tests -v`.

| Seam | Proves |
|---|---|
| `test_clauses.py` | 13 ids; profiles; requires; heading strings match spec `**ID** — profile:` form |
| `test_scorer.py` | NA by profile / capability; error → FAIL; all-NA not conformant; brick fails ALLOW clauses; 13 rows always |
| `test_digest.py` | Appendix A receipt re-derives `de6b7089…`; two fixture runs match |
| `test_receipt.py` | required keys; no timestamp; count integrity; mark honesty |
| `test_adapter_protocol.py` | out-of-profile methods not called; unclaimed capability methods not called |
| `test_cli.py` | `--help`, `selfcheck`, exit codes, adapter load failure → 2 |
| `test_import_isolation.py` | `import gak_conformance` leaves `deponent` out of `sys.modules`; core modules have no `deponent` import |
| `test_leavebehind.py` | tree scan: no `attest.py`, `00Agent`, `cds-compliance`, CMMC/RMF maps, ATO-in-a-Box, per-control maps |
| `test_deponent_adapter.py` | `@skipUnless` Deponent importable; live score 0 FAIL and ≥1 PASS; digest matches frozen v1 when kernel unchanged |

Fixtures (`gak_conformance/fixtures/`):

- **Fixture kernel** — tiny real action-gate with an in-memory chain (not a hardcoded PASS table). Claims `reconcile` + `attest` so selfcheck can exercise optional methods.
- **Brick** — deny-everything → FAIL `GAK-ALLOW-INBOUNDS` (and commit ALLOW if declared commit-gate).
- **All-NA** — profile/capability combination that scores 13 NA → not conformant.
- **Raising** — dispatched method raises → FAIL with exception type in `detail`.

Fixture receipts use kernel names `gak-fixture`, `gak-fixture-brick`, … Never `deponent`.

---

## 11. Failure / recovery

| Failure | Behavior | Recovery |
|---|---|---|
| Adapter module missing | exit 2 | fix `PYTHONPATH` / module name |
| Declaration invalid | exit 2, no receipt | fix name / profile / supports |
| Clause check raises | that clause FAIL; run continues | fix kernel or adapter; re-run |
| All NA | `conformant: false`, exit 1 | declare a real profile / implement methods |
| Brick / deny-everything | FAIL on ALLOW clauses, exit 1 | expected |
| Deponent not installed + deponent adapter | exit 2 | use fixture or install Deponent |
| Non-deterministic digest | `selfcheck` / tests fail; do not publish | remove time/entropy from harness |
| Spec ↔ `clauses.py` census drift | `check_consistency.py` exit 1 | fix the harness or the spec (clauses frozen) |
| Accidental `import deponent` in core | `test_import_isolation` fails | delete the import |
| Live Deponent status/digest change | do **not** silently refresh evidence | record run; refresh `v1/evidence/` only if justified |

No retry loops. No network fallback. No “skip clause”.

---

## 12. Threat / privacy (leave-behind)

**Shipped face:** spec + harness + adapter contract + receipt schema + one scored-kernel evidence pack + README. Language: *research prototype, not a security-evaluated product.* Mark language bounded by spec §8.

**Must not ship / import:**

- `deponent/attest.py`, `operator_attest.py`, `selfgate` as harness
- `00Agent`, `cds-compliance`
- CMMC-RMF coverage maps, ATO-in-a-Box, per-control maps
- API keys, tokens, network clients
- SVG / Deponent-branded badge as the product face

**Threats**

| ID | Threat | Control |
|---|---|---|
| T1 | Harness imports Deponent → stranger cannot run; vendor capture | import-isolation test; optional adapter only |
| T2 | Simulated adapter earns a void mark | documented §6.3/§8; cannot be mechanically proven; fixtures never published as product evidence |
| T3 | Timestamp / entropy in digest | no timestamp field; §5.3 two-run test |
| T4 | Private coupling leak in the tree | leave-behind scan test |
| T5 | Live Deponent 16-clause set leaks into v0 | `clauses.py` is a closed tuple of 13; census test vs spec §4 |
| T6 | `--adapter` imports attacker-controlled code | expected (user named the module); no `eval`; no implicit plugin scan |
| T7 | Fixture named `deponent` pollutes evidence | reserved names `gak-fixture*` |
| T8 | Receipt stores governed payload | `detail` is clause statement / NA reason, not tool params |

**Privacy**

- Scorer does not persist tool params, file contents, or sandbox paths.
- Receipts carry kernel name, profile, statuses, clause statements only.
- No PII/CUI plane. No attestation overlay. No phone-home.

---

## 13. Dependencies / licensing

- Runtime: **Python ≥ 3.10 stdlib only**.
- License: **Apache-2.0** (existing `LICENSE` + `NOTICE`). New files inherit that.
- No third-party packages. No `deponent` extra. No network at score time.
- Patent note stays in spec §10; implementing the harness requires no CDS-patented mechanism.

---

## 14. Data flow (score)

```
argv --adapter M:C
  → load.py (importlib)
  → validate declaration (name / profile / supports)
  → for clause in CLAUSES_V1:
        NA? (profile / capability)
        else dispatch §6 method
        raise → FAIL(detail=exc)
  → ConformanceReceipt (in memory)
  → counts + conformant (§3.4)
  → optional Certification + SHA-256 digest (§5.3)
  → stdout / --out / --cert
  → process exit 0 iff conformant
```

No write except the paths the user named.

---

## 15. Migration from `deponent.badge` (README path)

**Today (defect):**

```
python3 -m deponent.badge verify --kernel deponent
```

Also in spec §7.1 (`from deponent.conformance import run_conformance`) and Appendix A / Appendix B.

**v0 primary path (stranger):**

```
PYTHONPATH=. python3 -m gak_conformance --help
PYTHONPATH=. python3 -m gak_conformance selfcheck
PYTHONPATH=. python3 -m gak_conformance score \
  --adapter your.kernel.adapter:YourAdapter \
  --out receipt.json --cert cert.json
```

**Deponent, when installed locally:**

```
PYTHONPATH=. python3 -m gak_conformance score \
  --adapter gak_conformance.adapters.deponent:DeponentKernelAdapter \
  --out receipt.json --cert cert.json
```

README: this command is the documented entrypoint. Keep `python3 -m deponent.badge verify` as a **kernel-local / historical** footnote only — not the stranger path.

Spec §1 currently says the reference harness ships with Deponent. **Docs lane retargets §1 / §7 / Appendix A–B commands to this repo.** That is not a clause-set change (spec §9: non-normative command paths may move). Do not touch §3–§6 semantics.

`scripts/check_consistency.py` becomes a client of `gak_conformance`:

1. Parse spec `**GAK-…**` headings vs `clauses.CLAUSES` (expect 13 for v0; still assert frozen digest `de6b7089…` remains in the spec).
2. Re-derive digest of `v1/evidence/deponent-conformance-receipt.json` via `receipt.clauses_digest`.
3. If Deponent is importable, score the optional adapter and compare status set / digest to evidence. If not importable → exit 0 on spec+fixture+evidence checks; print NOTICE (do not exit 3 for missing Deponent — that was the old fail-closed-on-vendor bug).
4. **Never** `import deponent.badge` or `deponent.conformance`.

Out of scope: rewriting Deponent to call `gak_conformance`. Prefer an adapter note if Deponent's public adapter is missing a §6 method.

---

## 16. Rollback

The package is additive. Spec + `v1/evidence/` stay.

1. Remove `gak_conformance/`, `tests/`, `pyproject.toml` if added.
2. Restore README / spec command paths to `deponent.badge` / `deponent.conformance`.
3. Restore `scripts/check_consistency.py` imports if needed.
4. Oracle: frozen digest `de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406` still in spec + evidence.

No data migration. Receipts were never stored as system state.

---

## 17. Implementation order (for the next lane)

1. `adapter.py` + `clauses.py` + `receipt.py` + digest tests (including worked value).
2. `scorer.py` + fixture / brick / all-NA / raising tests.
3. `cli.py` + `selfcheck` + import-isolation + leave-behind scan.
4. Retarget `check_consistency.py`.
5. Optional `adapters/deponent.py`; skip-tested live score.
6. README (and spec command) migration. Refresh evidence only if a live v1 run disagrees.

Do not add SVG badges, sworn adapters, v1.1 scoring, or Deponent rewrites in v0.

---

## 18. Open risks

- Adapter honesty (§6.3) is social + void-mark, not mechanically closed.
- Live Deponent adapter uses `unittest.mock` inside `jail_fails_closed`; wrapping it inherits that. Acceptable (their kernel, their adapter).
- Detail-text drift vs old evidence does not change the digest; only refresh evidence if **status set or digest** changes.
- Spec §7 still teaches `deponent.conformance` until docs lane edits it — implementer must not wait on that to ship the package.
