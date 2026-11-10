from __future__ import annotations

import asyncio
import hashlib
import os
import secrets
import tempfile
from collections.abc import AsyncGenerator, Generator, Mapping
from contextlib import asynccontextmanager
from pathlib import Path
from typing import BinaryIO, Self

import httpx
from more_itertools import flatten
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

from subsonic.subsonic_rest_api import (
    AlbumId3,
    AlbumWithSongsId3,
    ArtistId3,
    ResponseStatus,
    SubsonicResponse,
)

from .caching import BlobCache
from .callbacks import CallbackList
from .config import SubsonicConfig


class NotCached(Exception):
    """There's no cached response and the server was either not asked or not reachable."""


def _query_params(kwargs: Mapping[str, str | int | bool]) -> httpx.QueryParams:
    return httpx.QueryParams({k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in kwargs.items()})


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
        self.parser = XmlParser(
            config=ParserConfig(fail_on_unknown_properties=False),
            context=XmlContext(),
        )
        self._responses = BlobCache("responses", 32 * 2**20)

        self.online = True
        self.online_callbacks = CallbackList[bool]()

    @classmethod
    @asynccontextmanager
    async def create(cls, config: SubsonicConfig) -> AsyncGenerator[Self, None]:
        base_url = httpx.URL(config.url)

        async with httpx.AsyncClient(base_url=base_url, auth=SubsonicAuth(config)) as client:
            yield cls(client, config)

    def _set_online(self, online: bool) -> None:
        if online != self.online:
            self.online = online
            self.online_callbacks(online)

    async def _send(self, method: str, path: str, params: httpx.QueryParams) -> bytes:
        try:
            response = await self.client.request(method, path, params=params)
            response.raise_for_status()
        except httpx.HTTPError:
            self._set_online(False)
            raise

        self._set_online(True)
        return response.content

    async def request(self, method: str, path: str, **kwargs: str | int | bool) -> SubsonicResponse:
        return self.parser.from_bytes(await self._send(method, path, _query_params(kwargs)), SubsonicResponse)

    async def query(self, path: str, *, cache_only: bool = False, **kwargs: str | int | bool) -> SubsonicResponse:
        """
        A GET request whose last successful response is kept on disk and served when the server can't be reached.
        With `cache_only`, the server is not contacted at all.
        """
        params = _query_params(kwargs)
        key = hashlib.sha256(f"{self.config.url}\0{self.config.user}\0{path}\0{params}".encode()).hexdigest()

        if cache_only:
            if not (cached := self._responses.read(key)):
                raise NotCached(f"{path} is not cached")
            return self.parser.from_bytes(cached, SubsonicResponse)

        try:
            content = await self._send("GET", path, params)
        except httpx.HTTPError as error:
            if not (cached := self._responses.read(key)):
                raise NotCached(str(error)) from error
            return self.parser.from_bytes(cached, SubsonicResponse)

        response = self.parser.from_bytes(content, SubsonicResponse)
        if response.status == ResponseStatus.OK:
            self._responses.store(key, content)

        return response

    async def get_artists(self, *, cache_only: bool = False) -> list[ArtistId3]:
        index = (await self.query("/rest/getArtists", cache_only=cache_only)).artists
        assert index is not None

        return list(flatten(item.artist for item in index.index))

    async def get_albums(self, *, cache_only: bool = False) -> list[AlbumId3]:
        albums = (
            await self.query("/rest/getAlbumList2", cache_only=cache_only, type="alphabeticalByArtist", size=500)
        ).album_list2
        assert albums is not None

        return albums.album

    async def get_album_details(self, album_id: str, *, cache_only: bool = False) -> AlbumWithSongsId3:
        album = (await self.query("/rest/getAlbum", cache_only=cache_only, id=album_id)).album
        assert album is not None

        return album

    async def scrobble(self, song_id: str, *, submission: bool) -> None:
        await self.request("GET", "/rest/scrobble", id=song_id, submission=submission)

    async def download_cover(self, cover_id: str, destination: BinaryIO) -> None:
        async with self.client.stream(
            "GET", "/rest/getCoverArt", params=httpx.QueryParams({"id": cover_id})
        ) as response:
            async for chunk in response.aiter_raw():
                destination.write(chunk)

    async def stream(self, song_id: str, buffer: Buffer) -> None:
        """Always finalizes `buffer`; a failed download leaves it incomplete."""
        try:
            async with self.client.stream("GET", "/rest/stream", params=httpx.QueryParams({"id": song_id})) as response:
                if response.is_success:
                    self._set_online(True)

                # On failure, Subsonic serves an XML document in place of the audio data, often with a 200 status
                content_type = response.headers.get("content-type", "")
                if not response.is_success or content_type.startswith(("text/xml", "application/xml")):
                    return

                buffer.allocate(int(response.headers["content-length"]))
                async for chunk in response.aiter_raw():
                    buffer.write(chunk)
        except httpx.TransportError:
            self._set_online(False)
        finally:
            if not buffer.started.is_set():
                buffer.allocate(0)
            buffer.finalize()


class Buffer:
    """A stream backed by a file that can be read while it's being written. Downloads are staged in `staging_dir`."""

    def __init__(self, staging_dir: Path | None = None) -> None:
        self.staging_dir = staging_dir
        self.path: Path | None = None
        self._file: BinaryIO  # set by `allocate` or `from_file`, before anything reads or writes
        self.size = 0
        self.bytes_written = 0
        self.cursor = 0
        self.started = asyncio.Event()
        self.finished = asyncio.Event()
        self.data_written = asyncio.Event()

    @classmethod
    def from_file(cls, file: BinaryIO) -> Self:
        buffer = cls()
        buffer._file = file
        buffer.size = buffer.bytes_written = os.fstat(file.fileno()).st_size
        buffer.started.set()
        buffer.finished.set()
        return buffer

    def allocate(self, size: int) -> None:
        fd, path = tempfile.mkstemp(dir=self.staging_dir)
        self._file = open(fd, "r+b")  # noqa: SIM115 - lives as long as the buffer
        self.path = Path(path)
        self.size = size
        self.started.set()

    def write(self, data: bytes) -> None:
        self._file.write(data)
        self._file.flush()
        self.bytes_written += len(data)
        self.data_written.set()

    @property
    def complete(self) -> bool:
        return 0 < self.bytes_written == self.size

    async def read(self, size: int) -> bytes:
        await self.started.wait()
        requested_pos = min(self.cursor + size, self.size)

        finished = asyncio.create_task(self.finished.wait())
        while not finished.done() and requested_pos > self.bytes_written:
            data_written = asyncio.create_task(self.data_written.wait())
            await asyncio.wait({finished, data_written}, return_when=asyncio.FIRST_COMPLETED)
            self.data_written.clear()
            data_written.cancel()

        finished.cancel()

        # Short of `requested_pos` only if the download failed - mpv takes that as the end of the stream
        data = os.pread(self._file.fileno(), requested_pos - self.cursor, self.cursor)
        self.cursor += len(data)
        return data

    def seek(self, pos: int) -> int:
        self.cursor = min(pos, self.size)
        self.data_written.set()
        return self.cursor

    def finalize(self) -> None:
        self.finished.set()

    def discard(self) -> None:
        """Delete the staged download, if any. Open readers keep working."""
        if self.path is not None:
            self.path.unlink(missing_ok=True)
