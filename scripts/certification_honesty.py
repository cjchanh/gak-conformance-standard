"""Honesty checks so a copied gak-certification JSON cannot read as third-party certification."""
from __future__ import annotations

from typing import Any

BARE_CONFORMANT_MARK = "GAK-conformant"
SELF_ASSESSED_MARK = "GAK-conformant (self-assessed)"
NOT_CONFORMANT_MARK = "not-conformant"


def honesty_errors(doc: dict[str, Any], *, source: str = "") -> list[str]:
    """Return problems that let a copied certification JSON look independently certified."""
    prefix = f"{source}: " if source else ""
    errors: list[str] = []
    if doc.get("self_assessed") is not True:
        errors.append(
            f"{prefix}self_assessed must be true (got {doc.get('self_assessed')!r})"
        )
    if doc.get("third_party_verified") is not False:
        errors.append(
            f"{prefix}third_party_verified must be false "
            f"(got {doc.get('third_party_verified')!r})"
        )
    mark = doc.get("mark")
    if doc.get("conformant") is True:
        if mark != SELF_ASSESSED_MARK:
            errors.append(
                f"{prefix}conformant mark must be {SELF_ASSESSED_MARK!r}, got {mark!r}"
            )
    elif doc.get("conformant") is False:
        if mark != NOT_CONFORMANT_MARK:
            errors.append(
                f"{prefix}non-conformant mark must be {NOT_CONFORMANT_MARK!r}, got {mark!r}"
            )
    return errors
