from __future__ import annotations

import itertools
from typing import Any

import pyanilist
from pyanilist import AniList, Media, MediaSort, MediaStatus, MediaType
from tqdm import tqdm

_DUB_INFO_QUERY = """
query Media($page: Int, $ids: [Int]) {
  Page(page: $page, perPage: 50) {
    pageInfo {
      lastPage
      total
      hasNextPage
      currentPage
    }
    media(
      type: ANIME
      format_not: MUSIC
      sort: POPULARITY_DESC
      id_in: $ids
    ) {
      id
      type
      title {
        romaji
        english
      }
      characters {
        edges {
          node {
            id
          }
          id,
          voiceActorRoles (language: ENGLISH) {
            voiceActor {
              name {
                first
                middle
                last
                full
                native
                userPreferred
              }
            }
            dubGroup
          }
        }
      }
    }
  }
}
"""


def enrich(ids: set[int]) -> dict[int, Media]:
    enriched: dict[int, Media] = {}
    batches = list(itertools.batched(sorted(ids), 200))
    with AniList() as anilist:
        for batch in tqdm(batches, desc="AniList", unit="batch"):
            for media in anilist.get_media_many(id_in=list(batch)):
                enriched[media.id] = media
    return enriched


def top_missing(seadex_ids: frozenset[int], count: int) -> tuple[Media, ...]:
    iterator = pyanilist.AniList().get_media_many(
        id_not_in=list(seadex_ids),
        sort=MediaSort.POPULARITY_DESC,
        type=MediaType.ANIME,
        status=MediaStatus.FINISHED,
    )
    return tuple(itertools.islice(tqdm(iterator, desc="Top missing", total=count, unit="entries"), count))


def dubbed_ids(ids: set[int]) -> frozenset[int]:
    dubbed: set[int] = set()
    id_list = sorted(ids)
    with AniList() as anilist:
        page = 1
        with tqdm(desc="AniList dubs", unit="page") as bar:
            while True:
                response: dict[str, Any] = anilist._post(
                    query=_DUB_INFO_QUERY, variables={"page": page, "ids": id_list}
                )
                page_info = response["Page"]["pageInfo"]
                for media in response["Page"]["media"]:
                    media_id = int(media["id"])
                    if any(char["voiceActorRoles"] for char in media["characters"]["edges"]):
                        dubbed.add(media_id)
                bar.update(1)
                if page_info["hasNextPage"] or page <= 10:
                    page += 1
                else:
                    return frozenset(dubbed)


__all__ = ["Media", "dubbed_ids", "enrich", "top_missing"]
