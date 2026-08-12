# DESIGN_DOCTRINE — GAK v0

**Status:** binding for this campaign (product lane)  
**Date:** 2026-08-12  
**Product:** vendor-neutral mechanical scorer + JSON receipt in *this* repo  
**Face:** research prototype, not a security-evaluated product  
**Clause set:** frozen `gak-conformance/v1` (13 clauses). v1.1 is out of v0 ship.

**Product verdict:** invert the README. A stranger clones this repo, runs one documented command, and gets a §5.1 JSON receipt. Deponent is the first *scored* kernel, not the owner, not the first-run path, not the harness.

---

## 1. Target user and job

**Primary user — kernel author.**  
Someone who already has (or is writing) an agent-action gate. They need a mechanical verdict they can publish, not a vendor relationship.

**Secondary user — verifier.**  
Someone who received a GAK-conformant claim and wants to re-derive the digest against the live kernel.

**Tertiary user — category skeptic.**  
A stranger testing the standard's own bar: *"a category is real when a third party can test against it and get a verdict."*

**Job to be done (one sentence):**  
Score a kernel against the frozen 13 clauses and leave with a re-derivable JSON receipt — without installing Deponent, without reading harness internals, without asking us.

**Not the job:** become a Deponent user; get a security audit; get a badge gallery; get partial credit.

---

## 2. Core value and core interaction

**Core value:** a third party can test the category and get a verdict.

**Core interaction:** one documented command → one JSON receipt + a fail-closed exit code.

```
command  →  stdout: ConformanceReceipt (§5.1)
         →  stderr: diagnostics only
         →  exit 0  iff §3.4 (no FAIL, ≥1 PASS)
         →  exit ≠0 otherwise
```

Everything else (spec, evidence pack, certifications, Deponent score) is supporting material around that interaction.

**What the user is buying:** testimony, not reassurance. The receipt is the product. The mark is a function of the receipt. Marketing copy is not a surface.

---

## 3. First-run experience (exact command sequence)

### Clone-to-run invariant

First-run MUST work with **CPython 3 + this repo only**.

- No `pip install`
- No network
- No Deponent
- No API keys
- No extra env files

If architecture needs a path prefix to make `python3 -m gak_conformance` importable from a clean clone, that prefix is part of the **one documented one-liner**, not a hidden step. Prefer a repo-root invocation that needs no prefix.

**Canonical entrypoint name** (stable, documented): `python3 -m gak_conformance`  
Implementation may add `python3 scripts/gak.py` as a clone-friendly alias. README documents **one** primary command. Do not document two competing CLIs.

### Sequence A — stranger, no Deponent (the first-run)

```text
git clone <this-repo-url>
cd gak-conformance-standard
python3 -m gak_conformance --help
python3 -m gak_conformance selfcheck
python3 -m gak_conformance score --adapter gak_conformance.fixtures:FixtureActionAdapter --out receipt.json
```

**Expected after `selfcheck`:** exit `0`; prints that the scorer, fixture adapters, receipt schema, and digest algorithm are internally consistent. Does **not** print a public mark claim.

**Expected after fixture `score`:** a §5.1 JSON file at `receipt.json`; exit `0` or `1` according to §3.4; kernel name is clearly a fixture (e.g. `fixture-action-gate`). README states: *this proves the scorer runs, not that a third-party kernel passed.*

`--help` and `selfcheck` MUST succeed with Deponent absent (`ImportError` on `deponent` is a product bug).

### Sequence B — score your kernel (the job)

```text
python3 -m gak_conformance score --adapter your_pkg.adapter:YourAdapter --out receipt.json
echo $?    # 0 = conformant; 1 = scored not-conformant; 2 = could not score
```

Author implements spec §6 against the **real** kernel. They do not import harness internals. They do not import Deponent.

### Sequence C — re-verify a published claim

```text
python3 -m gak_conformance verify --adapter your_pkg.adapter:YourAdapter --cert certification.json
```

Re-runs the harness, re-derives §5.3 digest, compares to the published `clauses_digest`. Exit `0` only if the mark is still earned **and** the digest matches. A previously published receipt does not save a failing re-run (spec §5.4).

