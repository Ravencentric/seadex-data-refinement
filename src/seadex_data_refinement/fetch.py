from __future__ import annotations

from collections.abc import Iterator

import httpx2
import seadex
from seadex import EntryRecord
from tqdm import tqdm

_SEADEX_ID_LIST_URL = "https://releases.moe/api/listIDs"


def snapshot() -> tuple[EntryRecord, ...]:
    with seadex.SeaDexEntry() as seadex_entry:
        iterator: Iterator[EntryRecord] = seadex_entry.iterator()
        return tuple(tqdm(iterator, desc="SeaDex", unit="entries", unit_scale=True))


def seadex_anilist_ids() -> frozenset[int]:
    response = httpx2.get(_SEADEX_ID_LIST_URL)
    response.raise_for_status()
    return frozenset(int(id_) for id_ in response.text.split(",") if id_)
