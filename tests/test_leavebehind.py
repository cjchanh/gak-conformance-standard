"""Public leave-behind has no private-coupling tokens or host paths."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

PRODUCT = [
    ROOT / "gak_conformance",
    ROOT / "scripts",
    ROOT / "tests",
    ROOT / "v1",
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "NOTICE",
    ROOT / "pyproject.toml",
]

# Joined at runtime so this file is not itself a hit.
NEEDLES = tuple(
    "".join(parts)
    for parts in (
        ("deponent/", "attest.py"),
        ("00", "Agent"),
        ("cds-", "compliance"),
        ("CMMC-", "RMF"),
        ("ATO-in-a-", "Box"),
        ("per-control ", "map"),
        ("/Users/", "cj"),
        ("marathon.", "pid"),
        ("BEGIN ", "PRIVATE KEY"),
    )
)

RELEASE_ZIP = ROOT / ".builder-foundry" / "release" / "artifact.zip"


def _iter_product_files():
    for item in PRODUCT:
        if item.is_file():
            yield item
        elif item.is_dir():
            for path in item.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts:
                    yield path


def test_product_tree_has_no_forbidden_tokens():
    hits = []
    for path in _iter_product_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for needle in NEEDLES:
            if needle in text:
                hits.append(f"{path.relative_to(ROOT)}: {needle}")
    assert hits == []


@pytest.mark.skipif(not RELEASE_ZIP.is_file(), reason="release artifact not built yet")
def test_release_zip_has_no_forbidden_members_or_tokens():
    with zipfile.ZipFile(RELEASE_ZIP) as zf:
        names = zf.namelist()
        assert any(n.endswith("gak_conformance/__main__.py") for n in names)
        assert any(n.endswith("LICENSE") for n in names)
        assert not any(".git/" in n for n in names)
        assert not any(n.startswith(".builder-foundry/") or "/.builder-foundry/" in n for n in names)
        assert not any(n.endswith("MISSION_FOUNDRY_GAK_V0.md") for n in names)
        assert not any(("marathon." + "pid") in n for n in names)
        for info in zf.infolist():
            if info.is_dir():
                continue
            data = zf.read(info.filename)
            if b"\x00" in data[:64]:
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            for needle in NEEDLES:
                assert needle not in text, f"{info.filename}: {needle}"
