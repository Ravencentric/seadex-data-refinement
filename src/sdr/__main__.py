import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal, assert_never

from sdr import archive, build, export, fetch, github, snapshot

SNAPSHOT = Path("snapshot.json")
HISTORY = Path("history")
ARCHIVE = Path("archives") / github.FILENAME


# https://github.com/meta/pyrefly/issues/5554
class Arguments(argparse.Namespace):
    command: Literal["fetch", "build", "export", "publish", "pack", "unpack"]  # pyrefly: ignore[uninitialized-instance-variable]


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sdr",
        description="Fetch source data, build the SDR site, or export, archive, and publish page history.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    description = "Fetch page history and save a snapshot of SeaDex and AniList data."
    commands.add_parser("fetch", help=description, description=description)

    description = "Build the site from a saved snapshot without fetching source data."
    commands.add_parser("build", help=description, description=description)

    description = "Append page observations from a saved snapshot to history."
    commands.add_parser("export", help=description, description=description)

    description = "Append page observations from a saved snapshot to fetched history and publish its archive."
    commands.add_parser("publish", help=description, description=description)

    description = "Package page history into one .tar.zst archive."
    commands.add_parser("pack", help=description, description=description)

    description = "Unpack the .tar.zst archive into an empty page history directory."
    commands.add_parser("unpack", help=description, description=description)
    return parser


def main() -> None:
    arguments = parser().parse_args(namespace=Arguments())
    match arguments.command:
        case "fetch":
            # Fail before starting source requests if local history cannot be replaced.
            if HISTORY.exists() and any(HISTORY.iterdir()):
                raise FileExistsError(f"History destination must be empty: {HISTORY}")
            with ThreadPoolExecutor(max_workers=1) as executor:
                histories = executor.submit(github.fetch, HISTORY)
                captured = fetch.fetch()
                histories.result()
            snapshot.save(captured, SNAPSHOT)
            print(f"Saved {len(captured.entries)} entries to {SNAPSHOT}")
        case "build":
            site = build.build(snapshot.load(SNAPSHOT), HISTORY)
            print(f"Built {site}")
        case "export":
            destination = export.export(snapshot.load(SNAPSHOT), HISTORY)
            print(f"Exported page observations to history in {destination}")
        case "publish":
            destination = github.publish(snapshot.load(SNAPSHOT), HISTORY, ARCHIVE)
            print(f"Published page history archive at {destination}")
        case "pack":
            destination = archive.pack(HISTORY, ARCHIVE)
            print(f"Packed page histories into {destination}")
        case "unpack":
            destination = archive.unpack(ARCHIVE, HISTORY)
            print(f"Restored page histories to {destination}")
        case _:
            assert_never(arguments.command)


if __name__ == "__main__":
    main()
