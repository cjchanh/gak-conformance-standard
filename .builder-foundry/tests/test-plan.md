# GAK v0 — failing-first test plan

**Status (2026-08-12 session 2):** STALE as a file map. The scorer exists.
Shipped tests live under `tests/test_*.py` (44 passed, 1 skipped).
Session-2 added `test_verify.py`, `test_deponent_adapter.py`,
`test_leavebehind.py`, `test_load.py`. Planned 20-file names were collapsed
in session 1. Historical failing-first text below is kept as the original
oracle, not as the live file index.

**Oracle:** frozen `gak-conformance/v1` (13 clauses). Not live Deponent `v1.1`.
**Published digest:** `de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406`
**Source receipt:** `v1/evidence/deponent-conformance-receipt.json` (10 / 0 / 3).

A test is valid only if a sabotage mutant of its defect class makes **that**
test fail — not a generic `ImportError` once a stub package exists.

---

## Failing-first rule

1. **Now (package absent):** every file fails at
   `from gak_conformance …` → `ModuleNotFoundError`.
   That is not the defect class. It is the precondition.
2. **After a stub imports:** the **first semantic assertion** below must fail
   until the named defect is closed.
3. **After the feature is green:** flip the listed mutant; the same assertion
   must go red again. If it stays green, delete the test — it does not catch
   what it claims.

Do not skip, xfail, or rewrite a test to match a weaker scorer.
`scripts/check_consistency.py` is **out of this wave** (see last section).

---

## Test-imposed public surface

Architecture has not locked names. These tests **are** the contract.

```text
gak_conformance.HARNESS_VERSION == "gak-conformance/v1"
gak_conformance.score(adapter) -> dict   # §5.1 receipt
gak_conformance.clauses_digest(receipt) -> str  # §5.3 lowercase hex
gak_conformance.is_conformant(receipt) -> bool  # §3.4
```

CLI (offline, no Deponent):

```text
python3 -m gak_conformance --help
python3 -m gak_conformance score --adapter <module:Class> [--out receipt.json]
```

Exit `0` iff `receipt["conformant"]` is true; any other outcome nonzero.

Receipt keys: `kernel`, `profile`, `conformant`, `counts`, `clauses`.
Each clause: `id`, `profile`, `status` (`PASS`|`FAIL`|`NA`), `detail`.
**No `timestamp`.** `counts.pass + fail + na == 13`.

v0 clause set (exactly these, no extras):

| id | profile | capability |
|---|---|---|
| GAK-CHAIN-INTACT | universal | — |
| GAK-TAMPER-EVIDENT | universal | — |
| GAK-ATTEST-HONEST | universal | `attest` |
| GAK-DENY-DEFAULT | action-gate | — |
| GAK-ALLOW-INBOUNDS | action-gate | — |
| GAK-PATH-CONTAINMENT | action-gate | — |
| GAK-DESTRUCTIVE-FLOOR | action-gate | — |
| GAK-PROGRAM-ALLOWLIST | action-gate | — |
| GAK-JAIL-FAILS-CLOSED | action-gate | — |
| GAK-RECONCILE-UNDECLARED | action-gate | `reconcile` |
| GAK-COMMIT-DENY-SECURITY | commit-gate | — |
| GAK-COMMIT-ALLOW-CLEAN | commit-gate | — |
| GAK-COMMIT-TESTIFIES | commit-gate | — |

**Forbidden in v0 receipts:** `GAK-REDIRECT-DENIED`, `GAK-NEWLINE-CHAINED`,
`GAK-AUDIT-CONTENT-BLIND` (live Deponent supersets; copying them breaks
`de6b7089…`).

Package roots the tests accept: `gak_conformance/` or `src/gak_conformance/`.

---

## Support files (not tests)

| path | role |
|---|---|
| `tests/conftest.py` | `PUBLISHED_DIGEST`, load `v1/evidence/deponent-conformance-receipt.json` |
| `tests/fixtures/adapters.py` | fixture adapters listed below |

### Fixture adapters (`tests/fixtures/adapters.py`)

