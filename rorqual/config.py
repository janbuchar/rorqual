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
    def from_file(cls) -> "Config":
        with (Path(user_config_dir("rorqual")) / "config.toml").open("rb") as file:
            config = tomli.load(file)

        return cls(
            subsonic_url=config["subsonic"]["url"],
            subsonic_user=config["subsonic"]["user"],
            subsonic_password=config["subsonic"]["password"],
            prefetch_worker_count=config.get("prefetching", {}).get("worker_count", 3),
        )
