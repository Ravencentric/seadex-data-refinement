from collections.abc import Iterable
from urllib.parse import urlsplit

from sdr.snapshot import Anime


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
