"""Command-line surface.

``--adapter module:Class`` imports and executes that module. Fixture adapters
test the harness; they are not kernel certifications.

Research prototype: a conformant receipt means the adapter passed
gak-conformance/v1 under its declared profile. Not secure, not audited,
not endorsed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import HARNESS_V1, HARNESS_V1_1, __version__
from .load import load_adapter
from .receipt import certification_from_receipt, clauses_digest
from .scorer import run_conformance

SELFCHECK_ADAPTER = "gak_conformance.fixtures.action_gate:PassingActionAdapter"


def _write_json(path: Path | None, payload: dict) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    if path is None:
        sys.stdout.write(text)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def cmd_score(args: argparse.Namespace) -> int:
    try:
        adapter = load_adapter(args.adapter)
        receipt = run_conformance(adapter, harness=args.harness)
    except Exception as exc:
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
        # JSON already on stdout; keep digest on stderr so pipes stay clean.
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
    args.out = args.out
    args.certify = False
    return cmd_score(args)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gak_conformance",
        description=(
            "Vendor-neutral mechanical scorer for governed agent kernels "
            "(gak-conformance/v1). Research prototype — not a security evaluation. "
            "--adapter module:Class imports and executes that Python module."
        ),
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

    sc = sub.add_parser(
        "score",
        help="Score an adapter and emit a JSON receipt.",
    )
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

    dg = sub.add_parser("digest", help="Re-derive §5.3 digest from an existing receipt.")
    add_harness(dg)
    dg.add_argument("--receipt", required=True, help="Path to a §5.1 receipt JSON.")
    dg.set_defaults(func=cmd_digest)

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
