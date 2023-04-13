import asyncio
from dataclasses import dataclass
from pathlib import Path

import tomli
from appdirs import user_config_dir


@dataclass
class Config:
    subsonic_url: str
    subsonic_user: str
    subsonic_password: str
    prefetch_worker_count: int

    @classmethod
    async def from_file(cls) -> "Config":
        with (Path(user_config_dir("rorqual")) / "config.toml").open("rb") as file:
            config = tomli.load(file)

        if "password" in config["subsonic"]:
            subsonic_password = config["subsonic"]["password"]
        elif "password_command" in config["subsonic"]:
            password_process = await asyncio.subprocess.create_subprocess_shell(
                config["subsonic"]["password_command"], stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await password_process.communicate()
            subsonic_password = stdout.decode().strip()
        else:
            raise ValueError("No subsonic password (specify either `password` or `password_command`)")

        return cls(
            subsonic_url=config["subsonic"]["url"],
            subsonic_user=config["subsonic"]["user"],
            subsonic_password=subsonic_password,
            prefetch_worker_count=config.get("prefetching", {}).get("worker_count", 3),
        )
