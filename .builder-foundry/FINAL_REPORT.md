# Builder Foundry Final Report

Independent final audit of campaign `mission-gak-v0-standard-20260812`.
This auditor did **not** implement the product. Product tree was not edited.

## Result

**GAK v0 is a runnable, vendor-neutral conformance product.**

A stranger can clone this repo, stay at the repository root, and run:

```text
python3 -m gak_conformance --help
python3 -m gak_conformance selfcheck
python3 -m gak_conformance score \
  --adapter gak_conformance.fixtures.action_gate:PassingActionAdapter \
  --out receipt.json
```

That path needs no pip, no network, and no Deponent. It emits a §5.1 JSON
receipt. `selfcheck` writes `HARNESS_OK` on stderr and is **not** a kernel
certification.

Session-4 closed the inbound artifact contract (H1/H2):

- `digest --receipt` of the published v1 receipt exits **0** with
  `de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406`.
- `digest --receipt` of a certification exits **2** with **empty stdout**
  (no silent `d35b3247…` identity).
- `verify --cert` of a §5.1 receipt exits **2** naming certification vs
  receipt, not `BLOCKED: 'clauses_digest'`.

The product is technically correct, evidenced, locally releasable, and
security-acceptable. Residual `--adapter` import-exec (ACE) is documented.
This is **AUTOMATED_WORTH_TESTING**, not “quality proven.”

## Branch and HEAD

| Field | Value |
|---|---|
| Repo | `/Users/cj/Workspace/active/gak-conformance-standard` |
| Branch | `foundry/gak-v0-standard` |
| Audit HEAD | `03c32090fc1d17820217b63da3ddc46fc0b9f133` — `chore(foundry): session-4 architecture contract, evidence, and release` |
| Product commit | `526bc8fb716590a1b1020b5a25058690e78523e6` — `feat(gak): type inbound receipts and certifications` |
| Campaign baseline | `e55b068d2e933a5deecfc396ffadb5d8edd377f9` |
| Local commits since baseline | 9 (profile minimum 4) |
| Product tree at audit | clean (no `gak_conformance/` / `v1/` / tests dirty) |
| Profile | `standard` |

Reviewer independence (this wave):

- `architecture-review-s04.json`: `mode=reviewer`, `implemented_work=false`, `verdict=pass`
- `security-s04.json`: `mode=reviewer`, `implemented_work=false`, `verdict=pass`
- This audit (`final-audit-s04.json`): `mode=reviewer`, `implemented_work=false`

Writer lanes that implemented (`architecture-s04`, `release-s04`) did not
review their own work.

## Install / build / launch

No pip. CPython 3.10+. Repository root. Stdlib only.

```text
python3 -m gak_conformance --help
python3 -m gak_conformance selfcheck
python3 -m gak_conformance score \
  --adapter gak_conformance.fixtures.action_gate:PassingActionAdapter \
  --out receipt.json
python3 -m gak_conformance digest \
  --receipt v1/evidence/deponent-conformance-receipt.json
python3 scripts/check_consistency.py
```

Launch commands match `campaign.json`. Wrong-cwd contract: from an empty
directory, `python3 -m gak_conformance` exits nonzero with
`No module named gak_conformance`. That is expected, not a crash.

`--adapter module:Class` **imports and executes** that Python module.
Fixture adapters test the harness; they are not kernel certifications.
`--certify` on a `fixture-*` kernel exits 2 and writes no file.

Optional Deponent path (not first-run):

```text
python3 -m gak_conformance score \
  --adapter gak_conformance.adapters.deponent:DeponentKernelAdapter \
  --out deponent-receipt.json
```

If Deponent is absent the command exits 2 with a skip message. That is not
a harness crash. Author evidence in `v1/evidence/` is **not** a third-party
verdict.

## Verification

Independent re-run on 2026-08-12T19:19:13Z (working tree = HEAD product):

