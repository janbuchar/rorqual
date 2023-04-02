from itertools import groupby

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Tree

from rorqual.subsonic_client import SubsonicClient
from subsonic.subsonic_rest_api import AlbumId3, ArtistId3


class RorqualApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, subsonic: SubsonicClient) -> None:
        super().__init__()
        self.subsonic = subsonic

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(id="tree")

    async def on_mount(self):
        artists = await self.subsonic.get_artists()
        albums = {
            str(artist_id): sorted(albums, key=lambda album: album.year or 0)
            for artist_id, albums in groupby(await self.subsonic.get_albums(), key=lambda album: album.artist_id or "")
        }

        artists_tree = Tree[ArtistId3 | AlbumId3]("Artists")
        artists_tree.root.expand()

        for artist in artists:
            artists_tree.root.add(artist.name, data=artist, expand=False)

        for node in artists_tree.root.children:
            assert node.data is not None
            for album in albums.get(node.data.id, []):
                node.add(f"[{album.year}] {album.name}", data=album)

        self.query_one("#tree").mount(artists_tree)
