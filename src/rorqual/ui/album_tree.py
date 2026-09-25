from typing import Any, cast, override

from rich.text import Text
from textual import events, on
from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Tree
from textual.widgets.tree import TreeNode

from rorqual.media_library import MediaLibrary
from rorqual.stream_manager import FetchingState, StreamManager
from rorqual.subsonic_client import NotCached, SubsonicClient
from subsonic.subsonic_rest_api import AlbumId3, AlbumWithSongsId3, ArtistId3

type LibraryItem = ArtistId3 | AlbumId3


def _set_dimmed(node: TreeNode[LibraryItem], dimmed: bool) -> None:
    label = cast(Text, node.label)
    if bool(label.style) != dimmed:
        node.set_label(Text(label.plain, style="dim" if dimmed else ""))


class AlbumTree(Widget):
    class AddAlbumToPlaylist(Message):
        def __init__(self, album: AlbumWithSongsId3) -> None:
            super().__init__()
            self.album = album

    media_library = reactive[MediaLibrary | None](None)
    offline = reactive(False)

    BINDINGS = [
        ("j", "down", "Down"),
        ("k", "up", "Up"),
        ("l", "expand", "Expand"),
        ("h", "collapse", "Collapse"),
        ("a", "add_to_playlist", "Add to playlist"),
        ("g", "go_to_top", "Go to top"),
        ("G", "go_to_bottom", "Go to bottom"),
    ]

    DEFAULT_CSS = """
    AlbumTree Tree {
        background: $background;
    }

    AlbumTree Tree > .tree--guides {
        color: $surface;
    }

    AlbumTree Tree > .tree--guides-hover {
        color: $warning;
        text-style: bold;
    }

    AlbumTree Tree > .tree--guides-selected {
        color: $warning;
        text-style: bold;
    }
    """

    def __init__(self, subsonic: SubsonicClient, stream_manager: StreamManager) -> None:
        super().__init__()
        self.subsonic = subsonic
        self.stream_manager = stream_manager
        self._album_songs = dict[str, list[str]]()
        """Song ids by album id, as far as the cached album details know"""

    @override
    def compose(self) -> ComposeResult:
        tree = Tree[LibraryItem]("Artists")
        tree.guide_depth = 2
        tree.root.expand()
        yield tree

    @on(events.Mount)
    def register_callbacks(self) -> None:
        self.offline = not self.subsonic.online
        self.subsonic.online_callbacks.register(self.handle_online_change)
        self.stream_manager.fetching_state_callbacks.register(self.handle_fetch_state_change)

    def handle_online_change(self, online: bool) -> None:
        self.offline = not online

    def handle_fetch_state_change(self, _id: str, state: FetchingState) -> None:
        if self.offline and state in ("done", "failed"):
            self.call_later(self._update_dimming)

    async def watch_offline(self) -> None:
        await self._update_dimming()

    async def watch_media_library(self, media_library: MediaLibrary | None) -> None:
        if media_library is None:
            return

        tree = self.query_one(Tree[LibraryItem])
        expanded = {cast(ArtistId3, node.data).id for node in tree.root.children if node.is_expanded}
        cursor = tree.cursor_node.data if tree.cursor_node else None
        cursor_key = (type(cursor), cursor.id) if cursor else None
        cursor_node = None

        tree.clear()

        for artist in media_library.artists.values():
            artist_node = tree.root.add(Text(artist.name), data=artist, expand=artist.id in expanded)
            if (ArtistId3, artist.id) == cursor_key:
                cursor_node = artist_node

            for album in media_library.albums_by_artist.get(artist.id, []):
                album_node = artist_node.add(Text(f"[{album.year}] {album.name}"), data=album)
                if (AlbumId3, album.id) == cursor_key:
                    cursor_node = album_node

        if cursor_node:
            # Node lines are only known once the tree renders
            self.call_after_refresh(tree.move_cursor, cursor_node)

        await self._update_dimming()

    async def _update_dimming(self) -> None:
        """Offline, dim albums that can't be played in full and artists with no such album."""
        offline = self.offline
        cached_streams = self.stream_manager.cached_streams() if offline else set[str]()

        for artist_node in self.query_one(Tree[LibraryItem]).root.children:
            artist_dimmed = offline

            for album_node in artist_node.children:
                album = cast(AlbumId3, album_node.data)
                album_dimmed = offline and not await self._is_cached(album.id, cached_streams)
                _set_dimmed(album_node, album_dimmed)
                artist_dimmed &= album_dimmed

            _set_dimmed(artist_node, artist_dimmed)

    async def _is_cached(self, album_id: str, cached_streams: set[str]) -> bool:
        if album_id not in self._album_songs:
            try:
                album = await self.subsonic.get_album_details(album_id, cache_only=True)
                self._album_songs[album_id] = [song.id for song in album.song]
            except NotCached:
                self._album_songs[album_id] = []

        songs = self._album_songs[album_id]
        return bool(songs) and cached_streams.issuperset(songs)

    def action_down(self) -> None:
        self.query_one(Tree).action_cursor_down()

    def action_up(self) -> None:
        self.query_one(Tree).action_cursor_up()

    def action_go_to_top(self) -> None:
        self.query_one(Tree).action_scroll_home()

    def action_go_to_bottom(self) -> None:
        self.query_one(Tree).action_scroll_end()

    def action_expand(self) -> None:
        tree = self.query_one(Tree[Any])
        if tree.cursor_node:
            tree.cursor_node.expand()

    def action_collapse(self) -> None:
        tree = self.query_one(Tree[Any])
        if tree.cursor_node:
            tree.cursor_node.collapse()

    async def action_add_to_playlist(self) -> None:
        node = self.query_one(Tree[Any]).cursor_node

        if node and isinstance(node.data, AlbumId3):
            try:
                album = await self.subsonic.get_album_details(node.data.id)
            except NotCached as error:
                self.notify(f"Could not load {node.data.name}: {error}", severity="error")
                return

            self._album_songs[album.id] = [song.id for song in album.song]
            self.post_message(self.AddAlbumToPlaylist(album))
