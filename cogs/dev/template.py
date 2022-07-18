"""
This is a template, it is never loaded.
This is just here to make it easier for developers to make new cogs.
"""
# import somebuiltin


import discord
from discord import Option
from discord.ext import commands

from munchi.config import Config

config = Config()


class TemplateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="A command")
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.dm_only()
    @commands.is_nsfw()
    @commands.is_owner()
    async def command(self, ctx, thing: Option(str, description="A thing")):
        await ctx.respond("A message!")


def setup(bot):
    bot.add_cog(TemplateCog(bot))
