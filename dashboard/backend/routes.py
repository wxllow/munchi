from sanic import Blueprint
from sanic.exceptions import BadRequest, NotFound

from munchi.config import Config
from munchi.db import Database

from .discord import *
from .utils import jsonify as json
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
        res = [
            {
                "id": guild.id,
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
            for guild in await client.fetch_my_guilds()
            if not (
                managable_only
                and not guild.my_permissions.all(guild.my_permissions.MANAGE_GUILD)
            )
        ]

    return json(res)


@bp.route("/me/guilds/<guild_id:int>")
@with_token
async def me_guild(request, guild_id, token):
    guild, server, _ = await get_user_guild_and_db(guild_id, token)

    guild.update(
        {
            "welcome_channel": server.get("welcome_channel"),
            "welcome_message": server.get("welcome_message"),
            "welcome_embed": server.get("welcome_embed", {}),
            "goodbye_channel": server.get("goodbye_channel"),
            "goodbye_message": server.get("goodbye_message"),
            "goodbye_embed": server.get("goodbye_embed", {}),
            "reaction_roles_message": [
                {
                    "message": doc["message"],
                    "guild": doc["guild"],
                    "type": doc.get("type", "normal"),
                    "roles": {i: doc["roles"][i] for i in doc["roles"]},
                }
                async for doc in db["reaction_roles_message"].find(
                    {"guild": int(guild["id"])}
                )
            ],
        }
    )

    return json(guild)


@bp.route("/guilds/<guild_id:int>/add_reaction_message", methods=["POST", "PATCH"])
@with_token
async def add_message(request, guild_id, token):
    try:
        message_id = int(request.json["message"])
        roles = {k: [int(x) for x in v] for k, v in request.json["roles"].items()}
        type_ = request.json.get("type", "normal")
    except KeyError as e:
        raise BadRequest(f"Missing {e}")
    except ValueError as e:
        raise BadRequest(f"Invalid field")

    await get_user_guild_and_db(guild_id, token)

    msg_q = {"guild": guild_id, "message": message_id}
    message = await db["reaction_roles_message"].find_one(msg_q)

    if not message:
        if request.method == "PATCH":
            raise NotFound("Message not found, use POST to create")

        await db["reaction_roles_message"].insert_one(msg_q)
        message = await db["reaction_roles_message"].find_one(msg_q)

    if not message.get("roles"):
        await db["reaction_roles_message"].update_one(msg_q, {"$set": {"roles": {}}})
        message["roles"] = {}

    message["roles"].update(roles)

    await db["reaction_roles_message"].update_one(
        msg_q,
        {
            "$set": {
                "roles": message["roles"],
                "type": type_ or message.get("type", "normal"),
            }
        },
    )

    return json({})


@bp.route(
    "/guilds/<guild_id:int>/remove_reaction_message/<message_id:int>",
    methods=["DELETE"],
)
@with_token
async def remove_message(request, guild_id, message_id, token):
    await get_user_guild_and_db(guild_id, token)

    # Check if server is in database
    msg_q = {"guild": guild_id, "message": message_id}
    message = await db["reaction_roles_message"].find_one(msg_q)

    if not message:
        raise NotFound("Message not found")

    await db["reaction_roles_message"].delete_one(msg_q)

    return json({})


@bp.route("/guilds/<guild_id:int>/update_objects", methods=["PATCH"])
@with_token
async def update_guild_config_objects(request, guild_id, token):
    _, server, query = await get_user_guild_and_db(guild_id, token)

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


@bp.route("/guilds/<guild_id:int>/update", methods=["PATCH"])
@with_token
async def update_guild_config(request, guild_id, token):
    _, _, query = await get_user_guild_and_db(guild_id, token)

    update_query = {}

    for k in request.json.keys():
        if k in [
            "welcome_channel",
            "welcome_message",
            "goodbye_channel",
            "goodbye_message",
        ]:
            v = request.json[k]

            if v and k in ["welcome_channel", "goodbye_channel"]:
                try:
                    v = int(v)
                except ValueError:
                    raise BadRequest(f"Invalid {k}: {v}. Must be an integer.")

            update_query[k] = v

    await db["server"].update_one(
        query,
        {"$set": update_query},
    )

    return json({})
