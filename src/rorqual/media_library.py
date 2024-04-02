from dataclasses import dataclass
from itertools import groupby
from typing import Self

from more_itertools import flatten

from subsonic.subsonic_rest_api import AlbumId3, ArtistId3

from .subsonic_client import SubsonicClient


@dataclass
class MediaLibrary:
    artists: dict[str, ArtistId3]
    albums: dict[str, AlbumId3]
    albums_by_artist: dict[str, list[AlbumId3]]

    @classmethod
    async def fetch(cls, subsonic: SubsonicClient) -> Self:
        artists = {artist.id or "": artist for artist in await subsonic.get_artists()}

        albums_by_artist = {
            str(artist_id): sorted(albums, key=lambda album: album.year or 0)
            for artist_id, albums in groupby(await subsonic.get_albums(), key=lambda album: album.artist_id or "")
        }

        albums = {album.id: album for album in flatten(albums_by_artist.values())}

        return cls(artists, albums, albums_by_artist)
