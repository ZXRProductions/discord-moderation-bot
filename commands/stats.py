import logging

import discord
from discord.ext import commands
from discord import app_commands

from db import db

logger = logging.getLogger(__name__)

class Stats(commands.Cog):
    """Server moderation statistics: /stats."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="stats",
        description="Show moderation statistics for this server.",
    )
    async def stats(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        stats = db.get_stats_for_guild(guild_id=guild.id, top_n=5)

        total = stats["total_warnings"]
        unique_users = stats["unique_users"]
        top_users_rows = stats["top_users"]

        embed = discord.Embed(
            title=f"Moderation Stats — {guild.name}",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Total warnings", value=str(total), inline=True)
        embed.add_field(name="Users warned", value=str(unique_users), inline=True)

        if top_users_rows:
            lines: list[str] = []
            for row in top_users_rows:
                user_id = int(row["user_id"])
                count = int(row["warning_count"])
                lines.append(f"<@{user_id}> — {count} warning(s)")

            embed.add_field(
                name="Top warned users",
                value="\n".join(lines),
                inline=False,
            )
        else:
            embed.add_field(
                name="Top warned users",
                value="No warnings recorded yet.",
                inline=False,
            )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )

        # Stats per-moderator
        moderator_rows = db.get_warnings_per_moderator(guild_id=guild.id)

        if moderator_rows:
            mod_lines = [
                f"<@{row['moderator_id']}> — {row['count']} warning(s)"
                for row in moderator_rows
            ]
            embed.add_field(
                name="Warnings per moderator",
                value="\n".join(mod_lines),
                inline=False,
            )
        else:
            embed.add_field(
                name="Warnings per moderator",
                value="No warnings recorded.",
                inline=False,
            )

        # Weekly stats
        day_rows = db.get_warnings_per_day(guild_id=guild.id, days=7)

        if day_rows:
            day_lines = [
                f"{row['day']}: {row['count']} warning(s)" for row in day_rows
            ]
            embed.add_field(
                name="Warnings per day (last 7 days)",
                value="\n".join(day_lines),
                inline=False,
            )
        else:
            embed.add_field(
                name="Warnings per day (last 7 days)",
                value="No warnings in the past week.",
                inline=False,
            )



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Stats(bot))
    logger.info("Stats cog loaded")