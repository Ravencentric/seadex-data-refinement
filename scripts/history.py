import os
import subprocess
from pathlib import Path

import httpx
import msgspec

from sdr import network
from sdr.archive import pack, unpack
from sdr.export import export
from sdr.snapshot import load

REPO = "Ravencentric/seadex-data-refinement"
TAG = "history"
TARGET = "main"
SNAPSHOT = Path("snapshot.json")
EXPORTS = Path("exports")
ARCHIVES = Path("archives")
TOKEN = os.environ["GH_TOKEN"]


class Asset(msgspec.Struct, frozen=True):
    name: str


class Release(msgspec.Struct, frozen=True):
    assets: tuple[Asset, ...]


def release() -> Release | None:
    """Find the history release, returning None only when it does not exist."""
    url = f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}"
    with network.Client() as client:
        try:
            response = client.get(
                url,
                headers={
                    "Authorization": f"Bearer {TOKEN}",
                    "Accept": "application/vnd.github+json",
                },
            )
        except httpx.HTTPStatusError as error:
            # Other API failures must stop the update so that they cannot
            # replace stored history with a fresh export.
            if error.response.status_code == 404:
                return None
            raise
    return msgspec.json.decode(response.content, type=Release)


def main() -> None:
    """Persist the saved snapshot's page histories in the history release."""
    snapshot = load(SNAPSHOT)
    year = str(snapshot.captured.year)
    existing = release()
    archive = ARCHIVES / f"{year}.tar.zst"

    if existing is not None and any(asset.name == archive.name for asset in existing.assets):
        subprocess.run(
            [
                "gh",
                "release",
                "download",
                TAG,
                "--repo",
                REPO,
                "--pattern",
                archive.name,
                "--dir",
                str(archive.parent),
            ],
            check=True,
        )
        unpack(archive, EXPORTS / year)

    export(snapshot, EXPORTS)
    pack(EXPORTS / year, archive)

    if existing is None:
        subprocess.run(
            [
                "gh",
                "release",
                "create",
                TAG,
                str(archive),
                "--repo",
                REPO,
                "--target",
                TARGET,
                "--title",
                "Page history",
                "--notes",
                "Yearly page history archives, updated automatically.",
                "--latest=false",
            ],
            check=True,
        )
    else:
        subprocess.run(
            [
                "gh",
                "release",
                "upload",
                TAG,
                str(archive),
                "--repo",
                REPO,
                "--clobber",
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
