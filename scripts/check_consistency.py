#!/usr/bin/env python3
"""check_consistency.py — fail-closed consistency check: spec.md vs live harness.

Verifies, mechanically, that the normative spec and the reference harness agree:

  1. clause census — the 13 clause IDs in v1/spec.md exactly match the harness
     CLAUSES set (ids, profiles, required capabilities);
  2. digest determinism — two consecutive certifications of the reference kernel
     produce the same clauses_digest;
  3. worked value — the digest in the spec's §5.3/Appendix A matches the live
     digest of the reference kernel;
  4. evidence freshness — the receipt in v1/evidence/ carries the same digest.

Exit codes: 0 = consistent; 1 = inconsistency found; 3 = cannot check
(harness not importable / files missing) — fail-closed, never a silent pass.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "v1" / "spec.md"
EVIDENCE_CERT = ROOT / "v1" / "evidence" / "deponent-certification.json"


def fail(code: int, msg: str) -> int:
    print(f"BLOCKED: {msg}", file=sys.stderr)
    return code


def main() -> int:
    if not SPEC.exists():
        return fail(3, f"spec not found: {SPEC}")
    spec_text = SPEC.read_text(encoding="utf-8")

    try:
        from deponent.badge import certify
        from deponent.conformance import CLAUSES
    except ImportError as e:
        return fail(3, f"reference harness not importable ({e}); cannot check")

    problems: list[str] = []

    # 1. clause census — every harness clause appears in the spec with its
    # profile; every GAK-* id in the spec's clause sections exists in the harness.
    harness_ids = {c.id for c in CLAUSES}
    spec_ids = set(re.findall(r"\*\*(GAK-[A-Z-]+)\*\*", spec_text))
    if spec_ids != harness_ids:
        problems.append(
            f"clause census mismatch: spec-only={sorted(spec_ids - harness_ids)} "
            f"harness-only={sorted(harness_ids - spec_ids)}")
    if len(CLAUSES) != 13:
        problems.append(f"harness clause count is {len(CLAUSES)}, spec says 13")
    for c in CLAUSES:
        anchor = f"**{c.id}** — profile: `{c.profile}`"
        if c.requires:
            anchor += f", requires capability: `{c.requires}`"
        if anchor not in spec_text:
            problems.append(f"spec heading drift for {c.id}: expected '{anchor}'")

    # 2 + 3. determinism and the worked value.
    d1 = certify("deponent").clauses_digest
    d2 = certify("deponent").clauses_digest
    if d1 != d2:
        problems.append(f"digest not deterministic: {d1} != {d2}")
    if d1 not in spec_text:
        problems.append(f"live reference digest {d1} not present in spec")

    # 4. evidence freshness.
    if EVIDENCE_CERT.exists():
        ev = json.loads(EVIDENCE_CERT.read_text(encoding="utf-8"))
        if ev.get("clauses_digest") != d1:
            problems.append(
                f"evidence certification digest {ev.get('clauses_digest')} "
                f"!= live {d1}")
    else:
        problems.append(f"evidence certification missing: {EVIDENCE_CERT}")

    if problems:
        for p in problems:
            print(f"INCONSISTENT: {p}", file=sys.stderr)
        return 1

    print(f"CONSISTENT: 13 clauses matched, digest deterministic ({d1[:16]}...), "
          f"spec worked value and evidence bundle agree with the live harness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
