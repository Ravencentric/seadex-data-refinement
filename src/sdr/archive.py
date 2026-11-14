import tarfile
from compression.zstd import CompressionParameter, DecompressionParameter
from pathlib import Path
from tempfile import TemporaryDirectory

# A 1 GiB window matches repeated observations across days. Readers must allow it too.
WINDOW = 30


def pack(source: Path, destination: Path) -> Path:
    """Archive a directory of page histories, replacing the destination atomically."""
    histories = sorted(path for path in source.iterdir() if path.suffix == ".jsonl")
    if not histories:
        raise ValueError(f"No page histories found in {source}")
    for path in histories:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Page history must be a regular file: {path}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    # Finish the compressed archive beside its destination before replacing it.
    with TemporaryDirectory(dir=destination.parent) as directory:
        temporary = Path(directory) / destination.name
        with tarfile.open(
            temporary,
            mode="w:zst",
            options={
                CompressionParameter.compression_level: 10,
                CompressionParameter.window_log: WINDOW,
            },
        ) as archive:
            for path in histories:
                archive.add(path, arcname=path.name, recursive=False)
        temporary.replace(destination)
    return destination


def unpack(source: Path, destination: Path) -> Path:
    """Restore archived page histories into an empty directory."""
    with tarfile.open(source, mode="r:zst", options={DecompressionParameter.window_log_max: WINDOW}) as archive:
        destination.mkdir(parents=True, exist_ok=True)
        if any(destination.iterdir()):
            raise FileExistsError(f"History destination must be empty: {destination}")

        names: set[str] = set()
        for member in archive:
            path = Path(member.name)
            if not member.isfile() or path.name != member.name or path.suffix != ".jsonl":
                raise ValueError(f"Archive must contain only page history files: {member.name!r}")
            if member.name in names:
                raise ValueError(f"Duplicate page history in archive: {member.name!r}")
            names.add(member.name)
            archive.extract(member, path=destination, filter="data")
        if not names:
            raise ValueError(f"No page histories found in {source}")
    return destination
