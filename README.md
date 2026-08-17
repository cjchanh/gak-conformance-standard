# GAK Conformance Standard

[![CI](https://github.com/cjchanh/gak-conformance-standard/actions/workflows/ci.yml/badge.svg)](https://github.com/cjchanh/gak-conformance-standard/actions/workflows/ci.yml)

A vendor-neutral mechanical scorer for governed agent kernels.
Thirteen executable clauses. One JSON receipt. Anyone can re-derive it.

> A category is real when a third party can test against it and get a verdict.

This is a **research prototype**, not a security-evaluated product.
The mark means exactly: *the adapter passed `gak-conformance/v1` under its declared profile.*
Not "secure." Not "audited." Not "endorsed." (spec §8)

## First run (no Deponent)

From the **repository root** of a clone. CPython 3.10+. No pip. No network. No Deponent.

```
python3 -m gak_conformance --help
python3 -m gak_conformance selfcheck
python3 -m gak_conformance score \
  --adapter gak_conformance.fixtures.action_gate:PassingActionAdapter \
  --out receipt.json
```

`selfcheck` writes `HARNESS_OK` on stderr and a fixture receipt on stdout.
That proves the **scorer** runs. It is **not** a kernel certification.

If you are not in the repository root, Python says `No module named gak_conformance`.
`cd` into the clone. Set `PYTHONPATH` only when you invoke from another directory.

`--adapter module:Class` imports and executes that Python module.

## How to read a receipt

JSON fields: `kernel`, `profile`, `conformant`, `counts`, and 13 `clauses`
each with `id` / `profile` / `status` / `detail`. No timestamp.

| Exit | Meaning |
|---|---|
| `0` | scored and conformant, or verify matched |
| `1` | scored not-conformant, all-NA, or verify digest mismatch |
| `2` | could not score (bad `--adapter`, missing file, invalid declaration) |

`conformant` is true only when there is no FAIL and at least one PASS.

| Situation | Status | Exit |
|---|---|---|
| Out of profile | NA | — |
| Unclaimed optional capability | NA | — |
| Claimed but broken / method raises | FAIL | 1 |
| Deny-everything brick | FAIL on ALLOW | 1 |
| All-NA | not conformant | 1 |

`--certify` is refused on fixture adapters. A fixture cannot mint `GAK-conformant`.

## Score your kernel

Copy [`examples/adapter_skeleton.py`](examples/adapter_skeleton.py).
Drive your **real** kernel. Do not fabricate outcomes. The untouched skeleton scores FAIL.

```
python3 -m gak_conformance score \
  --adapter your_pkg.adapter:YourAdapter \
  --out certification.json --certify
```

1. Declare `action-gate` or `commit-gate`.
2. Claim only `reconcile` / `attest` if you implement them — unclaimed optional clauses score NA, never FAIL.
3. Publish the certification JSON. Re-check with `verify`.

You do not need Deponent. You need spec §6.

## Verify a published claim

```
python3 -m gak_conformance verify \
  --adapter your_pkg.adapter:YourAdapter \
  --cert certification.json
```

`verify` **re-runs** the kernel (spec §5.4) and fail-closes if the live score is
not conformant or the digest does not match. A previously published receipt
does not save a failing re-run. Pass a **§5.2 certification**, not the receipt.
`verify` inherits `harness_version` from the certification. Omit `--harness`
unless you intend to pass the same value; a conflicting flag exits `2`
(usage), not `1` (kernel drift).

`digest --receipt FILE` re-derives the published v1 digest
`de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406`
**without** running any kernel. It accepts a **§5.1 receipt only**. A
certification already carries `clauses_digest`. A v1.1 receipt needs
`--harness gak-conformance/v1.1` — the default v1 table will refuse it
instead of printing a wrong hash.

## Optional: score Deponent if it is installed locally

Deponent is the first *scored* kernel, not the owner of this standard.
The in-repo harness does **not** import Deponent until you ask for this adapter.
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

## What is in this repository

| Artifact | Path |
|---|---|
| **In-repo scorer** | [`gak_conformance/`](gak_conformance/) |
| **The standard (normative)** — 13 clauses, receipt + digest, adapter contract | [`v1/spec.md`](v1/spec.md) |
| Adapter skeleton (raises; not a mark) | [`examples/adapter_skeleton.py`](examples/adapter_skeleton.py) |
| Author-scored v1 receipt (Deponent, action-gate) | [`v1/evidence/deponent-conformance-receipt.json`](v1/evidence/deponent-conformance-receipt.json) |
| Author-scored v1 certification | [`v1/evidence/deponent-certification.json`](v1/evidence/deponent-certification.json) |
| Spec ↔ harness consistency checker | [`scripts/check_consistency.py`](scripts/check_consistency.py) |
| License / notices | [`LICENSE`](LICENSE), [`NOTICE`](NOTICE) |

## Status

**v0 ships frozen `gak-conformance/v1`** — 13 clauses, digest `de6b7089…`.
That is the default harness. Optional `--harness gak-conformance/v1.1` adds
one capability-gated clause (`GAK-AUDIT-CONTENT-BLIND`) and does not change
v1 receipts. Breaking changes require v2 (spec §9).

The first scored kernel is [Deponent](https://github.com/cjchanh/deponent)
(Centennial Defense Systems). The standard is vendor-neutral: Deponent does
not own the command, the clause table, or the first-run path.

**Author-scored kernels to date: two** —
[Deponent](https://github.com/cjchanh/deponent) (action-gate) and
[sworncode](https://github.com/cjchanh/sworn) (commit-gate, v1.1 evidence
under `v1/evidence/sworn-*`). Both are built by this standard's author.
**Third-party verdicts to date: zero.**
Two kernels prove the harness runs across two shapes, not independent adoption.

## License

Apache-2.0. © 2026 CJ — Centennial Defense Systems. See `LICENSE` and `NOTICE`.
Patent status: spec §10 — the normative clauses are published to be implemented
freely.