### Sequence D — Deponent, only if present locally (not first-run)

```text
python3 -m gak_conformance score --adapter <deponent-adapter-spec> --out deponent-receipt.json
```

README places this **below** A/B. Label: *first scored kernel, not the owner of the standard.* Do not use `python3 -m deponent.badge` as the documented GAK command.

### Exit codes (normative for v0 UX)

| Exit | Meaning | Receipt on stdout / `--out` |
|---|---|---|
| `0` | Scored and conformant (§3.4) | Yes |
| `1` | Scored and not conformant (any FAIL, or all-NA) | Yes |
| `2` | Could not score (bad adapter, missing args, invalid declaration, unloadable module) | No |

`selfcheck` uses the same fail-closed rule: `0` only if every built-in probe passed.

---

## 4. Information hierarchy (what README leads with)

Current README leads with category prose → artifact table → **Deponent verify**. That is author-centric. Invert.

**README order (binding):**

1. **One-line what** — vendor-neutral mechanical scorer for governed agent kernels.
2. **Bounded claim** — passing means *passes `gak-conformance/v1` under the declared profile.* Not secure. Not audited. Not endorsed. Spec §8.
3. **Face** — research prototype, not a security-evaluated product.
4. **First-run (Sequence A)** — clone → `--help` → `selfcheck` → fixture `score` → JSON receipt. No Deponent.
5. **How to read a receipt** — `conformant`, `counts`, per-clause `status`/`detail`, no timestamp, digest, exit codes.
6. **Score your kernel (Sequence B)** — declare profile → claim only real capabilities → implement §6 → run the command. Link spec §6 and §7.2.
7. **What FAIL / NA / all-NA mean** — short table (see §7 below). Recovery is re-run, not a waiver.
8. **Verify a published claim (Sequence C).**
9. **Optional: score Deponent if installed (Sequence D)** — first scored kernel, not owner. Third-party verdicts to date: **zero**. Do not inflate.
10. **Spec + clause index** — link `v1/spec.md`. Do not dump 13 clauses in the README.
11. **Evidence pack** — Deponent + sworncode as *author-scored examples*, labeled as such.
12. **Status / license** — v1 frozen (13 clauses). v1.1 is an optional amendment, not the v0 face. Apache-2.0. Patent note → spec §10.

**What README must not lead with:**

- `python3 -m deponent.badge verify`
- An artifact inventory before a runnable command
- v1.1 as "the current version" of the v0 product
- Any implication that Deponent owns the mark

---

## 5. Quality bar and design principles

**Bar:** if a stranger cannot get a receipt on a Tuesday, from a clean clone, without us, v0 did not ship.

**Principles (in force):**

1. **Vendor-neutral first.** Deponent never owns the command, the package, or the first screen.
2. **One command, one receipt.** No dashboard. No wizard. No second CLI personality.
3. **The receipt is the product.** Stdout is JSON. Stderr is human. Pipes do not get a banner.
4. **Fail-closed is UX.** Uncertainty, errors, missing methods, all-NA → not-conformant or could-not-score. Never a silent pass.
5. **Honest NA.** Out-of-profile and unclaimed-capability are NA, never FAIL. Claimed-and-broken is FAIL, never optimistic NA.
6. **A brick is not a governor.** Deny-everything fails the ALLOW clauses (spec §3.4). Show this; do not hide it.
7. **Bounded mark language is above the fold**, not a footer.
8. **Fixture ≠ kernel.** Selfcheck proves the scorer. It does not mint a public mark.
9. **Reading load over completeness.** README is the on-ramp. Spec is the contract. Do not make the stranger hold both.
10. **Re-derive or it is an assertion.** Any public claim points at certification JSON.

**Craft tells (user-visible):**

- Receipt has no timestamp.
- Two unchanged runs, same digest.
- `counts.pass + fail + na == 13`.
- Clause `detail` is the statement or the NA/FAIL reason — not a stack dump alone.
- Adapter authors never need harness source (spec §6).

---

## 6. Explicit non-goals

v0 will **not**:

