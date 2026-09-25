import asyncio

from .subsonic_client import SubsonicClient
from .subsonic_player import SubsonicPlayer

# Last.fm's rule: a track counts as listened to after half its length or four minutes, whichever comes first
SCROBBLE_THRESHOLD = 240


class Scrobbler:
    """Reports playback to the Subsonic server. Player callbacks arrive on the mpv thread."""

    def __init__(self, subsonic: SubsonicClient, player: SubsonicPlayer, loop: asyncio.AbstractEventLoop) -> None:
        self._subsonic = subsonic
        self._player = player
        self._loop = loop
        self._submitted = False

        player.playlist_position_callbacks.register(self._handle_track_changed)
        player.time_position_callbacks.register(self._handle_time_position)

    def _scrobble(self, song_id: str, *, submission: bool) -> None:
        asyncio.run_coroutine_threadsafe(self._subsonic.scrobble(song_id, submission=submission), self._loop)

    def _handle_track_changed(self, _position: int | None) -> None:
        self._submitted = False
        if (track := self._player.current_track) is not None:
            self._scrobble(track.id, submission=False)

    def _handle_time_position(self, position: float | None) -> None:
        track = self._player.current_track
        if self._submitted or track is None or position is None:
            return

        # ponytail: a looped track is only scrobbled once, detect time-pos wrapping if that matters
        if position >= min((track.duration or 0) / 2, SCROBBLE_THRESHOLD):
            self._submitted = True
            self._scrobble(track.id, submission=True)
