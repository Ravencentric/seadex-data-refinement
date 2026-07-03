from __future__ import annotations

import itertools
import time
from datetime import datetime
from typing import Final, Literal, Self

import httpx
import pyanilist
import seadex
from prettytable import PrettyTable, TableStyle
from pydantic import BaseModel, ConfigDict

SEADEX_ANILIST_IDS_URL = "https://releases.moe/api/listIDs"

EXCLUSIVE_GROUPS: Final = {"-ZR-", "FraMeSToR", "NAN0", "KEKKU", "Doc", "Kitsune"}


class MediaEntry(BaseModel):
    """Represents a single media entry with metadata."""

    model_config = ConfigDict(frozen=True)

    id: int
    title: str
    year: int | None
    popularity: int | None
    updated_at: datetime | None
    seadex_url: str
    anilist_url: str


class MediaEntryCollection(BaseModel):
    """Represents a collection of media entries."""

    model_config = ConfigDict(frozen=True)

    entries: tuple[MediaEntry, ...]

    @classmethod
    def from_entry_records(
        cls,
        entries: dict[int, seadex.EntryRecord],
        sort_by: Literal["popularity", "updated_at"] = "popularity",
    ) -> Self:
        """Fetches and creates an MediaEntryCollection from AniList IDs."""
        results: list[MediaEntry] = []

        with pyanilist.AniList() as anilist:
            for ids in itertools.batched(entries, 200):
                for media in anilist.get_media_many(id_in=ids):
                    results.append(
                        MediaEntry(
                            id=media.id,
                            title=media.title.to_str(),
                            year=media.start_date.year if media.start_date else None,
                            updated_at=entries[media.id].updated_at,
                            popularity=media.popularity,
                            seadex_url=f"https://releases.moe/{media.id}/",
                            anilist_url=f"https://anilist.co/anime/{media.id}",
                        ),
                    )

                time.sleep(1)

        match sort_by:
            case "popularity":
                results.sort(
                    key=lambda x: x.popularity if x.popularity is not None else -1,
                    reverse=True,
                )
            case "updated_at":
                results.sort(key=lambda x: x.updated_at or datetime.min, reverse=True)

        return cls(entries=tuple(results))

    @classmethod
    def top_x_anilist_not_on_dex(cls, count: int = 4) -> Self:
        """Fetches and creates an MediaEntryCollection of the top X anime not on SeaDex.

        Parameters
        ----------
        count : Int, optional
            The amount of releases
        """
        results: list[MediaEntry] = []
        ids = [int(id) for id in httpx.get(SEADEX_ANILIST_IDS_URL).raise_for_status().text.split(",")]

        with pyanilist.AniList() as anilist:
            media_iter = itertools.islice(
                anilist.get_media_many(
                    id_not_in=ids,
                    sort=pyanilist.MediaSort.POPULARITY_DESC,
                    type=pyanilist.MediaType.ANIME,
                    status=pyanilist.MediaStatus.FINISHED,
                ),
                count,
            )
            for media in media_iter:
                results.append(
                    MediaEntry(
                        id=media.id,
                        title=media.title.to_str(),
                        year=media.start_date.year if media.start_date else None,
                        updated_at=None,
                        popularity=media.popularity,
                        seadex_url=f"https://releases.moe/{media.id}/",
                        anilist_url=f"https://anilist.co/anime/{media.id}",
                    ),
                )

            time.sleep(1)

        results.sort(
            reverse=True,
            key=lambda x: x.popularity if x.popularity is not None else -1,
        )

        return cls(entries=tuple(results))

    def to_markdown_table(self, *, header: str | None = None) -> str:
        """Converts the MediaEntryCollection to a Markdown table string."""
        table = PrettyTable()
        table.set_style(TableStyle.MARKDOWN)
        table.align = "l"
        table.field_names = ["Idx", "Title", "Year", "Updated At", "Links"]
        for idx, entry in enumerate(self.entries, start=1):
            table.add_row(
                [
                    idx,
                    entry.title,
                    entry.year,
                    entry.updated_at.strftime("%d %b %Y") if entry.updated_at else "-",
                    f"[SeaDex]({entry.seadex_url}), [AniList]({entry.anilist_url})",
                ],
            )

        return f"{header}\n{table.get_formatted_string()}" if header else table.get_formatted_string()

    def to_json(self) -> str:
        """Converts the MediaEntryCollection to a JSON string."""
        return self.model_dump_json(indent=2)


DUB_INFO = """
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


def remove_entries_without_dub(entries: dict[int, seadex.EntryRecord]) -> None:
    with pyanilist.AniList() as anilist:
        page = 1
        ids = [entry.anilist_id for entry in entries.values()]

        while True:
            time.sleep(5)
            response = anilist._post(query=DUB_INFO, variables={"page": page, "ids": ids})
            print(response["Page"]["pageInfo"])

            for media in response["Page"]["media"]:
                id = media["id"]
                if not any(char["voiceActorRoles"] for char in media["characters"]["edges"]):
                    entries.pop(id, None)
                    continue

            if response["Page"]["pageInfo"]["hasNextPage"]:
                page += 1
            else:
                return
