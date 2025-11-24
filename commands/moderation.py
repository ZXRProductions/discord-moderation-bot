import logging
from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands

from db import db


logger = logging.getLogger(__name__)


class Moderation(commands.Cog):
    """Moderation commands: /warn, /warnings."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="warn", description="Warn a member.")
    @app_commands.describe(
        user="The member you want to warn.",
        reason="Why are you warning them?",
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str,
    ) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        db.add_warning(
            user_id=user.id,
            moderator_id=interaction.user.id,
            guild_id=guild.id,
            reason=reason,
        )

        embed = discord.Embed(
            title="User Warned",
            description=f"{user.mention} has been warned.",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.set_footer(text=f"User ID: {user.id}")

        await interaction.response.send_message(embed=embed)

    @warn.error
    async def warn_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, app_commands.errors.MissingPermissions):
            # User missing Moderate Members permission
            if interaction.response.is_done():
                await interaction.followup.send(
                    "You don't have permission to use /warn.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "You don't have permission to use /warn.",
                    ephemeral=True,
                )
        else:
            logger.exception("Error in /warn: %r", error)
            try:
                if interaction.response.is_done():
                    await interaction.followup.send(
                        "Something went wrong while running /warn.",
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        "Something went wrong while running /warn.",
                        ephemeral=True,
                    )
            except Exception:
                pass

    @app_commands.command(
        name="warnings",
        description="Show recent warnings for a member in this server.",
    )
    @app_commands.describe(
        user="The member whose warnings you want to see.",
    )
    async def warnings(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
    ) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        rows = db.get_warnings_for_user(
            user_id=user.id,
            guild_id=guild.id,
            limit=10,
        )

        if not rows:
            await interaction.response.send_message(
                f"{user.mention} has no recorded warnings in this server.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title=f"Warnings for {user}",
            color=discord.Color.gold(),
        )

        for row in rows:
            ts = int(row["timestamp"])
            timestamp = datetime.fromtimestamp(ts)
            moderator_id = int(row["moderator_id"])

            embed.add_field(
                name=timestamp.strftime("%Y-%m-%d %H:%M"),
                value=(
                    f"**Reason:** {row['reason']}\n"
                    f"**Moderator:** <@{moderator_id}>"
                ),
                inline=False,
            )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
    logger.info("Moderation cog loaded")