- Require Deponent (or any other kernel) to `--help`, `selfcheck`, or score a fixture / third-party adapter
- Import `deponent.conformance` / `deponent.badge` as the harness
- Ship v1.1 (14th clause) as the v0 face — frozen 13-clause v1 only
- Provide a web UI, badge gallery, leaderboard, or "directory of conformant kernels"
- Auto-generate adapters or translate arbitrary kernels
- Detect every fabricated adapter (spec §6.3 void rule is honesty + contract, not a lie detector)
- Offer partial credit, waivers, or "mostly conformant"
- Claim third-party adoption (current count: **zero**)
- Stretch the mark to "secure / audited / endorsed / ATO / CMMC"
- Leak `deponent/attest.py`, `00Agent`, `cds-compliance`, CMMC-RMF maps, ATO-in-a-Box, per-control maps
- Flip Deponent visibility, rename Deponent, or publish to PyPI
- Start MoLA / paid APIs / push / GitHub visibility change
- Rewrite Deponent unless a proven public-adapter contract bug exists (prefer an adapter note)
- Be a security evaluation, pentest, or adversarial-robustness claim

---

## 7. Failure / recovery behavior

Every failure below is **user-observable**. Architecture implements; this table is the UX contract.

| Situation | User sees | Exit | Receipt? | Recovery |
|---|---|---|---|---|
| Missing `--adapter` / bad argv | stderr: exact usage; `--help` names `score` / `selfcheck` / `verify` | `2` | No | Fix argv |
| Module not importable | stderr: `could not load adapter: <module:Class>` + import error | `2` | No | Fix `PYTHONPATH` / module path |
| Class missing or not instantiable | stderr: class name + reason | `2` | No | Fix export |
| Invalid `profile` (not `action-gate` / `commit-gate`) | stderr: invalid declaration; no score | `2` | No | Fix adapter attribute |
| Invalid / unknown capability in `supports` | stderr: unknown capability; no score | `2` | No | Claim only `reconcile` / `attest` |
| Missing in-profile method | Receipt emitted; that clause **FAIL**; `detail` names method + "not implemented" / exception type | `1` | Yes | Implement the method against the real kernel |
| Method raises | That clause **FAIL**; `detail` records exception type and message (spec §6.3) | `1` if any FAIL | Yes | Fix kernel or adapter; re-run |
| Out-of-profile clause | **NA**; `detail` says `out of profile (<profile>); kernel is <declared>` | — | Yes | None needed |
| Unclaimed optional capability | **NA**; `detail` says kernel does not claim `attest` / `reconcile` | — | Yes | Claim only if implemented |
| Claimed capability, method missing or raises | **FAIL** (no optimistic NA) | `1` | Yes | Implement or drop the claim |
| All-NA receipt | `conformant: false`; stderr: all-NA is a refusal, not a pass (spec §3.4) | `1` | Yes | Fix profile / implement at least one in-profile behavior |
| Any FAIL clause | `conformant: false`; `detail` is the missing behavior (clause statement), plus error if any | `1` | Yes | Fix kernel (not formatting); re-run. No waiver. |
| Brick (deny-everything) | FAIL on `GAK-ALLOW-INBOUNDS` or `GAK-COMMIT-ALLOW-CLEAN` | `1` | Yes | Discriminate; a brick is not a governor |
| `--out` cannot be written | stderr: path + OS error | `2` | No file | Fix path/permissions |
| `verify` digest mismatch | stderr: expected vs derived digest; mark not earned | `1` | Re-run receipt may be written if `--out` given | Kernel changed, or published cert is stale |
| `verify` now not-conformant | Fail-closed; prior published receipt does not save it | `1` | Yes if scored | Fix kernel; republish only if earned |
| Fixture used as a public mark | README + selfcheck text: fixture is not a kernel mark | `0` on selfcheck | Fixture receipt only | Do not publish fixture receipts as certifications |
| Fabricated / simulated adapter | Cannot be fully detected. README + spec §8: claim is void | n/a | n/a | Drive the real kernel |

**What we never do on failure:** retry into a pass; drop a clause; convert FAIL to NA; print "GAK-conformant" on a non-conformant receipt; swallow an exception as skip.

---

## 8. What makes a second use worthwhile

First use proves the scorer exists. Second use is why a kernel author stays:

