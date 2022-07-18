from sanic import Blueprint
from sanic.exceptions import BadRequest, NotFound
from sanic.response import json

from munchi.config import Config
from munchi.db import Database

from .discord import *
from .utils import with_token

bp = Blueprint("routes")
config = Config()
db = Database().db


@bp.route("/oauth/callback")
async def oauth_callback(request):
    code = request.args.get("code")

    if not code:
        raise BadRequest("No code provided")

    return json({"token": await get_token(code)})


@bp.route("/me")
@with_token
async def me(request, token):
    """Get user info"""
    async with rest.acquire(token) as client:
        user = await client.fetch_my_user()

        return json(
            {
                "id": user.id,
                "username": user.username,
                "discriminator": user.discriminator,
                "avatar": user.avatar_url.url,
            }
        )


@bp.route("/me/guilds")
@with_token
async def me_guilds(request, token):
    """Get user's guilds"""
    managable_only = request.args.get("managable_only")

    async with rest.acquire(token) as client:
        res = []

        for guild in await client.fetch_my_guilds():
            if managable_only and not guild.my_permissions.all(
                guild.my_permissions.MANAGE_GUILD
            ):
                continue

            res.append(
                {
                    "id": str(guild.id),
                    "name": guild.name,
                    "icon_url": guild.icon_url.url if guild.icon_url else None,
                    "can_manage": guild.my_permissions.all(
                        guild.my_permissions.MANAGE_GUILD
                    ),
                    "has_munchi": (
                        guild.my_permissions.all(guild.my_permissions.MANAGE_GUILD)
                        and await member_in_guild(guild.id, config.application_id)
                    ),  # Only check if the server has munchi if it also is managable by the user (reduces load times significantly)
                }
            )

    return json(res)


@bp.route("/me/guilds/<guild_id>")
@with_token
async def me_guild(request, guild_id, token):
    guild = await get_user_guild(guild_id, token)

    if not guild:
        raise NotFound("Guild not found")

    query = {"guild": int(guild_id)}
    server = await db["server"].find_one(query)

    if not server:
        await db["server"].insert_one(query)

    guild.update(
        {
            "welcome_channel": str(server.get("welcome_channel") or ""),
            "welcome_message": server.get("welcome_message"),
            "welcome_embed": server.get("welcome_embed", {}),
            "goodbye_channel": str(server.get("goodbye_channel") or ""),
            "goodbye_message": server.get("goodbye_message"),
            "goodbye_embed": server.get("goodbye_embed", {}),
        }
    )

    return json(guild)


@bp.route("/guilds/<guild_id>/update_objects", methods=["PATCH"])
@with_token
async def update_guild_config_objects(request, guild_id, token):
    guild = await get_user_guild(guild_id, token)

    if not guild:
        raise NotFound("Guild not found")

    query = {"guild": int(guild_id)}
    server = await db["server"].find_one(query)

    if not server:
        await db["server"].insert_one(query)

    updated = server

    for k in request.json.keys():
        if k in [
            "welcome_embed",
            "goodbye_embed",
        ]:
            if k in updated and type(updated[k]) and type(request.json[k]) is dict:
                updated[k].update(dict(request.json[k]))
            else:
                updated[k] = dict(request.json[k])

    await db["server"].update_one(
        query,
        {"$set": updated},
    )

    return json({})


@bp.route("/guilds/<guild_id>/update", methods=["PATCH"])
@with_token
async def update_guild_config(request, guild_id, token):
    guild = await get_user_guild(guild_id, token)

    if not guild:
        raise NotFound("Guild not found")

    query = {"guild": int(guild_id)}
    server = await db["server"].find_one(query)

    if not server:
        await db["server"].insert_one(query)

    update_query = {}

    for k in request.json.keys():
        if k in [
            "welcome_channel",
            "welcome_message",
            "goodbye_channel",
            "goodbye_message",
        ]:
            v = request.json[k]

            if k in [
                "welcome_channel",
                "goodbye_channel",
            ]:
                v = int(v)

            update_query[k] = v

    await db["server"].update_one(
        query,
        {"$set": update_query},
    )

    return json({})
