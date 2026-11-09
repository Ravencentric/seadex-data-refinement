from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal

import msgspec
from atomicwriter import AtomicWriter

from sdr.pages import discover
from sdr.render import slug
from sdr.snapshot import Snapshot

type SlugToObservationMap = Mapping[str, Observation[object]]


class Observation[T](msgspec.Struct, frozen=True, kw_only=True, forbid_unknown_fields=True):
    """One complete page export, identified by its snapshot's capture time."""

    version: Literal[1]
    captured: Annotated[datetime, msgspec.Meta(tz=True)]
    data: T


def export(snapshot: Snapshot, destination: Path) -> Path:
    """Append page observations offline, skipping an already exported capture time."""
    observations = generate(snapshot)
    write(observations, destination)
    return destination


def generate(snapshot: Snapshot) -> SlugToObservationMap:
    """Collect every page's observation without reading or writing history files."""
    observations: dict[str, Observation[object]] = {}
    for page in discover().values():
        stem = slug(page.title)
        if not stem:
            raise ValueError(f"Page title {page.title!r} must produce a nonempty slug")
        filename = f"{stem}.jsonl"
        if filename in observations:
            raise ValueError(f"Page title {page.title!r} produces a duplicate output: {filename}")
        observations[filename] = Observation(version=1, captured=snapshot.captured, data=page.export(snapshot))
    return observations


def write(observations: SlugToObservationMap, destination: Path) -> None:
    """Append observations, preserving existing captures."""
    destination.mkdir(parents=True, exist_ok=True)
    pending: list[AtomicWriter] = []

    for filename, observation in observations.items():
        source = destination / filename
        exists = source.exists()

        if exists:
            # Get the time of the last observation
            # in the existing file
            captured = latest(source)
            if captured == observation.captured:
                # If our observation was recorded at exactly the same time
                # as the one already written to the file, skip it.
                # This will happen when you run an export against the same snapshot
                # several times, making this step idempotent
                continue

            # Ensure a new observartion comes strictly after the last one.
            # because appending an older capture would put the history out of order.
            if captured > observation.captured:
                raise ValueError(
                    f"Cannot append {observation.captured.isoformat()} to {source}: history ends at {captured}"
                )

        writer = AtomicWriter(source, overwrite=True)

        if exists:
            # Preserve existing records in the existing file
            with source.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    writer.write_bytes(chunk)

        writer.write_bytes(msgspec.json.encode(observation) + b"\n")
        pending.append(writer)

    # Commit at last
    for writer in pending:
        writer.commit()


def latest(path: Path) -> datetime:
    """Validate an existing history and return its last capture time."""
    decoder = msgspec.json.Decoder(Observation[msgspec.Raw])
    captured: datetime | None = None
    with path.open("rb") as stream:
        for number, line in enumerate(stream, start=1):
            if not line.endswith(b"\n"):
                raise ValueError(f"{path}, line {number}: observation must end with a newline")
            try:
                observation = decoder.decode(line)
            except msgspec.DecodeError as error:
                raise ValueError(f"{path}, line {number}: {error}") from error
            if captured is not None and observation.captured <= captured:
                raise ValueError(f"{path}, line {number}: capture times must be strictly increasing")
            captured = observation.captured
    if captured is None:
        raise ValueError(f"{path} contains no observations")
    return captured
