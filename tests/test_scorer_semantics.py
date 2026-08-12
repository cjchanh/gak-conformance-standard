"""Harness semantics: NA, FAIL-on-raise, brick, all-NA, counts."""

from __future__ import annotations

from gak_conformance.clauses import CLAUSES_V1
from gak_conformance.fixtures.action_gate import PassingActionAdapter
from gak_conformance.fixtures.brick import BrickActionAdapter, BrickCommitAdapter
from gak_conformance.fixtures.commit_gate import PassingCommitAdapter
from gak_conformance.fixtures.raising import IncompleteAdapter, RaisingActionAdapter
from gak_conformance.receipt import all_na_receipt
from gak_conformance.scorer import run_conformance


def _by_id(receipt, cid):
    return next(r for r in receipt.results if r.id == cid)


def test_passing_action_fixture_is_conformant_on_v1():
    r = run_conformance(PassingActionAdapter())
    assert r.conformant
    assert r.counts["fail"] == 0
    assert r.counts["pass"] + r.counts["fail"] + r.counts["na"] == 13
    assert _by_id(r, "GAK-ALLOW-INBOUNDS").status == "PASS"
    assert _by_id(r, "GAK-ATTEST-HONEST").status == "NA"
    assert _by_id(r, "GAK-RECONCILE-UNDECLARED").status == "NA"
    assert _by_id(r, "GAK-COMMIT-ALLOW-CLEAN").status == "NA"


def test_passing_commit_fixture_five_pass_eight_na():
    r = run_conformance(PassingCommitAdapter())
    assert r.conformant
    assert r.counts == {"pass": 5, "fail": 0, "na": 8}
    for cid in ("GAK-COMMIT-DENY-SECURITY", "GAK-COMMIT-ALLOW-CLEAN", "GAK-COMMIT-TESTIFIES"):
        assert _by_id(r, cid).status == "PASS"
    action = [x for x in r.results if x.profile == "action-gate"]
    assert action and all(x.status == "NA" for x in action)


def test_brick_action_fails_allow_inbounds():
    r = run_conformance(BrickActionAdapter())
    assert not r.conformant
    assert _by_id(r, "GAK-ALLOW-INBOUNDS").status == "FAIL"


def test_brick_commit_fails_allow_clean():
    r = run_conformance(BrickCommitAdapter())
    assert not r.conformant
    assert _by_id(r, "GAK-COMMIT-ALLOW-CLEAN").status == "FAIL"


def test_raise_is_fail_not_pass():
    r = run_conformance(RaisingActionAdapter())
    assert not r.conformant
    failed = [x for x in r.results if x.status == "FAIL"]
    assert failed
    assert any("RuntimeError" in x.detail for x in failed)


def test_missing_method_is_fail():
    r = run_conformance(IncompleteAdapter())
    assert not r.conformant
    assert _by_id(r, "GAK-DENY-DEFAULT").status == "FAIL"
    assert "AttributeError" in _by_id(r, "GAK-DENY-DEFAULT").detail


def test_host_path_is_redacted_in_detail():
    class PathRaising:
        name = "fixture-path-raise"
        profile = "action-gate"
        supports: frozenset[str] = frozenset()

        def verdict(self, tool, params):
            raise FileNotFoundError("/Users/" + "cj" + "/secret/vault.key")

        def clean_chain_verifies(self):
            return True

        def tamper_is_detected(self):
            return True

        def jail_fails_closed(self):
            return True

    r = run_conformance(PathRaising())
    detail = _by_id(r, "GAK-DENY-DEFAULT").detail
    assert "FileNotFoundError" in detail
    assert ("/Users/" + "cj") not in detail
    assert "<path>" in detail


def test_literal_anchors_are_dispatched():
    class Spy(PassingActionAdapter):
        name = "fixture-spy"

        def __init__(self):
            self.verdict_calls = []

        def verdict(self, tool, params):
            self.verdict_calls.append((tool, dict(params)))
            return super().verdict(tool, params)

    spy = Spy()
    run_conformance(spy)
    assert ("definitely_not_a_real_tool", {}) in spy.verdict_calls
    assert any(
        tool == "write_file" and params.get("path") == "ok.txt"
        for tool, params in spy.verdict_calls
    )


def test_claimed_attest_without_method_is_fail():
    class ClaimedNoAttest(PassingActionAdapter):
        name = "fixture-claimed-attest"
        supports = frozenset({"attest"})

    r = run_conformance(ClaimedNoAttest())
    assert not r.conformant
    assert _by_id(r, "GAK-ATTEST-HONEST").status == "FAIL"
    assert "AttributeError" in _by_id(r, "GAK-ATTEST-HONEST").detail


def test_all_na_is_not_conformant():
    r = all_na_receipt("empty", "action-gate", "gak-conformance/v1", [c.id for c in CLAUSES_V1])
    assert not r.conformant
    assert r.counts == {"pass": 0, "fail": 0, "na": 13}


def test_receipt_has_no_timestamp():
    r = run_conformance(PassingActionAdapter())
    assert "timestamp" not in r.to_dict()


def test_bad_profile_rejected():
    class Bad:
        name = "x"
        profile = "weird"
        supports = frozenset()

    try:
        run_conformance(Bad())
    except ValueError as exc:
        assert "profile" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_non_ascii_name_rejected():
    class Bad:
        name = "核"
        profile = "action-gate"
        supports = frozenset()

    try:
        run_conformance(Bad())
    except ValueError as exc:
        assert "ASCII" in str(exc)
    else:
        raise AssertionError("expected ValueError")
