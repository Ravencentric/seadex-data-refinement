import subprocess
from hashlib import file_digest
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from uuid import uuid4

from sdr import archive, export
from sdr.snapshot import Snapshot

REPO = "Ravencentric/seadex-data-refinement"
HISTORY = "history"
FILENAME = "seadex-data-refinement-history.tar.zst"


def format_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1000:
            return f"{value:.1f} {unit}"
        value /= 1000
    return f"{value:.1f} TB"


def filetree(source: Path) -> str:
    nodes = ["seadex-data-refinement-history/"]
    files = [p for p in source.iterdir() if p.suffix == ".jsonl"]

    for i, file in enumerate(files):
        branch = "└──" if i == len(files) - 1 else "├──"
        nodes.append(f"{branch} {file.name} ({format_size(file.stat().st_size)})")

    return "\n".join(nodes)


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

    expanded = sum(path.stat().st_size for path in source.iterdir() if path.suffix == ".jsonl")
    compressed = destination.stat().st_size

    notes = "\n".join(
        (
            "Historical data collected by every page, updated automatically.",
            f"Note that this {format_size(compressed)} archive expands to approximately {format_size(expanded)} of JSONL files.",
            "```",
            filetree(source),
            "```",
        )
    )

    started = perf_counter()
    temptag = f"{HISTORY}-{uuid4().hex}"
    command = ["gh", "release", "--repo", REPO]
    with destination.open("rb") as file:
        digest = file_digest(file, "sha256").hexdigest()

    # Stage the new release in draft
    subprocess.run(
        [
            *command,
            "create",
            temptag,
            str(destination),
            "--draft",
            "--target",
            commit,
            "--title",
            "History",
            "--notes",
            notes,
        ],
        check=True,
    )

    # Move the `history` tag to the latest commit
    subprocess.run(
        [
            "gh",
            "api",
            "--method",
            "PATCH",
            f"repos/{REPO}/git/refs/tags/{HISTORY}",
            "-f",
            f"sha={commit}",
            "-F",
            "force=true",
            "--silent",
        ],
        check=True,
    )

    # Delete the older release WITHOUT deleting it's tag
    subprocess.run([*command, "delete", HISTORY, "--yes"], check=True)

    # Change the draft release's tag to `history` and undraft it.
    subprocess.run([*command, "edit", temptag, "--tag", HISTORY, "--verify-tag", "--draft=false"], check=True)

    # Sanity check
    expected = (
        ".draft == false and any(.assets[]; "
        f'.name == "{FILENAME}" and .state == "uploaded" and .digest == "sha256:{digest}")'
    )
    release = subprocess.run(
        ["gh", "api", f"repos/{REPO}/releases/tags/{HISTORY}", "--jq", expected],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    if release.stdout.strip() != "true":
        raise RuntimeError(f"Published {HISTORY} release is missing the verified {FILENAME} asset")
    print(f"Published page history ({perf_counter() - started:.2f}s)", flush=True)
    return destination
