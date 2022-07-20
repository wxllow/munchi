"""Temporary voice channels"""

from discord.ext import commands

from munchi.db import Database

db = Database().db


class Cleanup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not await db["server"].find_one({"guild": guild.id}):
            await db["server"].insert_one({"guild": guild.id})

    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        if await db["server"].find_one({"guild": guild.id}):
            await db["server"].delete_one({"guild": guild.id})


def setup(bot):
    bot.add_cog(Cleanup(bot))
