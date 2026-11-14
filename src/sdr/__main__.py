import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from sdr import archive, build, export, fetch, github, snapshot

SNAPSHOT = Path("snapshot.json")
HISTORY = Path("history")
ARCHIVE = Path("archives") / github.FILENAME

COMMANDS = {
    "fetch": "Fetch page history and save a snapshot of SeaDex and AniList data.",
    "build": "Build the site from a saved snapshot without fetching source data.",
    "export": "Append page observations from a saved snapshot to history.",
    "publish": "Append page observations from a saved snapshot to fetched history and publish its archive.",
    "pack": "Package page history into one .tar.zst archive.",
    "unpack": "Unpack the .tar.zst archive into an empty page history directory.",
}


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sdr",
        description="Fetch source data, build the SDR site, or export, archive, and publish page history.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    for name, description in COMMANDS.items():
        commands.add_parser(name, help=description, description=description)
    return parser


def main() -> None:
    arguments = parser().parse_args()
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
            _snapshot = snapshot.load(SNAPSHOT)
            site = build.build(_snapshot, HISTORY)
            print(f"Built {site}")

        case "export":
            _snapshot = snapshot.load(SNAPSHOT)
            destination = export.export(_snapshot, HISTORY)
            print(f"Exported page observations to history in {destination}")

        case "publish":
            _snapshot = snapshot.load(SNAPSHOT)
            destination = github.publish(_snapshot, HISTORY, ARCHIVE)
            print(f"Published page history archive at {destination}")

        case "pack":
            destination = archive.pack(HISTORY, ARCHIVE)
            print(f"Packed page histories into {destination}")

        case "unpack":
            destination = archive.unpack(ARCHIVE, HISTORY)
            print(f"Restored page histories to {destination}")

        case _:
            raise ValueError(f"Unknown command: {arguments.command!r}")


if __name__ == "__main__":
    main()