| Command | Exit | Observed |
|---|---|---|
| `python3 -m pytest -q` | 0 | **83 passed, 1 skipped** (live Deponent not installed) |
| `python3 scripts/check_consistency.py` | 0 | `CONSISTENT: gak-conformance/v1 — 13 clauses matched, published receipt re-derives de6b7089f894e009..., spec + in-repo harness agree; frozen v1 record preserved.` |
| `python3 -m gak_conformance --help` | 0 | Subcommands exactly `{score,verify,digest,list-clauses,selfcheck}`. ACE sentence present. Face: research prototype, not a security evaluation. |
| `python3 -m gak_conformance selfcheck` | 0 | stderr `HARNESS_OK fixture=fixture-action digest=9949c515… (not a kernel certification)`. stdout §5.1 JSON: 8 PASS / 0 FAIL / 5 NA, `kernel=fixture-action`. |
| `digest --receipt v1/evidence/deponent-conformance-receipt.json` | 0 | stdout **exactly** `de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406` (matches spec §5.3 worked value). |
| `digest --receipt v1/evidence/deponent-certification.json` | 2 | **stdout empty**. stderr names certification vs receipt. `d35b3247` absent. |
| `digest` of v1.1 receipt under default v1 | 2 | stdout empty. stderr: expected 13, got 14; hint `--harness gak-conformance/v1.1`. |
| `digest` of v1.1 receipt + `--harness gak-conformance/v1.1` | 0 | `cf26befe5ad50a18afb427e7257f9272142873ac11879cf2ab81b90eaedbf664` |
| `verify --cert` of the published §5.1 receipt | 2 | Typed BLOCKED: expects certification, not a receipt. |
| `verify --cert` of published Deponent cert vs fixture adapter | 1 | Digest mismatch `9949c515… != de6b7089…` (foreign kernel; never VERIFIED). |
| Fake JSON with only a 64-hex `clauses_digest` | 2 | `schema_version must be gak-certification/v1`. Not `KeyError 'clauses_digest'`. |
| `--certify` on PassingActionAdapter | 2 | No `--out` file written. Cannot mint `GAK-conformant`. |

Additional isolation (this audit):

- `import gak_conformance` + `cli` / `artifacts` / `scorer` / `receipt` / `load` leaves `deponent` out of `sys.modules`.
- `gak_conformance/adapters/deponent.py` uses `importlib` strings; no `import deponent`.
- `scripts/check_consistency.py` does not import Deponent (paths to evidence files only).
- Published receipt is §5.1: keys `{kernel, profile, conformant, counts, clauses}`, 13 clauses, **no timestamp**, 10/0/3, `kernel=deponent`, `profile=action-gate`.
- `v1/spec.md` SHA-256 `cebbc8ed855bec85934de6b80ec53b93590296fd3b922d0ad1ae0bee1e00a9f5` still carries the frozen digest.

Campaign ledgers at audit time (structural, not quality):

| Ledger | Count | Profile min | Notes |
|---|---|---|---|
| Features | 57/57 pass | 30 | All have verification |
| Hypotheses | 23 keep + result | 8 / 8 resolved | |
| Iterations | 7, all `user_visible`, all `reviewer_verdict=pass` | 6 / 3 visible | ITER-0007 reviewed by `architecture-review-s04` |
| Lane reports | 17 (+ this audit) | 6 | Required lanes present; no reviewer with `implemented_work=true` |
| Evidence | 24 hashed | 12 | |
| Claims | 29 approved | — | |
| Red-team loops | RED-0001 pass | 1 | |
| Holdout audits | HOLD-0001 pass | 1 | |
| Open critical/high blockers | 0 | 0 | BLK-0001–0006 closed |

Independent QA (session 3, `independent-qa-s03`) scored first-use / trust /
reuse PASS and called **AUTOMATED_WORTH_TESTING**. This audit agrees.
That is not “quality proven.”

## Release artifact

| Field | Value |
|---|---|
| Path | `.builder-foundry/release/artifact.zip` |
| SHA-256 | `5dada14d8113a06e24feba316163ef709c01b2dd1c0bd3b57c26a886326c01a6` |
| Matches `release.json` | **yes** (byte-for-byte) |
| `release.json` file_count | 52 product members |
| Zip namelist | 53 = 52 payload + `RELEASE_MANIFEST.json` |
| `forbidden_scan` | pass |
| `smoke_status` | pass |
| Created | 2026-08-12T19:14:00Z (release-s04 rebuild after inbound contract) |

