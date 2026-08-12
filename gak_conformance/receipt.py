"""Receipt, certification, and §5.3 clauses digest."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

CERT_SCHEMA = "gak-certification/v1"


@dataclass(frozen=True)
class ClauseResult:
    id: str
    profile: str
    status: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "profile": self.profile,
            "status": self.status,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class ConformanceReceipt:
    kernel: str
    profile: str
    harness: str
    results: tuple[ClauseResult, ...]

    @property
    def conformant(self) -> bool:
        """Spec §3.4: no FAIL, and at least one PASS."""
        return all(r.status != "FAIL" for r in self.results) and any(
            r.status == "PASS" for r in self.results
        )

    @property
    def counts(self) -> dict[str, int]:
        passed = sum(r.status == "PASS" for r in self.results)
        failed = sum(r.status == "FAIL" for r in self.results)
        na = sum(r.status == "NA" for r in self.results)
        return {"pass": passed, "fail": failed, "na": na}

    def to_dict(self) -> dict[str, Any]:
        # Spec §5.1 receipt: no timestamp, no harness field required.
        return {
            "kernel": self.kernel,
            "profile": self.profile,
            "conformant": self.conformant,
            "counts": self.counts,
            "clauses": [r.to_dict() for r in self.results],
        }

    def render(self) -> str:
        lines = [
            f"GAK CONFORMANCE — {self.kernel}  (profile: {self.profile}; {self.harness})",
            "=" * 60,
        ]
        marks = {"PASS": "ok ", "FAIL": "XX ", "NA": "-- "}
        for r in self.results:
            lines.append(f"  {marks.get(r.status, '?? ')}[{r.id}] {r.detail}")
        if self.conformant:
            lines.append("\nCONFORMANT")
        else:
            lines.append("\nNOT CONFORMANT — a required clause FAILED or nothing PASSed")
        return "\n".join(lines)


def clauses_digest(receipt: Mapping[str, Any], harness: str) -> str:
    """Spec §5.3. Default json.dumps separators (spaces). Do not compact."""
    kernel = receipt["kernel"]
    if not isinstance(kernel, str) or not kernel.isascii() or not kernel:
        raise ValueError("kernel name must be non-empty ASCII (spec §5.3)")
    pairs = sorted((c["id"], c["status"]) for c in receipt["clauses"])
    body = json.dumps(
        {"clauses": [list(p) for p in pairs], "harness": harness, "kernel": kernel},
        sort_keys=True,
        separators=(", ", ": "),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def certification_from_receipt(receipt: Mapping[str, Any], harness: str) -> dict[str, Any]:
    digest = clauses_digest(receipt, harness)
    conformant = bool(receipt["conformant"])
    return {
        "schema_version": CERT_SCHEMA,
        "harness_version": harness,
        "kernel": receipt["kernel"],
        "profile": receipt["profile"],
        "conformant": conformant,
        "mark": "GAK-conformant" if conformant else "not-conformant",
        "counts": receipt["counts"],
        "clauses_digest": digest,
        "clauses": [{"id": c["id"], "status": c["status"]} for c in receipt["clauses"]],
    }


def all_na_receipt(kernel: str, profile: str, harness: str, ids: Iterable[str]) -> ConformanceReceipt:
    results = tuple(
        ClauseResult(i, "universal", "NA", "constructed all-NA fixture") for i in ids
    )
    return ConformanceReceipt(kernel, profile, harness, results)
