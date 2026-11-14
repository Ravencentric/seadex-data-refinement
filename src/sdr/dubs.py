from collections.abc import Iterable
from itertools import batched
from time import perf_counter

import msgspec

from sdr import network
from sdr.snapshot import AniListId

QUERY = """\
query Dubs($ids: [Int!]!) {
  page1: Page(page: 1, perPage: 50) {
    ...Dubs
  }
  page2: Page(page: 2, perPage: 50) {
    ...Dubs
  }
  page3: Page(page: 3, perPage: 50) {
    ...Dubs
  }
  page4: Page(page: 4, perPage: 50) {
    ...Dubs
  }
  page5: Page(page: 5, perPage: 50) {
    ...Dubs
  }
  page6: Page(page: 6, perPage: 50) {
    ...Dubs
  }
  page7: Page(page: 7, perPage: 50) {
    ...Dubs
  }
  page8: Page(page: 8, perPage: 50) {
    ...Dubs
  }
}

fragment Dubs on Page {
  media(id_in: $ids, type: ANIME, sort: ID) {
    id
    # AniList caps nested character pages at 25.
    characters(page: 1, perPage: 25, sort: FAVOURITES_DESC) {
      edges {
        # AniList needs the character node selected to populate voice actors.
        node {
          id
        }
        voiceActors(language: ENGLISH) {
          languageV2
        }
      }
    }
  }
}
"""


class Character(msgspec.Struct, frozen=True):
    id: int


class Actor(msgspec.Struct, frozen=True):
    language: str | None = msgspec.field(name="languageV2")


class Edge(msgspec.Struct, frozen=True):
    node: Character | None
    voice_actors: tuple[Actor | None, ...] | None = msgspec.field(name="voiceActors")


class Connection(msgspec.Struct, frozen=True):
    edges: tuple[Edge, ...]


class Media(msgspec.Struct, frozen=True):
    id: AniListId
    characters: Connection


class Page(msgspec.Struct, frozen=True):
    media: tuple[Media, ...]


class Data(msgspec.Struct, frozen=True):
    page1: Page
    page2: Page
    page3: Page
    page4: Page
    page5: Page
    page6: Page
    page7: Page
    page8: Page


class Error(msgspec.Struct, frozen=True):
    message: str


class Response(msgspec.Struct, frozen=True):
    data: Data | None = None
    errors: tuple[Error, ...] = ()


def is_dubbed(characters: Connection) -> bool:
    """Whether the selected characters list an English voice actor."""
    for edge in characters.edges:
        if edge.node is None:
            continue
        for actor in edge.voice_actors or ():
            if actor is not None and actor.language == "English":
                return True
    return False


def request(http: network.Client, identities: tuple[AniListId, ...]) -> tuple[Media, ...]:
    """Check the most popular characters for up to 400 anime."""
    response = http.post(
        "https://graphql.anilist.co",
        json={
            "query": QUERY,
            "variables": {"ids": identities},
        },
    )
    result = msgspec.json.decode(response.content, type=Response)
    if result.errors:
        raise ValueError("AniList dub query failed: " + "; ".join(error.message for error in result.errors))
    if result.data is None:
        raise ValueError("AniList returned no dub data")
    data = result.data
    media = (
        data.page1.media
        + data.page2.media
        + data.page3.media
        + data.page4.media
        + data.page5.media
        + data.page6.media
        + data.page7.media
        + data.page8.media
    )
    received = [record.id for record in media]
    if len(received) != len(identities) or set(received) != set(identities):
        raise ValueError(f"AniList dub query returned IDs {received}, expected {list(identities)}")
    return media


def dubs(identities: Iterable[AniListId]) -> dict[AniListId, bool]:
    """Check English credits among each anime's popular characters."""
    started = perf_counter()
    ordered = sorted(identities)
    total = len(ordered)
    records: dict[AniListId, bool] = {}
    print("Fetching AniList dub evidence...", flush=True)
    with network.Client() as http:
        for batch in batched(ordered, 400, strict=False):
            for media in request(http, batch):
                records[media.id] = is_dubbed(media.characters)
            print(f"Dub checks: {len(records)} of {total} anime checked", flush=True)
        print(
            f"Fetched dub evidence for {len(records)} AniList entries in {http.requests} HTTP requests "
            f"({perf_counter() - started:.2f}s)",
            flush=True,
        )

    return records
