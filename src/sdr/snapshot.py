from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, Literal, NewType

import msgspec
from pyanilist import Media
from seadex import EntryRecord

AniListId = NewType("AniListId", int)


class Anime(msgspec.Struct, frozen=True, kw_only=True, forbid_unknown_fields=True):
    """One SeaDex entry with additional metadata."""

    seadex: EntryRecord
    anilist: Media
    dubbed: bool

    @property
    def title(self) -> str:
        """Prefer English, then Romaji, then native."""
        return self.anilist.title.to_str()

    @property
    def year(self) -> int | None:
        """Convenient property for templates."""
        if self.anilist.start_date is not None:
            return self.anilist.start_date.year
        return None


class Snapshot(msgspec.Struct, frozen=True, kw_only=True, forbid_unknown_fields=True):
    """A snapshot of SeaDex and various AniList metadata."""

    version: Literal[3]
    captured: Annotated[datetime, msgspec.Meta(tz=True)]
    entries: Mapping[AniListId, Anime]
    missing: tuple[Media, ...]

    def __post_init__(self) -> None:
        for identity, anime in self.entries.items():
            if identity != anime.anilist.id or identity != anime.seadex.anilist_id:
                raise ValueError(f"Snapshot key {identity} must match its SeaDex and AniList IDs")

        seen: set[int] = set()
        for media in self.missing:
            if media.id in self.entries:
                raise ValueError(f"Missing title {media.id} already has a SeaDex entry")
            if media.id in seen:
                raise ValueError(f"Duplicate missing title {media.id}")
            seen.add(media.id)


def load(path: Path) -> Snapshot:
    """Load an existing snapshot from a JSON file."""
    return msgspec.json.decode(path.read_bytes(), type=Snapshot)


def save(snapshot: Snapshot, path: Path) -> None:
    """
    Save a snapshot to disk.
    """
    content = msgspec.json.encode(snapshot)
    path.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=path.parent) as directory:
        pending = Path(directory) / path.name
        pending.write_bytes(content)
        pending.replace(path)
