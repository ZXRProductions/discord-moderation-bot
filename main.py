import asyncio
import logging

import discord
from discord.ext import commands, tasks

from config import load_config
from db import db


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("bot")


class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self) -> None:
        # Load command cogs
        await self.load_extension("commands.basic")
        await self.load_extension("commands.moderation")
        await self.load_extension("commands.stats")

        cfg = load_config()

        # Sync slash commands
        if cfg.guild_id:
            guild = discord.Object(id=cfg.guild_id)
            synced = await self.tree.sync(guild=guild)
            logger.info("Synced %d command(s) to guild %s", len(synced), cfg.guild_id)
        else:
            synced = await self.tree.sync()
            logger.info("Synced %d command(s) globally", len(synced))

        # Start heartbeat task
        self.heartbeat.start()

    async def on_ready(self) -> None:
        logger.info("Logged in as %s (%s)", self.user, self.user.id)

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError,
    ) -> None:
        logger.error("Error while handling command %s: %r", interaction.command, error)

        try:
            if interaction.response.is_done():
                await interaction.followup.send(
                    "Something went wrong while running that command.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "Something went wrong while running that command.",
                    ephemeral=True,
                )
        except Exception as e:
            logger.error("Failed to send error message to user: %r", e)

    # heartbeat background task
    @tasks.loop(minutes=5)
    async def heartbeat(self) -> None:
        total_warnings = db.get_total_warnings()
        guild_count = len(self.guilds)
        member_total = sum((g.member_count or 0) for g in self.guilds)

        logger.info(
            "Heartbeat | guilds=%d | members≈%d | total_warnings=%d",
            guild_count,
            member_total,
            total_warnings,
        )

    @heartbeat.before_loop
    async def before_heartbeat(self) -> None:
        await self.wait_until_ready()


async def main() -> None:
    cfg = load_config()
    bot = Bot()

    async with bot:
        await bot.start(cfg.token)


if __name__ == "__main__":
    asyncio.run(main())