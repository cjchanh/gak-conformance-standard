"""Action-gate fixture that satisfies the v1 anchors and claims no optional caps."""

from __future__ import annotations


class PassingActionAdapter:
    """Harness fixture. Not a kernel."""

    name = "fixture-action"
    profile = "action-gate"
    supports: frozenset[str] = frozenset()

    def verdict(self, tool: str, params: dict) -> str:
        if tool == "definitely_not_a_real_tool":
            return "BLOCK"
        if tool == "write_file":
            path = str(params.get("path", ""))
            if path == "ok.txt":
                return "ALLOW"
            return "BLOCK"
        if tool == "run_cmd":
            return "BLOCK"
        return "BLOCK"

    def clean_chain_verifies(self) -> bool:
        return True

    def tamper_is_detected(self) -> bool:
        return True

    def jail_fails_closed(self) -> bool:
        return True
