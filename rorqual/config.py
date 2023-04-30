import asyncio
from pathlib import Path

import tomli
from platformdirs import user_config_dir
from pydantic import BaseModel, ByteSize


class BaseSubsonicConfig(BaseModel):
    url: str
    user: str


class SubsonicConfig(BaseSubsonicConfig):
    password: str


class PasswordCommandSubsonicConfig(BaseSubsonicConfig):
    password_command: str

    async def evaluate(self) -> SubsonicConfig:
        password_process = await asyncio.subprocess.create_subprocess_shell(
            self.password_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await password_process.communicate()
        password = stdout.decode().strip()
        return SubsonicConfig.parse_obj(self.dict() | {"password": password})


class PrefetchingConfig(BaseModel):
    worker_count: int = 3
    audio_cache_size: ByteSize = ByteSize(256 * 2**20)


class Config(BaseModel):
    subsonic: SubsonicConfig
    prefetching: PrefetchingConfig

    @classmethod
    async def from_file(cls) -> "Config":
        with (Path(user_config_dir("rorqual")) / "config.toml").open("rb") as file:
            config = tomli.load(file)
            parsed = RawConfig.parse_obj(config)

        return Config.parse_obj(
            parsed.dict()
            | {
                "subsonic": parsed.subsonic.evaluate()
                if isinstance(parsed.subsonic, PasswordCommandSubsonicConfig)
                else parsed.subsonic
            }
        )


class RawConfig(Config):
    subsonic: SubsonicConfig | PasswordCommandSubsonicConfig
