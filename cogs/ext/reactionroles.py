"""Reaction roles"""
from discord.ext import commands

from munchi.config import Config
from munchi.db import Database

config = Config()
db = Database().db


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_mrm(self, reaction):
        """Get member, role, and message"""
        member = reaction.member

        if not member:
            member = self.bot.get_guild(reaction.guild_id).get_member(reaction.user_id)

        # Check if server is in database
        message = await db["reaction_roles_message"].find_one(
            {"guild": reaction.guild_id, "message": reaction.message_id}
        )

        if not message:
            return member, None, None

        roles = message.get("roles", {}).get(
            reaction.emoji.name if reaction.emoji.id else str(reaction.emoji.id)
        )

        if not roles:
            return member, None, message

        return member, roles, message

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        """When someone adds a reaction to a message"""
        member, roles, message = await self.get_mrm(reaction)

        if member.bot:
            return

        if not roles or not message:
            return

        if message.get("type") == "verify":
            await (
                await self.bot.get_guild(reaction.guild_id)
                .get_channel(reaction.channel_id)
                .fetch_message(reaction.message_id)
            ).remove_reaction(reaction.emoji, member)

        rl = [
            self.bot.get_guild(reaction.guild_id).get_role(role)
            for role in roles
            if self.bot.get_guild(reaction.guild_id).get_role(role)
        ]

        await member.add_roles(*rl)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        """When someone removes a reaction from a message"""
        member, roles, message = await self.get_mrm(reaction)

        if member.bot:
            return

        if not roles or not message:
            return

        if message.get("type") == "verify":
            return

        rl = [
            self.bot.get_guild(reaction.guild_id).get_role(role)
            for role in roles
            if self.bot.get_guild(reaction.guild_id).get_role(role)
        ]

        await member.remove_roles(*rl)


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
