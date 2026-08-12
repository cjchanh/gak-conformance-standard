"""CLI: help, digest, selfcheck, score, fail-closed exits."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = "de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406"


def _run(args, **kwargs):
    return subprocess.run(
        [sys.executable, "-m", "gak_conformance", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        **kwargs,
    )


def test_no_args_exits_two():
    cp = _run([])
    assert cp.returncode == 2


def test_help_exits_zero():
    cp = _run(["--help"])
    assert cp.returncode == 0
    assert "adapter" in cp.stdout.lower()
    assert "imports and executes" in cp.stdout.lower()
    for name in ("score", "selfcheck", "verify", "list-clauses", "digest"):
        assert name in cp.stdout


def test_list_clauses_prints_v1_ids():
    cp = _run(["list-clauses"])
    assert cp.returncode == 0
    for cid in (
        "GAK-DENY-DEFAULT",
        "GAK-ALLOW-INBOUNDS",
        "GAK-COMMIT-ALLOW-CLEAN",
        "GAK-CHAIN-INTACT",
    ):
        assert cid in cp.stdout
    assert "GAK-AUDIT-CONTENT-BLIND" not in cp.stdout
    assert "GAK-REDIRECT-DENIED" not in cp.stdout
    assert cp.stdout.count("GAK-") == 13


def test_digest_published_receipt():
    cp = _run(
        [
            "digest",
            "--receipt",
            "v1/evidence/deponent-conformance-receipt.json",
        ]
    )
    assert cp.returncode == 0
    assert cp.stdout.strip() == PUBLISHED


def test_selfcheck_conformant():
    cp = _run(["selfcheck"])
    assert cp.returncode == 0
    receipt = json.loads(cp.stdout)
    assert receipt["conformant"] is True
    assert receipt["kernel"].startswith("fixture-")
    assert len(receipt["clauses"]) == 13
    assert "timestamp" not in receipt
    assert "HARNESS_OK" in cp.stderr
    assert "not a kernel certification" in cp.stderr
    assert "GAK-conformant" not in cp.stdout
    assert "GAK-conformant" not in cp.stderr
    assert "\nCONFORMANT" not in cp.stdout
    assert "\nCONFORMANT" not in cp.stderr


def test_selfcheck_out_does_not_print_mark_banner(tmp_path):
    dest = tmp_path / "fixture.json"
    cp = _run(["selfcheck", "--out", str(dest)])
    assert cp.returncode == 0
    assert dest.is_file()
    assert "HARNESS_OK" in cp.stderr
    assert "GAK-conformant" not in cp.stdout + cp.stderr
    assert "\nCONFORMANT" not in cp.stdout
    assert json.loads(dest.read_text())["kernel"].startswith("fixture-")


def test_score_brick_nonzero():
    cp = _run(
        [
            "score",
            "--adapter",
            "gak_conformance.fixtures.brick:BrickActionAdapter",
        ]
    )
    assert cp.returncode == 1
    receipt = json.loads(cp.stdout)
    assert receipt["conformant"] is False


def test_score_missing_adapter_nonzero():
    cp = _run(["score", "--adapter", "not.a.module:Nope"])
    assert cp.returncode == 2
    assert "BLOCKED" in cp.stderr


def test_score_out_writes_file(tmp_path):
    dest = tmp_path / "receipt.json"
    cp = _run(
        [
            "score",
            "--adapter",
            "gak_conformance.fixtures.action_gate:PassingActionAdapter",
            "--out",
            str(dest),
        ]
    )
    assert cp.returncode == 0
    data = json.loads(dest.read_text())
    assert data["kernel"] == "fixture-action"
    assert data["conformant"] is True
    assert "not a kernel certification" in cp.stderr
    assert "\nCONFORMANT" not in cp.stdout


def test_two_runs_same_digest(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    for dest in (a, b):
        cp = _run(
            [
                "score",
                "--adapter",
                "gak_conformance.fixtures.commit_gate:PassingCommitAdapter",
                "--out",
                str(dest),
            ]
        )
        assert cp.returncode == 0
    from gak_conformance.receipt import clauses_digest
    from gak_conformance import HARNESS_V1

    da = json.loads(a.read_text())
    db = json.loads(b.read_text())
    assert clauses_digest(da, HARNESS_V1) == clauses_digest(db, HARNESS_V1)
    assert len(clauses_digest(da, HARNESS_V1)) == 64


def test_score_refuses_to_certify_a_fixture():
    cp = _run(
        [
            "score",
            "--certify",
            "--adapter",
            "gak_conformance.fixtures.action_gate:PassingActionAdapter",
        ]
    )
    assert cp.returncode == 2
    assert "cannot be certified" in cp.stderr
    assert "GAK-conformant" not in cp.stdout
