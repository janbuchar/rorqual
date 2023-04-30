import os
from contextlib import suppress
from pathlib import Path

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

    def __contains__(self, key: str) -> bool:
        return (self._root / key).exists()

    def read(self, key: str) -> bytes | None:
        path = self._root / key

        try:
            result = path.read_bytes()
        except OSError:
            result = None

        if result:
            self._recently_fetched.add(key)
            with suppress(OSError):
                os.utime(path)

        return result

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