1. **Score *their* adapter** after the fixture — same command, different `--adapter`.
2. **Fix a FAIL and re-run** — `detail` names the missing behavior; next receipt should change only that clause (and counts/verdict/digest).
3. **Unchanged kernel → identical digest** — the second run is the trust event.
4. **`verify` a published certification** — the claim becomes checkable.
5. **Honest capability edit** — drop `attest` → NA; claim it without the method → FAIL. The difference is the lesson.
6. **Other profile** — a commit-gate adapter produces 5 PASS / 8 NA (no `attest`) without false FAILs. Proves the profile system is not a trap.

If the second command requires rereading the spec or installing Deponent, reuse has failed.

---

## 9. Measurable acceptance outcomes

These are product-acceptance checks, not implementation tasks.

| # | Outcome | Measure |
|---|---|---|
| A1 | Stranger first-run | Clean clone → documented command → §5.1 JSON. Deponent not installed. |
| A2 | Selfcheck offline | `python3 -m gak_conformance --help` and `selfcheck` exit `0` with no `deponent` import. |
| A3 | Receipt shape | `kernel`, `profile`, `conformant`, `counts`, 13 `clauses` each with `id` / `profile` / `status` / `detail`. No timestamp. |
| A4 | Verdict math | `conformant` iff no FAIL and ≥1 PASS. All-NA → `false`, exit `1`. |
| A5 | Count integrity | `pass + fail + na == 13`. |
| A6 | Exit contract | `0` conformant; `1` scored not-conformant; `2` could not score. |
| A7 | Determinism | Two runs, unchanged adapter, identical §5.3 digest. |
| A8 | Digest algorithm | Matches spec §5.3 (`json.dumps(..., sort_keys=True)` bytes → SHA-256 hex). |
| A9 | Adapter boundary | Scoring a third-party / fixture adapter does not import Deponent internals. |
| A10 | Deponent optional | When Deponent is present locally, a real §6 adapter can score v1; `conformant` matches §3.4. Author self-score ≠ third-party verdict. |
| A11 | README inversion | First command block is Sequence A. Deponent command is not above it. |
| A12 | Bounded language | "Not secure / not audited / not endorsed" appears before any worked "GAK-conformant" example. |
| A13 | Public-safe leave-behind | No `attest.py` / `00Agent` / CMMC / ATO / per-control maps in the shipped tree. |
| A14 | Face | README states research prototype, not a security-evaluated product. |
| A15 | Mark honesty | Certification `mark` is `GAK-conformant` only when `conformant` is true; else `not-conformant`. Fixture receipts are not public certifications. |
| A16 | Third-party count | README still says third-party verdicts: zero, unless a real outsider receipt exists. |

---

## 10. Worth-testing dimensions (for later AUTOMATED_WORTH_TESTING)

Score these three dimensions. Do not substitute unit-test green for them.

### First-use clarity

- First 40 lines of README contain a copy-paste command that produces a receipt without Deponent.
- `--help` names `score`, `selfcheck`, `verify` and the `--adapter module:Class` form.
- Receipt fields are understandable without opening the spec (status enum, counts, `conformant`).
- Exit codes sit next to the first command, not in an appendix.
- Fixture is named as fixture in the kernel field and in README.

**Fail the dimension if** the first command block requires Deponent, `pip`, or opening `v1/spec.md` §7.

### Trust

- Bounded mark language is above the fold.
- Face line (research prototype) is present.
- All-NA and brick paths are documented as refusals.
- FAIL `detail` names behavior + exception; not a bare traceback as the only output.
- No timestamp; two-run digest is documented.
- Deponent is labeled first scored kernel, not owner.
- Third-party count is not inflated.
- Fixture selfcheck does not emit a public mark.

**Fail the dimension if** a non-conformant run can print `GAK-conformant`, or if the harness is Deponent.

### Reuse

- Second `score` of an unchanged adapter matches digest.
- Switching `--adapter` requires no new conceptual model.
- `verify --cert` is one command.
- FAIL recovery is "fix kernel, re-run" with a stable clause id.
- Adapter contract is one hop from README (link to spec §6).
- Commit-gate vs action-gate is a declaration, not a different product.

**Fail the dimension if** a second kernel requires a different CLI, a Deponent install, or a spec reread to know the next flag.

