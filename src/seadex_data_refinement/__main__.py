from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .build import build


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="sdr",
        description="Render SeaDex Data Refinement reports to Markdown.",
    )
    parser.add_argument(
        "out",
        nargs="?",
        type=Path,
        default=Path("docs"),
        help="Output directory for Markdown files (default: docs)",
    )
    args = parser.parse_args()
    build(args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
