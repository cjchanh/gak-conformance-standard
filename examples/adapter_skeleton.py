"""Copy-paste adapter skeleton (spec §6).

This is not a kernel. Every method raises so a score produces FAIL,
never a fabricated PASS. Drive your real kernel; do not return canned
ALLOW/BLOCK strings that you did not compute.

Usage (from the repository root, after you put this class on PYTHONPATH):

    python3 -m gak_conformance score \\
      --adapter adapter_skeleton:YourKernelAdapter --out receipt.json
"""

from __future__ import annotations


class YourKernelAdapter:
    """Replace these attributes. Claim only what the kernel actually does."""

    name = "your-kernel"
    profile = "action-gate"  # or "commit-gate"
    supports: frozenset[str] = frozenset()  # add "reconcile" / "attest" only if real

    def clean_chain_verifies(self) -> bool:
        raise NotImplementedError("drive your real kernel's audit chain")

    def tamper_is_detected(self) -> bool:
        raise NotImplementedError("mutate one recorded field; verification must fail")

    def verdict(self, tool: str, params: dict) -> str:
        raise NotImplementedError("action-gate: return 'ALLOW' or 'BLOCK' from the kernel")

    def jail_fails_closed(self) -> bool:
        raise NotImplementedError("action-gate: refuse to run un-jailed")

    def commit_verdict(self, files: list) -> str:
        raise NotImplementedError("commit-gate only; omit this method on action-gate")

    def commit_testifies(self, files: list) -> bool:
        raise NotImplementedError("commit-gate only; omit this method on action-gate")
