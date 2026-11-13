import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

import msgspec

from sdr import network
from sdr.archive import pack, unpack
from sdr.export import export
from sdr.snapshot import Snapshot

REPO = "Ravencentric/seadex-data-refinement"
TAG = "history"
FILENAME = "seadex-data-refinement-history.tar.zst"


class Asset(msgspec.Struct, frozen=True):
    name: str
    url: str


class Release(msgspec.Struct, frozen=True):
    assets: tuple[Asset]


def release(client: network.Client) -> Release:
    """Fetch metadata for the required history release."""
    url = f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}"
    response = client.get(url, headers={"Accept": "application/vnd.github+json"})
    return msgspec.json.decode(response.content, type=Release)


def fetch(destination: Path) -> Path:
    """Download and unpack page history into an empty destination, discarding the archive."""
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"History destination must be empty: {destination}")

    started = perf_counter()
    print("Fetching page history...", flush=True)
    with network.Client() as client:
        token = os.environ.get("GH_TOKEN")
        if token:
            client.headers["Authorization"] = f"Bearer {token}"
        existing = release(client)
        (asset,) = existing.assets
        if asset.name != FILENAME:
            raise ValueError(f"History release is missing {FILENAME}; refusing to replace stored history")

        response = client.get(asset.url, headers={"Accept": "application/octet-stream"})
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Finish extraction beside the destination before exposing it to the build.
        with TemporaryDirectory(dir=destination.parent) as staging:
            temporary = Path(staging) / FILENAME
            temporary.write_bytes(response.content)
            restored = unpack(temporary, Path(staging) / "exports")
            if destination.exists():
                destination.rmdir()
            restored.replace(destination)
        print(
            f"Fetched {len(tuple(destination.glob('*.jsonl')))} page histories in {client.requests} HTTP requests "
            f"({perf_counter() - started:.2f}s)",
            flush=True,
        )
    return destination


def publish(snapshot: Snapshot, source: Path, archive: Path) -> Path:
    """Append and publish the histories already acquired before a successful build."""
    if not source.is_dir():
        raise FileNotFoundError(f"Fetched history directory does not exist: {source}")
    if not any(source.glob("*.jsonl")):
        raise ValueError(f"Fetched page histories are missing: {source}")

    export(snapshot, source)
    pack(source, archive)

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
    return archive
