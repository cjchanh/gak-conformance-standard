#!/usr/bin/env python3
"""Fail-closed check: spec.md, published certification JSON, and live harness agree."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from certification_honesty import honesty_errors

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "v1" / "spec.md"
EVIDENCE_DIR = ROOT / "v1" / "evidence"


def fail(code: int, msg: str) -> int:
    print(f"BLOCKED: {msg}", file=sys.stderr)
    return code


def published_cert_paths() -> list[Path]:
    return sorted(EVIDENCE_DIR.glob("*-certification*.json"))


def evidence_honesty_problems() -> list[str]:
    problems: list[str] = []
    for path in published_cert_paths():
        ev = json.loads(path.read_text(encoding="utf-8"))
        problems.extend(honesty_errors(ev, source=path.name))
    if not published_cert_paths():
        problems.append("no published *-certification*.json files under v1/evidence/")
    return problems


def main() -> int:
    if not SPEC.exists():
        return fail(3, f"spec not found: {SPEC}")
    spec_text = SPEC.read_text(encoding="utf-8")
    honesty = evidence_honesty_problems()

    try:
        from deponent.badge import HARNESS_VERSION, certify
        from deponent.conformance import CLAUSES
    except ImportError as e:
        if honesty:
            for p in honesty:
                print(f"INCONSISTENT: {p}", file=sys.stderr)
            return 1
        return fail(3, f"reference harness not importable ({e}); cannot check")

    # Version-aware: the live harness declares its own version. v1 stays frozen at
    # 13 clauses / de6b7089; v1.1 adds the optional content-blind clause (14 clauses).
    # The checker verifies the LIVE version against its own evidence + spec, and
    # separately asserts the frozen v1 digest is still preserved in the spec.
    FROZEN_V1_DIGEST = "de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406"
    EXPECTED = {"gak-conformance/v1": 13, "gak-conformance/v1.1": 14}
    expected_clauses = EXPECTED.get(HARNESS_VERSION)
    suffix = "" if HARNESS_VERSION == "gak-conformance/v1" else f"-{HARNESS_VERSION.split('/')[-1]}"
    evidence_cert = EVIDENCE_DIR / f"deponent-certification{suffix}.json"

    problems: list[str] = list(honesty)

    harness_ids = {c.id for c in CLAUSES}
    spec_ids = set(re.findall(r"\*\*(GAK-[A-Z-]+)\*\*", spec_text))
    if spec_ids != harness_ids:
        problems.append(
            f"clause census mismatch: spec-only={sorted(spec_ids - harness_ids)} "
            f"harness-only={sorted(harness_ids - spec_ids)}")
    if expected_clauses is None:
        problems.append(f"unknown harness version {HARNESS_VERSION!r}; add it to EXPECTED")
    elif len(CLAUSES) != expected_clauses:
        problems.append(f"harness clause count is {len(CLAUSES)}, {HARNESS_VERSION} expects {expected_clauses}")
    if FROZEN_V1_DIGEST not in spec_text:
        problems.append("frozen v1 digest de6b7089… missing from spec (v1 record must be preserved)")
    for c in CLAUSES:
        anchor = f"**{c.id}** — profile: `{c.profile}`"
        if c.requires:
            anchor += f", requires capability: `{c.requires}`"
        if anchor not in spec_text:
            problems.append(f"spec heading drift for {c.id}: expected '{anchor}'")

    d1 = certify("deponent").clauses_digest
    d2 = certify("deponent").clauses_digest
    if d1 != d2:
        problems.append(f"digest not deterministic: {d1} != {d2}")
    if d1 not in spec_text:
        problems.append(f"live reference digest {d1} not present in spec")

    if evidence_cert.exists():
        ev = json.loads(evidence_cert.read_text(encoding="utf-8"))
        if ev.get("clauses_digest") != d1:
            problems.append(
                f"evidence certification digest {ev.get('clauses_digest')} "
                f"!= live {d1}")
    else:
        problems.append(f"evidence certification missing: {evidence_cert}")

    sworn_cert_path = EVIDENCE_DIR / f"sworn-certification{suffix}.json"
    try:
        import sworn  # noqa: F401
        sworn_importable = True
    except ImportError:
        sworn_importable = False
    if sworn_importable:
        s1 = certify("sworn").clauses_digest
        s2 = certify("sworn").clauses_digest
        if s1 != s2:
            problems.append(f"sworn digest not deterministic: {s1} != {s2}")
        if sworn_cert_path.exists():
            sev = json.loads(sworn_cert_path.read_text(encoding="utf-8"))
            if sev.get("clauses_digest") != s1:
                problems.append(
                    f"sworn evidence certification digest "
                    f"{sev.get('clauses_digest')} != live {s1}")
        else:
            problems.append(
                f"sworn kernel importable but evidence missing: {sworn_cert_path}")
    elif sworn_cert_path.exists():
        print(
            "NOTICE: sworn evidence present but the sworncode kernel is not "
            "importable here — second-kernel digest not re-verified this run",
            file=sys.stderr,
        )

    if problems:
        for p in problems:
            print(f"INCONSISTENT: {p}", file=sys.stderr)
        return 1

    print(f"CONSISTENT (SELF-ASSESSED): {HARNESS_VERSION} — {len(CLAUSES)} clauses matched, digest "
          f"deterministic ({d1[:16]}...), spec + evidence agree with the live harness; "
          f"frozen v1 record preserved. This is a self-assessed conformance report run by the "
          f"implementer, not a certification; it is void for an adapter that returns canned outputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
