from __future__ import annotations

from dataclasses import dataclass

from pyanilist import Media
from seadex import EntryRecord


@dataclass(frozen=True, slots=True)
class EnrichedEntry:
    seadex: EntryRecord
    anilist: Media


__all__ = ["EnrichedEntry"]
