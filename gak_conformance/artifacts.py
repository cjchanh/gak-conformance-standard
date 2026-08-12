"""Inbound artifact contract: §5.1 receipt vs §5.2 certification.

The digest algorithm is a pure hash of (kernel, harness, clause pairs).
This module sits in front of the CLI so a certification cannot be
silently re-hashed as a receipt, and a receipt cannot be treated as
a published claim.

CUT-04: no explain-receipt command. Fail-closed messages on digest/verify
are the operator surface.
"""

from __future__ import annotations

from typing import Any, Mapping

from . import CERT_SCHEMA, HARNESS_V1, HARNESS_V1_1
from .clauses import clauses_for
from .receipt import clauses_digest

KIND_RECEIPT = "receipt"
KIND_CERTIFICATION = "certification"

ALLOWED_HARNESSES = frozenset({HARNESS_V1, HARNESS_V1_1})
ALLOWED_PROFILES = frozenset({"action-gate", "commit-gate"})
ALLOWED_STATUSES = frozenset({"PASS", "FAIL", "NA"})
_HEX64 = frozenset("0123456789abcdef")


class ArtifactError(ValueError):
    """Inbound JSON is the wrong type or fails the §5 contract."""


def classify_artifact(obj: Any) -> str:
    """Return KIND_RECEIPT or KIND_CERTIFICATION. Raise on unknown."""
    if not isinstance(obj, Mapping):
        raise ArtifactError("artifact must be a JSON object")
    schema = obj.get("schema_version")
    if schema == CERT_SCHEMA:
        return KIND_CERTIFICATION
    if "clauses_digest" in obj or obj.get("mark") in {
        "GAK-conformant",
        "not-conformant",
    }:
        return KIND_CERTIFICATION
    required = ("kernel", "profile", "conformant", "counts", "clauses")
    if all(key in obj for key in required):
        return KIND_RECEIPT
    raise ArtifactError(
        "unrecognized artifact: expected a §5.1 receipt "
        "(kernel/profile/conformant/counts/clauses) or a §5.2 certification "
        f"(schema_version={CERT_SCHEMA})"
    )


def _require_ascii_kernel(name: Any) -> str:
    if not isinstance(name, str) or not name or not name.isascii():
        raise ArtifactError("kernel name must be non-empty ASCII (spec §5.3)")
    return name


def _require_clauses(
    obj: Mapping[str, Any], *, need_receipt_fields: bool
) -> list[Mapping[str, Any]]:
    clauses = obj.get("clauses")
    if not isinstance(clauses, list) or not clauses:
        raise ArtifactError("clauses must be a non-empty array")
    out: list[Mapping[str, Any]] = []
    for item in clauses:
        if not isinstance(item, Mapping):
            raise ArtifactError("each clause must be an object")
        cid = item.get("id")
        if not isinstance(cid, str) or not cid:
            raise ArtifactError("each clause needs an id")
        if item.get("status") not in ALLOWED_STATUSES:
            raise ArtifactError(f"clause {cid!r} status must be PASS, FAIL, or NA")
        if need_receipt_fields:
            if "detail" not in item:
                raise ArtifactError(f"receipt clause {cid!r} needs detail (spec §5.1)")
            if "profile" not in item:
                raise ArtifactError(f"receipt clause {cid!r} needs profile (spec §5.1)")
        out.append(item)
    return out


def _counts_match(obj: Mapping[str, Any], clauses: list[Mapping[str, Any]]) -> None:
    counts = obj.get("counts")
    if not isinstance(counts, Mapping):
        raise ArtifactError("counts must be an object")
    derived = {
        "pass": sum(c["status"] == "PASS" for c in clauses),
        "fail": sum(c["status"] == "FAIL" for c in clauses),
        "na": sum(c["status"] == "NA" for c in clauses),
    }
    for key in ("pass", "fail", "na"):
        value = counts.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ArtifactError(f"counts.{key} must be a non-negative integer")
    if counts["pass"] + counts["fail"] + counts["na"] != len(clauses):
        raise ArtifactError("counts.pass + fail + na must equal the clause count")
    if {key: counts[key] for key in derived} != derived:
        raise ArtifactError("counts do not match clause statuses")


def _conformant_matches(obj: Mapping[str, Any], clauses: list[Mapping[str, Any]]) -> None:
    if not isinstance(obj.get("conformant"), bool):
        raise ArtifactError("conformant must be a boolean")
    expected = all(c["status"] != "FAIL" for c in clauses) and any(
        c["status"] == "PASS" for c in clauses
    )
    if bool(obj["conformant"]) is not expected:
        raise ArtifactError("conformant does not match §3.4 (no FAIL and ≥1 PASS)")


