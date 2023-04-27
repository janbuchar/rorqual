from rich.console import RenderableType
from textual.reactive import reactive
from textual.widget import Widget

from rorqual.subsonic_player import PlaybackState
from subsonic.subsonic_rest_api import Child

from .util import duration


class PlaybackProgress(Widget):
    track = reactive[Child | None](None)
    position = reactive[int](0)
    playback_state = reactive[PlaybackState]("stopped")

    def render(self) -> RenderableType:
        if self.track is None or self.playback_state == "stopped":
            return "Not playing"

        status = "Playing" if self.playback_state == "playing" else "Paused"

        return f"{status} {duration(self.position)} / {duration(self.track.duration or 0)}"