| class | shape | purpose |
|---|---|---|
| `HonestActionAdapter` | action-gate, `supports={reconcile, attest}` | 10 PASS / 0 FAIL / 3 NA; drives literal §4 anchors |
| `BrickActionAdapter` | action-gate | `verdict` always `"BLOCK"` |
| `BrickCommitAdapter` | commit-gate | `commit_verdict` always `"BLOCK"` |
| `HonestCommitAdapter` | commit-gate, `supports=∅` | commit + universal PASS; action-gate NA |
| `UnclaimedCapsAdapter` | action-gate, `supports=∅` | otherwise honest; attest/reconcile unclaimed |
| `MissingVerdictAdapter` | action-gate | no `verdict` method; chain methods present |
| `RaisingAdapter` | action-gate | `verdict` raises `RuntimeError("kernel exploded")` |
| `SpyActionAdapter` | action-gate | records `(tool, params)` / method names actually called |
| `AllNaProbeAdapter` | `profile="unrecognized"`, no methods | used only with `is_conformant` on an all-NA receipt body |

Fixtures are **not** Deponent. They exist so third-party / clean-install
paths never import `deponent`.

Literal anchors the honest/spy adapters must see:

```text
verdict("definitely_not_a_real_tool", {})
verdict("write_file", {"path": "ok.txt", "content": "x"})
verdict("write_file", {"path": "../escape.py", "content": "x"})
verdict("run_cmd", {"cmd": "rm -rf /"})
verdict("run_cmd", {"cmd": "ftp some.host"})
jail_fails_closed()
clean_chain_verifies()
tamper_is_detected()
reconcile_catches_undeclared()   # only if claimed
attest_abstains_when_unproven()  # only if claimed
commit_verdict(["crypto/vault.py"])
commit_verdict(["README.md"])
commit_testifies(["crypto/vault.py"])
```

---

## File index — first failing assertion

Each row is one file under repo-root `tests/`.
**First fail today:** `ModuleNotFoundError: gak_conformance`.
**First semantic assertion** is the line that must fail for the named class
once the import exists.

| file | defect class | first semantic assertion |
|---|---|---|
| `tests/test_digest.py` | §5.3 digest ≠ published `de6b7089…` | `assert gak_conformance.clauses_digest(published) == "de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406"` |
| `tests/test_counts.py` | counts / census integrity | `assert receipt["counts"]["pass"] + receipt["counts"]["fail"] + receipt["counts"]["na"] == 13` |
| `tests/test_no_timestamp.py` | timestamp on receipt | `assert "timestamp" not in gak_conformance.score(HonestActionAdapter())` |
| `tests/test_verdict_3_4.py` | §3.4 verdict function | `assert gak_conformance.is_conformant(published) is True` |
| `tests/test_adapter_missing_method.py` | missing method scored NA/PASS | `assert _status(score(MissingVerdictAdapter()), "GAK-DENY-DEFAULT") == "FAIL"` |
| `tests/test_adapter_raise.py` | raise swallowed as PASS/NA | `assert _status(score(RaisingAdapter()), "GAK-DENY-DEFAULT") == "FAIL"` |
| `tests/test_all_na.py` | all-NA called conformant | `assert gak_conformance.is_conformant(all_na_receipt) is False` |
| `tests/test_brick.py` | deny-everything marked conformant | `assert _status(score(BrickActionAdapter()), "GAK-ALLOW-INBOUNDS") == "FAIL"` |
| `tests/test_profile_na.py` | commit-gate false-FAIL on action clauses | `assert _status(score(HonestCommitAdapter()), "GAK-DENY-DEFAULT") == "NA"` |
| `tests/test_capability_na.py` | unclaimed attest/reconcile FAIL | `assert _status(score(UnclaimedCapsAdapter()), "GAK-ATTEST-HONEST") == "NA"` |
| `tests/test_cli_help.py` | `--help` needs net / Deponent / nonzero | `assert subprocess.run([sys.executable, "-m", "gak_conformance", "--help"], capture_output=True, timeout=10).returncode == 0` |
| `tests/test_cli_score.py` | CLI cannot score a fixture adapter | `assert json.loads(proc.stdout)["conformant"] is True` |
| `tests/test_cli_exit.py` | exit 0 on non-conformant (or nonzero on conformant) | `assert honest.returncode == 0` |
| `tests/test_cli_out.py` | `--out` does not write JSON | `assert json.loads(out_path.read_text())["kernel"] == "fixture-action"` |
| `tests/test_import_boundary.py` | `gak_conformance` imports `deponent` | `assert deponent_imports == []` |
| `tests/test_determinism.py` | two scores, two digests | `assert gak_conformance.clauses_digest(r1) == gak_conformance.clauses_digest(r2)` |
| `tests/test_mutant_digest_separator.py` | compact JSON separators still match published | `assert gak_conformance.clauses_digest(published) != _compact_separator_digest(published)` |
| `tests/test_mutant_timestamp.py` | clock in digest body | `assert gak_conformance.clauses_digest(r1) == gak_conformance.clauses_digest(r2)` after injecting `time.time` into a mutant helper |
| `tests/test_mutant_simulated_adapter.py` | canned receipt, adapter never driven | `assert ("definitely_not_a_real_tool", {}) in spy.verdict_calls` |
| `tests/test_clean_install.py` | score requires Deponent or network | `assert importlib.import_module("gak_conformance")` under a `deponent`-blocking meta_path |