---

## 11. Atomic user-observable features

Recommended ledger IDs. Each is independently demoable. None are implemented by this lane.

| ID | User-observable feature |
|---|---|
| FEAT-0001 | Offline `--help` lists `score`, `selfcheck`, `verify` |
| FEAT-0002 | `selfcheck` runs in-repo fixtures; no Deponent |
| FEAT-0003 | `score --adapter module:Class` prints §5.1 JSON on stdout |
| FEAT-0004 | `score --out PATH` writes that JSON to a file |
| FEAT-0005 | Exit `0` only when §3.4 conformant |
| FEAT-0006 | Exit `1` when scored and any FAIL |
| FEAT-0007 | Exit `1` on all-NA (`conformant: false`) |
| FEAT-0008 | Exit `2` when the adapter cannot be loaded or declared |
| FEAT-0009 | Receipt contains all 13 v1 clause ids |
| FEAT-0010 | Each clause has `id`, `profile`, `status`, `detail` |
| FEAT-0011 | Receipt has no timestamp field |
| FEAT-0012 | `counts.pass + counts.fail + counts.na == 13` |
| FEAT-0013 | `conformant` is computed, never trusted as input |
| FEAT-0014 | Companion certification JSON (`gak-certification/v1`) with `clauses_digest` |
| FEAT-0015 | Two unchanged runs produce identical `clauses_digest` |
| FEAT-0016 | Digest bytes match spec §5.3 |
| FEAT-0017 | In-repo `FixtureActionAdapter` (named fixture, not a mark claim) |
| FEAT-0018 | In-repo `FixtureCommitAdapter` (NA on action-gate clauses) |
| FEAT-0019 | In-repo `FixtureBrickAdapter` (deny-all) FAILs the ALLOW clause |
| FEAT-0020 | `selfcheck` asserts expected verdicts of those fixtures |
| FEAT-0021 | Unloadable adapter: stderr names `module:Class`; no receipt |
| FEAT-0022 | Missing in-profile method → that clause FAIL; method named in `detail`; receipt still emitted |
| FEAT-0023 | Raised method → FAIL; exception type + message in `detail` |
| FEAT-0024 | Out-of-profile clauses score NA, never FAIL, with reason in `detail` |
| FEAT-0025 | Unclaimed `attest` / `reconcile` score NA with reason |
| FEAT-0026 | Claimed capability without method scores FAIL (no optimistic NA) |
| FEAT-0027 | `--list-clauses` prints the 13 v1 ids, profiles, and required capabilities |
| FEAT-0028 | README first command block is Sequence A (fixture/selfcheck) |
| FEAT-0029 | README "score your kernel" is a copy-paste `score --adapter` line |
| FEAT-0030 | README bounded-claim + research-prototype face above the first mark example |
| FEAT-0031 | Optional Deponent score path labeled "when present locally; not the owner" |
| FEAT-0032 | `verify --adapter … --cert …` re-derives digest and fail-closes on mismatch or FAIL |
| FEAT-0033 | Certification `mark` is `GAK-conformant` or `not-conformant` and cannot disagree with `conformant` |
| FEAT-0034 | Stderr diagnostics never corrupt stdout JSON (pipe-safe) |
| FEAT-0035 | `--version` / help shows harness id `gak-conformance/v1` |
| FEAT-0036 | Copyable adapter skeleton (methods raise `NotImplementedError`; does not fabricate outcomes) |
| FEAT-0037 | Fixture receipts cannot be mistaken for a public certification (kernel name + README warning) |
| FEAT-0038 | Public leave-behind contains no Deponent private modules or compliance-map files |
| FEAT-0039 | Scoring path does not import `deponent.conformance` / `deponent.badge` |
| FEAT-0040 | `--help` / `selfcheck` / fixture `score` succeed with `deponent` absent |

---

## 12. Falsifiable hypotheses

For AUTOMATED_WORTH_TESTING / QA. Each can fail on evidence.

