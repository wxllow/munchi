"""For interacting with the Discord API"""

import logging

import aiohttp
import hikari
from sanic.exceptions import BadRequest

from munchi.config import Config

config = Config()
rest = hikari.RESTApp()


async def get_guild(guild: int) -> bool:
    """Get a guild"""
    headers = {"Authorization": f"Bot {config.token}"}

    async with aiohttp.ClientSession() as session:
        async with await session.get(
            f"https://discord.com/api/v10/guilds/{guild}?with_counts=true",
            headers=headers,
        ) as resp:
            resp.raise_for_status()
            return await resp.json()


async def get_user_guild(guild_id, token):
    """Get a user's guild via the bot (Uses user's token to check if bot is in guild)"""
    async with rest.acquire(token) as client:
        g = None

        # Check if user has and can manage guild
        for guild in await client.fetch_my_guilds():
            if guild.my_permissions.all(guild.my_permissions.MANAGE_GUILD) and str(
                guild.id
            ) == str(guild_id):
                g = guild
                break

        if not g:
            return

        # Get guild information from bot
        return await get_guild(guild_id)


async def get_token(code: str) -> str:
    """Get token from code"""
    async with aiohttp.ClientSession() as session:
        async with await session.post(
            "https://discord.com/api/v10/oauth2/token",
            data={
                "client_id": config.application_id,
                "client_secret": config.client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": config.redirect_uri,
            },
        ) as resp:
            logging.debug("ERROR", await resp.json())

            if resp.status != 200:
                raise BadRequest(str(await resp.json()))

            return (await resp.json())["access_token"]


async def member_in_guild(guild: int, member: int) -> bool:
    """Check if member is in guild"""
    # TODO: Use v10 API (I don't know how to do this with intents yet)
    headers = {"Authorization": f"Bot {config.token}"}

    async with aiohttp.ClientSession() as session:
        async with await session.get(
            f"https://discord.com/api/v6/guilds/{guild}/members/{member}",
            headers=headers,
        ) as resp:
            if resp.status in (403, 404):
                return False

            resp.raise_for_status()
            return True
