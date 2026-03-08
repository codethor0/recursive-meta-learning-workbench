"""
CLI entry point for RMLW.

Provides: rmlw scan --target URL [--mode baseline|learn] [--iterations N]
         [--format human|json] [--output FILE]
"""

import json
import sys
from typing import Any

from rmlw.learning import MetaController
from rmlw.url_utils import URLValidationError, validate_target_url
from rmlw.workbench import Finding, WebAttackWorkbench


def _serialise_finding(f: Finding) -> dict[str, Any]:
    """Convert Finding to JSON-serialisable dict."""
    return f.to_dict()


def _format_human(f: Finding) -> str:
    """Format a single finding for human-readable output."""
    return f"[{f.ftype}] {f.url} param={f.param} payload={f.payload!r}"


def main() -> None:
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Recursive Meta-Learning Workbench - authorised lab use only"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Run a scan")
    scan_parser.add_argument(
        "--target",
        required=True,
        help="Base URL of target (e.g. http://localhost:8080)",
    )
    scan_parser.add_argument(
        "--mode",
        choices=["baseline", "learn"],
        default="baseline",
        help="baseline: static workbench; learn: meta-controller iterations",
    )
    scan_parser.add_argument(
        "--iterations",
        type=int,
        default=5,
        help="Number of learning iterations (learn mode)",
    )
    scan_parser.add_argument(
        "--output",
        help="Output file for findings. Default: stdout",
    )
    scan_parser.add_argument(
        "--format",
        choices=["json", "human"],
        default="human",
        help="Output format: human (succinct summary) or json (machine-readable)",
    )

    args = parser.parse_args()

    if args.command == "scan":
        try:
            target_url = validate_target_url(args.target)
        except URLValidationError as e:
            parser.error(str(e))

        workbench = WebAttackWorkbench(target_url)

        if args.mode == "baseline":
            findings = workbench.run()
        else:
            controller = MetaController(workbench)
            findings = controller.run_iterations(args.iterations)

        data = [_serialise_finding(f) for f in findings]
        if args.format == "json":
            out_text = json.dumps(data, indent=2) + "\n"
        else:
            lines = [_format_human(f) for f in findings]
            out_text = "\n".join(lines) + "\n" if lines else "No findings.\n"

        sys.stdout.write(out_text)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(data, f, indent=2)
                f.write("\n")


if __name__ == "__main__":
    main()