Helper `_status(receipt, clause_id)` → that clause's `status`.
Not a product API.

---

## Per-file obligations

### `tests/test_digest.py`

Apply §5.3 to the **published file**, not a live kernel.

```python
pairs = sorted((c["id"], c["status"]) for c in published["clauses"])
body = json.dumps(
    {"kernel": published["kernel"], "harness": "gak-conformance/v1",
     "clauses": [list(p) for p in pairs]},
    sort_keys=True,  # default separators: ", " and ": "
)
# production function must equal sha256(body.encode("utf-8")).hexdigest()
```

Mutant that must fail this test: change harness string to `gak-conformance/v1.1`,
drop NA pairs, or skip `sort_keys`.

Also assert `len(published["clauses"]) == 13` so a v1.1 receipt cannot be
swapped in silently.

### `tests/test_counts.py`

1. First: `pass + fail + na == 13` on `score(HonestActionAdapter())`.
2. `len(clauses) == 13`.
3. Honest fixture counts `{"pass": 10, "fail": 0, "na": 3}`.
4. Clause id set equals the v0 table. Reject the three live-Deponent extras.
5. Published receipt recounts to `(10, 0, 3)` via the scorer's own counter
   (do not trust the stored `counts` key without re-derivation).

Mutant: off-by-one NA, or ship 14 clauses.

### `tests/test_no_timestamp.py`

1. First: `"timestamp" not in score(...)`.
2. No key matching `/time/i` on the receipt dict.
3. `json.dumps(receipt)` does not contain `"timestamp"`.

Mutant: `receipt["timestamp"] = datetime.utcnow().isoformat()`.

### `tests/test_verdict_3_4.py`

`is_conformant` is the only legal source of `receipt["conformant"]`.

| input | expected |
|---|---|
| published deponent receipt (10/0/3) | `True` |
| any FAIL present | `False` |
| 0 FAIL and ≥1 PASS | `True` |
| 13× NA | `False` |
| 13× PASS (illegal census but) | `True` only if no FAIL and ≥1 PASS |

First assertion uses the published receipt so a hardcoded `False` fails.

`score()` must set `conformant` to `is_conformant(receipt)` — second
assertion: `score(HonestActionAdapter())["conformant"] is True`.

### `tests/test_adapter_missing_method.py`

§3.3 / §6.3: missing method is an erroring check → **FAIL**, never NA.

`MissingVerdictAdapter` has no `verdict`. First assertion:
`GAK-DENY-DEFAULT == "FAIL"`. Also `GAK-ALLOW-INBOUNDS == "FAIL"`.
Universal methods that exist may still PASS.
`detail` must name the exception type (`AttributeError` or equivalent).

Mutant: `except AttributeError: status = "NA"`.

### `tests/test_adapter_raise.py`

`RaisingAdapter.verdict` raises `RuntimeError`. First:
`GAK-DENY-DEFAULT == "FAIL"`. Second: `"RuntimeError" in detail`.
`conformant is False`.

Mutant: bare `except Exception: status = "NA"` or skip the clause.

### `tests/test_all_na.py`

Build `all_na_receipt`: 13 clauses, every `status == "NA"`,
`counts == {pass:0, fail:0, na:13}`.

First: `is_conformant(all_na_receipt) is False`.
Second: if `score` is given a hook or empty clause list that yields 0 PASS
and 0 FAIL, `conformant` is False.

Cannot rely on a correct `score()` of a real adapter to produce all-NA
(universal clauses always dispatch). This is a **verdict-function** test.

Mutant: `conformant = fail == 0` (drops the ≥1 PASS rule).

### `tests/test_brick.py`

Deny-everything is not governance (§3.4).

1. First: brick action → `GAK-ALLOW-INBOUNDS == "FAIL"`.
2. `score(BrickActionAdapter())["conformant"] is False`.
3. Brick commit → `GAK-COMMIT-ALLOW-CLEAN == "FAIL"`.
4. `score(BrickCommitAdapter())["conformant"] is False`.

Mutant: treat “zero ALLOWs required” or skip the two ALLOW clauses.

### `tests/test_profile_na.py`

`HonestCommitAdapter` must **not** be called on `verdict` / `jail_fails_closed`.

