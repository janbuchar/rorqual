from dataclasses import dataclass
from pathlib import Path

import tomli
from appdirs import user_config_dir


@dataclass
class Config:
    subsonic_url: str
    subsonic_user: str
    subsonic_password: str

    @classmethod
    def from_file(cls) -> "Config":
        config = tomli.load((Path(user_config_dir("rorqual")) / "config.toml").open("rb"))

        return cls(
            subsonic_url=config["subsonic"]["url"],
            subsonic_user=config["subsonic"]["user"],
            subsonic_password=config["subsonic"]["password"],
        )