Independent zip inspection:

- **No `.git/` directory or objects.** Only `.gitignore` and `.gitattributes`.
- **No secrets:** no `BEGIN PRIVATE KEY`, `AKIA…`, `ghp_`, `xai-` keys, `sk-live`.
- **No host path `/Users/cj`.** No `marathon.pid`. No `deponent/attest.py`, `00Agent`, `cds-compliance`, `CMMC-RMF`, `ATO-in-a-Box`.
- **No** `.builder-foundry/`, `MISSION_FOUNDRY_GAK_V0.md`, `AGENTS.builder-foundry.md`, `.agents/`, `.claude/`, `.grok/`.
- Zip `gak_conformance/artifacts.py` SHA-256 `b57dd97cb40a449229a9dc1976a49f67a184c1c8f28918c4f625fa15db8658f5` matches working tree; contains `validate_receipt` / `validate_certification`.
- Zip `gak_conformance/cli.py` SHA-256 `e6c3c35f276e29d2f9439a463b447709f6d39fcfccf42d030424941f4e622986` matches working tree.

Extracted-zip smoke (`/tmp/gak-audit-zip.UOKS3R`, `PYTHONPATH=.`):

| Command | Exit | Result |
|---|---|---|
| `python3 -m gak_conformance --help` | 0 | same face as working tree |
| `python3 -m gak_conformance selfcheck` | 0 | `HARNESS_OK` / fixture digest `9949c515…` |
| `digest --receipt v1/evidence/deponent-conformance-receipt.json` | 0 | `de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406` |
| `digest --receipt v1/evidence/deponent-certification.json` | 2 | stdout **0 bytes** |
| fixture `score --adapter …PassingActionAdapter` | 0 | stderr NOTE: fixture adapter — not a kernel certification |

`security-s04` noted a **stale pre-contract zip** at 19:12. `release-s04` rebuilt
the zip at 19:14. This audit hashed the rebuilt archive. Do not ship the
session-3 hash `2091e6aa…`.

Local artifact only. **No publish.**

## Strongest user-visible changes

1. **Third-party score path exists.** `python3 -m gak_conformance` is the
   harness. Deponent is a scored kernel, not the owner. Fixture selfcheck
   works on a clean clone.
2. **Receipts are checkable.** Frozen v1 digest `de6b7089…` re-derives from
   the published Deponent receipt (spec §5.3). Two runs of an unchanged
   kernel must match; no timestamp enters the digest.
3. **Typed inbound artifacts (D-008 / ITER-0007).** Digest refuses
   certifications and wrong-census receipts (exit 2, no hash). Verify
   refuses receipts (typed name). Verify inherits `harness_version`.
   Self-inconsistent certs fail before adapter import. Foreign kernels
   still fail closed at exit 1 (published digest is not a waiver).
4. **Mark language is bounded (spec §8).** README first-run is Sequence A.
   `selfcheck` says `HARNESS_OK`, not `GAK-conformant`. Fixtures cannot
   `--certify`. Face: research prototype, not a security evaluation.
5. **Public-safe leave-behind.** Spec + harness + adapter skeleton +
   schemas + one author-scored evidence pack. No attest/compliance maps
   in the zip or product tree.
6. **Fail-closed exits.** 0 = scored conformant or verify matched; 1 =
   scored not-conformant / all-NA / digest mismatch; 2 = could not score
   (bad adapter, type error, missing file).

## Research and design decisions

Accepted, binding:

