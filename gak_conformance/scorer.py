"""Drive an adapter through the clause table. Fail-closed on raise."""

from __future__ import annotations

import re

from . import HARNESS_V1
from .adapter import KernelAdapter
from .clauses import Clause, clauses_for
from .receipt import ClauseResult, ConformanceReceipt

ALLOWED_PROFILES = frozenset({"action-gate", "commit-gate"})

# Spec §6.3 records type + message. CWE-209: do not publish host home paths.
_HOST_PATH = re.compile(
    r"(?:/Users/|/home/|[A-Za-z]:\\Users\\)[^\s'\"`,]+"
)


def _detail_for_exception(exc: BaseException, statement: str) -> str:
    redacted = _HOST_PATH.sub("<path>", str(exc))
    return f"check raised {type(exc).__name__}: {redacted}. {statement}"


def run_conformance(
    kernel: KernelAdapter,
    *,
    harness: str = HARNESS_V1,
    clauses: tuple[Clause, ...] | None = None,
) -> ConformanceReceipt:
    if getattr(kernel, "profile", None) not in ALLOWED_PROFILES:
        raise ValueError(
            f"adapter.profile must be 'action-gate' or 'commit-gate', got {getattr(kernel, 'profile', None)!r}"
        )
    name = getattr(kernel, "name", "")
    if not isinstance(name, str) or not name or not name.isascii():
        raise ValueError("adapter.name must be non-empty ASCII (spec §5.3)")
    table = clauses if clauses is not None else clauses_for(harness)
    supports = frozenset(getattr(kernel, "supports", ()) or ())
    results: list[ClauseResult] = []
    for c in table:
        if c.profile not in ("universal", kernel.profile):
            results.append(
                ClauseResult(
                    c.id,
                    c.profile,
                    "NA",
                    f"out of profile ({c.profile}); kernel is {kernel.profile}. {c.statement}",
                )
            )
            continue
        if c.requires and c.requires not in supports:
            results.append(
                ClauseResult(
                    c.id,
                    c.profile,
                    "NA",
                    f"kernel does not claim '{c.requires}'. {c.statement}",
                )
            )
            continue
        try:
            ok = bool(c.check(kernel))
        except Exception as exc:
            results.append(
                ClauseResult(
                    c.id,
                    c.profile,
                    "FAIL",
                    _detail_for_exception(exc, c.statement),
                )
            )
            continue
        results.append(
            ClauseResult(c.id, c.profile, "PASS" if ok else "FAIL", c.statement)
        )
    return ConformanceReceipt(name, kernel.profile, harness, tuple(results))
