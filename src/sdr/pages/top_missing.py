from dataclasses import dataclass

from pyanilist import Media, MediaFormat, MediaSeason

from sdr.pages import Page
from sdr.snapshot import Snapshot


@dataclass(frozen=True, slots=True, kw_only=True)
class MissingMedia:
    """Slimmed AniList metadata for a missing title."""

    id: int
    title: str
    year: int
    format: MediaFormat
    genres: tuple[str, ...]
    season: MediaSeason | None
    popularity: int


def prepare(snapshot: Snapshot) -> tuple[Media, ...]:
    """Return finished anime missing from SeaDex, ordered by popularity."""
    return snapshot.missing


def export(snapshot: Snapshot) -> tuple[MissingMedia, ...]:
    """A callable that's supposed to produce page data suitable for serialization."""
    entries: list[MissingMedia] = []
    for media in snapshot.missing:
        year = media.start_date.year if media.start_date is not None else None
        if year is None:
            raise ValueError(f"AniList {media.id} has no start year")
        format = media.format
        if format is None:
            raise ValueError(f"AniList {media.id} has no format")
        popularity = media.popularity
        if popularity is None:
            raise ValueError(f"AniList {media.id} has no popularity")
        entries.append(
            MissingMedia(
                id=media.id,
                title=media.title.to_str(),
                year=year,
                format=format,
                genres=media.genres,
                season=media.season,
                popularity=popularity,
            )
        )
    return tuple(entries)


def create() -> Page[tuple[Media, ...]]:
    return Page(title="Top 500 Missing Anime", prepare=prepare, export=export)
