"""The harness must not import Deponent internals."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "gak_conformance"


def test_no_deponent_import_in_harness_source():
    forbidden = ("deponent", "sworn")
    offenders = []
    for path in ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in forbidden:
                        offenders.append(f"{path}:{alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module.split(".")[0] in forbidden:
                    offenders.append(f"{path}:{node.module}")
    assert offenders == []


def test_artifact_contract_does_not_import_optional_adapters():
    """Data-flow ownership: classify/validate stay in the harness core."""
    text = (ROOT / "artifacts.py").read_text(encoding="utf-8")
    assert "adapters" not in text
    assert "deponent" not in text
    init = (ROOT / "__init__.py").read_text(encoding="utf-8")
    assert "from .artifacts import" in init
    assert "adapters.deponent" not in init
