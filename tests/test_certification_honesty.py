"""Published certification JSON must carry a self-assessed mark, not a bare GAK-conformant."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from certification_honesty import (  # noqa: E402
    BARE_CONFORMANT_MARK,
    SELF_ASSESSED_MARK,
    honesty_errors,
)

EVIDENCE = ROOT / "v1" / "evidence"


class HonestyPredicateTests(unittest.TestCase):
    def test_bare_conformant_mark_is_rejected(self) -> None:
        doc = {
            "conformant": True,
            "mark": BARE_CONFORMANT_MARK,
        }
        errors = honesty_errors(doc)
        self.assertTrue(errors)
        self.assertTrue(any("self_assessed" in e for e in errors))
        self.assertTrue(any(BARE_CONFORMANT_MARK in e for e in errors))

    def test_honest_self_assessment_is_accepted(self) -> None:
        doc = {
            "conformant": True,
            "mark": SELF_ASSESSED_MARK,
            "self_assessed": True,
            "third_party_verified": False,
        }
        self.assertEqual(honesty_errors(doc), [])


class PublishedEvidenceTests(unittest.TestCase):
    def test_every_certification_json_is_self_assessed(self) -> None:
        paths = sorted(EVIDENCE.glob("*-certification*.json"))
        self.assertGreaterEqual(len(paths), 3, "expected frozen certification JSON files")
        problems: list[str] = []
        for path in paths:
            doc = json.loads(path.read_text(encoding="utf-8"))
            problems.extend(honesty_errors(doc, source=path.name))
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
