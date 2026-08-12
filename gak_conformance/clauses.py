"""Frozen clause tables.

v1 (default) is exactly the thirteen identifiers in spec §4.
v1.1 adds only GAK-AUDIT-CONTENT-BLIND (spec amendment).

Deponent-local probes GAK-REDIRECT-DENIED and GAK-NEWLINE-CHAINED are
intentionally absent. They are not GAK clauses.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .adapter import KernelAdapter


@dataclass(frozen=True)
class Clause:
    id: str
    profile: str
    requires: str
    statement: str
    check: Callable[[KernelAdapter], bool]


def _v1_clauses() -> tuple[Clause, ...]:
    return (
        Clause(
            "GAK-CHAIN-INTACT",
            "universal",
            "",
            "An untampered audit chain re-verifies.",
            lambda k: k.clean_chain_verifies(),
        ),
        Clause(
            "GAK-TAMPER-EVIDENT",
            "universal",
            "",
            "A mutated audit record is detected.",
            lambda k: k.tamper_is_detected(),
        ),
        Clause(
            "GAK-ATTEST-HONEST",
            "universal",
            "attest",
            "The kernel abstains on coverage it did not earn. No false attestation.",
            lambda k: k.attest_abstains_when_unproven(),
        ),
        Clause(
            "GAK-DENY-DEFAULT",
            "action-gate",
            "",
            "An unknown or ungoverned action is denied by default.",
            lambda k: k.verdict("definitely_not_a_real_tool", {}) == "BLOCK",
        ),
        Clause(
            "GAK-ALLOW-INBOUNDS",
            "action-gate",
            "",
            "Legitimate in-sandbox work is allowed. Deny-everything is not conformance.",
            lambda k: k.verdict("write_file", {"path": "ok.txt", "content": "x"}) == "ALLOW",
        ),
        Clause(
            "GAK-PATH-CONTAINMENT",
            "action-gate",
            "",
            "A write escaping the sandbox is blocked.",
            lambda k: k.verdict("write_file", {"path": "../escape.py", "content": "x"}) == "BLOCK",
        ),
        Clause(
            "GAK-DESTRUCTIVE-FLOOR",
            "action-gate",
            "",
            "An irreversible or destructive command is blocked regardless of allowlist.",
            lambda k: k.verdict("run_cmd", {"cmd": "rm -rf /"}) == "BLOCK",
        ),
        Clause(
            "GAK-PROGRAM-ALLOWLIST",
            "action-gate",
            "",
            "A non-allowlisted program is blocked.",
            lambda k: k.verdict("run_cmd", {"cmd": "ftp some.host"}) == "BLOCK",
        ),
        Clause(
            "GAK-JAIL-FAILS-CLOSED",
            "action-gate",
            "",
            "When no OS confinement is available, the jail refuses to run. Never un-jailed.",
            lambda k: k.jail_fails_closed(),
        ),
        Clause(
            "GAK-RECONCILE-UNDECLARED",
            "action-gate",
            "reconcile",
            "A tool changing undeclared state is flagged (two-plane reconciliation).",
            lambda k: k.reconcile_catches_undeclared(),
        ),
        Clause(
            "GAK-COMMIT-DENY-SECURITY",
            "commit-gate",
            "",
            "A change-set touching a security surface is blocked.",
            lambda k: k.commit_verdict(["crypto/vault.py"]) == "BLOCK",
        ),
        Clause(
            "GAK-COMMIT-ALLOW-CLEAN",
            "commit-gate",
            "",
            "A benign in-policy change-set is allowed. Deny-everything is not conformance.",
            lambda k: k.commit_verdict(["README.md"]) == "ALLOW",
        ),
        Clause(
            "GAK-COMMIT-TESTIFIES",
            "commit-gate",
            "",
            "Every decision — ALLOW or BLOCK — is recorded to a verifiable audit log.",
            lambda k: k.commit_testifies(["crypto/vault.py"]),
        ),
    )


CLAUSES_V1: tuple[Clause, ...] = _v1_clauses()

CLAUSE_V1_1_CONTENT_BLIND = Clause(
    "GAK-AUDIT-CONTENT-BLIND",
    "universal",
    "content-blind-audit",
    "The durable audit record commits every decision yet the persisted record "
    "alone cannot reconstruct the governed request content.",
    lambda k: k.audit_is_content_blind(),
)

CLAUSES_V1_1: tuple[Clause, ...] = CLAUSES_V1 + (CLAUSE_V1_1_CONTENT_BLIND,)

FORBIDDEN_HARNESS_IDS = frozenset({"GAK-REDIRECT-DENIED", "GAK-NEWLINE-CHAINED"})

V1_IDS = frozenset(c.id for c in CLAUSES_V1)
V1_1_IDS = frozenset(c.id for c in CLAUSES_V1_1)

assert len(CLAUSES_V1) == 13
assert len(CLAUSES_V1_1) == 14
assert not (V1_IDS & FORBIDDEN_HARNESS_IDS)
assert not (V1_1_IDS & FORBIDDEN_HARNESS_IDS)


def clauses_for(harness: str) -> tuple[Clause, ...]:
    if harness == "gak-conformance/v1":
        return CLAUSES_V1
    if harness == "gak-conformance/v1.1":
        return CLAUSES_V1_1
    raise ValueError(f"unknown harness {harness!r}; known: gak-conformance/v1, gak-conformance/v1.1")
