"""Command-line surface.

``--adapter module:Class`` imports and executes that module. Fixture adapters
test the harness; they are not kernel certifications.

Research prototype: a conformant receipt means the adapter passed
gak-conformance/v1 under its declared profile. Not secure, not audited,
not endorsed.

Exit codes: 0 scored and conformant (or meta-command ok); 1 scored not
conformant or verify digest mismatch; 2 could not score / bad usage.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import HARNESS_V1, HARNESS_V1_1, __version__
from .clauses import clauses_for
from .load import load_adapter
from .receipt import certification_from_receipt, clauses_digest
from .scorer import run_conformance

SELFCHECK_ADAPTER = "gak_conformance.fixtures.action_gate:PassingActionAdapter"

_PARSER_KWARGS: dict = {}
if sys.version_info >= (3, 14):
    _PARSER_KWARGS["color"] = False


def _write_json(path: Path | None, payload: dict) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    if path is None:
        sys.stdout.write(text)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _load_or_block(spec: str) -> object:
    try:
        return load_adapter(spec)
    except (ValueError, ImportError, AttributeError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


def cmd_score(args: argparse.Namespace) -> int:
    adapter = _load_or_block(args.adapter)
    try:
        receipt = run_conformance(adapter, harness=args.harness)
    except ValueError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2
    payload = receipt.to_dict()
    if args.certify:
        out = certification_from_receipt(payload, args.harness)
        digest = out["clauses_digest"]
    else:
        out = payload
        digest = clauses_digest(payload, args.harness)
    dest = Path(args.out) if args.out else None
    _write_json(dest, out)
    if dest is not None:
        print(receipt.render())
        print(f"digest {digest}")
        print(f"wrote {dest}")
    else:
        print(f"digest {digest}", file=sys.stderr)
    return 0 if receipt.conformant else 1


def cmd_digest(args: argparse.Namespace) -> int:
    path = Path(args.receipt)
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        digest = clauses_digest(receipt, args.harness)
    except Exception as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2
    print(digest)
    return 0


def cmd_selfcheck(args: argparse.Namespace) -> int:
    args.adapter = SELFCHECK_ADAPTER
    args.certify = False
    return cmd_score(args)


def cmd_verify(args: argparse.Namespace) -> int:
    """Spec §5.4: re-score the kernel and compare the published digest."""
    cert_path = Path(args.cert)
    try:
        cert = json.loads(cert_path.read_text(encoding="utf-8"))
        expected = cert["clauses_digest"]
        if not isinstance(expected, str) or len(expected) != 64:
            raise ValueError("certification clauses_digest must be a 64-hex digest")
    except Exception as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2
    adapter = _load_or_block(args.adapter)
    try:
        receipt = run_conformance(adapter, harness=args.harness)
    except ValueError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2
    payload = receipt.to_dict()
    digest = clauses_digest(payload, args.harness)
    if args.out:
        _write_json(Path(args.out), payload)
    if not receipt.conformant:
        print(
            f"NOT CONFORMANT on re-run; published digest {expected} is not earned.",
            file=sys.stderr,
        )
        print(f"derived {digest}", file=sys.stderr)
        return 1
    if digest != expected:
        print(
            f"digest mismatch: derived {digest} != published {expected}",
            file=sys.stderr,
        )
        return 1
    print(f"VERIFIED {digest}")
    return 0


def cmd_list_clauses(args: argparse.Namespace) -> int:
    for clause in clauses_for(args.harness):
        req = clause.requires or "-"
        print(f"{clause.id}\tprofile={clause.profile}\trequires={req}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gak_conformance",
        description=(
            "Vendor-neutral mechanical scorer for governed agent kernels "
            "(gak-conformance/v1). Research prototype — not a security evaluation. "
            "--adapter module:Class imports and executes that Python module. "
            "Fixture adapters test the harness; they are not kernel certifications."
        ),
        epilog=(
            "Exits: 0 scored and conformant; 1 scored not-conformant or verify "
            "mismatch; 2 could not score. "
            "Example: python3 -m gak_conformance score "
            "--adapter gak_conformance.fixtures.action_gate:PassingActionAdapter"
        ),
        **_PARSER_KWARGS,
    )
    p.add_argument("--version", action="version", version=f"gak-conformance {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_harness(sp: argparse.ArgumentParser) -> None:
        sp.add_argument(
            "--harness",
            default=HARNESS_V1,
            choices=(HARNESS_V1, HARNESS_V1_1),
            help="Clause table. Default is frozen v1 (13 clauses).",
        )

    sc = sub.add_parser("score", help="Score an adapter and emit a JSON receipt.")
    add_harness(sc)
    sc.add_argument(
        "--adapter",
        required=True,
        help="module:Class implementing the spec §6 adapter. Import executes the module.",
    )
    sc.add_argument("--out", help="Write JSON here (default: stdout).")
    sc.add_argument(
        "--certify",
        action="store_true",
        help="Emit the §5.2 certification (digest-bearing) instead of the §5.1 receipt.",
    )
    sc.set_defaults(func=cmd_score)

    vf = sub.add_parser(
        "verify",
        help="Re-score an adapter and compare to a published certification digest (§5.4).",
    )
    add_harness(vf)
    vf.add_argument("--adapter", required=True, help="module:Class of the live kernel.")
    vf.add_argument("--cert", required=True, help="Path to a gak-certification/v1 JSON.")
    vf.add_argument("--out", help="Optional path for the live receipt.")
    vf.set_defaults(func=cmd_verify)

    dg = sub.add_parser("digest", help="Re-derive §5.3 digest from an existing receipt.")
    add_harness(dg)
    dg.add_argument("--receipt", required=True, help="Path to a §5.1 receipt JSON.")
    dg.set_defaults(func=cmd_digest)

    lc = sub.add_parser("list-clauses", help="Print the harness clause table.")
    add_harness(lc)
    lc.set_defaults(func=cmd_list_clauses)

    sm = sub.add_parser(
        "selfcheck",
        help="Score the in-repo action-gate fixture (harness test, not a kernel certification).",
    )
    add_harness(sm)
    sm.add_argument("--out", help="Optional receipt path.")
    sm.set_defaults(func=cmd_selfcheck)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
