"""§5.4 verify: live re-score + digest compare; stale cert is not ALLOW."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from gak_conformance import HARNESS_V1
from gak_conformance.fixtures.action_gate import PassingActionAdapter
from gak_conformance.receipt import certification_from_receipt
from gak_conformance.scorer import run_conformance

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = "gak_conformance.fixtures.action_gate:PassingActionAdapter"
BRICK = "gak_conformance.fixtures.brick:BrickActionAdapter"


def _write_library_cert(path: Path) -> None:
    """Verify needs a cert object. CLI refuses to certify fixtures."""
    payload = run_conformance(PassingActionAdapter()).to_dict()
    path.write_text(json.dumps(certification_from_receipt(payload, HARNESS_V1)))


def _run(args):
    return subprocess.run(
        [sys.executable, "-m", "gak_conformance", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_verify_matching_cert(tmp_path):
    cert = tmp_path / "cert.json"
    _write_library_cert(cert)
    verified = _run(["verify", "--adapter", FIXTURE, "--cert", str(cert)])
    assert verified.returncode == 0
    assert "VERIFIED" in verified.stdout


def test_verify_stale_digest_exits_1_even_if_live_conformant(tmp_path):
    """Doctrine H-12 / spec §5.4: published digest is not a waiver.

    A self-consistent cert for another kernel name is the stale-identity
    case. Mutating only clauses_digest makes the object self-inconsistent
    and is a load error (exit 2), not kernel drift.
    """
    payload = run_conformance(PassingActionAdapter()).to_dict()
    payload = {**payload, "kernel": "stale-kernel"}
    cert = tmp_path / "stale.json"
    cert.write_text(json.dumps(certification_from_receipt(payload, HARNESS_V1)))
    verified = _run(["verify", "--adapter", FIXTURE, "--cert", str(cert)])
    assert verified.returncode == 1
    assert "mismatch" in verified.stderr


def test_verify_nonconformant_live_exits_1(tmp_path):
    cert = tmp_path / "cert.json"
    _write_library_cert(cert)
    verified = _run(["verify", "--adapter", BRICK, "--cert", str(cert)])
    assert verified.returncode == 1
    assert "NOT CONFORMANT" in verified.stderr


def test_verify_bad_adapter_exits_2(tmp_path):
    cert = tmp_path / "cert.json"
    _write_library_cert(cert)
    verified = _run(["verify", "--adapter", "not.a.module:Nope", "--cert", str(cert)])
    assert verified.returncode == 2
    assert "BLOCKED" in verified.stderr


def test_verify_missing_cert_exits_2(tmp_path):
    verified = _run(
        ["verify", "--adapter", FIXTURE, "--cert", str(tmp_path / "missing.json")]
    )
    assert verified.returncode == 2
