import asyncio

import httpx

from rorqual.app import RorqualApp
from rorqual.config import Config
from rorqual.subsonic_client import SubsonicClient


async def main():
    config = Config.from_file()

    async with httpx.AsyncClient(base_url=config.subsonic_url) as httpx_client:
        subsonic = SubsonicClient(httpx_client, config)
        app = RorqualApp(subsonic)
        await app.run_async()


if __name__ == "__main__":
    asyncio.run(main())
