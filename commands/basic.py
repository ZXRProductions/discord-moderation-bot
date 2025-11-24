import logging

import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(__name__)


class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check if the bot is responding.")
    async def ping(self, interaction: discord.Interaction):
        logger.info("Received /ping from %s (%s)", interaction.user, interaction.user.id)

        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! `{latency_ms} ms`")


async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot))
    logger.info("Basic cog has been loaded")