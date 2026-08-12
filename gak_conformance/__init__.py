"""GAK conformance harness — vendor-neutral scorer for gak-conformance/v1.

This package is the mechanical mark. It does not import Deponent. A kernel
becomes scoreable by implementing the adapter contract in
``gak_conformance.adapter`` (spec §6).
"""

from __future__ import annotations

__version__ = "0.1.0"
HARNESS_V1 = "gak-conformance/v1"
HARNESS_V1_1 = "gak-conformance/v1.1"
CERT_SCHEMA = "gak-certification/v1"

from .adapter import KernelAdapter
from .receipt import CERT_SCHEMA, ConformanceReceipt, certification_from_receipt, clauses_digest
from .scorer import run_conformance

__all__ = [
    "CERT_SCHEMA",
    "HARNESS_V1",
    "HARNESS_V1_1",
    "ConformanceReceipt",
    "KernelAdapter",
    "__version__",
    "certification_from_receipt",
    "clauses_digest",
    "run_conformance",
]
