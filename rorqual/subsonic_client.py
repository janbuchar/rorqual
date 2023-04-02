from __future__ import annotations

import asyncio
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

    async def get_album_details(self, album_id: str) -> AlbumWithSongsId3:
        response = await self.client.get(
            "/rest/getAlbum",
            params=self._auth_params().merge(self.common_params).merge(httpx.QueryParams({"id": album_id})),
        )
        album = self.parser.from_string(response.text, SubsonicResponse).album
        assert album is not None

        return album

    async def stream(self, song_id: str, buffer: Buffer) -> None:
        async with self.client.stream(
            "GET",
            "/rest/stream",
            params=self._auth_params().merge(self.common_params).merge(httpx.QueryParams({"id": song_id})),
        ) as response:
            buffer.allocate(int(response.headers["content-length"]))
            try:
                async for chunk in response.aiter_raw():
                    buffer.write(chunk)
            finally:
                buffer.finalize()


class Buffer:
    def __init__(self) -> None:
        self.data = bytearray()
        self.bytes_written = 0
        self.cursor = 0
        self.started = asyncio.Event()
        self.finished = asyncio.Event()
        self.data_written = asyncio.Event()

    def allocate(self, size: int) -> None:
        self.started.set()
        self.data = bytearray(size)

    def write(self, data: bytes) -> None:
        self.data[self.bytes_written : self.bytes_written + len(data)] = data
        self.bytes_written += len(data)
        self.data_written.set()

    async def read(self, size: int) -> bytes:
        await self.started.wait()
        requested_pos = min(self.cursor + size, len(self.data))

        finished = asyncio.create_task(self.finished.wait())
        while not finished.done() and requested_pos > self.bytes_written:
            data_written = asyncio.create_task(self.data_written.wait())
            await asyncio.wait({finished, data_written}, return_when=asyncio.FIRST_COMPLETED)
            self.data_written.clear()
            data_written.cancel()

        finished.cancel()

        try:
            return self.data[self.cursor : requested_pos]
        finally:
            self.cursor = requested_pos

    def seek(self, pos: int) -> int:
        self.cursor = min(pos, len(self.data))
        self.data_written.set()
        return self.cursor

    def finalize(self) -> None:
        self.finished.set()
