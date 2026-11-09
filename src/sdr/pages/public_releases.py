from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated, Final

import msgspec
from seadex import Tag

from sdr.pages import Page
from sdr.shared import Summary, summarize
from sdr.snapshot import Anime, Snapshot

CUTOFF: Final[datetime] = datetime(2026, 9, 12, tzinfo=UTC)


@dataclass(frozen=True, slots=True, kw_only=True)
class Report[T]:
    """The matching entries and the date of the last manual AB-rule check."""

    cutoff: Annotated[datetime, msgspec.Meta(tz=True)]
    entries: tuple[T, ...]


def prepare(snapshot: Snapshot) -> Report[Anime]:
    """Find recent public releases whose groups have no private release listed."""
    entries: list[Anime] = []
    for anime in snapshot.entries.values():
        # Skip entries older than the cutoff date
        if anime.seadex.updated_at < CUTOFF:
            continue
        private = {
            torrent.release_group.casefold().strip()
            for torrent in anime.seadex.torrents
            if torrent.tracker.is_private()
        }
        if any(
            torrent.tracker.is_public()
            and Tag.INCOMPLETE not in torrent.tags
            and torrent.release_group.casefold().strip() not in private
            for torrent in anime.seadex.torrents
        ):
            entries.append(anime)
    ordered = tuple(sorted(entries, key=lambda anime: (anime.seadex.updated_at, anime.anilist.id), reverse=True))
    return Report(cutoff=CUTOFF, entries=ordered)


def export(snapshot: Snapshot) -> Report[Summary]:
    """A callable that's supposed to produce page data suitable for serialization."""
    report = prepare(snapshot)
    return Report(cutoff=report.cutoff, entries=summarize(report.entries))


def create() -> Page[Report[Anime]]:
    return Page(title="Releases Only on Public Trackers", prepare=prepare, export=export)
