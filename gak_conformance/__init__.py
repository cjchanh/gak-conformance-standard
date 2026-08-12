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
from .artifacts import (
    ArtifactError,
    classify_artifact,
    resolve_verify_harness,
    validate_certification,
    validate_receipt,
)
from .receipt import CERT_SCHEMA, ConformanceReceipt, certification_from_receipt, clauses_digest
from .scorer import run_conformance

__all__ = [
    "ArtifactError",
    "CERT_SCHEMA",
    "HARNESS_V1",
    "HARNESS_V1_1",
    "ConformanceReceipt",
    "KernelAdapter",
    "__version__",
    "certification_from_receipt",
    "classify_artifact",
    "clauses_digest",
    "resolve_verify_harness",
    "run_conformance",
    "validate_certification",
    "validate_receipt",
]
