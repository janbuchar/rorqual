import asyncio
import os
from pathlib import Path

from rorqual.subsonic_client import Buffer

DATA = os.urandom(300_001)
CHUNK = 65536


async def download(buffer: Buffer, data: bytes, *, size: int | None = None) -> None:
    buffer.allocate(len(data) if size is None else size)
    for i in range(0, len(data), CHUNK):
        buffer.write(data[i : i + CHUNK])
        await asyncio.sleep(0)  # let readers interleave with the writer
    buffer.finalize()


async def read_all(buffer: Buffer, size: int = 10_000) -> bytes:
    result = bytearray()
    while chunk := await buffer.read(size):
        result += chunk
    return bytes(result)


async def test_reader_following_a_download_gets_exact_bytes(tmp_path: Path) -> None:
    buffer = Buffer(tmp_path)

    # The reader starts before the download does, as mpv does when it opens a track that isn't fetched yet
    received, _ = await asyncio.wait_for(asyncio.gather(read_all(buffer), download(buffer, DATA)), 5)

    assert received == DATA
    assert buffer.complete


async def test_read_past_written_data_waits_for_it(tmp_path: Path) -> None:
    buffer = Buffer(tmp_path)
    buffer.allocate(len(DATA))
    buffer.write(DATA[:CHUNK])

    buffer.seek(200_000)
    pending = asyncio.create_task(buffer.read(100))
    await asyncio.sleep(0.01)
    assert not pending.done()

    buffer.write(DATA[CHUNK:])
    assert await asyncio.wait_for(pending, 1) == DATA[200_000:200_100]


async def test_failed_download_ends_the_stream_instead_of_padding_it(tmp_path: Path) -> None:
    buffer = Buffer(tmp_path)

    # The server promised more than it sent
    await download(buffer, DATA[:100_000], size=len(DATA))

    assert not buffer.complete
    assert await asyncio.wait_for(read_all(buffer), 1) == DATA[:100_000]


async def test_empty_download_is_not_complete(tmp_path: Path) -> None:
    buffer = Buffer(tmp_path)

    await download(buffer, b"", size=0)

    assert not buffer.complete
    assert await buffer.read(10) == b""


async def test_seek_is_clamped_to_size(tmp_path: Path) -> None:
    buffer = Buffer(tmp_path)
    await download(buffer, DATA)

    assert buffer.seek(len(DATA) + 1000) == len(DATA)
    assert await buffer.read(10) == b""


async def test_cached_file_reads_like_a_finished_download(tmp_path: Path) -> None:
    path = tmp_path / "cached"
    path.write_bytes(DATA)

    buffer = Buffer.from_file(path.open("rb"))

    assert buffer.complete
    buffer.seek(1234)
    assert await buffer.read(100) == DATA[1234:1334]


async def test_discarded_download_stays_readable_for_open_readers(tmp_path: Path) -> None:
    buffer = Buffer(tmp_path)
    await download(buffer, DATA)

    buffer.discard()

    assert buffer.path is not None and not buffer.path.exists()
    assert await read_all(buffer) == DATA
