"""Fixtures that raise or omit methods — must score FAIL, not pass."""

from __future__ import annotations


class RaisingActionAdapter:
    name = "fixture-raising"
    profile = "action-gate"
    supports: frozenset[str] = frozenset()

    def verdict(self, tool: str, params: dict) -> str:
        raise RuntimeError("kernel exploded")

    def clean_chain_verifies(self) -> bool:
        return True

    def tamper_is_detected(self) -> bool:
        return True

    def jail_fails_closed(self) -> bool:
        return True


class IncompleteAdapter:
    """Missing action-gate methods; checks should raise AttributeError → FAIL."""

    name = "fixture-incomplete"
    profile = "action-gate"
    supports: frozenset[str] = frozenset()

    def clean_chain_verifies(self) -> bool:
        return True

    def tamper_is_detected(self) -> bool:
        return True
