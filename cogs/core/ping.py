import discord
from discord.ext import commands

from munchi.config import Config

config = Config()
guilds = config.guilds


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=config.guilds)
    async def ping(self, ctx):
        try:
            await ctx.author.send(f"Pong!")
        except discord.errors.Forbidden:
            pass

        await ctx.respond("Pong!")


def setup(bot):
    bot.add_cog(PingCog(bot))
