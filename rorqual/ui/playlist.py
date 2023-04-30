from functools import cached_property
from itertools import accumulate, groupby, pairwise
from typing import cast

from more_itertools import interleave_longest
from rich.color import Color, ColorType
from rich.emoji import Emoji
from rich.segment import Segment
from rich.style import Style
from textual.geometry import Region, Size
from textual.message import Message
from textual.reactive import reactive
from textual.scroll_view import ScrollView
from textual.strip import Strip

from rorqual.media_library import MediaLibrary
from rorqual.stream_manager import FetchingState, StreamManager
from rorqual.subsonic_player import PlaybackState
from subsonic.subsonic_rest_api import AlbumId3, Child

from .util import duration


class PlaylistRows(list[tuple[AlbumId3, list[Child]]]):
    @cached_property
    def sublist_stops(self) -> list[int]:
        return list(accumulate((len(tracks) + 1 for _, tracks in self), initial=0))

    @property
    def total_size(self) -> int:
        return sum(len(tracks) + 1 for _, tracks in self)

    def sublist_index(self, y: int) -> int | None:
        return next((i for i, (_, next_stop) in enumerate(pairwise(self.sublist_stops)) if y < next_stop), None)


class Playlist(ScrollView, can_focus=True):
    tracks = reactive(list[Child]())
    track_index = reactive[int | None](None)
    playback_state = reactive[PlaybackState]("stopped")
    media_library = reactive[MediaLibrary | None](None)

    _highlighted_row = reactive[int](0)
    _playlist_rows = reactive[PlaylistRows](PlaylistRows())

    muted_text = Style(color=Color(name="muted", type=ColorType.STANDARD, number=8))
    active_row = Style(
        bgcolor=Color(name="active", type=ColorType.STANDARD, number=4),
        color=Color(name="foreground", type=ColorType.STANDARD, number=0),
        bold=True,
    )
    highlighted_background = Style(bgcolor=Color(name="highlighted", type=ColorType.STANDARD, number=0))

    def __init__(self, stream_manager: StreamManager):
        super().__init__()

        self._stream_manager = stream_manager
        self._fetching_state = dict[str, FetchingState]()

        self.virtual_size = Size(self.size.width, 0)

    BINDINGS = [
        ("j", "down", "Down"),
        ("k", "up", "Up"),
        ("space", "toggle", "Play/Pause"),
        ("enter", "play", "Play"),
        ("c", "clear", "Clear playlist"),
    ]

    class TrackSelected(Message):
        def __init__(self, track_index: int, track: Child) -> None:
            super().__init__()
            self.track_index = track_index
            self.track = track

    class PlayPause(Message):
        pass

    class ClearPlaylist(Message):
        pass

    def render_line(self, y: int) -> Strip:
        scroll_x, scroll_y = self.scroll_offset
        y += scroll_y

        sublist_stops = self._playlist_rows.sublist_stops

        if not self._playlist_rows or y >= sublist_stops[-1]:
            return Strip.blank(1)

        sublist_index = self._playlist_rows.sublist_index(y)
        assert sublist_index is not None

        if y in sublist_stops:
            album, tracks = self._playlist_rows[sublist_index]
            return self.album_strip(album, tracks).crop(scroll_x, scroll_x + self.size.width)

        sublist_track_index = y - sublist_stops[sublist_index] - 1
        track_index = y - sublist_index - 1

        return self.track_strip(self._playlist_rows[sublist_index][1][sublist_track_index], track_index).crop(
            scroll_x, scroll_x + self.size.width
        )

    def album_strip(self, album: AlbumId3, tracks: list[Child]) -> Strip:
        album_duration = sum(track.duration or 0 for track in tracks)
        style = Style(bgcolor=Color(name="background", type=ColorType.STANDARD, number=8), bold=True)

        max_width = self.size.width if self._playlist_rows.total_size < self.size.height else self.size.width - 2
        segments = [f"[{album.year}]", f"{album.artist} - {album.name}", duration(album_duration)]
        available_space = max(1, max_width - len(segments) - sum(len(segment) for segment in segments))

        return Strip(
            [
                Segment(" ", style=style),
                Segment(segments[0], style=style),
                Segment(" ", style=style),
                Segment(segments[1], style=style),
                Segment(" " * available_space, style=style),
                Segment(segments[2], style=style),
                Segment(" ", style=style),
            ],
        )

    def track_strip(self, track: Child, track_index: int) -> Strip:
        strip_style = Style()
        icon_style = Style()

        if track_index == self._highlighted_row:
            strip_style = self.highlighted_background

        if track_index == self.track_index:
            strip_style = self.active_row

            if self.playback_state == "playing":
                icon = Emoji("play_button")
            elif self.playback_state == "paused":
                icon = Emoji("pause_button")
            else:
                icon = ""
        else:
            fetch_state = self._fetching_state.get(track.id, "pending")
            icon_style = self.muted_text

            if fetch_state == "pending":
                icon = Emoji("stopwatch")
            elif fetch_state == "fetching":
                icon = Emoji("down_arrow")
            elif fetch_state == "done":
                icon = Emoji("heavy_check_mark")
            else:
                icon = ""

        max_width = self.size.width if self._playlist_rows.total_size < self.size.height else self.size.width - 2
        segments = [str(icon), f"{track.track or '':3}", track.title, duration(track.duration or 0)]
        available_space = max(1, max_width - len(segments) - sum(len(segment) for segment in segments))

        return Strip(
            [
                Segment(" ", style=strip_style),
                Segment(segments[0], style=strip_style + icon_style),
                Segment(" ", style=strip_style),
                Segment(segments[1], style=strip_style),
                Segment(" ", style=strip_style),
                Segment(segments[2], style=strip_style),
                Segment(" " * available_space, style=strip_style),
                Segment(segments[3], style=strip_style),
                Segment(" ", style=strip_style),
            ]
        )

    def on_mount(self) -> None:
        self._stream_manager.fetching_state_callbacks.register(self.on_fetch_state_change)

    async def watch_tracks(self, new_tracks: list[Child]) -> None:
        await self._stream_manager.prefetch(track.id for track in new_tracks)

    def compute__playlist_rows(self) -> PlaylistRows:
        result = PlaylistRows()

        if self.media_library:
            for album_id, tracks in groupby(self.tracks, lambda it: it.album_id):
                result.append((self.media_library.albums[cast(str, album_id)], list(tracks)))

        return result

    def watch__playlist_rows(self, new_rows: PlaylistRows) -> None:
        self.virtual_size = Size(
            self.size.width if new_rows.total_size < self.size.height else self.size.width - 2, new_rows.total_size
        )

    def watch__highlighted_row(self, new_row: int) -> None:
        new_row += self._playlist_rows.sublist_index(new_row) or 0
        self.scroll_to_region(Region(0, new_row, self.size.width, 3))

    def on_fetch_state_change(self, id: str, state: FetchingState) -> None:
        self._fetching_state[id] = state
        self.refresh()

    def action_down(self) -> None:
        self._highlighted_row = min(self._highlighted_row + 1, len(self.tracks) - 1)

    def action_up(self) -> None:
        self._highlighted_row = max(self._highlighted_row - 1, 0)

    def action_toggle(self) -> None:
        self.post_message(self.PlayPause())

    async def action_play(self) -> None:
        await self._stream_manager.prefetch(
            interleave_longest(
                (it.id for it in self.tracks[self._highlighted_row :]),
                (it.id for it in reversed(self.tracks[: self._highlighted_row])),
            )
        )
        self.post_message(self.TrackSelected(self._highlighted_row, self.tracks[self._highlighted_row]))

    def action_clear(self) -> None:
        self._stream_manager.abort_all_streams()
        self.post_message(self.ClearPlaylist())
