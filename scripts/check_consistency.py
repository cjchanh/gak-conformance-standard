#!/usr/bin/env python3
"""check_consistency.py — spec.md vs in-repo harness vs published evidence.

Does not import Deponent. Exit 0 = consistent; 1 = mismatch; 3 = files missing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SPEC = ROOT / "v1" / "spec.md"
EVIDENCE_RECEIPT = ROOT / "v1" / "evidence" / "deponent-conformance-receipt.json"
EVIDENCE_CERT = ROOT / "v1" / "evidence" / "deponent-certification.json"
FROZEN_V1_DIGEST = "de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406"


def fail(code: int, msg: str) -> int:
    print(f"BLOCKED: {msg}", file=sys.stderr)
    return code


def main() -> int:
    if not SPEC.exists():
        return fail(3, f"spec not found: {SPEC}")
    spec_text = SPEC.read_text(encoding="utf-8")

    try:
        from gak_conformance.clauses import CLAUSES_V1, FORBIDDEN_HARNESS_IDS, V1_IDS
        from gak_conformance.receipt import clauses_digest
    except ImportError as e:
        return fail(3, f"in-repo harness not importable ({e}); cannot check")

    problems: list[str] = []

    spec_ids = set(re.findall(r"\*\*(GAK-[A-Z-]+)\*\*", spec_text))
    # Spec also names the v1.1 optional clause; v1 census is §4 minus that one.
    spec_v1 = spec_ids - {"GAK-AUDIT-CONTENT-BLIND"}
    if spec_v1 != V1_IDS:
        problems.append(
            f"v1 clause census mismatch: spec-only={sorted(spec_v1 - V1_IDS)} "
            f"harness-only={sorted(V1_IDS - spec_v1)}"
        )
    if len(CLAUSES_V1) != 13:
        problems.append(f"in-repo v1 clause count is {len(CLAUSES_V1)}, expected 13")
    if FROZEN_V1_DIGEST not in spec_text:
        problems.append("frozen v1 digest de6b7089… missing from spec")
    leaked = V1_IDS & FORBIDDEN_HARNESS_IDS
    if leaked:
        problems.append(f"forbidden Deponent-local ids in v1 harness: {sorted(leaked)}")

    for c in CLAUSES_V1:
        anchor = f"**{c.id}** — profile: `{c.profile}`"
        if c.requires:
            anchor += f", requires capability: `{c.requires}`"
        if anchor not in spec_text:
            problems.append(f"spec heading drift for {c.id}: expected '{anchor}'")

    if not EVIDENCE_RECEIPT.exists():
        problems.append(f"evidence receipt missing: {EVIDENCE_RECEIPT}")
    else:
        receipt = json.loads(EVIDENCE_RECEIPT.read_text(encoding="utf-8"))
        digest = clauses_digest(receipt, "gak-conformance/v1")
        if digest != FROZEN_V1_DIGEST:
            problems.append(f"published receipt re-derives {digest}, expected {FROZEN_V1_DIGEST}")
        if EVIDENCE_CERT.exists():
            cert = json.loads(EVIDENCE_CERT.read_text(encoding="utf-8"))
            if cert.get("clauses_digest") != digest:
                problems.append(
                    f"evidence certification digest {cert.get('clauses_digest')} != re-derived {digest}"
                )
        else:
            problems.append(f"evidence certification missing: {EVIDENCE_CERT}")

    if problems:
        for p in problems:
            print(f"INCONSISTENT: {p}", file=sys.stderr)
        return 1

    print(
        f"CONSISTENT: gak-conformance/v1 — {len(CLAUSES_V1)} clauses matched, "
        f"published receipt re-derives {FROZEN_V1_DIGEST[:16]}..., "
        f"spec + in-repo harness agree; frozen v1 record preserved."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
