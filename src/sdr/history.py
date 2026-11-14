from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal

import msgspec

from sdr.snapshot import Snapshot


class Observation[T](msgspec.Struct, frozen=True, kw_only=True, forbid_unknown_fields=True):
    """A single observation, observed at a given point of time."""

    version: Literal[1]
    captured: Annotated[datetime, msgspec.Meta(tz=True)]
    data: T


type History[E] = Iterable[Observation[E]]


@dataclass(frozen=True, slots=True, kw_only=True)
class Export[E]:
    """Whatever was exported by a page."""

    type: type[E]
    collect: Callable[[Snapshot], E]

    def __call__(self, snapshot: Snapshot) -> E:
        return self.collect(snapshot)


def load[E](path: Path, schema: type[E]) -> Iterator[Observation[E]]:
    """Stream saved observations in capture order, validating each as it is read."""

    try:
        path.stat()
    except FileNotFoundError:
        # New page, no previous history
        return

    previous: datetime | None = None

    with open(path, "rb") as stream:
        envelope = msgspec.json.Decoder(Observation[msgspec.Raw])
        decoder = msgspec.json.Decoder(schema)
        for number, line in enumerate(stream, start=1):
            location = f"{path}, line {number}"
            if not line.endswith(b"\n"):
                raise ValueError(f"{location}: observation must end with a newline")
            try:
                raw = envelope.decode(line)
                data = decoder.decode(raw.data)
            except msgspec.DecodeError as error:
                raise ValueError(f"{location}: {error}") from error

            if previous is not None and raw.captured <= previous:
                raise ValueError(f"{location}: capture times must be strictly increasing")

            previous = raw.captured
            yield Observation(version=raw.version, captured=raw.captured, data=data)

    if previous is None:
        raise ValueError(f"{path} contains no observations")
