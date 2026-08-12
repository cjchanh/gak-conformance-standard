"""Commit-gate fixture that satisfies the v1 commit anchors."""

from __future__ import annotations


class PassingCommitAdapter:
    """Harness fixture. Not a kernel."""

    name = "fixture-commit"
    profile = "commit-gate"
    supports: frozenset[str] = frozenset()

    def commit_verdict(self, files: list) -> str:
        needles = ("crypto/", "auth/", "keys/")
        if any(any(n in f for n in needles) for f in files):
            return "BLOCK"
        return "ALLOW"

    def commit_testifies(self, files: list) -> bool:
        return True

    def clean_chain_verifies(self) -> bool:
        return True

    def tamper_is_detected(self) -> bool:
        return True
