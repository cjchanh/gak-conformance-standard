"""Harness fixtures — not kernel certifications.

These adapters exist so a stranger can run the scorer without Deponent and so
the harness can be tested. They special-case spec §4 anchors. A receipt they
produce is evidence about the *harness*, not about a real kernel (spec §6.3).
"""

from .action_gate import PassingActionAdapter
from .brick import BrickActionAdapter, BrickCommitAdapter
from .commit_gate import PassingCommitAdapter
from .raising import IncompleteAdapter, RaisingActionAdapter

__all__ = [
    "BrickActionAdapter",
    "BrickCommitAdapter",
    "IncompleteAdapter",
    "PassingActionAdapter",
    "PassingCommitAdapter",
    "RaisingActionAdapter",
]
