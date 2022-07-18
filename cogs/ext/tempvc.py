"""Temporary voice channels"""

import discord
from discord import Option
from discord.ext import commands

from munchi.config import Config
from munchi.db import Database, VCTypes

config = Config()
db = Database().db


class VCCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_vc_join(self, member, before, after):
        """When someone joins a VC"""
        # Check if VC is in database
        vc = await db["vc"].find_one({"channel": after.channel.id})

        if not vc:
            return

        if vc.get("type") == VCTypes.CREATOR:
            tempvc = await member.guild.create_voice_channel(
                f"{member.display_name}'s room", category=after.channel.category
            )

            await db["vc"].insert_one(
                {"channel": tempvc.id, "guild": tempvc.guild.id, "type": VCTypes.TEMP}
            )

            await member.move_to(tempvc)

    async def on_vc_leave(self, member, before, after):
        """When someone leaves a VC"""
        # Check if VC is in database
        if len(before.channel.members) > 0:
            return

        vc = await db["vc"].find_one({"channel": before.channel.id})

        if not vc:
            return

        # If VC is creator
        if vc.get("type") == VCTypes.TEMP:
            await before.channel.delete()

            await db["vc"].delete_one({"channel": before.channel.id})

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel and before.channel != after.channel:
            await self.on_vc_join(member, before, after)

        if before.channel and before.channel != after.channel:
            await self.on_vc_leave(member, before, after)

    @commands.slash_command(description="Make a voice channel a creator for temp. VCs!")
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def makecreator(
        self,
        ctx,
        channelid: Option(
            str, description="ID of the voice channel you want to use as a creator"
        ),
    ):
        print("Making creator")
        channelid = int(channelid)

        vc = await db["vc"].find_one({"channel": channelid})
        print("Uh we found it?")
        if vc:
            if vc.get("type"):
                return await ctx.respond(
                    "This voice channel is already either a creator or temp VC!"
                )

        await db["vc"].insert_one(
            {"guild": ctx.guild.id, "channel": channelid, "type": VCTypes.CREATOR}
        )

        await ctx.respond(
            f"The voice channel will now create temporary voice channels when joined!"
        )

        print("Ok done")

    @commands.slash_command(
        description="Unmake a voice channel a creator for temp. VCs!"
    )
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def unmakecreator(
        self,
        ctx,
        channelid: Option(
            str,
            description="ID of the voice channel you want to no longer use as a creator",
        ),
    ):
        channelid = int(channelid)

        vc = await db["vc"].find_one({"channel": channelid})

        if not vc or not vc.get("type"):
            return await ctx.respond("This voice channel isn't a creator.")

        await db["vc"].delete_one(
            {"guild": ctx.guild.id, "channel": channelid, "type": VCTypes.CREATOR}
        )

        await ctx.respond(
            f"The voice channel will no longer create temporary voice channels when joined!"
        )


def setup(bot):
    bot.add_cog(VCCog(bot))
