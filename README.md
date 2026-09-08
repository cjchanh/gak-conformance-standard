# GAK Conformance Standard

A vendor-neutral, mechanically testable standard for agent-action gates.
Thirteen executable clauses any kernel can be scored against, plus a
reproducible JSON record anyone can re-derive.

**Install.** This repository is the standard, not a pip package:

```
git clone https://github.com/cjchanh/gak-conformance-standard.git
```

**Example.** Re-score the reference kernel (Deponent must be installed):

```
python3 -m deponent.badge verify --kernel deponent
```

**Refuses.** A copied badge or JSON as third-party certification; a fabricated
adapter; any claim beyond the clause set. Results published here are
self-assessed by the standard's author.

## What is in this repository

| Artifact | Path |
|---|---|
| **The standard (normative)** — 7-primitive thesis, 3 profiles, 13 clauses, record + digest schema, adapter contract, worked example (a *hypothetical* commit-gate kernel, spec §7.2) | [`v1/spec.md`](v1/spec.md) |
| Reference conformance record (Deponent, action-gate) | [`v1/evidence/deponent-conformance-receipt.json`](v1/evidence/deponent-conformance-receipt.json) |
| Reference conformance report (self-assessed; digest-bearing) | [`v1/evidence/deponent-certification.json`](v1/evidence/deponent-certification.json) |
| Second-kernel conformance record (sworncode, commit-gate) | [`v1/evidence/sworn-conformance-receipt-v1.1.json`](v1/evidence/sworn-conformance-receipt-v1.1.json) |
| Second-kernel conformance report (self-assessed; digest-bearing) | [`v1/evidence/sworn-certification-v1.1.json`](v1/evidence/sworn-certification-v1.1.json) |
| Verifier output (fail-closed command, exit 0) | [`v1/evidence/deponent-verify-output.txt`](v1/evidence/deponent-verify-output.txt) |
| Two-run determinism proof (identical digests) | [`v1/evidence/determinism-proof.txt`](v1/evidence/determinism-proof.txt) |
| Harness clause census | [`v1/evidence/harness-clause-list.txt`](v1/evidence/harness-clause-list.txt) |
| Spec ↔ harness consistency checker | [`scripts/check_consistency.py`](scripts/check_consistency.py) |
| Why a third-party run is still the remaining test | [`docs/category.md`](docs/category.md) |
| License / notices | [`LICENSE`](LICENSE), [`NOTICE`](NOTICE) |

## The claim, bounded

A kernel that passes the harness may describe itself as **GAK-conformant
(self-assessed)** when the author ran the evaluator — meaning exactly: *it
passes the `gak-conformance/v1` clause set under its declared profile.* Not
"secure," not "audited," not "endorsed," not independently certified. The
bounded claim language is part of the standard (spec §8).

GAK is authored and maintained by [Centennial Defense Systems](https://centennialsystems.com/standards/gak). Passing a CDS-provided evaluator is **not third-party certification**.

## Verify the reference kernel

With the reference implementation (Deponent) installed:

```
python3 -m deponent.badge verify --kernel deponent
```

Re-runs the harness, re-derives the clauses digest, exits `0` only if the mark
is earned. Expected digest for the reference kernel:

```
de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406
```

Published certification JSON in this repo carries `self_assessed: true` and
`third_party_verified: false`. Check that without Deponent:

```
python3 -m unittest tests.test_certification_honesty -v
```

## Score your own kernel

You do not need Deponent's code to conform — you need the adapter contract
(spec §6) and a harness run (spec §7). Short version:

1. Declare your profile: `action-gate` (gates live tool calls) or
   `commit-gate` (gates proposed change-sets).
2. Claim only capabilities you implement (`reconcile`, `attest`) — unclaimed
   optional clauses score NA, never FAIL.
3. Implement the adapter methods for your profile against your **real** kernel.
4. Run the harness; publish your conformance-report JSON (self-declared until
   independently reproduced) so the claim is re-checkable.

Spec §7.2 walks a complete hypothetical commit-gate kernel through the process.

## Status

`gak-conformance/v1.1` — the current version. **v1 stays frozen** (13 clauses,
digest `de6b7089…`); **v1.1** adds one *optional* clause (`GAK-AUDIT-CONTENT-BLIND`,
content-blind audit) — 14 clauses, digest `cf26befe…`. The addition is
capability-gated, so no v1 record changes; see the **v1.1 Amendment** in the spec.
Breaking changes require v2 (spec §9). Reference implementation:
[Deponent](https://github.com/cjchanh/deponent) (Centennial Defense Systems). The
standard is vendor-neutral: Deponent is the first kernel scored against it, not the
owner of it.

**Scored kernels to date: two, across two gate shapes** —
[Deponent](https://github.com/cjchanh/deponent) (action-gate, 11 pass / 3 na) and
[sworncode](https://github.com/cjchanh/sworn) (commit-gate, 5 pass / 9 na, digest
`e65dd28b…`). Both are built by this standard's author. **Third-party verdicts to
date: zero.** See [`docs/category.md`](docs/category.md).

## License

Apache-2.0. © 2026 CJ — Centennial Defense Systems. See `LICENSE` and `NOTICE`.
Patent status: spec §10 — the normative clauses are published to be implemented
freely.
