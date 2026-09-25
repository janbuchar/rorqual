from dataclasses import dataclass
from itertools import groupby
from typing import Self

from subsonic.subsonic_rest_api import AlbumId3, ArtistId3

from .subsonic_client import SubsonicClient


@dataclass
class MediaLibrary:
    artists: dict[str, ArtistId3]
    albums_by_artist: dict[str, list[AlbumId3]]

    @classmethod
    async def fetch(cls, subsonic: SubsonicClient, *, cache_only: bool = False) -> Self:
        artists = {artist.id or "": artist for artist in await subsonic.get_artists(cache_only=cache_only)}

        albums_by_artist = {
            str(artist_id): sorted(albums, key=lambda album: album.year or 0)
            for artist_id, albums in groupby(
                await subsonic.get_albums(cache_only=cache_only), key=lambda album: album.artist_id or ""
            )
        }

        return cls(artists, albums_by_artist)