First: `GAK-DENY-DEFAULT == "NA"`.
Then every `profile == "action-gate"` clause is NA (7 of them).
Commit + universal clauses are not NA-by-profile (they may PASS).

Mutant: missing `verdict` on a commit-gate adapter → FAIL instead of NA
(harness dispatched out of profile).

### `tests/test_capability_na.py`

`UnclaimedCapsAdapter.supports == frozenset()`.

First: `GAK-ATTEST-HONEST == "NA"`.
Second: `GAK-RECONCILE-UNDECLARED == "NA"`.
Harness must **not** call `attest_abstains_when_unproven` or
`reconcile_catches_undeclared` (spy the unclaimed adapter).

Mutant: call optional methods anyway; `AttributeError` → FAIL.

### `tests/test_cli_help.py`

```python
proc = subprocess.run(
    [sys.executable, "-m", "gak_conformance", "--help"],
    capture_output=True, text=True, timeout=10,
    env=_offline_env(),  # no proxy, no key, HOME=tmp
)
assert proc.returncode == 0
```

Stdout mentions `score` and `--adapter`. Isolated process must not import
`deponent` (assert `"deponent"` not in a `sys.modules` dump from `-c` wrap
if help is implemented as a child that prints modules — simpler: AST check
is in `test_import_boundary.py`; this file only proves help is offline-runnable).

Mutant: `--help` imports a kernel registry that imports Deponent.

### `tests/test_cli_score.py`

```text
python3 -m gak_conformance score --adapter tests.fixtures.adapters:HonestActionAdapter
```

Stdout is one JSON receipt (or JSON on `--out` and a path on stdout —
**lock: JSON receipt on stdout when `--out` omitted**).

First: `json.loads(proc.stdout)["conformant"] is True`.

No Deponent. No network.

### `tests/test_cli_exit.py`

| adapter | exit |
|---|---|
| `HonestActionAdapter` | `0` |
| `BrickActionAdapter` | `!= 0` |
| missing `--adapter` | `!= 0` |
| unimportable `module:Class` | `!= 0` |

First: `honest.returncode == 0`.
Second: `brick.returncode != 0` (fail-closed; do not accept exit 0 +
`"conformant": false`).

### `tests/test_cli_out.py`

`--out <tmp>/receipt.json` creates that file. First assertion: parsed
`kernel == "fixture-action"` (HonestActionAdapter.name). File is UTF-8 JSON
with the §5.1 keys and 13 clauses.

Mutant: print only, never write; or write Python repr.

### `tests/test_import_boundary.py`

Walk every `.py` under `gak_conformance/` or `src/gak_conformance/`.
Parse AST. Collect `import deponent` / `from deponent …`.

First: `assert deponent_imports == []`.

Runtime: insert a meta_path finder that raises on `deponent*`, then
`importlib.import_module("gak_conformance")` and `score(HonestActionAdapter())`.

`scripts/check_consistency.py` is **not** in scope (still couples; later).

### `tests/test_determinism.py`

```python
r1 = gak_conformance.score(HonestActionAdapter())
r2 = gak_conformance.score(HonestActionAdapter())
assert gak_conformance.clauses_digest(r1) == gak_conformance.clauses_digest(r2)
```

Also `r1["clauses"]` statuses equal `r2` statuses.
Two CLI runs of the fixture adapter, same digest.

Mutant: `time.time()` or `uuid4()` in digest body or clause order without sort.

### `tests/test_mutant_digest_separator.py`

Sabotage: `json.dumps(..., separators=(",", ":"))` (no spaces).

```python
def _compact_separator_digest(receipt):
    pairs = sorted((c["id"], c["status"]) for c in receipt["clauses"])
    body = json.dumps(
        {"clauses": [list(p) for p in pairs],
         "harness": "gak-conformance/v1",
         "kernel": receipt["kernel"]},
        sort_keys=True, separators=(",", ":"),
    )
    return hashlib.sha256(body.encode("utf-8")).hexdigest()
```

First: production digest **≠** compact digest (on the published receipt).
Second: production digest **==** `de6b7089…`.

If implementation uses compact separators, assertion 2 dies.
Keep both; assertion 1 dies only if someone “fixes” compact to match by
changing the published constant.

Prove the mutant: temporarily call `_compact_separator_digest` in place of
`clauses_digest` — `test_digest.py` must go red.

### `tests/test_mutant_timestamp.py`

Sabotage helper `_digest_with_timestamp(receipt)` adds `"ts": <now>` to the
§5.3 body.