def _ids_match_harness(clauses: list[Mapping[str, Any]], harness: str) -> None:
    if harness not in ALLOWED_HARNESSES:
        raise ArtifactError(
            f"unknown harness {harness!r}; known: {HARNESS_V1}, {HARNESS_V1_1}"
        )
    expected = {clause.id for clause in clauses_for(harness)}
    got = [c["id"] for c in clauses]
    got_set = set(got)
    if len(got) != len(got_set):
        raise ArtifactError("artifact has duplicate clause ids")
    if got_set == expected:
        return
    hint = ""
    v1_ids = {clause.id for clause in clauses_for(HARNESS_V1)}
    v11_ids = {clause.id for clause in clauses_for(HARNESS_V1_1)}
    if got_set == v11_ids and harness == HARNESS_V1:
        hint = f" Use --harness {HARNESS_V1_1}."
    elif got_set == v1_ids and harness == HARNESS_V1_1:
        hint = f" This looks like a v1 artifact; use --harness {HARNESS_V1}."
    raise ArtifactError(
        f"clause ids do not match {harness} "
        f"(expected {len(expected)}, got {len(got_set)}).{hint}"
    )


def validate_receipt(obj: Any, *, harness: str = HARNESS_V1) -> Mapping[str, Any]:
    """Accept only a §5.1 receipt whose clause census matches harness."""
    if not isinstance(obj, Mapping):
        raise ArtifactError("artifact must be a JSON object")
    kind = classify_artifact(obj)
    if kind != KIND_RECEIPT:
        raise ArtifactError(
            f"digest --receipt expects a §5.1 receipt, not a {kind}. "
            "Pass the conformance receipt JSON. A certification already "
            "carries clauses_digest."
        )
    if "timestamp" in obj:
        raise ArtifactError("receipt must not contain timestamp (spec §5.1)")
    _require_ascii_kernel(obj.get("kernel"))
    if obj.get("profile") not in ALLOWED_PROFILES:
        raise ArtifactError("profile must be action-gate or commit-gate")
    clauses = _require_clauses(obj, need_receipt_fields=True)
    _ids_match_harness(clauses, harness)
    _counts_match(obj, clauses)
    _conformant_matches(obj, clauses)
    return obj


def validate_certification(obj: Any) -> Mapping[str, Any]:
    """Accept only a self-consistent §5.2 certification."""
    if not isinstance(obj, Mapping):
        raise ArtifactError("artifact must be a JSON object")
    kind = classify_artifact(obj)
    if kind != KIND_CERTIFICATION:
        raise ArtifactError(
            f"verify --cert expects a §5.2 certification "
            f"(schema_version={CERT_SCHEMA}), not a {kind}. "
            "Pass the certification JSON, not the receipt."
        )
    if obj.get("schema_version") != CERT_SCHEMA:
        raise ArtifactError(f"schema_version must be {CERT_SCHEMA}")
    harness = obj.get("harness_version")
    if harness not in ALLOWED_HARNESSES:
        raise ArtifactError(f"unknown harness_version {harness!r}")
    _require_ascii_kernel(obj.get("kernel"))
    if obj.get("profile") not in ALLOWED_PROFILES:
        raise ArtifactError("profile must be action-gate or commit-gate")
    clauses = _require_clauses(obj, need_receipt_fields=False)
    _ids_match_harness(clauses, harness)
    _counts_match(obj, clauses)
    _conformant_matches(obj, clauses)
    expected_mark = "GAK-conformant" if obj["conformant"] else "not-conformant"
    if obj.get("mark") != expected_mark:
        raise ArtifactError(
            f"mark {obj.get('mark')!r} is dishonest for "
            f"conformant={obj['conformant']} (spec §5.2 requires {expected_mark!r})"
        )
    digest = obj.get("clauses_digest")
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(ch not in _HEX64 for ch in digest)
    ):
        raise ArtifactError("clauses_digest must be a 64-hex digest")
    derived = clauses_digest({"kernel": obj["kernel"], "clauses": clauses}, harness)
    if derived != digest:
        raise ArtifactError(
            "certification clauses_digest does not match its own clause pairs "
            f"(derived {derived} != published {digest})"
        )
    return obj


def resolve_verify_harness(
    cert: Mapping[str, Any], requested: str | None
) -> str:
    """Inherit harness_version unless the operator passed a conflicting flag."""
    declared = cert["harness_version"]
    if requested is None or requested == declared:
        return str(declared)
    raise ArtifactError(
        f"--harness {requested} disagrees with certification "
        f"harness_version {declared}. Omit --harness to inherit the "
        "certification, or pass the matching value."
    )
