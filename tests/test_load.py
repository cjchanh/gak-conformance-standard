"""Loader grammar: PEP 517 module:Class, reject paths and ``..``."""

from __future__ import annotations

import pytest

from gak_conformance.fixtures.action_gate import PassingActionAdapter
from gak_conformance.load import load_adapter


@pytest.mark.parametrize(
    "spec",
    [
        "foo..bar:X",
        "..pkg:X",
        "a:b:c",
        ":Cls",
        "mod:",
        "/tmp/x:Y",
        r"..\x:Y",
        "mod:Class.factory",
        "1mod:Cls",
        "mod:1Cls",
    ],
)
def test_rejects_non_grammar(spec):
    with pytest.raises(ValueError):
        load_adapter(spec)


def test_loads_fixture():
    obj = load_adapter("gak_conformance.fixtures.action_gate:PassingActionAdapter")
    assert isinstance(obj, PassingActionAdapter)


def test_missing_class():
    with pytest.raises(ValueError, match="no attribute"):
        load_adapter("gak_conformance.fixtures.action_gate:NoSuch")
