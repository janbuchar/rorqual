from __future__ import annotations

import asyncio
import hashlib
import secrets
from contextlib import asynccontextmanager
from typing import AsyncGenerator, BinaryIO, Generator, Self

import httpx
from more_itertools import flatten
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser

from subsonic.subsonic_rest_api import AlbumId3, AlbumWithSongsId3, ArtistId3, SubsonicResponse

from .config import SubsonicConfig


class SubsonicAuth(httpx.Auth):
    def __init__(self, config: SubsonicConfig) -> None:
        super().__init__()
        self.config = config

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        salt = secrets.token_urlsafe(12)
        request.url = request.url.copy_merge_params(
            httpx.QueryParams(
                {
                    "u": self.config.user,
                    "s": salt,
                    "t": hashlib.md5((self.config.password + salt).encode()).hexdigest(),
                    "v": "1.16.1",
                    "c": "rorqual",
                }
            )
        )

        yield request


class SubsonicClient:
    def __init__(self, client: httpx.AsyncClient, config: SubsonicConfig) -> None:
        self.client = client
        self.config = config
        self.parser = XmlParser(context=XmlContext())

    @classmethod
    @asynccontextmanager
    async def create(cls, config: SubsonicConfig) -> AsyncGenerator[Self, None]:
        base_url = httpx.URL(config.url)

        async with httpx.AsyncClient(base_url=base_url, auth=SubsonicAuth(config)) as client:
            yield cls(client, config)

    async def request(self, method: str, path: str, **kwargs: str | int) -> SubsonicResponse:
        params = httpx.QueryParams({k: str(v) for k, v in kwargs.items()}) if kwargs else None
        response = await self.client.request(method, path, params=params)

        return self.parser.from_string(response.text, SubsonicResponse)

    async def get_artists(self) -> list[ArtistId3]:
        index = (await self.request("GET", "/rest/getArtists")).artists
        assert index is not None

        return list(flatten(item.artist for item in index.index))

    async def get_albums(self) -> list[AlbumId3]:
        albums = (await self.request("GET", "/rest/getAlbumList2", type="alphabeticalByArtist", size=500)).album_list2
        assert albums is not None

        return albums.album

    async def get_album_details(self, album_id: str) -> AlbumWithSongsId3:
        album = (await self.request("GET", "/rest/getAlbum", id=album_id)).album
        assert album is not None

        return album

    async def download_cover(self, cover_id: str, destination: BinaryIO) -> None:
        async with self.client.stream(
            "GET", "/rest/getCoverArt", params=httpx.QueryParams({"id": cover_id})
        ) as response:
            async for chunk in response.aiter_raw():
                destination.write(chunk)

    async def stream(self, song_id: str, buffer: Buffer) -> None:
        async with self.client.stream("GET", "/rest/stream", params=httpx.QueryParams({"id": song_id})) as response:
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
