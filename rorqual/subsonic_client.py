import hashlib
import secrets

import httpx
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser

from rorqual.config import Config
from subsonic.subsonic_rest_api import AlbumId3, AlbumWithSongsId3, ArtistId3, SubsonicResponse


class SubsonicClient:
    common_params = httpx.QueryParams({"v": "1.16.1", "c": "rorqual"})

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client
        self.parser = XmlParser(context=XmlContext())
        self.config = Config.from_file()
        client.base_url = self.config.subsonic_url

    def _auth_params(self) -> httpx.QueryParams:
        salt = secrets.token_urlsafe(12)

        return httpx.QueryParams(
            {
                "u": self.config.subsonic_user,
                "s": salt,
                "t": hashlib.md5((self.config.subsonic_password + salt).encode()).hexdigest(),
            }
        )

    async def get_artists(self) -> list[ArtistId3]:
        response = await self.client.get("/rest/getArtists", params=self._auth_params().merge(self.common_params))
        index = self.parser.from_string(response.text, SubsonicResponse).artists
        assert index is not None

        result = list[ArtistId3]()

        for item in index.index:
            result.extend(item.artist)

        return result

    async def get_albums(self) -> list[AlbumId3]:
        response = await self.client.get(
            "/rest/getAlbumList2",
            params=self._auth_params()
            .merge(self.common_params)
            .merge(httpx.QueryParams({"type": "alphabeticalByArtist", "size": 500})),
        )
        albums = self.parser.from_string(response.text, SubsonicResponse).album_list2
        assert albums is not None

        return albums.album

    async def get_album_details(self, album_id: int) -> AlbumWithSongsId3:
        response = await self.client.get(
            "/rest/getAlbum",
            params=self._auth_params().merge(self.common_params).merge(httpx.QueryParams({"id": str(album_id)})),
        )
        album = self.parser.from_string(response.text, SubsonicResponse).album
        assert album is not None

        return album
