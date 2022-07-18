import json
import random

import aiohttp

from .config import Config

config = Config()
guilds = config.guilds


async def random_gif(q, limit=10, contentfilter="medium"):
    """Get a random gif with the specified search query from GIPHY (requires valid API key)"""
    params = {
        "key": config.tenor_key,
        "q": q,
        "locale": "en_US",
        "contentfilter": contentfilter,
        "media_filter": "gif",
        "limit": limit,
    }

    search_url = f"https://g.tenor.com/v1/search"

    async with aiohttp.ClientSession() as session:
        async with await session.get(search_url, params=params) as resp:
            resp.raise_for_status()

            data = json.loads(await resp.text())

    results = []

    for res in data["results"]:
        if len(res["media"]) > 0:
            results.append(res)

    random_choice = random.choice(results)

    return random_choice["media"][0]["gif"]["url"]
