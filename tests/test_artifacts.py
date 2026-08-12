"""Inbound artifact contract: receipt vs certification, harness inheritance."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from gak_conformance import HARNESS_V1, HARNESS_V1_1
from gak_conformance.artifacts import (
    KIND_CERTIFICATION,
    KIND_RECEIPT,
    ArtifactError,
    classify_artifact,
    resolve_verify_harness,
    validate_certification,
    validate_receipt,
)
from gak_conformance.fixtures.action_gate import PassingActionAdapter
from gak_conformance.receipt import certification_from_receipt
from gak_conformance.scorer import run_conformance

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = "de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406"
PUBLISHED_V11 = "cf26befe5ad50a18afb427e7257f9272142873ac11879cf2ab81b90eaedbf664"
WRONG_V11_AS_V1 = "d35b32472cb9353e248eb1312ebcaa79b1eb3a472e7f0c795471621900b416ca"
FIXTURE = "gak_conformance.fixtures.action_gate:PassingActionAdapter"
V1_RECEIPT = ROOT / "v1/evidence/deponent-conformance-receipt.json"
V1_CERT = ROOT / "v1/evidence/deponent-certification.json"
V11_RECEIPT = ROOT / "v1/evidence/deponent-conformance-receipt-v1.1.json"
V11_CERT = ROOT / "v1/evidence/deponent-certification-v1.1.json"


def _run(args):
    return subprocess.run(
        [sys.executable, "-m", "gak_conformance", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def _library_cert(path: Path, *, harness: str = HARNESS_V1, kernel: str | None = None) -> None:
    payload = run_conformance(PassingActionAdapter(), harness=harness).to_dict()
    if kernel is not None:
        payload = {**payload, "kernel": kernel}
    path.write_text(json.dumps(certification_from_receipt(payload, harness)))


def test_classify_published_receipt_and_cert():
    receipt = json.loads(V1_RECEIPT.read_text())
    cert = json.loads(V1_CERT.read_text())
    assert classify_artifact(receipt) == KIND_RECEIPT
    assert classify_artifact(cert) == KIND_CERTIFICATION


def test_digest_published_v1_receipt_still_matches():
    cp = _run(["digest", "--receipt", str(V1_RECEIPT)])
    assert cp.returncode == 0
    assert cp.stdout.strip() == PUBLISHED


def test_digest_refuses_published_certification():
    cp = _run(["digest", "--receipt", str(V1_CERT)])
    assert cp.returncode == 2
    err = cp.stderr.lower()
    assert "certification" in err
    assert "receipt" in err
    assert PUBLISHED not in cp.stdout


def test_digest_v11_receipt_without_harness_does_not_emit_wrong_hash():
    cp = _run(["digest", "--receipt", str(V11_RECEIPT)])
    assert cp.returncode == 2
    assert WRONG_V11_AS_V1 not in cp.stdout
    assert "v1.1" in cp.stderr
    cp_ok = _run(
        ["digest", "--receipt", str(V11_RECEIPT), "--harness", HARNESS_V1_1]
    )
    assert cp_ok.returncode == 0
    assert cp_ok.stdout.strip() == PUBLISHED_V11


def test_digest_v11_certification_does_not_emit_wrong_hash():
    cp = _run(["digest", "--receipt", str(V11_CERT)])
    assert cp.returncode == 2
    assert WRONG_V11_AS_V1 not in cp.stdout
    assert "certification" in cp.stderr.lower()


def test_digest_refuses_timestamped_receipt(tmp_path):
    data = json.loads(V1_RECEIPT.read_text())
    data["timestamp"] = "2026-08-12T00:00:00Z"
    path = tmp_path / "ts.json"
    path.write_text(json.dumps(data))
    cp = _run(["digest", "--receipt", str(path)])
    assert cp.returncode == 2
    assert "timestamp" in cp.stderr
    assert PUBLISHED not in cp.stdout


def test_verify_refuses_receipt_with_type_error():
    cp = _run(["verify", "--adapter", FIXTURE, "--cert", str(V1_RECEIPT)])
    assert cp.returncode == 2
    assert "clauses_digest" not in cp.stderr or "certification" in cp.stderr.lower()
    assert "receipt" in cp.stderr.lower()
    assert "BLOCKED:" in cp.stderr
    assert "'clauses_digest'" not in cp.stderr


def test_verify_inherits_v11_harness_from_cert(tmp_path):
    cert = tmp_path / "v11.json"
    _library_cert(cert, harness=HARNESS_V1_1)
    cp = _run(["verify", "--adapter", FIXTURE, "--cert", str(cert)])
    assert cp.returncode == 0, cp.stderr
    assert "VERIFIED" in cp.stdout


def test_verify_harness_flag_mismatch_exits_2(tmp_path):
    cert = tmp_path / "v11.json"
    _library_cert(cert, harness=HARNESS_V1_1)
    cp = _run(
        [
            "verify",
            "--adapter",
            FIXTURE,
            "--cert",
            str(cert),
            "--harness",
            HARNESS_V1,
        ]
    )
    assert cp.returncode == 2
    assert "disagrees" in cp.stderr
    assert "mismatch" not in cp.stderr


def test_verify_self_inconsistent_cert_exits_2(tmp_path):
    cert = tmp_path / "broken.json"
    _library_cert(cert)
    data = json.loads(cert.read_text())
    data["clauses_digest"] = "0" * 64
    cert.write_text(json.dumps(data))
    cp = _run(["verify", "--adapter", FIXTURE, "--cert", str(cert)])
    assert cp.returncode == 2
    assert "own clause pairs" in cp.stderr


def test_verify_self_consistent_foreign_digest_exits_1(tmp_path):
    """§5.4: a well-formed cert for another kernel is a mismatch, not a load error."""
    cert = tmp_path / "other.json"
    _library_cert(cert, kernel="stale-kernel")
    cp = _run(["verify", "--adapter", FIXTURE, "--cert", str(cert)])
    assert cp.returncode == 1
    assert "mismatch" in cp.stderr


def test_validate_receipt_rejects_cert_object():
    cert = json.loads(V1_CERT.read_text())
    try:
        validate_receipt(cert)
    except ArtifactError as exc:
        assert "certification" in str(exc)
    else:
        raise AssertionError("expected ArtifactError")


def test_validate_certification_rejects_receipt_object():
    receipt = json.loads(V1_RECEIPT.read_text())
    try:
        validate_certification(receipt)
    except ArtifactError as exc:
        assert "receipt" in str(exc)
    else:
        raise AssertionError("expected ArtifactError")


def test_resolve_verify_harness_inherits_and_conflicts():
    cert = json.loads(V1_CERT.read_text())
    assert resolve_verify_harness(cert, None) == HARNESS_V1
    assert resolve_verify_harness(cert, HARNESS_V1) == HARNESS_V1
    try:
        resolve_verify_harness(cert, HARNESS_V1_1)
    except ArtifactError as exc:
        assert "disagrees" in str(exc)
    else:
        raise AssertionError("expected ArtifactError")


def test_certification_from_receipt_rederives_conformant():
    payload = run_conformance(PassingActionAdapter()).to_dict()
    payload["conformant"] = False
    cert = certification_from_receipt(payload, HARNESS_V1)
    assert cert["conformant"] is True
    assert cert["mark"] == "GAK-conformant"


def test_classify_bypass_would_fail_census_gate():
    """Sabotage: hashing a v1.1 receipt under v1 is exactly the silent-wrong path."""
    receipt = json.loads(V11_RECEIPT.read_text())
    try:
        validate_receipt(receipt, harness=HARNESS_V1)
    except ArtifactError:
        pass
    else:
        raise AssertionError("census gate must catch a v1.1 receipt under v1")
    from gak_conformance.receipt import clauses_digest

    raw = clauses_digest(receipt, HARNESS_V1)
    assert raw == WRONG_V11_AS_V1
