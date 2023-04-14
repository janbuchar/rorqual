from pathlib import Path

from platformdirs import user_cache_dir

from subsonic.subsonic_rest_api import AlbumId3, Child

from .callbacks import CallbackList
from .subsonic_client import SubsonicClient


class CoverManager:
    def __init__(self, subsonic: SubsonicClient) -> None:
        self._subsonic = subsonic
        self._covers_path = Path(user_cache_dir("rorqual")) / "covers"

        self.cover_fetched_callbacks = CallbackList[[]]()

    def _determine_cover_path(self, subject: AlbumId3 | Child) -> Path | None:
        if subject.cover_art is None:
            return None

        return (self._covers_path / subject.cover_art).with_suffix(".jpg").absolute()

    def get_cover_url(self, subject: AlbumId3 | Child) -> str | None:
        path = self._determine_cover_path(subject)
        if path is None or not path.exists():
            return None

        return f"file://{path}"

    async def fetch_cover(self, subject: AlbumId3 | Child) -> None:
        path = self._determine_cover_path(subject)

        if path is None or subject.cover_art is None:
            return

        if path.exists():
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as destination:
            await self._subsonic.download_cover(subject.cover_art, destination)

        self.cover_fetched_callbacks()
