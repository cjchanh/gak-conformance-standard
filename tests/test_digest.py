"""§5.3 digest must match published evidence; compact JSON must not."""

from __future__ import annotations

import json
from pathlib import Path

from gak_conformance.receipt import clauses_digest

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = "de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406"
COMPACT_WRONG = "65f40400dbaa6145afacdf5cd1de979c83150be6cfbab8d038ec0dacb14b2733"


def test_published_v1_receipt_rederives():
    receipt = json.loads((ROOT / "v1/evidence/deponent-conformance-receipt.json").read_text())
    assert clauses_digest(receipt, "gak-conformance/v1") == PUBLISHED


def test_v1_1_and_sworn_rederive():
    dep = json.loads((ROOT / "v1/evidence/deponent-conformance-receipt-v1.1.json").read_text())
    assert (
        clauses_digest(dep, "gak-conformance/v1.1")
        == "cf26befe5ad50a18afb427e7257f9272142873ac11879cf2ab81b90eaedbf664"
    )
    sworn = json.loads((ROOT / "v1/evidence/sworn-conformance-receipt-v1.1.json").read_text())
    assert (
        clauses_digest(sworn, "gak-conformance/v1.1")
        == "e65dd28b321406eee8f8fd0f4bbd9e7add16baf5a0f1fd04ca6459a34e28a6f1"
    )


def test_compact_separators_are_not_the_standard():
    receipt = json.loads((ROOT / "v1/evidence/deponent-conformance-receipt.json").read_text())
    got = clauses_digest(receipt, "gak-conformance/v1")
    assert got != COMPACT_WRONG
    assert got == PUBLISHED
