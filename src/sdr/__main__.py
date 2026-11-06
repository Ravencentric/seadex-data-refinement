import argparse
from pathlib import Path
from typing import Literal, assert_never

from sdr.build import build
from sdr.fetch import fetch
from sdr.snapshot import load


class Arguments(argparse.Namespace):
    command: Literal["fetch", "build"]  # pyrefly: ignore[uninitialized-instance-variable]
    snapshot: Path  # pyrefly: ignore[uninitialized-instance-variable]


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sdr",
        description="Fetch source data or build the SDR site from a saved snapshot.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name, description in (
        ("fetch", "Fetch SeaDex and AniList data and save a snapshot."),
        ("build", "Build the site from a saved snapshot without fetching source data."),
    ):
        command = commands.add_parser(name, help=description, description=description)
        command.add_argument(
            "--snapshot", type=Path, default=Path("snapshot.json"), help="Snapshot file (default: %(default)s)"
        )
    return parser


def main() -> None:
    arguments = parser().parse_args(namespace=Arguments())
    match arguments.command:
        case "fetch":
            snapshot = fetch(arguments.snapshot)
            print(f"Saved {len(snapshot.entries)} entries to {arguments.snapshot}")
        case "build":
            site = build(load(arguments.snapshot))
            print(f"Built {site}")
        case _:
            assert_never(arguments.command)


if __name__ == "__main__":
    main()
