"""
Commands for bot owner only :)
"""


import discord
from discord import Option
from discord.ext import commands

from munchi.config import Config

config = Config()


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    owner = discord.SlashCommandGroup("owner", "Owner only commands")

    @owner.command(description="Send message in a channel")
    @commands.is_owner()
    async def echo(
        self,
        ctx,
        message: Option(str, description="Message"),
        channel: Option(
            discord.TextChannel, description="The channel you wish to send this to"
        ),
    ):
        """Send message in a channel"""
        await channel.send(message)
        await ctx.respond(f"Sent!", ephemeral=True)

    @owner.command(description="Load a cog")
    @commands.is_owner()
    async def load(self, ctx, cog: Option(str, description="The cog you wish to load")):
        """Loads a cog"""
        if cog.startswith("cog."):
            cog = f"cogs.{cog}"

        self.bot.load_extension(cog)

        await ctx.respond(f"Loaded {cog}!")

    @owner.command(description="Unload a cog")
    @commands.is_owner()
    async def unload(
        self, ctx, cog: Option(str, description="The cog you wish to unload")
    ):
        """Unloads a cog"""
        if cog.startswith("cog."):
            cog = f"cogs.{cog}"

        self.bot.unload_extension(cog)

        await ctx.respond(f"Unloaded {cog}!")

    @owner.command(description="Load a cog")
    @commands.is_owner()
    async def reload(
        self, ctx, cog: Option(str, description="The cog you wish to reload")
    ):
        """Reloads a cog"""
        if cog.startswith("cog."):
            cog = f"cogs.{cog}"

        self.bot.unload_extension(cog)
        self.bot.load_extension(cog)

        await ctx.respond(f"Reloaded {cog}!")


def setup(bot):
    bot.add_cog(OwnerCog(bot))
