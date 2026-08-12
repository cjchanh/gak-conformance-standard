"""Product journeys: first-use, repo-root contract, spec §7.1, skeleton."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from gak_conformance.scorer import run_conformance

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
SPEC = (ROOT / "v1" / "spec.md").read_text(encoding="utf-8")


def _first_fence(text: str) -> str:
    match = re.search(r"```(?:[a-z]*)\n(.*?)```", text, flags=re.S)
    assert match, "expected a fenced command block"
    return match.group(1)


def _run(args, *, cwd: Path):
    return subprocess.run(
        [sys.executable, "-m", "gak_conformance", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
    )


def test_readme_first_40_lines_are_sequence_a():
    head = "\n".join(README.splitlines()[:40])
    assert "research prototype" in head.lower()
    assert "not a security-evaluated product" in head.lower()
    assert 'Not "secure."' in head
    assert 'Not "audited."' in head
    assert 'Not "endorsed."' in head
    assert "repository root" in head
    assert "python3 -m gak_conformance --help" in head
    assert "python3 -m gak_conformance selfcheck" in head
    assert "PassingActionAdapter" in head
    assert "deponent.badge" not in head
    assert "from deponent" not in head


def test_readme_first_fence_is_fixture_score_not_deponent():
    fence = _first_fence(README)
    assert "python3 -m gak_conformance --help" in fence
    assert "selfcheck" in fence
    assert "gak_conformance.fixtures.action_gate:PassingActionAdapter" in fence
    assert "deponent.badge" not in fence
    assert "your_pkg.adapter" not in fence


def test_readme_names_skeleton_and_repo_root_contract():
    assert "examples/adapter_skeleton.py" in README
    assert "No module named gak_conformance" in README
    assert "Third-party verdicts to date: zero" in README


def test_readme_primary_table_is_v1_not_v11_sworn():
    table = README.split("## Status", 1)[0]
    assert "sworn-conformance-receipt-v1.1.json" not in table
    assert "deponent-conformance-receipt.json" in table


def test_spec_7_1_first_python_import_is_in_repo_harness():
    section = SPEC.split("### 7.1", 1)[1].split("### 7.2", 1)[0]
    fence = _first_fence(section)
    assert "from gak_conformance import run_conformance" in fence
    assert "from deponent.conformance import run_conformance" not in section
    assert "python3 -m gak_conformance score" in section


def test_spec_appendix_entrypoint_is_in_repo_harness():
    assert "python3 -m gak_conformance verify" in SPEC
    assert "python3 -m gak_conformance list-clauses" in SPEC
    assert "not the category entrypoint" in SPEC


def test_spec_frozen_v1_digest_untouched():
    assert (
        "de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406" in SPEC
    )


def test_clean_tree_from_repo_root_runs_help_and_selfcheck(tmp_path):
    dest = tmp_path / "clone"
    shutil.copytree(
        ROOT / "gak_conformance",
        dest / "gak_conformance",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    help_cp = _run(["--help"], cwd=dest)
    assert help_cp.returncode == 0, help_cp.stderr
    self_cp = _run(["selfcheck"], cwd=dest)
    assert self_cp.returncode == 0, self_cp.stderr
    assert "HARNESS_OK" in self_cp.stderr
    receipt = json.loads(self_cp.stdout)
    assert receipt["kernel"].startswith("fixture-")
    assert len(receipt["clauses"]) == 13


def test_empty_cwd_without_path_cannot_import_harness(tmp_path):
    cp = _run(["--help"], cwd=tmp_path)
    assert cp.returncode != 0
    assert "No module named gak_conformance" in (cp.stderr + cp.stdout)


def test_untouched_skeleton_scores_fail_not_a_mark():
    path = ROOT / "examples" / "adapter_skeleton.py"
    spec = importlib.util.spec_from_file_location("adapter_skeleton", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    receipt = run_conformance(mod.YourKernelAdapter())
    assert receipt.conformant is False
    assert any(row.status == "FAIL" for row in receipt.results)
    assert receipt.kernel == "your-kernel"
