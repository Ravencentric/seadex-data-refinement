import argparse
from pathlib import Path
from typing import Literal, assert_never

from sdr.archive import pack, unpack
from sdr.build import build
from sdr.export import export
from sdr.fetch import fetch
from sdr.snapshot import load


# https://github.com/meta/pyrefly/issues/5554
class Arguments(argparse.Namespace):
    command: Literal["fetch", "build", "export", "pack", "unpack"]  # pyrefly: ignore[uninitialized-instance-variable]
    snapshot: Path  # pyrefly: ignore[uninitialized-instance-variable]
    destination: Path  # pyrefly: ignore[uninitialized-instance-variable]
    source: Path  # pyrefly: ignore[uninitialized-instance-variable]


def parser() -> argparse.ArgumentParser:
    archive = Path("archives/seadex-data-refinement-history.tar.zst")
    snapshot = argparse.ArgumentParser(add_help=False)
    snapshot.add_argument(
        "--snapshot", type=Path, default=Path("snapshot.json"), help="Snapshot file (default: %(default)s)"
    )

    parser = argparse.ArgumentParser(
        prog="sdr",
        description="Fetch source data, build the SDR site, or export and archive page history.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    description = "Fetch SeaDex and AniList data and save a snapshot."
    commands.add_parser("fetch", parents=[snapshot], help=description, description=description)

    description = "Build the site from a saved snapshot without fetching source data."
    commands.add_parser("build", parents=[snapshot], help=description, description=description)

    description = "Export the reports as JSONL files."
    command = commands.add_parser("export", parents=[snapshot], help=description, description=description)
    command.add_argument(
        "--destination", type=Path, default=Path("exports"), help="Export directory (default: %(default)s)"
    )

    description = "Package the exported JSONL files into one .tar.zst archive."
    command = commands.add_parser("pack", help=description, description=description)
    command.add_argument(
        "source", type=Path, nargs="?", default=Path("exports"), help="Export directory (default: %(default)s)"
    )
    command.add_argument(
        "--destination",
        type=Path,
        default=archive,
        help="Archive file (default: %(default)s)",
    )

    description = "Unpack the .tar.zst archive into an empty export directory."
    command = commands.add_parser("unpack", help=description, description=description)
    command.add_argument(
        "source",
        type=Path,
        nargs="?",
        default=archive,
        help="Archive file (default: %(default)s)",
    )
    command.add_argument(
        "--destination", type=Path, default=Path("exports"), help="Export directory (default: %(default)s)"
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
        case "export":
            destination = export(load(arguments.snapshot), arguments.destination)
            print(f"Exported snapshot to {destination}")
        case "pack":
            destination = pack(arguments.source, arguments.destination)
            print(f"Packed page histories into {destination}")
        case "unpack":
            destination = unpack(arguments.source, arguments.destination)
            print(f"Restored page histories to {destination}")
        case _:
            assert_never(arguments.command)


if __name__ == "__main__":
    main()
