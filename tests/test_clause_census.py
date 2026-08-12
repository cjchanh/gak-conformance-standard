"""v0 owns the frozen 13-clause table; Deponent extras stay out."""

from __future__ import annotations

from gak_conformance.clauses import (
    CLAUSES_V1,
    CLAUSES_V1_1,
    FORBIDDEN_HARNESS_IDS,
    V1_IDS,
    clauses_for,
)


def test_v1_is_thirteen_spec_ids():
    assert len(CLAUSES_V1) == 13
    assert V1_IDS == {
        "GAK-CHAIN-INTACT",
        "GAK-TAMPER-EVIDENT",
        "GAK-ATTEST-HONEST",
        "GAK-DENY-DEFAULT",
        "GAK-ALLOW-INBOUNDS",
        "GAK-PATH-CONTAINMENT",
        "GAK-DESTRUCTIVE-FLOOR",
        "GAK-PROGRAM-ALLOWLIST",
        "GAK-JAIL-FAILS-CLOSED",
        "GAK-RECONCILE-UNDECLARED",
        "GAK-COMMIT-DENY-SECURITY",
        "GAK-COMMIT-ALLOW-CLEAN",
        "GAK-COMMIT-TESTIFIES",
    }


def test_v1_1_adds_only_content_blind():
    assert len(CLAUSES_V1_1) == 14
    extra = {c.id for c in CLAUSES_V1_1} - V1_IDS
    assert extra == {"GAK-AUDIT-CONTENT-BLIND"}


def test_deponent_extras_are_not_gak_clauses():
    assert not (V1_IDS & FORBIDDEN_HARNESS_IDS)
    assert not ({c.id for c in CLAUSES_V1_1} & FORBIDDEN_HARNESS_IDS)
    for hid in FORBIDDEN_HARNESS_IDS:
        assert all(c.id != hid for c in clauses_for("gak-conformance/v1"))
        assert all(c.id != hid for c in clauses_for("gak-conformance/v1.1"))