| ID | Decision |
|---|---|
| D-001 | Own the frozen v1 scorer in this repo. Do not import `deponent.conformance` / `deponent.badge` as the harness. |
| D-002 | Digest uses Python `json.dumps(..., sort_keys=True)` default separators. Compact separators rejected. |
| D-003 | Deponent adapter is optional (`find_spec` + exit 2). No extra dependency. |
| D-004 | `verify` re-scores live and fail-closes. A published digest is not a waiver. |
| D-005 | Release zip excludes campaign/mission/agent trees. LICENSE + NOTICE + PEP 639. No REUSE gate. |
| D-006 | v0 cuts: no second CLI, no `explain-receipt`, no badge gallery, no adapter sandbox, no v1.1-primary table, no Deponent optional-dep, no frozen-spec edit. |
| D-007 | spec §7 / Appendix command path retargeted to `gak_conformance`. Frozen §3–§6 and digest untouched. |
| D-008 | Inbound JSON is typed (SLSA-style predicateType check, not signatures). Digest = §5.1 only. Verify = §5.2 only. Inherit `harness_version`. Type error = exit 2. |

Session-4 research (`session-04-artifact-contract.md`) copied the SLSA v1.2
*type check* and rejected Cosign / DSSE / TSA / auto-detect. Mission stays
offline SHA-256.

Spec §8 still bounds the mark: GAK-conformant means the adapter passed
`gak-conformance/v1` under its declared profile. Not secure. Not audited.
Not endorsed. A public claim MUST publish the certification JSON.

## Red-team and holdout

**RED-0001** (pass, remediations landed session 3): attacked README first
fence, no-args, path-like adapters, fixtures-as-mark, non-repo cwd, spec
§7 Deponent path, missing skeleton, mutated digest. Defects closed by
D-007, `HARNESS_OK`, fixture `--certify` refuse, adapter skeleton, README
repository-root contract, journey tests.

**HOLD-0001** (independent-holdout-s03, `implemented_work=false`, pass):
commit-gate first-run, brick FAIL, untouched skeleton FAIL, spec §7.1
imports `gak_conformance`, extracted-package help+selfcheck, empty-cwd
module error, library-built cert + fixture verify → VERIFIED.

Session-4 architecture review (C1–C8) and security review (H1/H2, ACE,
leave-behind, isolation) independently re-ran the oracles. This audit
re-ran them again. No remaining S1/S2 product defects.

## Remaining risks

These are **accepted residuals**, not closure blockers:

1. **`--adapter` is trusted-code ACE by design.** `load.py` is identifier-only
   `importlib` (no path / `eval` / pickle). Help, score help, README line 30,
   and CUT-10 document that import executes the module. Not a sandbox.
2. **`clauses_digest()` is a pure function.** A caller who bypasses
   `artifacts.validate_receipt` can still hash a v1.1 object under
   `HARNESS_V1` and get `d35b3247…`. The CLI / `artifacts.py` gate is
   fail-closed. D-008 chose this split.
3. **Adapter honesty (§6.3) is social.** A fabricated adapter that returns
   the right bools still scores. A claim from a simulated adapter is void.
   Not mechanically detectable without a live kernel.
4. **Live Deponent 13-clause re-score is environment-blocked** here
   (pytest skip: Deponent not installed). Published receipts validate
   self-consistent. They are author evidence, not a third-party verdict.
5. **Process residual:** `.gitignore` ignores `.builder-foundry/locks/` and
   `logs/` only. `git add -A` can still stage campaign host paths. The
   **release zip** does not contain `.builder-foundry/`.
6. **Not a security evaluation.** Spec §8. Residual exception-detail paths
   (`/tmp`, `/var/folders`) are not redacted (S3). Fixture certify refuse
   is by `fixture-` name prefix.

No open critical or high product defects. H1 (wrong public identity) and
H2 (untyped verify) are closed on the tree and in the rebuilt zip.

```text
TECHNICAL_VERDICT: PASS
PRODUCT_VERDICT: AUTOMATED_WORTH_TESTING
EVIDENCE_VERDICT: PASS
SECURITY_VERDICT: PASS
RELEASE_VERDICT: PASS
CAMPAIGN_GUARD: PASS
```

`python3 .builder-foundry-kit/scripts/foundry_guard.py --repo . --run-commands --write-report` exit 0 after this audit wave and evidence-hash repair (EVID-JOURNEYS-DOC, superseded EVID-RELEASE-S03 now tracks the rebuilt `release.json`; current identity is EVID-RELEASE-S04).

## Remote mutation

None. No push, deploy, publish, upload, PyPI, GitHub visibility change,
or operator-authorized external send was performed.
