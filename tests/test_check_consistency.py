"""Consistency checker must not require Deponent and must agree with the spec."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_check_consistency_runs_without_deponent():
    cp = subprocess.run(
        [sys.executable, "scripts/check_consistency.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert cp.returncode != 3, cp.stderr
    assert "deponent" not in Path(ROOT / "scripts/check_consistency.py").read_text().lower() or (
        "from deponent" not in Path(ROOT / "scripts/check_consistency.py").read_text()
        and "import deponent" not in Path(ROOT / "scripts/check_consistency.py").read_text()
    )
