import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from uuid import uuid4

from sdr import archive, export
from sdr.snapshot import Snapshot

REPO = "Ravencentric/seadex-data-refinement"
HISTORY = "history"
FILENAME = "seadex-data-refinement-history.tar.zst"


def fetch(destination: Path) -> Path:
    """Download and unpack page history into an empty destination, discarding the archive."""
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"History destination must be empty: {destination}")

    started = perf_counter()
    print("Fetching page history...", flush=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Finish extraction beside the destination before exposing it to the build.
    with TemporaryDirectory(dir=destination.parent) as staging:
        temporary = Path(staging) / FILENAME
        subprocess.run(
            [
                "gh",
                "release",
                "download",
                HISTORY,
                "--repo",
                REPO,
                "--pattern",
                FILENAME,
                "--output",
                str(temporary),
            ],
            check=True,
        )
        restored = archive.unpack(temporary, Path(staging) / "history")
        if destination.exists():
            destination.rmdir()
        restored.replace(destination)
    print(
        f"Fetched {len(tuple(destination.glob('*.jsonl')))} page histories ({perf_counter() - started:.2f}s)",
        flush=True,
    )
    return destination


def publish(snapshot: Snapshot, source: Path, destination: Path) -> Path:
    """Append page observations to history and replace its release after uploading a new archive."""
    if not source.is_dir():
        raise FileNotFoundError(f"Fetched history directory does not exist: {source}")
    if not any(source.glob("*.jsonl")):
        raise ValueError(f"Fetched page histories are missing: {source}")

    commit = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    export.export(snapshot, source)
    archive.pack(source, destination)

    started = perf_counter()
    temptag = f"{HISTORY}-{uuid4().hex}"
    command = ["gh", "release", "--repo", REPO]
    # The CLI uploads assets before publishing the new release. Keep the old
    # release until that succeeds, then recreate its rolling tag at this commit.
    subprocess.run(
        [
            *command,
            "create",
            temptag,
            str(destination),
            "--target",
            commit,
            "--title",
            "SeaDex Data Refinement History",
            "--notes",
            "Page history, updated automatically.\n",
        ],
        check=True,
    )
    subprocess.run([*command, "delete", HISTORY, "--yes", "--cleanup-tag"], check=True)
    # If retagging fails, the uploaded release remains available on its temporary tag.
    subprocess.run([*command, "edit", temptag, "--tag", HISTORY, "--target", commit], check=True)
    subprocess.run(["gh", "api", "--method", "DELETE", f"repos/{REPO}/git/refs/tags/{temptag}"], check=True)
    print(f"Published page history ({perf_counter() - started:.2f}s)", flush=True)
    return destination