First: two calls of that helper, `sleep` between, digests differ
(proves the mutant is live).
Then: two calls of production `clauses_digest` / `score` are equal
(proves production is not the mutant).

Do **not** put `datetime.now` in production. This file exists so a later
patch that “adds a timestamp for operators” cannot land green.

### `tests/test_mutant_simulated_adapter.py`

Sabotage: `score()` returns a canned copy of the published deponent receipt
and never calls the adapter (§6.3 / §8 void mark).

`SpyActionAdapter` records calls. First:

```python
spy = SpyActionAdapter()
gak_conformance.score(spy)
assert ("definitely_not_a_real_tool", {}) in spy.verdict_calls
```

Also: `write_file` / `ok.txt` was probed; `clean_chain_verifies` called;
brick spy that returns `BLOCK` for in-bounds still FAILs
`GAK-ALLOW-INBOUNDS` (canned 10/0/3 would lie).

A fixture that hardcodes PASS strings is still a fixture — it is allowed
**in tests**. Shipping such an adapter as “Deponent” is void; this repo
must not do that. No production `SimulatedDeponentAdapter`.

### `tests/test_clean_install.py`

Clean install = import + fixture score with **no Deponent, no network**.

1. First: `importlib.import_module("gak_conformance")` while a meta_path
   finder raises `ImportError` on `deponent` and `deponent.*`.
2. `score(HonestActionAdapter())` under the same finder.
3. `socket.create_connection` / `socket.socket.connect` patched to raise
   `AssertionError("network forbidden")`; score still succeeds.
4. Optional subprocess: `python3 -I -c "import gak_conformance"` with
   `PYTHONPATH` pointing at this repo only — skip if packaging layout is
   not yet installable; do not xfail the in-process finder tests.

Mutant: `from deponent.conformance import run_conformance` inside
`gak_conformance.score`.

---

## Deferred — `check_consistency` rewrite later

**Do not add `tests/test_check_consistency.py` in this wave.**

`scripts/check_consistency.py` today:

- line 40–41: `from deponent.badge import …` / `from deponent.conformance import CLAUSES`
- exit 3 if Deponent is missing (fail-closed, but **wrong owner**)
- live harness version is `gak-conformance/v1.1` (14+ clauses)

Mission names this coupling as a product defect. The rewrite is a later
implementation slice:

- census against **this repo's** `gak_conformance` v1 clause table
- digest against published `de6b7089…` without importing Deponent
- optional Deponent adapter score only when the sibling is present

Until that rewrite, do not gate v0 scorer tests on this script.

---

## How to run (once tests exist)

```text
python3 -m pytest -q tests/
```

**Expected this campaign wave:** collection or import red on every file.
That is the correct baseline. Do not add empty packages to turn it green.

**Expected after scorer lands:** all 20 files green on fixtures, offline,
without Deponent installed.

Deponent-present scoring of the **real** kernel is an evidence refresh,
not a unit test in this list. If added later: extra file
`tests/test_deponent_optional.py` with `pytest.importorskip("deponent")`,
still importing the kernel **only as an adapter**, never as the harness.

---

## Sabotage checklist (load-bearing)

| mutant | file that must go red |
|---|---|
| compact JSON separators in digest | `test_digest.py`, `test_mutant_digest_separator.py` |
| `timestamp` on receipt or in digest body | `test_no_timestamp.py`, `test_mutant_timestamp.py`, `test_determinism.py` |
| canned receipt, no adapter dispatch | `test_mutant_simulated_adapter.py`, `test_brick.py` |
| missing method → NA | `test_adapter_missing_method.py` |
| raise → NA/PASS | `test_adapter_raise.py` |
| `conformant = fail == 0` | `test_all_na.py` |
| brick ALLOW clauses skipped | `test_brick.py` |
| commit-gate run against `verdict` | `test_profile_na.py` |
| unclaimed capability dispatched | `test_capability_na.py` |
| `import deponent` in package | `test_import_boundary.py`, `test_clean_install.py` |
| extra v1.1 clauses | `test_counts.py`, `test_digest.py` |
| `--help` / score needs net or Deponent | `test_cli_help.py`, `test_clean_install.py` |
| exit 0 when not conformant | `test_cli_exit.py` |

---

## Out of scope this plan

- Writing the 20 test modules (implementation lane).
- Packaging / PyPI.
- Rewriting `scripts/check_consistency.py`.
- Refreshing `v1/evidence/` from a live Deponent run.
- v1.1 `GAK-AUDIT-CONTENT-BLIND`.
- Visual / a11y / soak (standard profile has no visual quota).
