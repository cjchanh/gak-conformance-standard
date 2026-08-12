"""Optional Deponent adapter: absent path is skip/exit 2, never a 16-clause crash."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from gak_conformance.adapters.deponent import (
    SKIP_MESSAGE,
    DeponentKernelAdapter,
    deponent_available,
)
from gak_conformance.clauses import FORBIDDEN_HARNESS_IDS, V1_IDS

ROOT = Path(__file__).resolve().parents[1]


def test_package_import_does_not_load_deponent():
    import gak_conformance.adapters.deponent as dep

    assert "deponent" not in sys.modules
    assert dep.deponent_available() is deponent_available()


def test_construct_without_deponent_raises():
    if deponent_available():
        pytest.skip("Deponent is importable; absent-path not exercised")
    with pytest.raises(ImportError, match="not importable"):
        DeponentKernelAdapter()


def test_cli_absent_deponent_is_exit_2():
    if deponent_available():
        pytest.skip("Deponent is importable; absent-path not exercised")
    cp = subprocess.run(
        [
            sys.executable,
            "-m",
            "gak_conformance",
            "score",
            "--adapter",
            "gak_conformance.adapters.deponent:DeponentKernelAdapter",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert cp.returncode == 2
    assert "BLOCKED" in cp.stderr
    assert "not importable" in cp.stderr


def test_skip_message_points_at_fixture():
    assert "fixture" in SKIP_MESSAGE.lower()


@pytest.mark.skipif(not deponent_available(), reason="Deponent not installed")
def test_live_deponent_scores_thirteen_v1_clauses():
    from gak_conformance.load import load_adapter
    from gak_conformance.scorer import run_conformance

    adapter = load_adapter("gak_conformance.adapters.deponent:DeponentKernelAdapter")
    receipt = run_conformance(adapter)
    ids = {r.id for r in receipt.results}
    assert ids == V1_IDS
    assert not (ids & FORBIDDEN_HARNESS_IDS)
    assert "GAK-AUDIT-CONTENT-BLIND" not in ids
    assert receipt.counts["fail"] == 0
    assert receipt.counts["pass"] >= 1
    assert adapter.supports <= frozenset({"reconcile", "attest"})
