"""Adapter contract (spec §6) — the whole integration surface.

A kernel author implements these attributes and the methods for their profile.
Implementing this MUST NOT require reading any kernel's internals.

``--adapter module:Class`` imports Python and executes the module. That is
intentional and residual: the harness cannot sandbox an adapter. Adapters
MUST drive a real kernel. Fixture adapters in ``gak_conformance.fixtures``
exist to test the *harness*; a receipt they produce is not a kernel
certification (spec §6.3 / §8).
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class KernelAdapter(Protocol):
    """What a kernel exposes to be GAK-tested."""

    name: str
    profile: str
    supports: frozenset

    def clean_chain_verifies(self) -> bool:
        """Untampered audit chain re-verifies (universal)."""

    def tamper_is_detected(self) -> bool:
        """A mutated audit record is detected (universal)."""

    def verdict(self, tool: str, params: dict) -> str:
        """Evaluate one live action → 'ALLOW' | 'BLOCK' (action-gate)."""

    def jail_fails_closed(self) -> bool:
        """Refuse to run un-jailed when confinement is unavailable (action-gate)."""

    def reconcile_catches_undeclared(self) -> bool:
        """Flag undeclared state change (requires capability 'reconcile')."""

    def attest_abstains_when_unproven(self) -> bool:
        """Abstain on unearned coverage (requires capability 'attest')."""

    def commit_verdict(self, files: list) -> str:
        """Evaluate a change-set → 'ALLOW' | 'BLOCK' (commit-gate)."""

    def commit_testifies(self, files: list) -> bool:
        """Decision lands in a verifiable audit log (commit-gate)."""

    def audit_is_content_blind(self) -> bool:
        """Optional v1.1: integrity without recoverable request content."""
