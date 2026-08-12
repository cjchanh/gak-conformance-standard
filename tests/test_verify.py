"""§5.4 verify: live re-score + digest compare; stale cert is not ALLOW."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = "gak_conformance.fixtures.action_gate:PassingActionAdapter"
BRICK = "gak_conformance.fixtures.brick:BrickActionAdapter"


def _run(args):
    return subprocess.run(
        [sys.executable, "-m", "gak_conformance", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_verify_matching_cert(tmp_path):
    cert = tmp_path / "cert.json"
    scored = _run(["score", "--certify", "--adapter", FIXTURE, "--out", str(cert)])
    assert scored.returncode == 0
    verified = _run(["verify", "--adapter", FIXTURE, "--cert", str(cert)])
    assert verified.returncode == 0
    assert "VERIFIED" in verified.stdout


def test_verify_stale_digest_exits_1_even_if_live_conformant(tmp_path):
    """Doctrine H-12 / spec §5.4: published digest is not a waiver."""
    cert = tmp_path / "stale.json"
    _run(["score", "--certify", "--adapter", FIXTURE, "--out", str(cert)])
    data = json.loads(cert.read_text())
    data["clauses_digest"] = "0" * 64
    cert.write_text(json.dumps(data))
    verified = _run(["verify", "--adapter", FIXTURE, "--cert", str(cert)])
    assert verified.returncode == 1
    assert "mismatch" in verified.stderr


def test_verify_nonconformant_live_exits_1(tmp_path):
    cert = tmp_path / "cert.json"
    _run(["score", "--certify", "--adapter", FIXTURE, "--out", str(cert)])
    verified = _run(["verify", "--adapter", BRICK, "--cert", str(cert)])
    assert verified.returncode == 1
    assert "NOT CONFORMANT" in verified.stderr


def test_verify_bad_adapter_exits_2(tmp_path):
    cert = tmp_path / "cert.json"
    _run(["score", "--certify", "--adapter", FIXTURE, "--out", str(cert)])
    verified = _run(["verify", "--adapter", "not.a.module:Nope", "--cert", str(cert)])
    assert verified.returncode == 2
    assert "BLOCKED" in verified.stderr


def test_verify_missing_cert_exits_2(tmp_path):
    verified = _run(
        ["verify", "--adapter", FIXTURE, "--cert", str(tmp_path / "missing.json")]
    )
    assert verified.returncode == 2
