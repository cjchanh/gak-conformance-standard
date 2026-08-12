"""Load an adapter from a module:Class token. Import executes the module."""

from __future__ import annotations

import importlib


def load_adapter(spec: str) -> object:
    if spec.count(":") != 1:
        raise ValueError(
            f"adapter spec must be module:Class (exactly one colon), got {spec!r}"
        )
    module_name, class_name = spec.split(":", 1)
    if not module_name or not class_name:
        raise ValueError(f"adapter spec must be module:Class, got {spec!r}")
    if "/" in module_name or "\\" in module_name:
        raise ValueError("adapter spec must be a module path, not a filesystem path")
    module = importlib.import_module(module_name)
    try:
        cls = getattr(module, class_name)
    except AttributeError as exc:
        raise ValueError(f"module {module_name!r} has no attribute {class_name!r}") from exc
    obj = cls() if isinstance(cls, type) else cls
    return obj
