import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    token: str
    guild_id: int | None = None


def load_config() -> Config:
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing DISCORD_BOT_TOKEN in .env file")

    guild_id = os.getenv("DISCORD_GUILD_ID")
    return Config(
        token=token,
        guild_id=int(guild_id) if guild_id else None
    )