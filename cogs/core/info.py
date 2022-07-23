from datetime import datetime
from importlib.metadata import version

import discord
import psutil
from discord import Option
from discord.ext import commands
from humanfriendly import format_timespan
from psutil._common import bytes2human

from munchi.config import Config

config = Config()


class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.uptime = datetime.now()

    @commands.slash_command(description="Info about Munchi")
    async def about(self, ctx):
        """Sends info about Munchi"""

        embed = discord.Embed(title="About Munchi", colour=discord.Colour.blue())

        embed.set_author(
            name="Munchi by wxllow",
            url="https://github.com/wxllow/munchi",
            icon_url="https://avatars.githubusercontent.com/u/35239049",
        )

        embed.description = f"""
Free, fast, powerful, and open-source replacement for all your Discord server's needs.

***Note: Munchi is still early in development :)***

**Servers:** {len(self.bot.guilds):,}
**Users:** {len(self.bot.users):,}

**Ping:** {round(self.bot.latency * 1000):,}ms 🏓
**Uptime:** {format_timespan(datetime.now() - self.uptime)}
        """.strip()

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(InfoCog(bot))
