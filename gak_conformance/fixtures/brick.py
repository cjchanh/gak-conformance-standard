"""Deny-everything fixtures — must not be conformant."""

from __future__ import annotations


class BrickActionAdapter:
    name = "fixture-brick-action"
    profile = "action-gate"
    supports: frozenset[str] = frozenset()

    def verdict(self, tool: str, params: dict) -> str:
        return "BLOCK"

    def clean_chain_verifies(self) -> bool:
        return True

    def tamper_is_detected(self) -> bool:
        return True

    def jail_fails_closed(self) -> bool:
        return True


class BrickCommitAdapter:
    name = "fixture-brick-commit"
    profile = "commit-gate"
    supports: frozenset[str] = frozenset()

    def commit_verdict(self, files: list) -> str:
        return "BLOCK"

    def commit_testifies(self, files: list) -> bool:
        return True

    def clean_chain_verifies(self) -> bool:
        return True

    def tamper_is_detected(self) -> bool:
        return True
