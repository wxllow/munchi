import datetime

import discord
import humanfriendly
from discord import Option
from discord.ext import commands

from munchi.config import Config

config = Config()


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Use the ban hammer!")
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(
        self,
        ctx,
        user: Option(discord.User, description="Who do you want to ban"),
        reason: Option(str, description="The reason for this ban", default=None),
    ):
        """Bans a user"""
        await ctx.guild.ban(user, reason=reason)

        embed = discord.Embed(
            description=f"{user.mention} has been banned{f' for {reason}' if reason else ''}!",
            colour=discord.Colour.blue(),
        )

        embed.set_footer(text=f"User ID: {user.id}")

        await ctx.respond(embed=embed)

    @commands.slash_command(description="Kick someone out your lawn!")
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(
        self,
        ctx,
        user: Option(discord.Member, description="Who do you want to kick"),
        reason: Option(str, description="The reason for this kick", default=None),
    ):
        """Kicks a member"""
        await user.kick(reason=reason)

        embed = discord.Embed(
            description=f"{user.mention} has been kicked{f' for {reason}' if reason else ''}!",
            colour=discord.Colour.blue(),
        )

        embed.set_footer(text=f"User ID: {user.id}")

        await ctx.respond(embed=embed)

    @commands.slash_command(description="Give someone a second (or 100th) chance!")
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(
        self, ctx, user: Option(discord.User, description="Who do you want to unban")
    ):
        """Unbans a user"""
        await ctx.guild.unban(user)

        embed = discord.Embed(
            description=f"{user.mention} has been unbanned!",
            colour=discord.Colour.blue(),
        )

        embed.set_footer(text=f"User ID: {user.id}")

        await ctx.respond(embed=embed)

    @commands.slash_command(description="Time someone out!")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def timeout(
        self,
        ctx,
        user: Option(discord.Member, description="Who do you want to time out"),
        time: Option(str, description="Time"),
        reason: Option(str, description="The reason for this timeout", default=None),
    ):
        """Timeout a member"""
        # The parsed time
        t = humanfriendly.parse_timespan(time)

        await user.timeout(
            until=discord.utils.utcnow() + datetime.timedelta(seconds=t), reason=reason
        )

        embed = discord.Embed(
            description=f"{user.mention} has been timed out{f' for {reason}' if reason else ''}!",
            colour=discord.Colour.blue(),
        )

        embed.set_footer(text=f"User ID: {user.id}")

        await ctx.respond(embed=embed)

    @commands.slash_command(description="Remove someone's time out!")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def untimeout(
        self,
        ctx,
        user: Option(discord.Member, description="Who do you want to untimeout"),
        reason: Option(
            str, description="The reason for removing this timeout", default=None
        ),
    ):
        """Remove a member's timeout"""
        await user.timeout(until=None, reason=reason)

        embed = discord.Embed(
            description=f"{user.mention}'s timeout has been removed{f' for {reason}' if reason else ''}!",
            colour=discord.Colour.blue(),
        )

        embed.set_footer(text=f"User ID: {user.id}")

        await ctx.respond(embed=embed)

    @commands.slash_command(
        help="Purges specified amount of messages (or as much as possible)",
        aliases=["clear"],
        guild_ids=guilds,
    )
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def purge(
        self, ctx, amount: Option(int, description="How many messages to purge")
    ):
        """Delete a specified amount of messages"""
        await ctx.channel.purge(limit=amount)

        await ctx.respond(f"Cleared last {amount} messages! :)", delete_after=5)


def setup(bot):
    bot.add_cog(ModerationCog(bot))
