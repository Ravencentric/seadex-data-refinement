from collections.abc import Iterable
from dataclasses import dataclass
from urllib.parse import urlsplit

from pyanilist import MediaFormat, MediaSeason
from seadex import EntryRecord

from sdr.snapshot import Anime


@dataclass(frozen=True, slots=True, kw_only=True)
class Summary:
    """A SeaDex entry with minimal AniList metadata."""

    id: int
    seadex: EntryRecord
    title: str
    year: int
    format: MediaFormat
    genres: tuple[str, ...]
    season: MediaSeason | None
    popularity: int
    dubbed: bool


def summarize(items: Iterable[Anime]) -> tuple[Summary, ...]:
    """Summarize entries, preserving order."""
    entries: list[Summary] = []
    for anime in items:
        year = anime.year
        if year is None:
            raise ValueError(f"AniList {anime.anilist.id} has no start year")
        format = anime.anilist.format
        if format is None:
            raise ValueError(f"AniList {anime.anilist.id} has no format")
        popularity = anime.anilist.popularity
        if popularity is None:
            raise ValueError(f"AniList {anime.anilist.id} has no popularity")
        entries.append(
            Summary(
                id=anime.anilist.id,
                seadex=anime.seadex,
                title=anime.title,
                year=year,
                format=format,
                genres=anime.anilist.genres,
                season=anime.anilist.season,
                popularity=popularity,
                dubbed=anime.dubbed,
            )
        )
    return tuple(entries)


def is_slowpics_url(url: str) -> bool:
    """Check if the URL is a slow.pics link."""
    try:
        parsed = urlsplit(url)
        return parsed.scheme == "https" and parsed.hostname == "slow.pics"
    except ValueError:
        return False


def sort_by_popularity(items: Iterable[Anime]) -> tuple[Anime, ...]:
    """Sory by popularity (obviously) in a descending order."""

    def key(anime: Anime) -> tuple[bool, int, int]:
        popularity = anime.anilist.popularity
        return popularity is not None, popularity or 0, anime.anilist.id

    return tuple(sorted(items, key=key, reverse=True))
