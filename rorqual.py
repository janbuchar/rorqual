import asyncio
import os

import httpx
import typer
from textual.features import FeatureFlag

from rorqual.app import RorqualApp
from rorqual.config import Config
from rorqual.subsonic_client import SubsonicClient
from rorqual.subsonic_player import SubsonicPlayer


def main(dev: bool = False):
    features = set[FeatureFlag]()
    if dev:
        features = features.union({"debug", "devtools"})

    os.environ["TEXTUAL"] = ",".join(sorted(features))

    async def run_rorqual():
        config = Config.from_file()

        async with httpx.AsyncClient(base_url=config.subsonic_url) as httpx_client:
            subsonic = SubsonicClient(httpx_client, config)
            player = SubsonicPlayer(subsonic, asyncio.get_running_loop())
            app = RorqualApp(subsonic, player)
            await app.run_async()

    asyncio.run(run_rorqual())


if __name__ == "__main__":
    typer.run(main)
