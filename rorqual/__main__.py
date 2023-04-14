import asyncio
import os
from threading import Thread

import typer
from mpris_server.server import Server
from textual.features import FeatureFlag

from .app import RorqualApp
from .config import Config
from .cover_manager import CoverManager
from .mpris import RorqualEventAdapter, RorqualMprisAdapter
from .stream_manager import StreamManager
from .subsonic_client import SubsonicClient
from .subsonic_player import SubsonicPlayer


def main(dev: bool = False):
    features = set[FeatureFlag]()
    if dev:
        features = features.union({"debug", "devtools"})

    os.environ["TEXTUAL"] = ",".join(sorted(features))

    async def run_rorqual():
        config = await Config.from_file()

        async with SubsonicClient.create(config) as subsonic:
            stream_manager = StreamManager(subsonic, config)
            cover_manager = CoverManager(subsonic)
            player = SubsonicPlayer(stream_manager, asyncio.get_running_loop())

            mpris_server = Server("Rorqual", adapter=RorqualMprisAdapter(player, cover_manager))
            RorqualEventAdapter(player, cover_manager, mpris_server)
            mpris_server.publish()
            mpris_thread = Thread(target=mpris_server.loop, daemon=True)
            mpris_thread.start()

            app = RorqualApp(subsonic, player, stream_manager)
            await app.run_async()

    asyncio.run(run_rorqual())


if __name__ == "__main__":
    typer.run(main)