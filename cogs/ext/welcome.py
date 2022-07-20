"""Welcome messages"""

import discord
from discord import Embed
from discord.ext import commands

from munchi.config import Config
from munchi.db import Database

config = Config()
db = Database().db


class Welcome(commands.Cog):
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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """When someone joins a server"""
        # Check if server is in database
        server = await db["server"].find_one({"guild": member.guild.id})

        if not server:
            return

        if server.get("welcome_channel"):
            format_args = {
                "user": member.display_name,
                "user_mention": member.mention,
                "server": member.guild.name,
            }

            channel = self.bot.get_channel(server["welcome_channel"])

            if server.get("welcome_message"):
                await channel.send(server["welcome_message"].format(**format_args))

            if server.get("welcome_embed"):
                props: dict = server["welcome_embed"]

                for i in ["title", "description"]:
                    if props.get(i):
                        props[i] = props[i].format(**format_args)

                embed = Embed(
                    title=props.get("title", None),
                    description=props.get("description", None),
                    color=props.get("color", discord.Color.green()),
                )

                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Check if server is in database
        server = await db["server"].find_one({"guild": member.guild.id})

        if not server:
            return

        if server.get("goodbye_channel"):
            format_args = {
                "user": member.display_name,
                "user_mention": member.mention,
                "server": member.guild.name,
            }

            channel = self.bot.get_channel(server["goodbye_channel"])

            if server.get("goodbye_message"):
                await channel.send(server["welcome_message"].format(**format_args))

            if server.get("goodbye_embed"):
                props: dict = server["goodbye_embed"]

                for i in ["title", "description"]:
                    if props.get(i):
                        props[i] = props[i].format(**format_args)

                embed = Embed(
                    title=props.get("title", None),
                    description=props.get("description", None),
                    color=props.get("color", discord.Color.red()),
                )

                await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))
