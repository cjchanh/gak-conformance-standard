# GAK Conformance Standard

A vendor-neutral, mechanically testable standard defining what makes an
agent-action gate a **governed agent kernel** (GAK): deny-by-default,
fail-closed, audit-chained, tamper-evident, bounded, honest, contained —
reduced to **thirteen executable clauses** any kernel can be scored against,
with a reproducible conformance receipt anyone can re-derive.

> A category is real when a third party can test against it and get a verdict.

## Score a kernel (no Deponent required)

From a clone of this repository:

```
python3 -m gak_conformance --help
python3 -m gak_conformance selfcheck
python3 -m gak_conformance score \
  --adapter gak_conformance.fixtures.action_gate:PassingActionAdapter \
  --out receipt.json
```

`selfcheck` and the `fixtures.*` adapters exercise the **harness**. They are
not a kernel certification. To score *your* kernel, implement spec §6 and
point `--adapter` at your `module:Class`. `--adapter` imports and executes
that module.

```
python3 -m gak_conformance score \
  --adapter your_pkg.adapter:YourAdapter \
  --out receipt.json
python3 -m gak_conformance verify \
  --adapter your_pkg.adapter:YourAdapter \
  --cert certification.json
python3 -m gak_conformance digest \
  --receipt v1/evidence/deponent-conformance-receipt.json
```

`digest` re-derives the published v1 digest
`de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406`
**without** running any kernel. `verify` **does** re-run the kernel (spec §5.4)
and fail-closes if the live score is not conformant or the digest does not
match.

| Exit | Meaning |
|---|---|
| `0` | scored and conformant, or verify matched |
| `1` | scored not-conformant, all-NA, or verify digest mismatch |
| `2` | could not score (bad `--adapter`, missing file, invalid declaration) |

A receipt is JSON with `kernel`, `profile`, `conformant`, `counts`, and 13
`clauses` each with `id` / `profile` / `status` / `detail`. No timestamp.
`conformant` is true only when there is no FAIL and at least one PASS. A
deny-everything brick FAILs the ALLOW clauses. All-NA is a refusal.

This is a **research prototype**, not a security-evaluated product. The mark
means exactly: *the adapter passed `gak-conformance/v1` under its declared
profile.* Not "secure," not "audited," not "endorsed" (spec §8).

## What is in this repository

| Artifact | Path |
|---|---|
| **In-repo scorer** — vendor-neutral harness (`python3 -m gak_conformance`) | [`gak_conformance/`](gak_conformance/) |
| **The standard (normative)** — 7-primitive thesis, 3 profiles, 13 clauses, receipt + digest schema, adapter contract, worked example (a *hypothetical* commit-gate kernel, spec §7.2) | [`v1/spec.md`](v1/spec.md) |
| Reference conformance receipt (Deponent, action-gate) | [`v1/evidence/deponent-conformance-receipt.json`](v1/evidence/deponent-conformance-receipt.json) |
| Reference certification (digest-bearing) | [`v1/evidence/deponent-certification.json`](v1/evidence/deponent-certification.json) |
| Second-kernel conformance receipt (sworncode, commit-gate) | [`v1/evidence/sworn-conformance-receipt-v1.1.json`](v1/evidence/sworn-conformance-receipt-v1.1.json) |
| Second-kernel certification (digest-bearing) | [`v1/evidence/sworn-certification-v1.1.json`](v1/evidence/sworn-certification-v1.1.json) |
| Verifier output (fail-closed command, exit 0) | [`v1/evidence/deponent-verify-output.txt`](v1/evidence/deponent-verify-output.txt) |
| Two-run determinism proof (identical digests) | [`v1/evidence/determinism-proof.txt`](v1/evidence/determinism-proof.txt) |
| Harness clause census | [`v1/evidence/harness-clause-list.txt`](v1/evidence/harness-clause-list.txt) |
| Spec ↔ harness consistency checker | [`scripts/check_consistency.py`](scripts/check_consistency.py) |
| License / notices | [`LICENSE`](LICENSE), [`NOTICE`](NOTICE) |

## The claim, bounded

A kernel that passes the harness may describe itself as **GAK-conformant** —
meaning exactly: *it passes the `gak-conformance/v1` clause set under its
declared profile.* Not "secure," not "audited," not "endorsed." The bounded
claim language is part of the standard (spec §8).

## Score Deponent if it is installed locally (optional)

Deponent is the first *scored* kernel, not the owner of this standard. The
in-repo harness does **not** import Deponent until you ask for this adapter.
If Deponent is not installed, the command exits `2` with a skip message —
that is not a harness crash.

```
python3 -m gak_conformance score \
  --adapter gak_conformance.adapters.deponent:DeponentKernelAdapter \
  --out deponent-receipt.json
```

Author-produced evidence in `v1/evidence/` is **not** a third-party verdict.
The historical `python3 -m deponent.badge verify` command lives in Deponent
and is not the GAK entrypoint.

Expected digest for the published v1 evidence pack:

```
de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406
```

## Score your own kernel

```
python3 -m gak_conformance score \
  --adapter your_pkg.adapter:YourAdapter \
  --out receipt.json --certify
```

You do not need Deponent. You need spec §6 (one class: `name`, `profile`,
`supports`, and the methods for your shape) driving your **real** kernel.

1. Declare `action-gate` or `commit-gate`.
2. Claim only `reconcile` / `attest` if you implement them — unclaimed
   optional clauses score NA, never FAIL.
3. Publish the certification JSON and re-check with `verify --cert`.

Spec §7.2 walks a hypothetical commit-gate kernel through the process.

## Status

**v0 ships frozen `gak-conformance/v1`** — 13 clauses, digest `de6b7089…`.
That is the default harness. Optional `--harness gak-conformance/v1.1` adds
one capability-gated clause (`GAK-AUDIT-CONTENT-BLIND`, digest `cf26befe…`)
and does not change v1 receipts. Breaking changes require v2 (spec §9).

The first scored kernel is [Deponent](https://github.com/cjchanh/deponent)
(Centennial Defense Systems). The standard is vendor-neutral: Deponent does
not own the command, the clause table, or the first-run path.

**Scored kernels to date: two, across two governance shapes** —
[Deponent](https://github.com/cjchanh/deponent) (action-gate, 11 pass / 3 na) and
[sworncode](https://github.com/cjchanh/sworn) (commit-gate, 5 pass / 9 na, digest
`e65dd28b…`). Both are built by this standard's author. **Third-party verdicts to
date: zero.** By the standard's own bar — "a category is real when a third party
can test against it and get a verdict" — that test is still open: two kernels prove
the harness runs across two governance shapes, not that the category has independent
adoption. If you score a kernel against the harness, open an issue with your receipt.

## License

Apache-2.0. © 2026 CJ — Centennial Defense Systems. See `LICENSE` and `NOTICE`.
Patent status: spec §10 — the normative clauses are published to be implemented
freely.
