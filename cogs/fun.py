import random

import discord
from discord import Embed, Option
from discord.ext import commands

from munchi.config import Config
from munchi.gifs import random_gif

config = Config()


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Search for a random GIF")
    async def gif(self, ctx, q: Option(str, description="Search query")):
        """Sends a random gif from a search query"""
        # Allow NSFW gifs if channel is marked as NSFW
        embed = discord.Embed(
            description=f'Random gif for "{q}"', colour=discord.Colour.blue()
        )

        gif = await random_gif(q)

        embed.set_image(url=gif)

        await ctx.respond(embed=embed)

    @commands.slash_command(description="Give someone a hug 🤗")
    async def hug(
        self, ctx, user: Option(discord.User, description="Who you want to hug")
    ):
        """Sends a hugging GIF and says author hugged user"""
        embed = discord.Embed(
            description=f"{ctx.author.mention} hugged {user.mention} :)",
            colour=discord.Colour.blue(),
        )

        searches = ["hug anime", "hug lesbian anime", "hug gay anime"]

        gif = await random_gif(random.choice(searches), 25)

        embed.set_image(url=gif)

        embed.set_footer(text="Powered by Tenor")

        await ctx.respond(embed=embed)

    @commands.slash_command(description="Give someone a kiss 💋")
    async def kiss(
        self, ctx, user: Option(discord.User, description="Who you want to kiss")
    ):
        """Sends a kissing GIF and says author kissed user"""
        embed = discord.Embed(
            description=f"{ctx.author.mention} kissed {user.mention} <3",
            colour=discord.Colour.blue(),
        )

        searches = ["kiss anime", "kiss lesbian anime", "kiss gay anime"]

        gif = await random_gif(random.choice(searches), 25)

        embed.set_image(url=gif)

        embed.set_footer(text="Powered by Tenor")

        await ctx.respond(embed=embed)

    @commands.slash_command(description="Pull a Will Smith 🥊")
    @commands.guild_only()
    async def slap(
        self, ctx, user: Option(discord.User, description="Who you want to slap")
    ):
        """Sends a slapping GIF and says author slapped user"""
        embed = discord.Embed(
            description=f"{ctx.author.mention} slapped {user.mention} 🥊",
            colour=discord.Colour.blue(),
        )

        gif = await random_gif("slap anime", 50)

        embed.set_image(url=gif)

        embed.set_footer(text="Powered by Tenor")

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(FunCog(bot))
