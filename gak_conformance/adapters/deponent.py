"""Optional Deponent adapter — drives the kernel, does not own the harness.

This module is safe to import when Deponent is absent. Construction loads
the kernel's public §6 class via importlib (string name). It never imports
``deponent.conformance`` or ``deponent.badge``.
"""

from __future__ import annotations

import importlib
import importlib.util

_INNER_MODULE = "deponent.adapters.deponent"
_INNER_CLASS = "DeponentAdapter"
_V1_CAPS = frozenset({"reconcile", "attest"})

SKIP_MESSAGE = (
    "Deponent is not importable. Install Deponent locally or score a fixture "
    "/ your own adapter. This harness does not require Deponent."
)


def deponent_available() -> bool:
    return importlib.util.find_spec("deponent") is not None


class DeponentKernelAdapter:
    """Thin wrap of Deponent's public adapter. Scores frozen v1 (13 clauses)."""

    def __init__(self) -> None:
        if not deponent_available():
            raise ImportError(SKIP_MESSAGE)
        try:
            mod = importlib.import_module(_INNER_MODULE)
            inner_cls = getattr(mod, _INNER_CLASS)
        except (ImportError, AttributeError) as exc:
            raise ImportError(
                "Deponent is installed but the public adapter "
                f"{_INNER_MODULE}:{_INNER_CLASS} is missing. {SKIP_MESSAGE}"
            ) from exc
        inner = inner_cls()
        self._inner = inner
        self.name = getattr(inner, "name", "deponent")
        self.profile = getattr(inner, "profile", "action-gate")
        claimed = frozenset(getattr(inner, "supports", ()) or ())
        self.supports = claimed & _V1_CAPS

    def clean_chain_verifies(self) -> bool:
        return self._inner.clean_chain_verifies()

    def tamper_is_detected(self) -> bool:
        return self._inner.tamper_is_detected()

    def verdict(self, tool: str, params: dict) -> str:
        return self._inner.verdict(tool, params)

    def jail_fails_closed(self) -> bool:
        return self._inner.jail_fails_closed()

    def reconcile_catches_undeclared(self) -> bool:
        return self._inner.reconcile_catches_undeclared()

    def attest_abstains_when_unproven(self) -> bool:
        return self._inner.attest_abstains_when_unproven()

    def commit_verdict(self, files: list) -> str:
        return self._inner.commit_verdict(files)

    def commit_testifies(self, files: list) -> bool:
        return self._inner.commit_testifies(files)
