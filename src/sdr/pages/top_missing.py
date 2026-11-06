from pyanilist import Media

from sdr.pages import Page
from sdr.snapshot import Snapshot


def prepare(snapshot: Snapshot) -> tuple[Media, ...]:
    """Return finished anime missing from SeaDex, ordered by popularity."""
    return snapshot.missing


def create() -> Page[tuple[Media, ...]]:
    return Page(title="Top 500 Missing Anime", prepare=prepare)
