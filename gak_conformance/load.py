"""Load an adapter from a PEP 517 / entry-point ``module:Class`` token.

Import executes the module. This is trusted-code loading, not a sandbox.
"""

from __future__ import annotations

import importlib
import re

# PyPA entry-points: each dotted/colon part is a Python identifier.
_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def load_adapter(spec: str) -> object:
    if spec.count(":") != 1:
        raise ValueError(
            f"adapter spec must be module:Class (exactly one colon), got {spec!r}"
        )
    if "/" in spec or "\\" in spec or ".." in spec:
        raise ValueError("adapter spec must be a module path, not a filesystem path")
    module_name, class_name = spec.split(":", 1)
    if not module_name or not class_name:
        raise ValueError(f"adapter spec must be module:Class, got {spec!r}")
    if not all(_IDENT.fullmatch(part) for part in module_name.split(".")):
        raise ValueError(
            f"adapter module must be PEP 517 identifiers, got {module_name!r}"
        )
    if not _IDENT.fullmatch(class_name):
        raise ValueError(
            f"adapter class must be a single PEP 517 identifier, got {class_name!r}"
        )
    module = importlib.import_module(module_name)
    try:
        cls = getattr(module, class_name)
    except AttributeError as exc:
        raise ValueError(f"module {module_name!r} has no attribute {class_name!r}") from exc
    obj = cls() if isinstance(cls, type) else cls
    return obj
