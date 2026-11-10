import os
from contextlib import suppress
from pathlib import Path
from typing import BinaryIO

from platformdirs import user_cache_dir


class BlobCache:
    def __init__(self, namespace: str, max_size: int) -> None:
        self._max_size = max_size
        self._root = Path(user_cache_dir("rorqual")) / namespace
        self._root.mkdir(parents=True, exist_ok=True)
        self._recently_fetched = set[str]()

    def store(self, key: str, content: bytes | bytearray | memoryview) -> None:
        (self._root / key).write_bytes(content)
        self._recently_fetched.add(key)
        self._cleanup()

    def adopt(self, key: str, path: Path) -> None:
        """Move a finished file into the cache. It must live on the same filesystem."""
        os.replace(path, self._root / key)
        self._recently_fetched.add(key)
        self._cleanup()

    def discard(self, key: str) -> None:
        self._recently_fetched.discard(key)
        with suppress(OSError):
            (self._root / key).unlink()

    def __contains__(self, key: str) -> bool:
        return (self._root / key).exists()

    def keys(self) -> set[str]:
        return {path.name for path in self._root.iterdir()}

    def read(self, key: str) -> bytes | None:
        if (file := self.open(key)) is None:
            return None

        with file:
            return file.read()

    def open(self, key: str) -> BinaryIO | None:
        try:
            file = (self._root / key).open("rb")
        except OSError:
            return None

        self._recently_fetched.add(key)
        with suppress(OSError):
            os.utime(file.fileno())

        return file

    def _cleanup(self) -> None:
        files = list(self._root.iterdir())
        files.sort(key=lambda file: file.stat().st_mtime)
        total_size = sum(file.stat().st_size for file in files)

        for file in files:
            if total_size <= self._max_size:
                break

            if file.name not in self._recently_fetched:
                total_size -= file.stat().st_size
                file.unlink()