| ID | Hypothesis | Falsified when |
|---|---|---|
| H-01 | A stranger following only the first README command block gets a §5.1 JSON file without installing Deponent. | First block requires Deponent, pip, or opening the spec. |
| H-02 | `python3 -m gak_conformance selfcheck` exits `0` on a clean clone with Deponent not importable. | `ImportError: deponent` or nonzero exit. |
| H-03 | `--help` works offline and names `score`, `selfcheck`, `verify`. | Help imports Deponent, touches the network, or omits a subcommand. |
| H-04 | Two consecutive fixture scores produce the same `clauses_digest`. | Digests differ. |
| H-05 | An adapter missing an in-profile method still emits a receipt with that clause `FAIL` and the method name in `detail`. | Process crashes with no receipt, or clause is NA/skipped. |
| H-06 | An all-NA adapter is `conformant: false` and exit `1`. | `conformant: true` or exit `0`. |
| H-07 | `FixtureBrickAdapter` (always BLOCK) FAILs `GAK-ALLOW-INBOUNDS` or `GAK-COMMIT-ALLOW-CLEAN`. | Brick marked conformant. |
| H-08 | `FixtureCommitAdapter` scores every action-gate clause `NA`, never `FAIL`. | Any action-gate FAIL on a well-formed commit-gate fixture. |
| H-09 | Claiming `attest` without implementing it scores `GAK-ATTEST-HONEST` as `FAIL`, not `NA`. | Optimistic NA after claim. |
| H-10 | README's first fenced command is not a `deponent.badge` / `deponent.conformance` invocation. | Deponent command appears first. |
| H-11 | Bounded claim language ("not secure", "not audited", "not endorsed") appears before the first "GAK-conformant" example. | Mark shown without the bound. |
| H-12 | `verify` against a stale cert (wrong digest) exits nonzero even if the live kernel is conformant. | Exit `0` on digest mismatch. |

Minimum for the campaign profile: 8. These 12 are the product set.

---

## 13. Current README journeys vs required

| Current journey | Verdict |
|---|---|
| "Verify the reference kernel" via `python3 -m deponent.badge verify --kernel deponent` | **Wrong first-run.** Requires Deponent. Demotes this repo to a pamphlet. Move to Sequence D, relabeled. |
| "Score your own kernel" as four prose steps, no in-repo command, pointing at spec §7 and `from deponent.conformance import run_conformance` | **Incomplete.** Replace with Sequence B. Spec §7.1's Deponent import is a defect the product must not copy. |
| Artifact table before a runnable command | **Wrong hierarchy.** Table after first-run. |
| Status leads with v1.1 as current | **Wrong face for v0.** v1 (13 clauses) is the ship surface. v1.1 may be footnoted. |
| Honest "third-party verdicts: zero" | **Keep.** |

---

## 14. Conflicts with the current tree (do not silently paper over)

- `README.md` first-run is Deponent-owned (`python3 -m deponent.badge verify`).
- `v1/spec.md` §1 and §7.1 name Deponent as the reference harness (`from deponent.conformance import run_conformance`).
- `scripts/check_consistency.py` imports `deponent.badge` / `deponent.conformance` — mission-named coupling defect.
- Evidence pack and Appendix A still document the Deponent verify command as *the* verifier. v0 verifier lives in this repo.
- v1.1 amendment + v1.1 evidence exist; v0 product face is frozen v1.

Spec edits and harness extraction are **not** this lane. They are inputs to architecture / implementation. This doctrine binds the user-visible shape those lanes must hit.

---

## 15. Open product risks

- **Import story:** `python3 -m gak_conformance` on a raw clone needs a packaging decision. Hidden `PYTHONPATH` breaks first-use clarity.
- **Fixture honesty:** a fixture that returns the right answers is a simulation. It is legal only as selfcheck, never as a published mark.
- **Python-centric `--adapter module:Class`.** Acceptable for v0 (spec examples are Python). Do not pretend language neutrality in the CLI.
- **Fabricated adapters** cannot be fully detected. Trust UX is the void-claim language, not a detector.
- **Two CLIs** (`gak_conformance` vs leftover `deponent.badge` docs) will confuse if README is only half-updated.
- **Author-scored kernels (Deponent, sworncode) are not third-party verdicts.** Keep the count at zero.

---

*This doctrine does not implement features. Implementation, architecture, and QA consume the IDs above.*
