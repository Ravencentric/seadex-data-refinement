from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final

from seadex import Tag

from sdr.pages import Page
from sdr.snapshot import Anime, Snapshot

CUTOFF: Final[datetime] = datetime(2026, 9, 12, tzinfo=UTC)


@dataclass(frozen=True, slots=True, kw_only=True)
class Report:
    """The matching entries and the date of the last manual AB-rule check."""

    cutoff: datetime
    entries: tuple[Anime, ...]


def prepare(snapshot: Snapshot) -> Report:
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


def create() -> Page[Report]:
    return Page(title="Releases Only on Public Trackers", prepare=prepare)
